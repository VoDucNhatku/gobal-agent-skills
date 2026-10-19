# Conventions (shared, short)

## Language
Prose to the user: Vietnamese, academic register; first use of a term writes
`thuật ngữ tiếng Việt (English term)`. Code, identifiers, file names, commit messages: English.
Never translate model, dataset, library or API names.

## Answer first, file second
- A question about a source ("bài này dùng lr bao nhiêu?") is answered in chat with the
  locator (section, table, file:line). No artifact file.
- Write a file only when the user asks for a note, the mode is a deep read
  (`summary`, `think`, `method`), or the result will be reused by a later step.
- When a file is written, chat gets a short preview (≤ 8 lines) and the path, never the whole file.

## Project files (relative to the project root)
| File | Holds |
|---|---|
| `notes/INDEX.md` | one row per artifact: `id · skill · path · one-line gist` |
| `notes/<id>-<skill>[-<mode>].md` | distilled artifacts, deterministic names |
| `notes/claims-ledger.md` | claims, `SCOPE` rows, `T-` technical corrections, revisions |
| `notes/corrections.md` | short list of corrected facts (optional if the ledger has `T-` rows) |
| `notes/lessons.md` | confirmed mistakes and what to do instead (see research-memory) |
| `notes/experiments.md` | one row per run: config, seed, metric, log path |

Check `notes/INDEX.md` before re-reading a large source; reuse a fresh artifact.

## Reading economy
Search before reading: grep for the section, table or symbol, then read that range.
Do not read a whole file twice. Do not print whole files or logs to answer one question.
