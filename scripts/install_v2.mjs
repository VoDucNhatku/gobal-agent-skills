// Install the v2 skill suite from .claude/skills into a host's skill directory.
// Usage:
//   node scripts/install_v2.mjs [--target ~/.claude/skills] [--dry-run]
//   node scripts/install_v2.mjs --retire-rules ~/.claude/rules
//   node scripts/install_v2.mjs --target C:\dsh-lab\home\skills
// What it does:
//   1. Backs up every directory it will replace or remove to <target>/../skills-backup-<stamp>/.
//   2. Removes suite skills that v2 absorbed (listed in REMOVED), leaving unrelated skills alone.
//   3. Copies every skill directory and the shared `_shared/` folder from the source.
//   4. With --retire-rules <dir>: moves the old suite rule files out of an auto-loaded rules
//      directory (e.g. ~/.claude/rules) into the backup, because v2 reads them on demand, then
//      installs the always-on rules v2 still ships (.claude/rules/, i.e. evidence-first.md)
//      into that directory, creating it if needed and backing up any different copy.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const source = path.resolve(here, '..', '.claude', 'skills');
const rulesSource = path.resolve(here, '..', '.claude', 'rules');
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
let backup = path.join(path.dirname(opt.target), `skills-backup-${stamp}`);
for (let i = 2; fs.existsSync(backup); i++) backup = path.join(path.dirname(opt.target), `skills-backup-${stamp}-${i}`);
const plan = [];
for (const n of [...incoming, ...REMOVED]) {
  const p = path.join(opt.target, n);
  if (fs.existsSync(p)) plan.push({ backup: p, remove: true, install: incoming.includes(n) });
}

// Always-on rules v2 ships; they replace the copy of the same name instead of being retired.
const keptRules = fs.existsSync(rulesSource)
  ? fs.readdirSync(rulesSource).filter((n) => n.endsWith('.md'))
  : [];
const rulePlan = [];
if (opt.retireRules) {
  for (const r of OLD_RULES) {
    if (!keptRules.includes(r) && fs.existsSync(path.join(opt.retireRules, r))) rulePlan.push({ retire: r });
  }
  for (const r of keptRules) {
    const dest = path.join(opt.retireRules, r);
    const fresh = fs.readFileSync(path.join(rulesSource, r));
    if (!fs.existsSync(dest)) rulePlan.push({ install: r });
    else if (!fs.readFileSync(dest).equals(fresh)) rulePlan.push({ install: r, replace: true });
  }
}

const log = (m) => console.log((opt.dryRun ? '[dry-run] ' : '') + m);
log(`source  ${source}`);
log(`target  ${opt.target}`);
log(`install ${incoming.length} entries; replace/remove ${plan.length}; backup -> ${backup}`);
if (opt.retireRules) {
  for (const item of rulePlan) {
    if (item.retire) log(`rules   retire ${item.retire}`);
    else log(`rules   ${item.replace ? 'update' : 'add'} ${item.install} -> ${opt.retireRules}`);
  }
}
if (opt.dryRun) process.exit(0);

// fs.cpSync is avoided: on some Windows Node versions it aborts the process (0xC0000409)
// when a path contains non-ASCII characters, e.g. a Vietnamese user name.
function copyDir(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    if (SKIP.has(entry.name) || entry.name.endsWith('.pyc')) continue;
    const src = path.join(from, entry.name);
    if (entry.isDirectory()) copyDir(src, path.join(to, entry.name));
    else fs.copyFileSync(src, path.join(to, entry.name));
  }
}

fs.mkdirSync(opt.target, { recursive: true });
if (plan.length) fs.mkdirSync(backup, { recursive: true });
for (const item of plan) {
  // The backup sits next to the target, on the same volume, so a rename moves it whole.
  fs.renameSync(item.backup, path.join(backup, path.basename(item.backup)));
}
for (const n of incoming) copyDir(path.join(source, n), path.join(opt.target, n));
if (opt.retireRules) {
  const ruleBackup = path.join(backup, 'rules');
  fs.mkdirSync(opt.retireRules, { recursive: true });
  for (const item of rulePlan) {
    if (item.retire) {
      fs.mkdirSync(ruleBackup, { recursive: true });
      fs.renameSync(path.join(opt.retireRules, item.retire), path.join(ruleBackup, item.retire));
      log(`retired rule ${item.retire}`);
      continue;
    }
    const dest = path.join(opt.retireRules, item.install);
    if (item.replace) {
      fs.mkdirSync(ruleBackup, { recursive: true });
      fs.copyFileSync(dest, path.join(ruleBackup, item.install));
    }
    fs.copyFileSync(path.join(rulesSource, item.install), dest);
    log(`${item.replace ? 'updated' : 'added'} rule ${item.install}`);
  }
}
log(`done: ${incoming.length} installed, backup at ${backup}`);
log('start a new Claude Code session: rules and skill lists load when a session opens');
