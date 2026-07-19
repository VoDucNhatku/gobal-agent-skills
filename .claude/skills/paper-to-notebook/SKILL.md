---
name: paper-to-notebook
description: Turns one paper into a runnable Jupyter notebook (.ipynb), Colab- or local-ready. Modes — reproduce (full method pipeline annotated with paper section refs, adapting official/third-party code when it exists) and run-results (load pretrained weights, run the official eval, show results vs the paper's reported numbers). Searches Papers With Code / GitHub / Hugging Face for official code first, then offloads notebook assembly to a bundled builder (never hand-writes nbformat JSON). Code + comments English; chat report Vietnamese. Triggers — code the paper, viết code bài báo, implement the method, tái lập, reproduce results, tái lập kết quả, run pretrained, chạy mô hình, make a notebook, tạo notebook, turn paper into code. Produces a notebook; for serverless GPU deployment + cost use run-on-modal; for method analysis use paper-method.
argument-hint: <id|file|path> [reproduce|run-results] [repo-url]
---

# Paper → Notebook (viết code tái lập bài báo)

Generates `notebooks/<id>-<mode>.ipynb` from one paper. Two modes:
- **`reproduce`** (default) — the full method as runnable, annotated cells; clone/adapt official
  or third-party code if found, else implement from the method note + PDF.
- **`run-results`** — find official weights, follow the exact setup, run the published
  evaluation, and display the produced numbers next to the paper's reported numbers.

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (input resolution §2,
output + preview-not-dump §3, reuse-before-read §4, fidelity §8, **script-offloading §9**, scope
handoff §10). The code-discovery procedure (Papers With Code → arXiv → GitHub → Hugging Face)
lives in `references/code-search.md` — read it when you run; **reference it, never inline it**.
Notebook code/comments are English; the chat report is Vietnamese.

## Procedure

### Phase 0 — Resolve target, mode, optional repo
Resolve `$ARGUMENTS` per §2 (id | filename | path). Parse mode (`reproduce` default |
`run-results`) and an optional explicit repo URL. If empty/ambiguous, ask **once**.

### Phase 1 — Reuse-before-read (§4)
Consult `notes/INDEX.md`, then prefer the distilled method note over the PDF:
`notes/<id>-method.md` (especially mode `recipe` — the pipeline table) → `notes/<id>-read-summary.md`.
Open the PDF only for the architecture / hyperparameters / dataset details a note omits (§6).
Extract: architecture, hyperparameters, dataset(s) + URLs, evaluation metrics, and any official
code URL printed in the paper.

### Phase 2 — Find official code (load `references/code-search.md`)
Follow the search order in the reference (stop at the first official repo). Decide
**official / third-party / none**, and record for the builder: repo URL, dependencies, dataset
file list + URLs, pretrained weight files, HF repo id (+ whether gated), and the exact eval
command. For `run-results`, locating real weights is mandatory; if none exist, say so and offer
`reproduce` instead.

### Phase 3 — Build the JSON spec and offload (§9 — do NOT hand-write nbformat)
Assemble a compact spec and write it to `/tmp/paper-to-notebook_<id>_<mode>.json`, then call:

```
python "<skills>/paper-to-notebook/scripts/nb_builder.py" /tmp/paper-to-notebook_<id>_<mode>.json
```

The builder writes `notebooks/<id>-<mode>.ipynb` with all boilerplate cells auto-inserted: GPU
check, `pip install`, a parallel downloader for datasets/weights, repo clone (when a URL is
given), the section-annotated method/eval cells you specify, and a results-vs-paper comparison
cell (`run-results`). **You provide facts and the per-stage code/markdown; the script provides
every byte of nbformat JSON** — never hand-write notebook structure.

Spec shape (see the builder's `--help` / header for the full schema):
```json
{
  "paper_id": "003", "title": "...", "mode": "reproduce",
  "repo_url": "https://github.com/... | null",
  "dependencies": ["torch", "torchvision"],
  "dataset_files": [{"name": "ava.zip", "url": "https://..."}],
  "weight_files":  [{"name": "model.pth", "url": "https://..."}],
  "hf_repo": "org/model | null", "needs_hf_token": false,
  "sections": [{"kind": "markdown|code", "title": "Stage 1 — ...",
                "paper_ref": "§3.2 / Eq. 4", "body": "..."}],
  "manual_steps": ["Accept the dataset license on ...", "..."]
}
```

### Phase 4 — Report (§3)
Print to chat ONLY a **6–9 line** Vietnamese report + the saved path: code found
(official/third-party/none) + repo, the notebook path, a short section map (cell titles), and any
manual steps (license acceptance, HF token, GPU需求). Do **not** paste notebook cells into chat.

## Output
`notebooks/<id>-<mode>.ipynb` (written by `scripts/nb_builder.py`). No `notes/` artifact. Chat
gets the 6–9 line report + path only.

## Gotchas
- **Offload nbformat (§9).** Never hand-write the `.ipynb` JSON — assemble the spec and call
  `nb_builder.py`. Hand-writing cell/metadata structure is the classic token + correctness leak.
- **Find code before writing code (§4).** Adapting official weights/code is far cheaper and more
  faithful than reimplementing; resolve official/third-party/none first.
- **Don't fabricate (§8).** Use real hyperparameters, dataset URLs, and weight files. Missing →
  mark it a manual step; never invent a download URL or a shape.
- **`run-results` needs real weights.** If none exist, fall back to `reproduce` and say so.
- **Don't dump cells to chat (§3).** The notebook holds the cells; chat gets the report + path.
- **Stay in scope (§10).** This skill writes a notebook:
  - `→ dùng run-on-modal cho` deploy GPU serverless + ước tính chi phí.
  - `→ dùng paper-method cho` phân tích phương pháp / pipeline trước khi code.
