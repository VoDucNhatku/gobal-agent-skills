---
name: "latex-fix"
description: "Repairs math in notes/ artifacts so it renders on BOTH VS Code (KaTeX) and GitHub (MathJax). Runs a bundled linter that flags only the offending spans — plain-text math (L_total, ||x||, theta, argmin), wrong delimiters (\[...\], \(...\), ```math fences), and KaTeX-fragile macros (\tag, \label, \ref, \boldsymbol, \operatorname) — then fixes only those spans in place, leaving prose and Mermaid untouched. Output prose is Vietnamese; the fix-log is a compact table. Triggers — fix LaTeX, sửa LaTeX, fix the math, sửa công thức, latex render broken, công thức không hiện, fix \tag, fix delimiters, sửa delimiter, make math render on GitHub, KaTeX MathJax, fix all notes math. Repairs existing math formatting only; it does NOT author analysis (use paper-method / paper-read) or translate (use vi-translate)."
argument-hint: "<notes-path|id|all>"
allowed-tools: "Skill Agent Read Write Glob Bash"
---

# LaTeX Fix (sửa LaTeX cho cả KaTeX + MathJax)

Batch math repair over `notes/` files. Targets the **intersection** of KaTeX (VS Code preview)
and MathJax (GitHub) so a single `$$` block never silently breaks on one engine. Fixes **only
the flagged spans** — never re-renders or rewrites the surrounding prose.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (input resolution §2,
output + preview-not-dump §3, script-offloading §9, scope handoff §10) and
`~/.claude/rules/latex-katex-compat.md` as the authoritative compatibility table — **reference
it, never inline it**. Human-facing prose (the fix-log preview) is Vietnamese.

## Procedure

### Phase 0 — Resolve target
Resolve `$ARGUMENTS` per §2: a `notes/` file path, a paper id (→ all `notes/<id>-*.md`), or
`all` (every `*.md` in `notes/`). If empty, list `notes/` and ask **once**.

### Phase 1 — Lint (offload to the script, §9)
Do **not** scan files by eye. Run the bundled linter, which returns flagged spans with line
numbers and a severity per `latex-katex-compat.md`:

```
python "<skills>/latex-fix/scripts/latex_lint.py" <path-or-glob>
```

It detects: plain-text math (`L_total`, `||x||`, `theta`, `argmin`), wrong/legacy delimiters
(`\[...\]`, `\(...\)`, ```` ```math ````), display `$$` blocks missing the surrounding blank
lines, and KaTeX-unsupported macros (`\tag`, `\label`, `\ref`, `\eqref`, `\boldsymbol`,
`\operatorname{custom}`, `\middle\|`). It **skips fenced code and Mermaid blocks**.

### Phase 2 — Fix only the flagged spans
For each flagged span, apply the fix from `latex-katex-compat.md`:
- delimiters: `\[...\]`→`$$...$$` (blank lines around), `\(...\)`→`$...$`, ```` ```math ````→`$$`;
- macros: drop `\tag{N}` (append `*(phương trình N trong paper)*` after the block), drop
  `\label`/`\ref`/`\eqref` (or replace with a plain number), `\boldsymbol`→`\mathbf`,
  `\operatorname{custom}`→`\mathrm{custom}`, `\middle\|`→`\mid`;
- plain-text math → proper LaTeX (`L_{total}`, `\|x\|`, `\theta`, `\arg\min`).
Edit **in place**, one pass, touching only the flagged spans — never reflow prose, never alter
Mermaid, never change content meaning.

### Phase 3 — Preview (§3)
Print to chat ONLY the fix-log as a compact table — `| File | Dòng | Gốc | Sửa thành |` — capped
at a **6–20 line** preview (if many fixes, show the first rows + a `(+N nữa)` count) plus the
list of files touched. Do not paste full file bodies.

## Output
Files in `notes/` are rewritten in place (no new artifact). The chat output is the fix-log table
only; no separate file is written (this is a repair mode).

## Gotchas
- **Offload the scan (§9).** Use `scripts/latex_lint.py` to find spans; don't hand-scan whole
  files. Fix only what it flags.
- **One bad macro kills the whole block in KaTeX.** `\tag`/`\boldsymbol`/`\operatorname` are the
  usual culprits — check `latex-katex-compat.md` before fixing.
- **Touch only flagged spans.** Never reflow prose, re-render equations the author wrote
  deliberately, or edit inside Mermaid / code fences.
- **Don't dump files to chat (§3).** Output is the fix-log table; the repaired math lives in the
  files.
- **Stay in scope (§10).** This skill repairs math formatting. It does not write analysis or
  translate:
  - `→ dùng paper-method / paper-read cho` việc viết phân tích.
  - `→ dùng vi-translate cho` dịch thuật.
