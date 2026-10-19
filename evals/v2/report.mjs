// Merge eval runs per arm and print a Markdown comparison.
// Usage: node evals/v2/report.mjs --arm baseline=baseline-r1,baseline-r1b --arm v2=v2-r2 [--out file.md]
// Later labels override earlier ones for the same case id (used for re-runs of stalled cases).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { cases } from './cases.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const runsDir = path.resolve(here, '..', '..', '.tmp', 'runs');
const args = process.argv.slice(2);
const arms = [];
let out;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--arm') {
    const [name, labels] = args[++i].split('=');
    arms.push({ name, labels: labels.split(',') });
  } else if (args[i] === '--out') out = args[++i];
}

function load(labels) {
  const byId = new Map();
  for (const label of labels) {
    const f = path.join(runsDir, label, 'results.jsonl');
    if (!fs.existsSync(f)) continue;
    for (const line of fs.readFileSync(f, 'utf8').split('\n').filter(Boolean)) {
      const r = JSON.parse(line);
      byId.set(r.id, { ...r, fromLabel: label });
    }
  }
  return byId;
}

const data = arms.map((a) => ({ ...a, results: load(a.labels) }));
const kinds = ['routing', 'quality', 'regression'];
const fmtK = (n) => (n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(n));
const median = (xs) => {
  const s = [...xs].sort((a, b) => a - b);
  return s.length ? (s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2) : 0;
};

const lines = [];
lines.push('| Arm | Cases | Pass | Mean score | Input tokens (sum) | Input / case (median) | Output tokens | Timed out | Stalled retries |');
lines.push('|---|---|---|---|---|---|---|---|---|');
for (const a of data) {
  const rs = [...a.results.values()];
  const timedOut = rs.filter((r) => r.checks.some((c) => c.check === 'completed' && !c.pass)).length;
  lines.push(`| ${a.name} | ${rs.length} | ${rs.filter((r) => r.pass).length} | ${(rs.reduce((s, r) => s + r.score, 0) / Math.max(1, rs.length)).toFixed(2)} | ${fmtK(rs.reduce((s, r) => s + r.inputTokens, 0))} | ${fmtK(median(rs.map((r) => r.inputTokens)))} | ${fmtK(rs.reduce((s, r) => s + r.outputTokens, 0))} | ${timedOut} | ${rs.reduce((s, r) => s + (r.stalledAttempts ?? 0), 0)} |`);
}
lines.push('');
lines.push('| Kind | ' + data.map((a) => `${a.name} pass`).join(' | ') + ' | ' + data.map((a) => `${a.name} median input`).join(' | ') + ' |');
lines.push('|---|' + data.map(() => '---|').join('') + data.map(() => '---|').join(''));
for (const k of kinds) {
  const cells = data.map((a) => {
    const rs = [...a.results.values()].filter((r) => r.kind === k);
    return `${rs.filter((r) => r.pass).length}/${rs.length}`;
  });
  const tok = data.map((a) => fmtK(median([...a.results.values()].filter((r) => r.kind === k).map((r) => r.inputTokens))));
  lines.push(`| ${k} | ${cells.join(' | ')} | ${tok.join(' | ')} |`);
}
lines.push('');
lines.push('| Case | ' + data.map((a) => `${a.name}`).join(' | ') + ' |');
lines.push('|---|' + data.map(() => '---|').join(''));
for (const c of cases) {
  const cells = data.map((a) => {
    const r = a.results.get(c.id);
    if (!r) return '—';
    const failed = r.checks.filter((x) => !x.pass).map((x) => x.check.split(':')[0] === 'must' || x.check.split(':')[0] === 'mustNot' ? x.check.slice(0, 18) : x.check).join('; ');
    return `${r.pass ? '✅' : '❌'} ${fmtK(r.inputTokens)} · ${r.skills.join(', ') || 'no skill'}${failed ? ` · fail: ${failed}` : ''}`;
  });
  lines.push(`| ${c.id} | ${cells.join(' | ')} |`);
}
const md = lines.join('\n');
if (out) fs.writeFileSync(out, md + '\n');
console.log(md);
