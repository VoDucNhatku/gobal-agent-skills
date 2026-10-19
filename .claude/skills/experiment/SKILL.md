---
name: "experiment"
description: "Runs the experimental side of ML research: reproduce a paper as a notebook, run it on a GPU (local or Modal), and read training results honestly — seeds, variance, learning curves, best epoch, claimed gains versus logs. Use for train, reproduce, notebook, GPU, logs, metrics. Triggers — tái lập, chạy code bài báo, notebook, train, GPU, Modal, log huấn luyện, mAP, seed, epoch."
argument-hint: "<paper id|run dir|log> [plan|notebook|modal|analyze]"
allowed-tools: "Read Write Edit Glob Grep Bash WebSearch WebFetch"
---

# experiment — from paper to numbers you can defend

## Modes
| Mode | Use | Output |
|---|---|---|
| `plan` | before writing code | ordered steps, data/compute needs, the baseline number to beat, risks |
| `notebook` | reproduce or run released weights | `notebooks/<id>-<mode>.ipynb` via `scripts/nb_builder.py` |
| `modal` | serverless GPU run | `modal_apps/<id>-<mode>/modal_app.py` via `scripts/modal_builder.py` |
| `analyze` (default for logs/CSVs) | interpret runs | answer in chat with the computed numbers |

## Plan and build
1. Get the method from `notes/<id>-method.md` (`recipe`) if it exists; otherwise read the
   paper's method and implementation details (`paper-read` mode `recipe`).
2. Look for official code first: [references/code-search.md](references/code-search.md).
3. List every hyperparameter the paper gives and every one it omits (`không nêu`); never
   invent omitted values — choose a default and label it as your choice.
4. Notebook or Modal app: write a JSON spec and call the builder; never hand-write nbformat
   or Modal boilerplate. Spec shapes: [references/builders.md](references/builders.md).
   GPU sizing and price notes: [references/gpu-cost-matrix.md](references/gpu-cost-matrix.md).
5. Report path, sections and manual steps (licences, tokens) in ≤ 9 lines.

## Analyze results (the part most often done wrong)
- Compute from the raw files with a short script: per-seed values, mean, std, delta of means.
- One seed is an observation, not a result. With n seeds, compare the delta of means to the
  seed spread; if the spread is comparable, say the gain is not established.
- A claimed gain is checked against the logs, not against the text that claims it.
- Learning curves: best epoch = best validation metric (or lowest validation loss — say
  which); rising validation loss with falling training loss = overfitting.
- When a run changed several things at once (module, epochs, augmentation), the gain cannot
  be attributed to one of them; propose the controlled run.
- Record each run in `notes/experiments.md`: date · config/commit · seed · metric · log path.

## Running code
Only run training or downloads the user asked for; state the command, expected time and
cost before a long or paid run. Report what ran and what did not.
