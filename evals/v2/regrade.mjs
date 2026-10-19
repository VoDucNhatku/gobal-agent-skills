// Re-grade saved runs with the current cases.mjs, without calling any model.
// Usage: node evals/v2/regrade.mjs --label <run label> --arm <baseline|v2|none>
// Rewrites .tmp/runs/<label>/results.jsonl in place; the previous file is kept as results.orig.jsonl.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { cases } from './cases.mjs';
import { capabilities } from './capabilities.mjs';
import { gradeEvents } from './grade.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const label = args[args.indexOf('--label') + 1];
const arm = args[args.indexOf('--arm') + 1];
const runDir = path.resolve(here, '..', '..', '.tmp', 'runs', label);
const resultsPath = path.join(runDir, 'results.jsonl');
const original = fs.readFileSync(resultsPath, 'utf8').split('\n').filter(Boolean).map((l) => JSON.parse(l));
const orig = path.join(runDir, 'results.orig.jsonl');
if (!fs.existsSync(orig)) fs.copyFileSync(resultsPath, orig);

const overlay = fs.readFileSync(path.join(runDir, 'overlay.yml'), 'utf8');
const armDir = (overlay.match(/customSkillDirs:\s*\n\s*-\s*'([^']+)'/) || [])[1] ?? '';
const changed = [];
const out = original.map((r) => {
  const c = cases.find((x) => x.id === r.id);
  const raw = fs.readFileSync(path.join(runDir, r.id, 'events.jsonl'), 'utf8');
  const g = gradeEvents(c, raw, { armDir, capMap: capabilities[arm] ?? {} });
  if (g.pass !== r.pass) changed.push(`${r.id}: ${r.pass ? 'PASS' : 'FAIL'} -> ${g.pass ? 'PASS' : 'FAIL'}`);
  return { ...r, pass: g.pass, score: g.score, checks: g.checks };
});
fs.writeFileSync(resultsPath, out.map((r) => JSON.stringify(r)).join('\n') + '\n');
console.log(`${label}: ${changed.length ? changed.join('; ') : 'no verdict changed'}`);
