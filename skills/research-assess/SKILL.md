---
name: "research-assess"
description: "Judges a research proposal, direction, hypothesis or claim before time is spent on it: checks the project's own scope, the premise, the closest prior work, the reasoning, and designs the experiment that would decide it. Use for 'có khả thi không', 'đáng làm không', 'lập luận này đúng không', 'đủ tầm chưa'. Triggers — thẩm định, phản biện đề xuất, khả thi, novelty, đủ Q2 chưa, lập luận đúng không."
---

# research-assess — decide what is known, what is not, and what would settle it

Past failures came from wrong inferences and ignored project scope, not from too little
reading. Follow the steps in order; each one can end the assessment early. This page is
self-contained: read the project files directly and do not also load `evidence-check`.
A single argument ("lập luận này đúng không") needs Steps 0, 1
and 3 and a short verdict.

## Step 0 — Load the project's scope (always)
Read `notes/claims-ledger.md` in full: the header, every `SCOPE` row, every `active` row
(not only the chain you are asked about), and `T-`/`revised→` rows. Read the project
README or protocol if present, and `notes/lessons.md` (first 40 lines). Quote any row that
constrains the answer (e.g. "no venue band", "internal report").

## Step 1 — Check the premise
Restate the question as a checkable claim. If the premise is false or ambiguous according
to the project's files (e.g. the pipeline already handles the case), say so with the file
and line before anything else. Ask one question only if two readings lead to different answers.

## Step 2 — Closest prior evidence
Name what the proposal depends on and read it at the depth the claim needs; load
`paper-read` only when a paper must be read at method depth. Record the depth reached
(`abstract` · `skim` · `full`). Without `full` reading, novelty is "chưa xác lập".

## Step 3 — Reasoning check
Run these six questions (the checklist of `../_shared/reasoning-check.md`, which only adds
examples) on every derived, causal or universal claim in the proposal:
1. **Scope** — what does the source, theorem or table guarantee, and what is it used for?
2. **Bound type** — upper bound, lower bound, expectation or one observation; used as that type?
3. **Counter-example** — one concrete case where the premise holds and the conclusion fails.
4. **Control** — for "X caused the gain", list every other change in the same run.
5. **Same problem class** — same task, data regime and metric?
6. **Depth vs strength** — was the source read deeply enough for the wording?

Typical catches: a theorem used beyond what it guarantees; a gain attributed to one change
while several changed; "no prior work" from abstracts; a bound used as an expectation.

## Step 4 — Independent critic (deep mode or high stakes)
If the host offers subagents and the user asked for depth (`sâu`, "phản biện độc lập"),
give a fresh agent only the proposal and the source files, not your conclusions, and ask
it for the strongest objections and one counter-example. Merge only objections you can
verify against the files.

## Step 5 — Decide and design
Output, in Vietnamese:
1. **Kết luận ngắn** — giữ / thu hẹp / bác, one sentence each for the main claims.
2. **Điều đã biết** (with file:line or source + depth) and **điều chưa biết**.
3. **Thí nghiệm phân định** — the smallest experiment whose outcome would separate the
   competing explanations (data, metric, control, expected sign of the effect).
4. **Khả thi** — data, compute (with the basis), baseline, dependencies; missing → "chưa chạy được như mô tả".
5. Venue or novelty wording only if the project scope allows. Project `SCOPE` rows override
   any rubric. A venue band needs the user's request, scope permission and its conditions
   in the same sentence; otherwise write `Venue band: chưa gán — <why>, <what would allow it>`.
   Never upgrade a band because the user pushes back. Open `../_shared/research-integrity.md`
   only to tag formulas in a proposal or to record a revision.

Write `notes/assess-<slug>.md` and ledger rows (via `research-memory`) only when the user
asks to record the assessment; otherwise offer it in one line. A revision of an earlier
claim records its evidence class.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
