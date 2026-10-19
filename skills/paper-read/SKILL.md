---
name: "paper-read"
description: "Reads ONE paper or technical document and answers about it at the depth needed: targeted questions with locators, gist, section summary, argument map, method and math critique, reimplementation recipe. Use for any question about a single paper. Triggers — đọc bài, tóm tắt, bài này nói gì, công thức, phương pháp, ablation, siêu tham số, có tái lập được không."
---

# paper-read — one paper, the depth the question needs

## 1. Resolve the source
Accept an id (`003`), a file name or partial title, a path anywhere, or a URL. Papers
usually live in `papers/`, but any path works. For a URL, save the extracted text to
`.cache/papers/<slug>.txt` (do not commit it if the repo is public) and read from there.
If two files match, list them and ask once. Check `notes/INDEX.md` for a fresh artifact
of the same paper and mode; reuse it instead of re-reading.

## 2. Pick the mode
| Mode | When | Read | Output |
|---|---|---|---|
| `answer` (default for a question) | "lr bao nhiêu?", "dataset bao nhiêu ảnh?", "có nói X không?" | grep the terms, read only the hit sections and tables | answer in chat with locator (§, Table, Eq.); no file |
| `gist` | should I read this? | abstract, intro, conclusion, headings, captions | chat, ≤ 8 lines |
| `summary` (default when asked to summarize) | faithful condensation | whole paper, section by section | `notes/<id>-read-summary.md` + preview |
| `think` | does the evidence carry the claims? | contributions, every results and ablation table | claims→evidence map, ablation causality, assumptions, what would falsify |
| `method` | math, design, novelty, limits, reproducibility | method, equations, losses, protocol | `notes/<id>-method.md` |
| `recipe` | prepare a reimplementation | method and implementation details | ordered stage table + Mermaid flow |
| `eli5`, `mindmap` | intuition or structure | see reference | see reference |

Templates for `gist/summary/eli5/mindmap/think`: [references/depth-modes.md](references/depth-modes.md).
Reproducibility checklist for `method`/`recipe`: [references/method-modes.md](references/method-modes.md).

## 3. Fidelity rules (all modes)
- Copy numbers, equations and hyperparameters exactly; give the locator.
- When the abstract and the tables disagree, report both and say which the tables support.
- Missing information: `không nêu trong nguồn (not stated)`. Do not supply typical values.
- State reading depth (`abstract` / `skim` / `full`) when a conclusion depends on it.
- In `think` and `method`, check ablations: a row that removes two components at once
  does not isolate either; a single run does not establish a gain; a SOTA claim is only
  as strong as the baselines in the table.
- Gloss equations from the paper's own text; your own interpretation is marked `(suy luận)`.

## 4. Mode `method` sections
Formulation · notation table · key equations (verbatim, glossed) · losses and weights ·
novelty versus the cited prior work · ablation causality table
(`Thành phần | Delta | Kết luận của bài | Có kiểm soát? có/gián tiếp/không`) · stated and
inferred limitations · 6-row reproducibility score + verdict and the biggest blocker.
Math must render in KaTeX and MathJax: `$…$`, `$$…$$` with blank lines, no `\tag`/`\label`.

## 5. Output
Answer in Vietnamese; identifiers in English. Files only for `summary`, `think`,
`method`, `recipe` or when the user asks; then a ≤ 8-line preview plus the path, and one
row in `notes/INDEX.md`. Next steps when relevant: several papers → `paper-synthesize`;
judging a proposal built on this paper → `research-assess`; running it → `experiment`.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
