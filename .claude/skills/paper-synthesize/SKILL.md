---
name: paper-synthesize
description: Synthesizes ACROSS many papers — the cross-paper Worker of the Workbench suite. Modes — compare (side-by-side table + differentiators + a hybrid-pipeline proposal), taxonomy (organizing dimensions + named categories + matrix), gaps (recurring weaknesses, white space → concrete research opportunities), expand (generalize ONE problem into its broader class, relaxable assumptions, open sub-problems). Reasons over already-distilled notes/ when present. Triggers — compare papers, so sánh bài báo, which is better, đề xuất pipeline kết hợp, systematize, hệ thống hóa, build a taxonomy, dựng khung phân loại, research gaps, khoảng trống nghiên cứu, future directions, hướng nghiên cứu, what's missing, generalize the problem, khái quát vấn đề. It does NOT condense one paper (use paper-read), critique one method (use paper-method), or extract typed entities (use knowledge-graph).
argument-hint: <ids|all|topic> [compare|taxonomy|gaps|expand]
allowed-tools: Skill Agent Read Write Glob Bash
---

# Paper Synthesize (tổng hợp liên-paper)

Cross-paper / cross-topic synthesis. Four modes, selected by `$ARGUMENTS`:
- **`compare`** (default) — side-by-side comparison table (rows = papers, cols = dimensions)
  + narrative differentiators + per-stage **hybrid-pipeline** proposal (best component per
  stage) with a Mermaid flowchart and integration risks.
- **`taxonomy`** — derive organizing dimensions, group papers into named categories with a
  rationale, then a comparison matrix; narrate clusters / trends / outliers.
- **`gaps`** — aggregate recurring weaknesses, untested settings, shared assumptions, eval/
  data gaps, and white space; convert each gap → opportunity (why it matters + a concrete
  direction), cited to source ids.
- **`expand`** — zoom OUT from one paper/topic: name the broader problem class, give an
  abstract formulation (LaTeX), list relaxable assumptions, map neighbouring problems
  (specializations / generalizations / duals), and surface open sub-problems.

This folds the former `compare-papers`, `knowledge-systemize`, `research-gap`, and
`problem-expand` skills into one mode-parameterized cross-paper skill.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (bilingual §1,
input resolution §2, output + preview-not-dump §3, reuse-before-read §4, fidelity §8, mode
scaling by cardinality §7, scope handoff §10) and pulls `~/.claude/rules/latex-katex-compat.md`
at run time for any math in `expand`/`gaps` — **reference it, never inline it**. `gaps`/`expand`
additionally pull `~/.claude/rules/research-proposal-integrity.md` (novelty tiers, Venue Claim
Card, claims ledger, math provenance) — every proposed direction is graded there BEFORE any
venue word is written. Human-facing
prose is Vietnamese (học thuật); ids, equations, dataset/model names stay English/LaTeX.

## Procedure

### Phase 0 — Resolve scope & mode
Resolve `$ARGUMENTS` per §2: a list of ids (`001 003 008`), the literal `all`, or a topic
keyword. Parse the trailing mode token: `compare` (default) | `taxonomy` | `gaps` | `expand`.
**One mode per run.** `expand` takes a single paper id or a topic phrase; the other three take
2+ papers. If empty/ambiguous, list `papers/` + `notes/INDEX.md` and ask **once**.

### Phase 1 — Reuse-before-read (§4), then scale by cardinality (§7)
Consult `notes/INDEX.md` first. For each paper in scope, prefer an existing distilled artifact
**in this order** — read it instead of the raw PDF:
1. `notes/<id>-read-summary.md` (faithful condense) →
2. `notes/<id>-method.md` (method critique/recipe) →
3. `notes/<id>-read-gist.md` (orientation).

**Source granularity is gated by N (this is the token bound — do not skip it):**
- **≤4 papers (Deep):** read each paper's full distillate (summary/method note); full detail
  per paper (~3 differentiators / gaps each).
- **5–12 papers (Overview):** read each distillate but emit only ~1 line per paper; focus on
  cross-cutting structure.
- **>12 papers (Corpus scale):** **do NOT open per-paper note bodies.** Reason ONLY over the
  pre-compressed sources — the one-line gist rows in `notes/INDEX.md` and (for `compare`/
  `taxonomy`/`gaps`) `notes/knowledge-graph.md` if it exists. If the deliverable genuinely needs
  deeper per-paper detail at this scale, **shard**: synthesize sub-batches of ≤12 and merge their
  outputs — never load N full distillates into one context.

Open a raw PDF only for a single paper that has **no** note at all, reading only its high-density
regions (§6). If **many** ids in scope lack a distillate, stop and hand back to
`workbench-orchestrator` to dispatch reads first — do not fill the gap by opening many PDFs here
(that re-expands what ingest worked to bound).

