# Finding official code for a paper (reference for `paper-to-notebook`)

Loaded at run time by `paper-to-notebook` (and reused by `run-on-modal`). Binding
conventions live in `~/.claude/rules/workbench-conventions.md`; this file only adds
the code-discovery procedure. Goal: spend a small fixed search budget to decide
**official / third-party / none**, then record what the notebook builder needs.

## Why this matters
Reproducing from official weights/code is far cheaper and more faithful than
reimplementing from the PDF. Always resolve the code-availability question **before**
writing any model code, so `mode reproduce` can *adapt* rather than rebuild, and
`mode run-results` knows where pretrained weights live.

## Search order (stop as soon as you find official code)
1. **Papers With Code** — `paperswithcode.com/paper/<slug>` or search the exact
   title. The "Code" tab lists repos and marks the **official** one. The "Results"
   tab gives the reported numbers you must reproduce, and the dataset/benchmark links.
2. **arXiv abstract page** — the "Code & Data" (Links to Code) section, and any
   GitHub/project URL printed in the paper's abstract, footer, or first-page footnote.
3. **GitHub search** — try, in order:
   - `"<exact paper title>"` (quoted)
   - `<distinctive method name / acronym>` (e.g. the model's coined name)
   - `<first-author surname> <year> <keyword>`
   - filter/scan for `org:<lab>` when the lab is known (e.g. `facebookresearch`,
     `google-research`, `openai`, `huggingface`).
   Prefer the repo linked from the paper; treat unlinked matches as third-party.
4. **Hugging Face Hub** — `huggingface.co/models?search=<name>` for pretrained
   **weights**, and `huggingface.co/datasets?search=<name>` for data. Note the exact
   repo id (`org/model`), whether it is **gated** (needs an HF token), the file names
   of the weights, and any `transformers`/`diffusers` one-liner the model card gives.
5. **Project page** — a `*.github.io` / lab site often links the canonical repo,
   checkpoints, and a Colab demo. Google Scholar "version" links can surface it too.

Use `WebSearch` / `WebFetch` for steps 1–5; do not guess URLs — confirm they resolve.

## Classify the result
- **official** — repo authored by the paper's authors/lab, or linked from the paper /
  Papers With Code "official" badge. Adapt this; do not reinvent.
- **third-party** — a faithful community reimplementation. Usable for `reproduce`, but
  flag in the notebook header that it is unofficial and may diverge from reported
  numbers. Prefer one with stars, recent commits, and a matching results table.
- **none** — no usable code found. `reproduce` implements from the
  `notes/<id>-method.md` recipe from scratch; `run-results` is likely infeasible
  (no weights) — say so and fall back to `reproduce`.

## What to RECORD (these feed the `nb_builder.py` JSON spec)
Record exactly the fields the builder needs — never paste repo contents into chat:

- `code_status`: `official` | `third-party` | `none`
- `repo_url`: clone URL (and the specific subdir / branch / commit if it matters)
- `weights`: HF repo id(s) or direct checkpoint URLs (for `run-results`); mark
  `gated: true` when an HF token / license click-through is required
- `dataset`: name + download URL(s) or HF dataset id; note size and any auth
- `requirements`: how deps are declared — `requirements.txt`, `environment.yml`,
  `pyproject.toml`, `setup.py`; capture pinned versions (esp. `torch` + CUDA build)
  and any system/`apt` packages (`ffmpeg`, `libgl1`, `git-lfs`)
- `entrypoint`: the file/command to run inference or eval (`python demo.py`,
  `scripts/eval.sh`, a notebook), and the config/checkpoint flags it expects
- `stated_gpu_reqs`: any VRAM / GPU / runtime the README or paper states (e.g.
  "trained on 8×A100-80GB", "inference fits in 16 GB") — hand this to `run-on-modal`
  for GPU-tier selection
- `repro_notes`: known caveats — non-deterministic ops, missing data, results that
  the repo's own issues say don't reproduce

## Output
Put these fields into the JSON spec for `scripts/nb_builder.py` (the builder writes
the `git clone`, `pip install`, and download cells from them — see the skill body).
In the notebook header and the chat preview, state the chosen `code_status` and the
source URL so the reader knows whether results are official, adapted, or from scratch.

## Gotchas
- A GitHub match with the right name can still be unofficial — verify it is linked
  from the paper before trusting its numbers.
- `requirements.txt` often omits the correct `torch`+CUDA wheel; pin it explicitly in
  the spec or the install cell silently grabs a CPU build.
- Gated HF weights fail at download time, not install time — record `gated: true` so
  the builder emits the token/secret cell up front.
- Do not deep-read the repo. Skim README + requirements + the entrypoint; record the
  fields above and move on (strategic reading, token economy).
