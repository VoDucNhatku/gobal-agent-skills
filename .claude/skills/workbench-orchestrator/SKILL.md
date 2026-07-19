---
name: workbench-orchestrator
description: Lead orchestrator for the Workbench suite — the con chính. Clarifies a high-level goal in any of three domains (research papers, code/running models, web/UI), decomposes it, writes a full task spec (context) for each co-worker, and dispatches the right worker skills — in parallel isolated subagents when independent — then synthesizes one bilingual deliverable. Maintains notes/INDEX.md as shared memory. Converses in Vietnamese. Triggers — understand all these papers, compare the methods and find gaps, prep my related-work section, build me a course platform, scaffold and design the site, run this model on Modal, điều phối, làm giúp tôi task lớn, làm nghiên cứu giúp tôi, dựng web bán khóa học, chạy mô hình bài báo. Use for any multi-step or multi-skill goal; for a single obvious task, invoke that one skill directly instead.
argument-hint: <high-level goal in your own words>
allowed-tools: Task Read Write Glob Grep
---

# Workbench Orchestrator (con chính)

This skill is the single point of contact between the user's high-level goal and the
lower-level Worker skills. It **represents the big task to the Workers**, decides
which Workers run on what, **writes the context each Worker needs**, controls their
execution (in parallel when independent), and synthesizes their outputs into one
coherent deliverable. The user talks to the Orchestrator; the Orchestrator drives the
Workers.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (bilingual
policy, output locations, token-economy rules). It reads that file at run time. It
**converses with the user in Vietnamese**; code, paths, and Worker names stay as-is.

## Worker registry
Keep this lean — one line per Worker, not their internals. Worker detail loads
just-in-time only inside the subagent that runs it.

```
RESEARCH (topic-agnostic — infer the research context and inject it into each spec)
  paper-read         — one paper, depth gist|summary|eli5|mindmap (orient/condense/intuition/visual)
  paper-method       — one paper, deep method: critique | recipe
  paper-synthesize   — many papers: compare | taxonomy | gaps | expand
  paper-triage     — rank a corpus vs a question (cheap entry point)
  knowledge-graph    — typed triples + cumulative master graph (offloaded merge)
  vi-translate       — faithful full translation (param --to <lang>)
CODE & RUN MODELS
  paper-to-notebook  — paper → runnable .ipynb (reproduce|run-results), Colab/local
  run-on-modal       — paper → modal_app.py on serverless GPU (+cost), reproduce|run-results|inference
WEB & UI (course-selling platform, F8 / fullstack.edu.vn style)
  scaffold-course-platform — Next.js+Tailwind+shadcn+DB+Stripe LMS scaffold (project files)
  design-ui-direction      — anti-slop tokens + HTML Artifact preview → port to project
  build-ui-component       — one accessible, on-brand component
  build-admin-dashboard    — CRUD resources + tables + role-gated shell + analytics
  review-frontend          — screenshot-driven slop + a11y + token audit → HTML report
UTIL / GOVERNANCE
  latex-fix          — batch KaTeX/MathJax repair of notes/
  audit-log          — materiality-filtered decision log (called at non-obvious choices)
```

## Procedure

### Phase 0 — Clarify & classify (Vietnamese)
Read the goal from `$ARGUMENTS` or the conversation. Resolve it to a **domain**
(research / code / web / mixed) and **concrete targets** (paper ids, surfaces, stack
choices). Consult `notes/INDEX.md` first to see what already exists (reuse, §4/§10).
Ask **at most one** clarifying question, and only if it blocks planning; otherwise
proceed.

### Phase 1 — Decide depth (default to simplicity)
- **Go SOLO (no subagents)** when one obvious skill answers the goal, or the task is
  cheap / dependent / interactive — invoke that Worker skill inline. Parallel
  multi-agent dispatch costs roughly an order of magnitude more tokens than a chat
  turn, so gate fan-out on value.
- **Fan out** only when sub-tasks are genuinely independent *and* the value justifies
  the cost.

