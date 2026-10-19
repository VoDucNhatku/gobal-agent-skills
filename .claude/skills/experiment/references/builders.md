# Builder scripts (notebook and Modal)

Run each script with the project directory as the working directory; resolve the script path
relative to this skill. Write specs to `.tmp/experiment_<id>_<target>.json` (never `/tmp`).

## Notebook — `scripts/nb_builder.py <spec> [--out-dir notebooks]`

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

## Modal — `scripts/modal_builder.py <spec> [--out-root modal_apps]`

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
