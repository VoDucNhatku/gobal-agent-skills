# Gated Residual Fusion for Tiny Object Detection in Aerial Images

*Synthetic evaluation fixture. Not a real publication.*

## Abstract

Tiny objects (< 16 px) remain hard for aerial detectors. We propose Gated Residual
Fusion (GRF), a lightweight neck that gates high-resolution features into the detection
head. GRF improves AP_tiny by **+4.1** over the baseline and achieves state-of-the-art
results on AI-TOD-S, a dataset of 12,400 images. GRF adds only 0.8 M parameters.

## 1. Introduction

Feature pyramids lose spatial detail when downsampling. Prior necks (FPN, PANet) fuse
levels with fixed weights. We argue fusion should be conditioned on object scale.

## 2. Method

Given backbone features P2 and P3, GRF computes a gate

    g = sigmoid(W_g * [P2 ; up(P3)] + b_g)                         (1)

and the fused feature

    F = g ⊙ P2 + (1 − g) ⊙ up(P3) + P3_res                          (2)

where up(·) is 2× nearest upsampling, ⊙ is element-wise product and P3_res is a 1×1
projection of P3. The gate is shared across channels.

## 3. Experiments

### 3.1 Setup

AI-TOD-S: 12,400 images (8,680 train / 3,720 test). Backbone ResNet-50.
Optimizer SGD, learning rate 0.01, batch size 16, 24 epochs. Weight decay is not reported.
All results are from a single training run.

### 3.2 Main results

| Method        | AP   | AP_tiny | Params |
|---------------|------|---------|--------|
| FPN (2017)    | 18.6 | 9.4     | 41.5 M |
| PANet (2018)  | 19.1 | 10.2    | 44.0 M |
| GRF (ours)    | 20.4 | 12.5    | 42.3 M |

### 3.3 Ablation

| Variant                                   | AP_tiny |
|-------------------------------------------|---------|
| GRF full                                  | 12.5    |
| w/o gate and w/o P3_res (both removed)    | 10.1    |

## 4. Conclusion

GRF is a simple, effective neck. Removing the gate drops AP_tiny, showing that the gate
is the key component. Future work: video detection.
