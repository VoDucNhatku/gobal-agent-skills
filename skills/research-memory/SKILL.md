---
name: "research-memory"
description: "Keeps a research project's memory in files so later sessions do not repeat mistakes: claims ledger with scope rows and revisions, technical corrections, lessons from confirmed errors, experiment log, artifact index. Use to record a decision, a correction or a lesson, or to recover where a project stands. Triggers — ghi lại, lưu, nhớ, bài học, đính chính, ledger, phiên trước làm gì, tiếp tục dự án."
---

# research-memory — files that make the next session smarter

All paths are relative to the project root. Create a file on first use with the header shown.
Append; never rewrite history (mark old rows instead).

## Files and row formats
| File | Row |
|---|---|
| `notes/claims-ledger.md` | `\| ID \| date \| claim \| type \| status \| scope / evidence class \|` — ID `SCOPE-n` (project rules, e.g. no venue band), `C-n` (claims), `T-n` (technical facts); status `active` / `revised→<id>` / `dropped` |
| `notes/corrections.md` | `- T-n (date): <old statement> → <corrected statement>. Evidence: <run / file:line / source>.` |
| `notes/lessons.md` | `- L-n (date) [<area>]: Sai: <what went wrong>. Vì: <cause>. Lần sau: <concrete rule>. Ca kiểm: <eval id or "chưa có">.` |
| `notes/experiments.md` | `\| date \| run id \| config/commit \| seed \| metric=value \| log path \|` |
| `notes/INDEX.md` | `\| id \| skill \| path \| one-line gist \| date \|` |

Ledger details (sources, stance, review) for deep evidence work:
`../admin/references/claim-ledger.md`.

## Modes
- `recall` — read `notes/INDEX.md`, ledger header + `SCOPE` + `active` rows, the last 10
  lessons and corrections; answer "where does the project stand" in ≤ 10 lines.
- `claim` — add or revise a claim. A revision states its evidence class
  (`run result` · `full method read` · `abstract only` · `inference` · `user argument`); the
  last two cannot change a claim on their own (see `../_shared/research-integrity.md` §4).
- `correct` — record a corrected technical fact in `corrections.md` and as a `T-` ledger row.
- `lesson` — record a confirmed mistake (one the user or a check confirmed, not a guess).
- `run` — log an experiment row.
- `index` — add or refresh an artifact row.

## The improvement loop
A lesson is only useful if it changes behaviour:
1. Record it in `notes/lessons.md` with a concrete "Lần sau" rule.
2. Research skills read the first 40 lines of `lessons.md` before research work, so keep
   the newest and most general lessons at the top and merge duplicates.
3. If the mistake would recur in other projects, propose an eval case for the skill suite
   (`evals/v2/cases.mjs` in the skills repo) and name it in "Ca kiểm". The suite owner decides.

Write to `notes/` only. Never store secrets, tokens or personal data in these files.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
