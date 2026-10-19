// Run the eval cases against one skill arm on dsh headless and grade them.
// Usage:
//   node evals/v2/run.mjs --arm-dir .tmp/arms/baseline --arm baseline --label baseline-r1
//        [--only R01,Q05] [--concurrency 2] [--timeout-min 12]
// --arm none runs with an empty skill directory (no skills at all).
// Output: .tmp/runs/<label>/results.jsonl and summary.json; workspaces kept for inspection.
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { cases } from './cases.mjs';
import { capabilities } from './capabilities.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..', '..');
const DSH_BIN = process.env.DSH_BIN ?? 'C:\\dsh-lab\\app-0.2.1-rc.2\\node_modules\\@deepseek-ai\\dsh\\lib\\bin.js';
const DSH_HOME = process.env.DSH_HOME ?? 'C:\\dsh-lab\\home';

const opt = { concurrency: 2, timeoutMin: 12 };
const argv = process.argv.slice(2);
for (let i = 0; i < argv.length; i++) {
  const k = argv[i].replace(/^--/, '');
  opt[k.replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = argv[++i];
}
if (!opt.arm || !opt.label) throw new Error('need --arm <baseline|v2|none> and --label <name>');
const runDir = path.join(repo, '.tmp', 'runs', opt.label);
fs.mkdirSync(runDir, { recursive: true });

let armDir = opt.armDir ? path.resolve(opt.armDir) : path.join(runDir, 'empty-skills');
if (opt.arm === 'none') fs.mkdirSync(armDir, { recursive: true });
const capMap = capabilities[opt.arm] ?? {};

const overlay = fs.readFileSync(path.join(here, 'overlay-base.yml'), 'utf8') + `
- id: skill-filesystem
  name: "@deepseek-ai/dsh-skill-filesystem"
  config:
    includeDefaultRoots: false
    customSkillDirs:
      - '${armDir}'
`;
const overlayPath = path.join(runDir, 'overlay.yml');
fs.writeFileSync(overlayPath, overlay);

const selected = opt.only ? cases.filter((c) => opt.only.split(',').includes(c.id)) : cases;

function runOne(c) {
  const caseDir = path.join(runDir, c.id);
  const ws = path.join(caseDir, 'ws');
  fs.rmSync(caseDir, { recursive: true, force: true });
  fs.mkdirSync(ws, { recursive: true });
  if (c.fixture) fs.cpSync(path.join(here, 'fixtures', c.fixture), ws, { recursive: true });

  return new Promise((resolve) => {
    const started = Date.now();
    const child = spawn(process.execPath, [DSH_BIN, '--profile', 'headless', '--patch', overlayPath, '--json', c.prompt], {
      cwd: ws,
      env: { ...process.env, DSH_HOME, DSH_TELEMETRY_MODE: 'DISABLED' },
      windowsHide: true,
    });
    let out = '';
    let err = '';
    child.stdout.on('data', (d) => { out += d; });
    child.stderr.on('data', (d) => { err += d; });
    const timer = setTimeout(() => child.kill(), Number(opt.timeoutMin) * 60_000);
    child.on('close', (code) => {
      clearTimeout(timer);
      fs.writeFileSync(path.join(caseDir, 'events.jsonl'), out);
      if (err) fs.writeFileSync(path.join(caseDir, 'stderr.txt'), err);
      resolve(grade(c, out, code, Date.now() - started));
    });
  });
}

function grade(c, raw, exitCode, ms) {
  const events = raw.split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  const final = events.filter((e) => e.type === 'final').map((e) => e.text).join('\n')
    || events.filter((e) => e.type === 'text').map((e) => e.text).join('');
  const calls = events.filter((e) => e.type === 'tool_call');
  const loaded = calls.filter((e) => e.tool === 'skill').map((e) => e.input?.name).filter(Boolean);
  // v2 registry route: SKILL.md read from the arm directory counts as engaging that skill.
  const armNorm = armDir.replace(/\\/g, '/').toLowerCase();
  for (const e of calls) {
    if (e.tool === 'skill') continue;
    const s = JSON.stringify(e.input ?? {}).replace(/\\\\/g, '/').toLowerCase();
    const m = s.match(/([a-z0-9-]+)\/skill\.md/);
    if (m && s.includes(armNorm.slice(-30))) loaded.push(m[1]);
  }
  let input = 0; let output = 0; let steps = 0;
  for (const e of events) {
    if (e.type === 'status' && e.phase === 'step_end' && e.usage) {
      steps++;
      input += (e.usage.inputTokens ?? 0) + (e.usage.cacheReadTokens ?? 0);
      output += e.usage.outputTokens ?? 0;
    }
  }
  const checks = [];
  const has = (cap) => (capMap[cap] ?? []).some((s) => loaded.includes(s));
  for (const cap of c.expect ?? []) checks.push({ check: `expect:${cap}`, pass: has(cap) });
  for (const cap of c.forbid ?? []) checks.push({ check: `forbid:${cap}`, pass: !has(cap) });
  if (c.forbidAnySkill) checks.push({ check: 'forbid:any-skill', pass: loaded.length === 0 });
  for (const re of c.must ?? []) checks.push({ check: `must:${re.source}`, pass: new RegExp(re.source, 'iu').test(final) });
  for (const re of c.mustNot ?? []) checks.push({ check: `mustNot:${re.source}`, pass: !new RegExp(re.source, 'iu').test(final) });
  const completed = events.some((e) => e.type === 'final');
  if (!completed) checks.push({ check: 'completed', pass: false });
  return {
    id: c.id, kind: c.kind, arm: opt.arm, label: opt.label,
    pass: checks.every((x) => x.pass), score: checks.filter((x) => x.pass).length / Math.max(1, checks.length),
    checks, skills: [...new Set(loaded)], toolCalls: calls.length, steps, inputTokens: input, outputTokens: output,
    seconds: Math.round(ms / 1000), exitCode, finalChars: final.length,
  };
}

const results = [];
let next = 0;
async function worker() {
  while (next < selected.length) {
    const c = selected[next++];
    const r = await runOne(c);
    results.push(r);
    fs.appendFileSync(path.join(runDir, 'results.jsonl'), JSON.stringify(r) + '\n');
    console.log(`${r.id} ${r.pass ? 'PASS' : 'FAIL'} score=${r.score.toFixed(2)} skills=[${r.skills.join(',')}] in=${r.inputTokens} out=${r.outputTokens} ${r.seconds}s`);
  }
}
fs.rmSync(path.join(runDir, 'results.jsonl'), { force: true });
await Promise.all(Array.from({ length: Number(opt.concurrency) }, worker));

const by = (k) => {
  const g = {};
  for (const r of results) (g[r[k]] ??= []).push(r);
  return Object.fromEntries(Object.entries(g).map(([key, rs]) => [key, {
    n: rs.length, pass: rs.filter((r) => r.pass).length,
    meanScore: +(rs.reduce((a, r) => a + r.score, 0) / rs.length).toFixed(3),
    inputTokens: rs.reduce((a, r) => a + r.inputTokens, 0),
    outputTokens: rs.reduce((a, r) => a + r.outputTokens, 0),
  }]));
};
const summary = { label: opt.label, arm: opt.arm, armDir, total: by('arm')[opt.arm], byKind: by('kind') };
fs.writeFileSync(path.join(runDir, 'summary.json'), JSON.stringify(summary, null, 2));
console.log(JSON.stringify(summary, null, 2));
