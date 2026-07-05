# GPU Cost Matrix (Modal)

Approximate on-demand prices for Modal GPU tiers.
Read this file; reference it, never inline it.

| Tier | GPU | VRAM | vCPU | Price/hr (est.) | Use for |
|------|-----|------|------|----------------|---------|
| T4 | NVIDIA T4 | 16 GB | 4 | ~$0.60 | Inference, small models |
| L4 | NVIDIA L4 | 24 GB | 4 | ~$1.10 | Inference, medium models |
| A10G | NVIDIA A10G | 24 GB | 4 | ~$1.50 | Training small, inference large |
| A100-40GB | A100 | 40 GB | 8 | ~$3.50 | Training medium models |
| A100-80GB | A100 | 80 GB | 8 | ~$4.50 | Training large models |
| H100 | H100 | 80 GB | 16 | ~$8.00 | Training very large, Llama-70B+ |

## Selection Heuristic

1. Read VRAM requirement from paper or estimate from model size
2. Add 20% margin for framework overhead
3. Pick cheapest tier that fits
4. CPU tier (free) for data download / preprocessing
