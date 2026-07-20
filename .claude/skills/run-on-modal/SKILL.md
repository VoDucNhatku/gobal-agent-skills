---
name: run-on-modal
description: Deploys one paper's code on Modal serverless GPU. Profiles VRAM from compute signals (param count, batch size, precision), picks the cheapest GPU tier with a safety margin, estimates cost, then offloads to a bundled builder that writes a two-phase modal_app.py (CPU download function + GPU compute function + local entrypoint). Modes — reproduce, run-results, inference. Code English; the chat report (hardware pick + cost + quick-start) is Vietnamese. Triggers — run on Modal, chạy trên Modal, deploy to GPU, serverless GPU, ước tính chi phí GPU, chọn GPU, estimate VRAM, modal_app, run the model in the cloud. Produces a Modal app + cost estimate; for a local/Colab notebook use paper-to-notebook; for method analysis use paper-method.
argument-hint: <id|file|path> [reproduce|run-results|inference] [repo-url]
allowed-tools: Skill Agent Read Write Glob Bash
---

# Run on Modal (chạy trên Modal serverless GPU)

Generates `modal_apps/<id>-<mode>/modal_app.py` plus a hardware recommendation and cost estimate.
Three modes: `reproduce` (train/run the full method), `run-results` (pretrained eval), `inference`
(single forward pass / demo).

## Conventions
This skill treats `~/.claude/rules/workbench-conventions.md` as binding (input resolution §2,
output + preview-not-dump §3, reuse-before-read §4, fidelity §8, **script-offloading §9**, scope
handoff §10). The GPU ladder, VRAM-estimation rules, multi-GPU syntax, and the tier-selection
rule live in `references/gpu-cost-matrix.md` — read it when you run; **reference it, never inline
it**. The code-discovery procedure is shared from `paper-to-notebook/references/code-search.md`.
Modal code is English; the chat report is Vietnamese.

## Procedure

### Phase 0 — Resolve target, mode, optional repo
Resolve `$ARGUMENTS` per §2 (id | filename | path). Parse mode (`reproduce` | `run-results` |
`inference`) and an optional repo URL. If empty/ambiguous, ask **once**.

### Phase 1 — Reuse-before-read (§4)
Consult `notes/INDEX.md`, then prefer the distilled notes over the PDF: `notes/<id>-method.md`
(architecture, params, batch size) → `notes/<id>-read-summary.md`. Open the PDF only for compute
signals a note omits (§6). Resolve official code per `code-search.md` (reuse the search you ran
for `paper-to-notebook` if a code note already exists).

### Phase 2 — Profile hardware (load `references/gpu-cost-matrix.md`)
Extract the compute signals: parameter count, batch size, precision (fp32/fp16/bf16), and any
explicit VRAM figure the paper gives. Estimate VRAM per the reference's rules (inference ≈
params × bytes/param + overhead; training ≈ params × 16 bytes + activations). Pick the **cheapest**
tier on the ladder whose VRAM ≥ 1.2× the estimate (safety margin). Compute a cost estimate =
tier price/hr × expected runtime. If the paper omits a signal, state the assumption you made
(§8) — never fabricate a hardware number.

### Phase 3 — Build the JSON spec and offload (§9 — do NOT hand-write the Modal envelope)
Assemble a compact spec and write it to `.tmp/run-on-modal_<id>_<mode>.json`
(project-relative, never `/tmp/` — see conventions §9), then call:

```
python "<skills>/run-on-modal/scripts/modal_builder.py" .tmp/run-on-modal_<id>_<mode>.json
```

The builder writes `modal_apps/<id>-<mode>/modal_app.py` with the **two-phase architecture**
auto-inserted: (a) a CPU-only `download_data()` function (no GPU, idempotent, `Volume.commit()`),
(b) a GPU `run_experiment()` function reading from the Volume, (c) an `@app.local_entrypoint()`
that calls both in order — plus the Image build (deps + apt + repo clone), the cost-estimate
header comment, and the quick-start commands. **You provide facts + the experiment body; the
script provides every byte of the Modal decorator boilerplate.**

Spec shape (see the builder header for the full schema):
```json
{
  "paper_id": "003", "mode": "run-results", "app_name": "paper-003-run",
  "gpu": "A100-40GB", "gpu_count": 1, "timeout": 3600, "python_version": "3.11",
  "repo_url": "https://github.com/... | null",
  "dependencies": ["torch"], "apt_packages": [], "run_commands": [],
  "hf_repo": "org/model | null", "needs_hf_token": false,
  "volumes": [{"name": "paper-003-data", "mount": "/data"}],
  "dataset_files": [{"name": "ava.zip", "url": "https://..."}],
  "weight_files":  [{"name": "model.pth", "url": "https://..."}],
  "experiment_body": "…python that runs on GPU and reads /data…",
  "cost_estimate": {"gpu": "A100-40GB", "price_per_hr": 2.10, "est_hours": 0.5, "est_cost": 1.05},
  "vram_estimate": "~14 GB (params 7B × 2 bytes + overhead)",
  "manual_steps": ["modal token new", "Accept dataset license"]
}
```

### Phase 4 — Report (§3)
Print to chat ONLY a **6–9 line** Vietnamese report + the saved path: recommended GPU tier +
why (VRAM estimate vs tier), the cost-estimate line (`tier × giờ ≈ $X`), the quick-start commands
(`modal run modal_app.py`), and any manual steps. Do **not** paste the `modal_app.py` body.

## Output
`modal_apps/<id>-<mode>/modal_app.py` (written by `scripts/modal_builder.py`). Optional companion
notebook only if asked. Chat gets the 6–9 line report + path.

## Gotchas
- **Offload the envelope (§9).** Never hand-write the `@app.function(gpu=...)` decorators, the
  Volume setup, or the two-phase split — emit the spec and call `modal_builder.py`.
- **Two phases, always.** Download on CPU (cheap, no GPU billing), compute on GPU; the entrypoint
  sequences them. Downloading inside the GPU function burns GPU-hours on I/O.
- **Cheapest tier with margin.** Pick the lowest tier with VRAM ≥ 1.2× estimate (`gpu-cost-matrix.md`).
  Don't default to an H100 when an L4 fits.
- **Don't fabricate compute numbers (§8).** State assumptions for missing signals; never invent a
  param count or a VRAM figure.
- **Don't dump the app to chat (§3).** The file holds the code; chat gets the report + path.
- **Stay in scope (§10).** This skill deploys to Modal GPU:
  - `→ dùng paper-to-notebook cho` notebook chạy local / Colab.
  - `→ dùng paper-method cho` phân tích phương pháp trước khi deploy.
