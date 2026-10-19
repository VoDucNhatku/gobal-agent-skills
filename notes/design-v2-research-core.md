# Design — v2 research core

**Date:** 2026-10-20 · **Branch:** `v2-research-core` · **Status:** implemented, measured on dsh (see Results)

## Why

The suite is used mostly for reading papers, running training code and deep multi-domain
research. Three measured problems in v1:

1. **Catalog cost.** 64 skills were model-visible; their descriptions cost ~9.4k tokens on
   every turn (script estimate) and Claude Code dropped the descriptions of 37 skills when
   the listing exceeded its budget (F-01).
2. **Chained loading.** A narrow question pulled `admin` → `research-admin` → workers →
   rule files from `~/.claude/rules` (~18k tokens auto-loaded in Claude Code). On dsh one
   short-paper summary cost 236,597 input tokens; two baseline cases ran past 12 minutes.
3. **Reasoning errors, not reading errors.** 11 of 14 confirmed errors in the NCKH T07 session
   were inference errors (F-19…F-28); a global venue rubric overrode the project's own scope (F-18).

## Architecture

| Layer | Content | In the catalog? |
|---|---|---|
| Core (9) | `admin`, `paper-read`, `paper-synthesize`, `research-assess`, `evidence-check`, `experiment`, `code-senior`, `research-memory`, `research-write` | yes (~1k tokens) |
| Packs (48) | writing/LaTeX, learning, code process, web, ops, career | no — `disable-model-invocation: true`; `admin` lists them and reads `../<skill>/SKILL.md` on demand |
| Shared policy | `.claude/skills/_shared/` (`evidence.md`, `reasoning-check.md`, `research-integrity.md`, `conventions.md`, `rules/`) | no — read only when a skill points to it |

`~/.claude/rules` keeps at most `evidence-first.md` (~20 lines). Everything else moved into
`_shared` so it is no longer injected on every turn.

## Old → new

| v1 | v2 |
|---|---|
| `paper-read`, `paper-method` | `paper-read` (modes `answer`, `gist`, `summary`, `think`, `method`, `recipe`, `eli5`, `mindmap`) |
| `paper-triage`, `paper-synthesize` | `paper-synthesize` (adds `triage`, `conflicts`) |
| `research-admin`, `ieee-q1-devil-advocate` (proposal stage) | `research-assess` (project scope first, premise, prior, six reasoning questions, independent critic, deciding experiment) |
| `hallucination-guard` (+ parts of `verification-before-completion`) | `evidence-check` (numbers recomputed, versions, corrections, reasoning, explicit check scope) |
| `paper-to-notebook`, `run-on-modal` | `experiment` (plan, notebook, Modal, honest analysis of seeds and curves) |
| `debug-investigator`, `code-senior` | `code-senior` |
| `project-memory`, `learnings-db`, `audit-log`, `artifact-manager` | `research-memory` (ledger with `SCOPE`/`T-` rows, corrections, lessons, experiments, index) |
| `research-admin` manuscript chain | `research-write` (thin pipeline over the writing pack) |
| `admin`, `code-admin`, `workbench-admin`, `skill-router`, `web-admin` | `admin` (one routing decision + the hidden-skill table) |
| 7 deprecated aliases | removed |
| `rules/research-proposal-integrity.md` | `_shared/research-integrity.md` (project scope overrides the rubric; "chưa gán" is a valid band; revisions record evidence class) |

## The improvement loop ("càng dùng càng tinh")

1. A confirmed mistake is written to the project's `notes/lessons.md` (`research-memory lesson`).
2. Core research skills read the first 40 lines of `lessons.md` before research work.
3. A mistake that would recur elsewhere becomes a case in `evals/v2/cases.mjs`.
4. Any change to a skill is accepted only if `node evals/v2/run.mjs` does not regress.

## Measurement

`evals/v2/` runs 30 cases headless on DeepSeek Harness (GPT 6.1 Sol via 9Router):
12 routing (right skill, or none), 12 quality (answers checked by regex against fixtures
with known answers), 6 regression replays of NCKH T07 errors. Each arm gets a frozen
skill directory; tokens = input + cache-read summed over steps.

## Host status

- **Claude Code:** install with `node scripts/install_v2.mjs` (backs up first; `--retire-rules ~/.claude/rules` moves the old auto-loaded rules into the backup).
- **dsh:** same installer with `--target C:\dsh-lab\home\skills` (and `skills-admin`); the
  frontmatter flags are honoured by dsh's skill loader (`dsh-skill-filesystem`).
- **Antigravity:** `scripts/build_antigravity.py` still expects the v1 inventory and
  `~/.claude/rules` paths; the generated `skills/` tree on this branch is the v1 build.
  Updating the builder is a separate task.

## Results

See `notes/eval-v2-2026-10-20.md`.
