# Reproducibility Checklist

Reproducibility scoring templates for paper-method and paper-to-notebook.
Read this file; reference it, never inline it.

## Categories & Scoring

For each category, rate `full` / `partial` / `missing`.

### Environment
- [ ] Hardware specified (GPU model, VRAM)
- [ ] Software versions (framework, CUDA, drivers)
- [ ] Random seeds reported and fixed
- [ ] Dependencies listed (requirements.txt or equivalent)

### Data
- [ ] Dataset names + download links
- [ ] Train/val/test split sizes
- [ ] Preprocessing code available
- [ ] Data augmentation described

### Training
- [ ] Loss function formula + all weights
- [ ] Optimizer + learning rate + schedule
- [ ] Batch size, gradient accumulation
- [ ] Number of epochs / early stopping criteria
- [ ] Regularization (dropout, weight decay)

### Evaluation
- [ ] Metric definitions (not just names)
- [ ] Inference procedure (greedy, beam search k, temperature)
- [ ] Comparison baseline details

### Ablation causality
- [ ] Per-component ablation table provided (rows = "w/o X")
- [ ] Each ablation row maps to a claim it tests
- [ ] Components not ablated are flagged (asserted without evidence)

### Code Availability
- [ ] Official code repo linked and runnable
- [ ] Third-party reimplementation works
- [ ] Expected outputs reproducible within tolerance

## Scoring

| Score | Criteria |
|-------|----------|
| A (full) | All checked, code runs end-to-end |
| B (substantial) | 1-2 unchecked, core pipeline reproducible |
| C (partial) | Several unchecked, key equations available |
| D (minimal) | Mostly unchecked, only paper claims |
| F (not reproducible) | Insufficient info to attempt |

Honesty over optimism: a paper with all formulas but no code may still deserve B, while a paper with everything except one critical hyperparameter is only C.