### Phase 2 — Author the artifact (per mode)
- **`compare`:** comparison table → narrative (per paper: strength · limitation · key technical
  decision, cited) → hybrid-pipeline (map the best component to each stage) + Mermaid
  `flowchart LR` + integration risks → per-paper improvement suggestions (Deep: ~3 each;
  Overview: 1 each) as `problem → source → application → risk`.
- **`taxonomy`:** organizing dimensions (derive from the corpus, don't hard-code) → named
  categories with rationale → comparison matrix (rows = papers, cols = dimensions) → narration
  of clusters / convergence / divergence / outliers.
- **`gaps`:** per-paper limitations (author-stated + observed) → aggregated cross-cutting gaps →
  white space (what no paper attempts) → opportunities table (`gap → why it matters → concrete
  direction → source ids → novelty tier T1/T2/T3 + venue band` per integrity rules §1). Any
  direction presented as a serious proposal gets a full Venue Claim Card + a `notes/claims-ledger.md`
  row (§2–3).
- **`expand`:** specific problem (precise) → broader class + abstract formulation (LaTeX) →
  relaxable assumptions → neighbouring problems → landscape position → open sub-problems.

**Cross-cutting — Claim Conflicts section (auto, when N ≥ 3):** when two or more
papers make contradictory / incompatible claims about the same phenomenon (A
reports X improves Y while B reports X harms Y), emit a `## Claim Conflicts`
section **in addition to** the mode's own output. **Do not harmonize or fabricate
consensus** — the row stays `unresolved` unless one paper explicitly addresses
the other, or the conflict dissolves under a stated condition (scope, input
range, metric definition). Averaging or picking the "majority" claim is
fabricating consensus.

| Claim | Source ids | Conflict type | Resolution status |
|-------|-----------|---------------|-------------------|
| A: X↑Y vs B: X↓Y | `001` vs `003` | contradictory / conditional / scope-dependent | `unresolved` / `resolved — <why>` |

Every cross-paper claim is attributable to a specific id (§8). Missing items →
`bài báo không nêu (not stated)`. Preserve quantitative results exactly.

### Phase 3 — Math compatibility (binding, when math is present)
Conform every formula to `latex-katex-compat.md` (`$...$` / `$$...$$` with blank lines; drop
`\tag`/`\label`/`\ref`; prefer `\mathbf`/`\mathrm`/`\mid`). Must render under KaTeX **and**
MathJax.

### Phase 4 — Write & preview (§3)
Write to `notes/synthesize-<mode>-<slug>.md` (cross-paper) or `notes/<id>-expand.md` (`expand`
on one id), with the standard header (scope · worker `paper-synthesize` · mode · date). Then
print to chat ONLY a **6–9 line** Vietnamese preview + the absolute path:
- `compare`: the 2–3 sharpest differentiators + the hybrid-pipeline one-liner + path.
- `taxonomy`: the category names + the dimension list + path.
- `gaps`: the top 3 opportunities (one line each) + path.
- `expand`: the broader problem class + 2 open sub-problems + path.
**Never** paste the full table / matrix / Mermaid chart into chat — they live in the file. End
with the handoff note.

## Output schema (file)
One mode's structure (header + sections above). If domain terms are defined, close with a
`## Thuật ngữ (Glossary)` table (`| English | Tiếng Việt | Giải thích ngắn |`) per §1.

## Gotchas
- **Reason over distilled notes, not raw PDFs.** Reuse `notes/<id>-*` first (§4); a raw read is
  the fallback for an un-distilled paper only. Re-reading PDFs you already condensed wastes
  tokens.
- **Mode dispatch is explicit.** `compare`/`taxonomy`/`gaps`/`expand` are PARAMS of one skill;
  run exactly one, default `compare`.
- **Scale down as N grows (§7).** At `all` you produce structure, not 80 deep paragraphs — one
  line per paper plus the cross-cutting synthesis.
- **Every claim cites an id (§8).** No invented connection between two papers without evidence;
  no fabricated metric. Missing → `bài báo không nêu (not stated)`.
- **No venue word without a tier (integrity rules).** A `gaps`/`expand` direction never says
  "đủ Q1/Q4" bare — always tier + band + điều kiện, and formulas carry [cited]/[derived]/[design]
  tags. This is what prevents the propose-then-walk-back drift.
- **Don't dump the file to chat (§3).** Tables and Mermaid stay in the file; chat gets the
  6–9 line preview + path.
- **Stay in scope (§10).** This skill works ACROSS papers (or generalizes one problem). It does
  not condense or critique a single paper:
  - `→ dùng paper-read cho` overview / summary / intuition / mindmap của MỘT bài.
  - `→ dùng paper-method cho` phân tích sâu phương pháp / pipeline của MỘT bài.
  - `→ dùng knowledge-graph cho` trích entity–relation có kiểu (typed triples).
