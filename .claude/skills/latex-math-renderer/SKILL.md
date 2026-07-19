---
name: latex-math-renderer
description: LaTeX math renderer for GOBAL AGENT — renders mathematical expressions as HTML for web display. Handles KaTeX (VS Code) and MathJax (GitHub/web) output formats. Modes: render (convert LaTeX to HTML), preview (show rendered output + compatibility notes), batch (process multiple expressions). Source: ~/.claude/rules/latex-katex-compat.md + KaTeX/MathJax documentation. It renders; it does NOT write math content (use paper-method for that).
argument-hint: <latex-expression | file> [render|preview|batch]
allowed-tools: Read Write Bash Glob
---

# LaTeX Math Renderer

> **Source:** ~/.claude/rules/latex-katex-compat.md + KaTeX/MathJax documentation
> **Purpose:** Render LaTeX math for web display, compatible with both engines.

## Engine Selection

| Context | Engine | Why |
|---------|--------|-----|
| VS Code Markdown preview | KaTeX | Fast, lightweight, built-in |
| GitHub README/issues | MathJax | Full LaTeX support |
| Web application (static) | KaTeX | Faster load, smaller bundle |
| Web application (dynamic) | MathJax | More commands supported |
| Jupyter notebook | MathJax | Default in Jupyter |

---

## Render Modes

### Mode: render

Convert LaTeX expression to HTML for web display.

**Process:**
1. Validate LaTeX syntax (balanced braces, supported commands)
2. Choose engine based on context
3. Generate HTML wrapper with appropriate class/attributes
4. Return HTML snippet + fallback text for non-JS environments

**Output formats:**

**KaTeX:**
```html
<span class="math-tex">$$ \mathcal{L} = \lambda_1 \mathcal{L}_{rec} + \lambda_2 \mathcal{L}_{perceptual} $$</span>
<script>renderMathInElement(document.body)</script>
```

**MathJax:**
```html
<script src="https://cdn.jsdelivr.net/npm/mathjax@4/es5/tex-mml-chtml.js"></script>
$$ \mathcal{L} = \lambda_1 \mathcal{L}_{rec} + \lambda_2 \mathcal{L}_{perceptual} $$
```

---

### Mode: preview

Show rendered output description:
1. List which commands are used
2. Note any cross-platform compatibility issues
3. Suggest alternatives for KaTeX-incompatible commands
4. Provide both KaTeX and MathJax versions

---

### Mode: batch

Process multiple LaTeX expressions from a file:
1. Read file, extract all `$$...$$` and `$...$` blocks
2. Validate each block
3. Generate HTML for each
4. Report: total expressions, issues found, compatibility notes

---

## Common Patterns

| Pattern | LaTeX | Notes |
|---------|-------|-------|
| Loss function | `\mathcal{L} = \lambda_1 \mathcal{L}_{rec} + \lambda_2 \mathcal{L}_{perceptual}` | Safe in both engines |
| Norm | `\|x\|_2` | Use `\|` not `||` |
| Argmin | `\arg\min_{\theta}` | Use `\arg\min` not ASCII |
| Fraction | `\frac{a}{b}` | Safe in both |
| Matrix | `\begin{pmatrix} a & b \\ c & d \end{pmatrix}` | Use `pmatrix` (KaTeX supports) |
| Cases | `\begin{cases} x & \text{if } y \\ z & \text{otherwise} \end{cases}` | Keep conditions ASCII-only for KaTeX |
| Summation | `\sum_{i=1}^{N} x_i` | Safe in both |

---

## Cross-References

- `latex-fix` → Repair broken LaTeX before rendering
- `~/.claude/rules/latex-katex-compat.md` → Full compatibility rules (read at runtime)
- `paper-method` → Source LaTeX from paper analysis
- `vi-translate` → Translated papers with math
