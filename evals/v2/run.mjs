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
import { gradeEvents } from './grade.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..', '..');
const DSH_BIN = process.env.DSH_BIN ?? 'C:\\dsh-lab\\app-0.2.1-rc.2\\node_modules\\@deepseek-ai\\dsh\\lib\\bin.js';
const DSH_HOME = process.env.DSH_HOME ?? 'C:\\dsh-lab\\home';

// --stall-sec: a case that emits no event for this long is an infrastructure stall (upstream
// silently dropped the request); it is killed and retried up to --retries times. The same
// rule applies to every arm, and wasted tokens of stalled attempts are reported separately.
const opt = { concurrency: 2, timeoutMin: 12, stallSec: 240, retries: 2 };
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

async function runCase(c) {
  const wasted = { attempts: 0, inputTokens: 0, outputTokens: 0 };
  for (let attempt = 1; ; attempt++) {
    const r = await runOne(c);
    if (!r.stalled || attempt > Number(opt.retries)) {
      return { ...r, attempt, stalledAttempts: wasted.attempts, wastedInputTokens: wasted.inputTokens };
    }
    wasted.attempts++;
    wasted.inputTokens += r.inputTokens;
    wasted.outputTokens += r.outputTokens;
    console.log(`${c.id} stalled on attempt ${attempt} after ${r.seconds}s; retrying`);
  }
}

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
    let lastActivity = Date.now();
    let stalled = false;
    child.stdout.on('data', (d) => { out += d; lastActivity = Date.now(); });
    child.stderr.on('data', (d) => { err += d; });
    const timer = setTimeout(() => child.kill(), Number(opt.timeoutMin) * 60_000);
    const watchdog = setInterval(() => {
      if (Date.now() - lastActivity > Number(opt.stallSec) * 1000) {
        stalled = true;
        child.kill();
      }
    }, 5_000);
    child.on('close', (code) => {
      clearTimeout(timer);
      clearInterval(watchdog);
      fs.writeFileSync(path.join(caseDir, 'events.jsonl'), out);
      if (err) fs.writeFileSync(path.join(caseDir, 'stderr.txt'), err);
      resolve({ ...grade(c, out, code, Date.now() - started), stalled });
    });
  });
}

function grade(c, raw, exitCode, ms) {
  return { ...gradeEvents(c, raw, { armDir, capMap }), arm: opt.arm, label: opt.label, exitCode, seconds: Math.round(ms / 1000) };
}

const results = [];
let next = 0;
async function worker() {
  while (next < selected.length) {
    const c = selected[next++];
    const r = await runCase(c);
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
