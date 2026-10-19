// Install the v2 skill suite from .claude/skills into a host's skill directory.
// Usage:
//   node scripts/install_v2.mjs [--target ~/.claude/skills] [--dry-run]
//   node scripts/install_v2.mjs --target C:\dsh-lab\home\skills
// What it does:
//   1. Backs up every directory it will replace or remove to <target>/../skills-backup-<stamp>/.
//   2. Removes suite skills that v2 absorbed (listed in REMOVED), leaving unrelated skills alone.
//   3. Copies every skill directory and the shared `_shared/` folder from the source.
//   4. With --retire-rules <dir>: moves the old suite rule files out of an auto-loaded rules
//      directory (e.g. ~/.claude/rules) into the backup, because v2 reads them on demand.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const source = path.resolve(here, '..', '.claude', 'skills');
const args = process.argv.slice(2);
const opt = { target: path.join(os.homedir(), '.claude', 'skills'), dryRun: false, retireRules: null };
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--target') opt.target = args[++i].replace(/^~/, os.homedir());
  else if (args[i] === '--dry-run') opt.dryRun = true;
  else if (args[i] === '--retire-rules') opt.retireRules = args[++i].replace(/^~/, os.homedir());
}

// Skills that existed in v1 and were merged into v2 skills.
const REMOVED = [
  'research-admin', 'paper-method', 'paper-triage', 'run-on-modal', 'code-admin',
  'debug-investigator', 'learnings-db', 'audit-log', 'artifact-manager', 'hallucination-guard',
  'paper-to-notebook', 'project-memory', 'build-ui-component', 'design-ui-direction',
  'latex-math-renderer', 'reuse-checker', 'skill-router', 'web-admin', 'workbench-admin',
];
// Rule files of the v1 suite that were auto-loaded from ~/.claude/rules.
const OLD_RULES = [
  'workbench-conventions.md', 'research-proposal-integrity.md', 'paper-writing-integrity.md',
  'latex-katex-compat.md', 'frontend-aesthetics.md', 'course-domain-model.md',
  'architecture-integrity.md', 'evidence-first.md',
];

const SKIP = new Set(['__pycache__', 'test-reports']);
const incoming = fs.readdirSync(source).filter((n) => {
  const p = path.join(source, n);
  return fs.statSync(p).isDirectory() && !SKIP.has(n) && (n === '_shared' || fs.existsSync(path.join(p, 'SKILL.md')));
});

const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
const backup = path.join(path.dirname(opt.target), `skills-backup-${stamp}`);
const plan = [];
for (const n of [...incoming, ...REMOVED]) {
  const p = path.join(opt.target, n);
  if (fs.existsSync(p)) plan.push({ backup: p, remove: true, install: incoming.includes(n) });
}

const log = (m) => console.log((opt.dryRun ? '[dry-run] ' : '') + m);
log(`source  ${source}`);
log(`target  ${opt.target}`);
log(`install ${incoming.length} entries; replace/remove ${plan.length}; backup -> ${backup}`);
if (opt.dryRun) process.exit(0);

fs.mkdirSync(opt.target, { recursive: true });
for (const item of plan) {
  fs.cpSync(item.backup, path.join(backup, path.basename(item.backup)), { recursive: true });
  fs.rmSync(item.backup, { recursive: true, force: true });
}
for (const n of incoming) {
  fs.cpSync(path.join(source, n), path.join(opt.target, n), {
    recursive: true,
    filter: (p) => !SKIP.has(path.basename(p)) && !p.endsWith('.pyc'),
  });
}
if (opt.retireRules) {
  for (const r of OLD_RULES) {
    const p = path.join(opt.retireRules, r);
    if (!fs.existsSync(p)) continue;
    fs.mkdirSync(path.join(backup, 'rules'), { recursive: true });
    fs.renameSync(p, path.join(backup, 'rules', r));
    log(`retired rule ${r}`);
  }
}
log(`done: ${incoming.length} installed, backup at ${backup}`);
