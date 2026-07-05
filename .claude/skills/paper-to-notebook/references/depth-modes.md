# Depth Modes — Scaling Table

Modes for paper-read, paper-to-notebook, and related skills.
Read this file; reference it, never inline it.

## paper-read Depth Levels

| Mode | Token budget | Input | Output lines |
|------|-------------|-------|-------------|
| `gist` | ~500 | Abstract + section headings + captions only | 5–6 |
| `summary` | ~1500 | Abstract + intro + conclusion + key figures | 8–10 |
| `eli5` | ~1200 | Full paper read, distilled to plain language | 5–7 |
| `mindmap` | ~800 | Abstract + section structure | 5–6 |

## paper-to-notebook Modes

| Mode | Description | Time estimate |
|------|-------------|---------------|
| `reproduce` | Full method as annotated notebook | 1–2 hours |
| `run-results` | Pretrained weights + official eval | 30–60 min |

## N-paper Scaling Rules

| Paper count | Approach |
|-------------|----------|
| 1–2 | Full read per paper, synthesize directly |
| 3–5 | Full read + 1x1 synthesis, then full synthesis |
| 6–8 | Triage → shard deep-reads (waves of 4–5) → merge → synthesize |
| 9+ | Triage → filter to top ~8 → shard deep-reads → merge → synthesize |

## Token Budget per Skill Run

| Skill | Lite | Standard | Deep |
|-------|------|----------|------|
| paper-read | 500 | 1500 | 3000 |
| paper-method critique | 2000 | 4000 | 8000 |
| paper-method recipe | 1500 | 3000 | 6000 |
| paper-synthesize (N papers) | 1000 + 200*N | 2000 + 400*N | 4000 + 800*N |
