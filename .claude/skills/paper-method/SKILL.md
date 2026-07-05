---
name: "paper-method"
description: "Deep-reads one paper's method at a chosen lens. Mode critique = formulation, notation, math, losses, novelty, stated + unstated limitations, and a reproducibility checklist (the most math-dense mode); mode recipe = an ordered, reimplementation-ready pipeline table + a Mermaid data-flow chart. Triggers — methodology read, phân tích phương pháp, đọc kỹ phương pháp, explain the math, giải thích công thức, is this reproducible, có tái lập được không, critique the method, đánh giá phương pháp, novelty and limitations, hạn chế của phương pháp, extract the pipeline, trích xuất pipeline, implementation recipe, các bước của phương pháp, công thức loss. Distills one paper's method faithfully — it does not give a general overview (use paper-read), compare papers (use paper-synthesize), or write runnable code (use paper-to-notebook / run-on-modal)."
argument-hint: "<id|file|path> [critique|recipe]"
allowed-tools: "Skill Agent Read Write Glob Bash"
---

# Paper Method (đọc kỹ phương pháp)

Deep method analysis of **one** paper. Two modes, selected by `$ARGUMENTS`:
- **`critique`** (default) — the math-dense deep read: formulation, notation table, key
  equations, loss functions, novelty, stated + unstated limitations, closing with a
  reproducibility checklist + verdict.
- **`recipe`** — the same method reformatted as an ordered, reimplementation-ready
  pipeline (one row per stage) + a Mermaid data-flow chart.

This is a single-pass Worker on one paper. It folds the former `methodology-read` and
`pipeline-extract` skills into one mode-parameterized skill.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (bilingual
policy, output location + preview-not-dump §3, reuse-before-read §4, fidelity §8, scope
handoff §10), and pulls `~/.claude/rules/latex-katex-compat.md` at run time for all math
(delimiters, KaTeX-safe macros) — **reference it, never inline it**. The full output
schema and templates live in `references/repro-checklist.md`; read it when you run.
Human-facing prose is Vietnamese (học thuật); equations, notation, and identifiers stay
English/LaTeX.

## Procedure

### Phase 0 — Resolve target & mode
Resolve `$ARGUMENTS` per conventions §2 (id `003` | filename | path → a concrete file
under `./papers/`). If empty or ambiguous, list candidates and ask **once**, then
proceed. Parse the trailing mode token: `critique` (default) or `recipe`. **One mode per
run** — never emit both.

### Phase 1 — Reuse-before-read (§4)
Before opening the raw PDF, consult `notes/INDEX.md`, then check for a fresh prior
distillation **in this priority order**:
1. `notes/<id>-read-summary.md` — a faithful section-by-section condense (orient fast).

If a fresh artifact exists (same session/day or reconfirmed), seed your structural
understanding from it and open the PDF only to read the **method section, equations, and
the relevant tables** — not the whole paper. Otherwise read the PDF directly, focusing on
the method/approach, loss/objective, architecture, and experimental-protocol regions.
Read the actual source; never analyze from the title (§8).

### Phase 2 — Author the artifact (load the schema first)
Read `references/repro-checklist.md` and follow its templates exactly. Do not invent your
own column set or section order.

**Mode `critique`** — in this order:
1. **Formulation** — the problem and the proposed approach, in Vietnamese prose.
2. **Notation table** — symbols → meaning, in KaTeX-safe LaTeX.
3. **Key equations** — the load-bearing equations copied faithfully, each glossed.
4. **Loss / objective** — every loss term and how they combine (with weights).
5. **Novelty** — what is genuinely new vs prior work, attributable to the paper.
6. **Limitations** — both **stated** and **unstated** (inferred but flagged as inferred).
7. **Reproducibility checklist** (the closer) — the 5-criterion table scored
   yes/partial/no with one Vietnamese line of evidence each (section/table/equation), then
   `## Phán quyết tái lập (Reproducibility verdict)` = dễ tái lập / tái lập một phần / khó
   tái lập + the single biggest blocker. Be strict: `partial` is the honest default when
   unsure; never infer `yes` from a title.

**Mode `recipe`** — the ordered pipeline:
- One row per stage in **execution order**: `Stage | Input | Operation + key
  params/equations | Output`. The Operation column is load-bearing — put the governing
  equation (KaTeX-safe) and the driving hyperparameters there.
- Follow with a **Mermaid `flowchart TD`** of the data flow (per the template).

Anything the paper omits → write `bài báo không nêu (not stated)`; do not invent values
(metrics, hyperparameters, shapes). Preserve all quantitative results exactly (§8).

### Phase 3 — Apply math compatibility (binding)
Before saving, conform every formula to `latex-katex-compat.md`: `$...$` inline /
`$$...$$` display with blank lines around the block; replace `\[...\]`→`$$`, `\(...\)`→`$`,
fenced ```` ```math ````→`$$`; drop `\tag`/`\label`/`\ref` (note the equation number in
prose instead); prefer `\mathbf`/`\mathrm`/`\mid` over the KaTeX-fragile alternatives.
Math must render under **both** KaTeX and MathJax.

### Phase 4 — Write & preview (preview-not-dump §3)
Write the full artifact to `notes/<id>-method.md` with the standard header (id · title ·
source filename · worker `paper-method` · date `YYYY-MM-DD`). Then print to chat ONLY a
**6–8 line** Vietnamese preview + the absolute saved path:
- `critique`: the 5 checklist scores as a compact list + the verdict + the biggest
  blocker + path.
- `recipe`: the ordered stage names as a numbered list + the stage count + path.

**Never** paste the notation table, equation block, stage table, or Mermaid chart into
chat — they live in the file. End the preview with the handoff note (below).

## Output schema (file)
`notes/<id>-method.md` — exactly one mode's structure as templated in
`references/repro-checklist.md`:
- **`critique`** → formulation · notation table · key equations · loss · novelty ·
  limitations (stated + unstated) · 5-criterion reproducibility table · verdict.
- **`recipe`** → ordered `Stage | Input | Operation | Output` table · Mermaid
  `flowchart TD`.

If the artifact defines domain terms, close with a `## Thuật ngữ (Glossary)` table
(`| English | Tiếng Việt | Giải thích ngắn |`) per conventions §1.

## Gotchas
- **Mode dispatch is explicit.** `critique` and `recipe` are PARAMS of one skill, not
  separate skills. Run exactly one per invocation; default to `critique`.
- **Honesty over optimism.** `partial`/`no` is more useful than an inflated `yes` — every
  score and stage cites a section / equation; no claim from the title alone (§8).
- **Unstated ≠ invented.** Mark inferred limitations as inferred; mark missing values
  `bài báo không nêu (not stated)`. Do not fabricate hyperparameters or shapes.
- **Math renders on both engines.** Check `latex-katex-compat.md` for unsupported macros
  and delimiter rules before writing; one bad macro silently breaks the whole `$$` block
  in KaTeX.
- **Don't dump the file to chat.** Tables, equations, and the Mermaid block stay in the
  file; chat gets the 6–8 line preview + path only (§3).
- **Stay in scope (§10).** This skill analyzes the method of ONE paper. It does not give a
  general overview, run code, or compare papers:
  - `→ dùng paper-read cho` overview / intuition / mindmap của một bài.
  - `→ dùng paper-to-notebook / run-on-modal cho` việc viết và chạy code.
  - `→ dùng paper-synthesize cho` so sánh / phân loại / khoảng trống across papers.
