# LaTeX / KaTeX vs MathJax Compatibility (binding for math skills)

Satellite rules file pulled at run time by the Workbench skills that emit or repair
mathematical content: `paper-method` (math-dense method analysis), `latex-fix` (batch
math repair), and any web skill that writes copy containing formulas. It refines — and
never overrides — `~/.claude/rules/workbench-conventions.md`. Read it only when math is
in scope; keep it out of always-loaded context.

The problem: notes render in two different engines. **VS Code Markdown preview** uses
**KaTeX** (~v0.13–0.16) — lightweight, fast, a *subset* of LaTeX; an unsupported command
silently breaks the **entire** `$$` block. **GitHub** uses **MathJax 4.1.1** — a full TeX
implementation that accepts far more. The rule is therefore: **target the intersection**
— write only commands safe in BOTH engines. When a command works on GitHub alone, use the
cross-platform alternative below instead.

## Baseline notation (always)
- **Inline math:** `$...$` — e.g. `$\mathcal{L}_{total}$`.
- **Display math:** `$$...$$` with a **blank line before and after** the block.
  markdown-it requires those blank lines to recognise display math; without them the
  parser treats the content as plain text and renders raw source. e.g.:

  ```
  $$
  \mathcal{L} = \lambda_1 \mathcal{L}_{rec} + \lambda_2 \mathcal{L}_{perceptual}
  $$
  ```

- **Always use proper LaTeX:** subscripts `_{...}`, superscripts `^{...}`, Greek
  `\alpha \beta \theta`, calligraphic `\mathcal{}`, bold `\mathbf{}`, hat `\hat{}`, norm
  `\|\cdot\|`, argmin/argmax `\arg\min`, fractions `\frac{}{}`.
- **Never** write `L_total`, `||x||`, `theta`, or `argmin` as raw ASCII in any output
  that contains mathematical content.

## Cross-platform command rules

| Command | GitHub (MathJax) | VS Code (KaTeX) | Rule |
|---------|------------------|-----------------|------|
| `\tag{N}` | ✓ | ⚠️ display only (KaTeX ≥0.13) | Remove; append `*(phương trình N trong paper)*` after the closing `$$` |
| `\label{...}` | ✓ | ✗ | Remove silently |
| `\ref{...}` / `\eqref{...}` | ✓ | ✗ | Remove or replace with a plain number |
| `\boldsymbol{...}` | ✓ | ⚠️ KaTeX ≥0.10, edge cases | Use `\mathbf{}` for latin/upright; `\pmb{}` only if `\mathbf` is unavailable |
| `\operatorname{custom}` | ✓ | ⚠️ requires amsopn | Use `\mathrm{custom}` for custom operators; predefined (`\max`, `\min`, `\arg`, `\log`) are always safe |
| `\middle\|` inside `\left...\right` | ✓ | ⚠️ KaTeX bug #683 | Use `\mid` — universally supported, semantically correct for set-builder "such that" |
| `\text{<non-ASCII>}` inside `\begin{cases}` / `\begin{array}` | ⚠️ | ⚠️ unstable | Keep condition columns pure math or ASCII-only; move Vietnamese / non-ASCII annotations to prose after the closing `$$` |
| `` ```math...``` `` fenced block | ✓ | ✗ | Replace with `$$...$$` |
| `\[...\]` delimiter | ✓ | ✗ | Replace with `$$...$$` |
| `\(...\)` delimiter | ✓ | ✗ | Replace with `$...$` |
| `\xrightarrow{\text{...}}` | ✓ | ✓ | Safe; if it overflows use `\longrightarrow \quad \text{(...)}` |

When in doubt, check the supported-function lists:
[KaTeX supported functions](https://katex.org/docs/supported.html) ·
[MathJax extensions](https://docs.mathjax.org/en/latest/input/tex/extensions/).

## Notes for specific skills
- **`vi-translate`:** copy equations **verbatim** from the source paper — do not
  re-render or simplify them — but still apply the fixes above so copied equations render
  on both engines.
- **`latex-fix`:** the bundled `scripts/latex_lint.py` detects the issues in the table
  above (plain-text math, wrong `$$`/`\(`/`\[` delimiters, KaTeX-unsupported macros,
  malformed `\tag`) and returns flagged spans with line numbers. Fix **only the flagged
  spans** against this table — never re-read or re-emit the whole file.
- **`paper-method`:** reference this file; do not inline its content into the skill body.