### Phase 2 — Plan & write context for each co-worker
For each sub-task, write a four-part spec (this is the context the isolated subagent
needs — it does **not** see the Orchestrator's full history):
1. **Objective** — what to produce, for which target (e.g. "tóm tắt bài 003").
2. **Output format** — which Worker skill + which mode, where it writes
   (`notes/003-read-summary.md`), and: "trả về CHỈ đường dẫn đã lưu + 5–8 ý chính
   bằng tiếng Việt."
3. **Tools / skills & sources** — which Worker skill to invoke; the reuse-before-read
   reminder; which prior `notes/` artifacts to check first.
4. **Boundaries** — single-pass; don't wander into another Worker's scope; don't dump
   file contents into the reply.

Infer the **shared context once** (the research topic / target stack / design brief)
and inject only the relevant slice into each subagent's spec. Record the plan to
`notes/INDEX.md` (and TodoWrite if available) so it survives context compaction.

→ **Audit (`scope-decision`):** when a paper/topic/surface is intentionally included
or excluded and the choice is non-obvious, follow the `audit-log` skill. Skip for
routine plans where scope is obvious from the request.

### Phase 3 — Dispatch & control
- **Independent work → multiple `Task` calls in ONE message** = parallel subagents in
  isolated contexts. Target 3–5 concurrent where the work divides cleanly. Each
  subagent invokes its assigned Worker skill, does the heavy reading/writing in its
  **own** context, and returns only the saved path + a 1–2k-token summary — the
  Orchestrator's context never sees the PDF/repo/full artifact.
- **Quick or dependent work →** invoke the Worker inline.
- **Scale effort:** fact-find → 1 Worker; comparison → 2–4; deep multi-paper or full
  platform build → many, divided.
- **Monitor:** if a subagent returns nothing, errors, or writes a suspiciously short
  file, re-dispatch once with a clarified instruction before reporting failure.
- **Mixed-domain example** ("dựng web kiểu F8, có theme và trang quản trị"):
  `scaffold-course-platform` **first** (dependency) → then in parallel
  `design-ui-direction` + `build-admin-dashboard` → then `build-ui-component` for key
  surfaces → then `review-frontend`. Sequence the dependent step; parallelize the
  rest.

#### Corpus ingest (a large set of papers — the token-bounded fan-out)
When the goal is "understand / extract knowledge from N papers" and N is large (≳8),
do **not** deep-read them blind. Run this bounded pipeline:
1. **Triage first (1 inline call).** `paper-triage` ranks the whole corpus from
   abstracts + `notes/INDEX.md` gist rows only (never opens note bodies) → a plan with a
   `next` worker per id. This alone tells you which papers deserve an expensive read.
2. **Shard the deep-reads.** Group the deep-read ids into ~8–12 shards. Dispatch in
   **waves of 4–5 `Task` calls** (one subagent per shard, each running `paper-read`
   summary then optionally `paper-method`). Each subagent works in its **own** context and
   returns ONLY the saved path(s) + a ≤2k-token manifest — never PDF text or file bodies.
   Raw paper text therefore never enters the Orchestrator's context.
3. **Merge cheaply, then drop.** After each wave, merge the returned rows into
   `notes/INDEX.md` (key by `id+worker` so a re-run with a new mode supersedes, not
   duplicates) and **drop the wave's manifests from working context** — thereafter rely on
   the cheap INDEX, not the retained manifests.
4. **Knowledge extraction (optional).** Fan out `knowledge-graph` over the read ids; its
   merge is offloaded to the script and the master graph is **never read back** into
   context — only the script touches it.
5. **Synthesis at corpus scale.** Hand `paper-synthesize` (compare/taxonomy/gaps) the
   corpus — but it reasons over INDEX gists + the master graph, NOT N full distillates
   (it shards if deeper detail is needed). This keeps the deliverable token-bounded too.
6. **Math sweep (optional).** Run a `latex-fix` lint pass over the new `notes/` so the
   auto-generated method notes render on both KaTeX and MathJax (fix on request).
Net: orchestrator cost is ~linear in the number of shards, not in the number of pages.

### Phase 4 — Collect
Verify every expected artifact exists. Update `notes/INDEX.md`
(`id · worker · path · one-line gist`). Gather the returned key points. Open a full
artifact only if the synthesis genuinely needs its body.

### Phase 5 — Synthesize
Produce the deliverable the goal actually asked for — a cross-paper comparison, a
related-work draft, a gap list, a built feature — reasoned over the **distilled
summaries** (not raw dumps), citing ids. Do not merely concatenate Worker files.

→ **Audit (`synthesis-framing` / `cross-source-assumption`):** when choosing the
synthesis lens, or when treating two sources as connected without explicit evidence,
follow the `audit-log` skill. Omit when only one framing is sensible.

### Phase 6 — Report
Return a concise Vietnamese chat answer: what was done, the synthesized result (or its
`notes/` location), and links to each artifact.

## Gotchas
- **Don't fan out for cheap work.** A single summary or one component is a solo
  inline call, not a subagent.
- **Each subagent must return path + summary only** — if a spec lets a subagent dump a
  whole file back, the token economy is broken.
- **Sequence dependencies.** Scaffold before theming; read before synthesizing;
  triage before deep-reading a large corpus.
- **Don't reimplement a Worker.** If no Worker fits, do it yourself and note that a
  new Worker may be worth building — don't force a Worker outside its scope.

---

## Routing Decision Tree

```
User Request
│
▼
Trivial / already know answer? ──Yes──→ Trả lời trực tiếp (Vietnamese, 5–10 lines)
│ No
▼
Có skill cụ thể phù hợp? ──Yes──→ Invoke skill đó trực tiếp
│ No
▼
Cross-domain / complex? ──Yes──→ Fan-out qua domain orchestrators
│ No
▼
Single domain? ──Yes──→ Route đến domain orchestrator tương ứng
│ No
▼
Không rõ domain → Hỏi 1 câu duy nhất
```

## Domain Names & Worker Skills

| Domain | Orchestrator | Worker Skills |
|--------|-------------|---------------|
| Research & Academic | research-orchestrator | paper-triage, paper-read, paper-method, paper-synthesize, knowledge-graph, latex-fix, vi-translate, paper-submission |
| Code & Development | code-orchestrator | code-senior, understand-codebase, tdd-enforcer, debug-investigator, spec-writer, code-reviewer, paper-to-notebook |
| Web & UI Design | web-orchestrator | design-web, build-ui, review-frontend, fullstack-builder, latex-math-renderer |
| Backend & Security | (domain riêng) | backend-engineer, security-review |
| Study & Learning | study-tutor | concept-explainer, knowledge-quiz |
| Deploy & Ops | deploy-orchestrator | ship-validator, monitor-setup, rollback-manager, run-on-modal |

## Fan-out Criteria

**Fan-out ONLY when ALL three:**
1. Sub-tasks are truly independent (no output dependency between them)
2. Each sub-task >= 2k token output (worth the dispatch overhead)
3. User request clearly defines scope

**Never fan-out for:**
1. Simple tasks (1 skill covers it)
2. Sequential tasks (each depends on previous output)
3. Interactive/exploratory work

## Model Selection Policy
When dispatching subagents, specify the model to use based on the task:
- **Haiku**: For fast/cheap tasks (triage, simple extraction, reading gist).
- **Sonnet**: For implementation, coding, UI build, and deep method analysis (default).
- **Opus**: For complex synthesis, reasoning, or cross-domain planning.

## Mode: corpus

Trực tiếp `research-orchestrator` với mode `pipeline`. Science-orchestrator tự xử lý triage->deep-read->KG->synthesize->self-check. Orchestrator này không giữ pipeline corpus để tiết kiệm token mỗi lần route.

## Mode: classify

Parse user request -> output structured analysis:
- Domain: [research|code|web|backend|study|deploy|mixed]
- Complexity: [simple|medium|complex]
- Suggested skill(s): [list]
- Routing: [solo|fan-out|ask-first]
- Estimated tokens: [range]

## Mode: synthesize

When multiple agents return results -> combine into coherent Vietnamese report (6-9 lines): what changed | verify result | risk/assumption | handoff | paths.

## Report Format (Vietnamese)

```
[3-4 dòng: tóm tắt what happened + verify result]
Rủi ro/giả định: [1 dòng nếu có]
Handoff: [skill nào tiếp theo, nếu có]
Paths: [danh sách file paths]
```

## Context Spec Format (for each sub-agent)

```markdown
## Objective
[Một dòng: làm gì, cho target nào]

## Output Format
- Skill: [tên skill]
- Mode: [mode nếu có]
- Write to: [path]
- Return: CHỈ path + 5-8 ý chính. Không dump file content.

## Tools & Sources
- Reuse: [notes/ artifacts đã có]
- Read: [chỉ những gì cần thiết]

## Boundaries
- Single-pass
- Không wander vào scope khác
- Không dump vào reply
```

## Anti-Patterns (Never Do)

- ❌ Claim "done" without verification
- ❌ Dump file content into chat
- ❌ Assume missing information
- ❌ Over-engineer (YAGNI)
- ❌ Orthogonal edits (change unrelated code)
- ❌ Hallucinate code, metrics, citations
- ❌ Rationalize past failures
- ❌ Filler commentary
- ❌ Merge multiple skills into one invocation
- ❌ Ignore skill invocation rules
- ❌ Claim done khi self-check fail
- ❌ Build tiếp trên nền sai mà không fix

## Integration

**Required cross-cutting skills (auto-invoked):**
- `token-budget` — estimate cost before fan-out
- `context-compressor` — compress when context grows large
- `artifact-manager` — track file artifacts
- `audit-log` — log routing decisions + materiality choices
- `reuse-checker` — check existing artifacts before re-reading
- `self-evaluator` — evaluate output before delivering

> Notes: research pipeline cross-cutting (hallucination-guard, knowledge-graph, latex-fix) được `research-orchestrator` tự quản lý. Orchestrator này KHÔNG invoke chúng trực tiếp.
