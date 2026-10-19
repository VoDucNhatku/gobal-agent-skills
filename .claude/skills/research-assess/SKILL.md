---
name: "research-assess"
description: "Judges a research proposal, direction, hypothesis or claim before time is spent on it: checks the project's own scope, the premise, the closest prior work, the reasoning, and designs the experiment that would decide it. Use for 'có khả thi không', 'đáng làm không', 'lập luận này đúng không', 'đủ tầm chưa'. Triggers — thẩm định, phản biện đề xuất, khả thi, novelty, đủ Q2 chưa, lập luận đúng không."
argument-hint: "<proposal path or claim> [quick|deep]"
allowed-tools: "Skill Agent AskUserQuestion Read Write Glob Grep Bash WebSearch WebFetch"
---

# research-assess — decide what is known, what is not, and what would settle it

Past failures came from wrong inferences and ignored project scope, not from too little
reading. Follow the steps in order; each one can end the assessment early.

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
Name what the proposal depends on and read it at the depth the claim needs (via
`paper-read`). Record the depth reached. Without `full` reading, novelty is "chưa xác lập".

## Step 3 — Reasoning check
Run the six questions of `../_shared/reasoning-check.md` on every derived, causal or
universal claim in the proposal. Typical catches: a theorem used beyond what it
guarantees; a gain attributed to one change while several changed; "no prior work" from
abstracts; a bound used as an expectation.

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
5. Venue or novelty wording only if the project scope allows; follow `../_shared/research-integrity.md`.

Write `notes/assess-<slug>.md` when the assessment will be reused; append claim rows to the
ledger via `research-memory`. A revision of an earlier claim records its evidence class.
