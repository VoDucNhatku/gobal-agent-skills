// Build an isolated skill directory ("arm") for one eval run.
// Usage: node build-arm.mjs --src <skillsDir> [--src <dir> ...] --out <dir> [--hide-deprecated]
// Copies real files (no junctions) so arms stay frozen while sources change.
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const srcs = [];
let out;
let hideDeprecated = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--src') srcs.push(args[++i]);
  else if (args[i] === '--out') out = args[++i];
  else if (args[i] === '--hide-deprecated') hideDeprecated = true;
}
if (!srcs.length || !out) throw new Error('usage: --src <dir> --out <dir>');

const SKIP = new Set(['__pycache__', 'test-reports', 'synced', '.git']);
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });

let count = 0;
for (const src of srcs) {
  for (const name of fs.readdirSync(src)) {
    const dir = path.join(src, name);
    if (SKIP.has(name) || !fs.statSync(dir).isDirectory()) continue;
    // Shared, non-skill resources (e.g. skills/_shared) travel with the skills.
    if (name.startsWith('_')) {
      fs.cpSync(dir, path.join(out, name), { recursive: true });
      continue;
    }
    if (!fs.existsSync(path.join(dir, 'SKILL.md'))) continue;
    fs.cpSync(dir, path.join(out, name), {
      recursive: true,
      filter: (p) => !SKIP.has(path.basename(p)),
    });
    if (hideDeprecated) {
      const f = path.join(out, name, 'SKILL.md');
      const text = fs.readFileSync(f, 'utf8');
      if (/^description:\s*"?DEPRECATED/m.test(text) && !/^disable-model-invocation:/m.test(text)) {
        fs.writeFileSync(f, text.replace(/^---(\r?\n)/, '---$1disable-model-invocation: true$1'));
      }
    }
    count++;
  }
}
console.log(JSON.stringify({ out, skills: count }));
