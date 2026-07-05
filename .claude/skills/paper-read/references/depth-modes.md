# paper-read — depth modes (pulled on demand)

Binding rules: `~/.claude/rules/workbench-conventions.md` (bilingual §1, preview §3,
strategic reading §6, mode scaling §7). This file is the per-mode spec: **what to
read**, the **output template**, the **chat-preview budget**, and **how `all` scales
output down**. Output prose is Vietnamese (học thuật); identifiers/code English.

Output file (single id): `notes/<id>-read-<mode>.md`. Every file opens with the
standard header: `paper id · title · source filename · worker (paper-read) · date`.

---

## Mode: `gist` — should-I-read overview
- **What to read (strategic, §6):** abstract + introduction + conclusion + section
  headings + figure/table captions only. Do NOT read the full body.
- **Template:**
  ```markdown
  ## Một câu (One-liner)        <!-- problem→approach→headline result, 1 sentence -->
  ## Vấn đề & động lực (Problem & motivation)
  ## Ý tưởng cốt lõi (Core idea)         <!-- 2–3 bullets -->
  ## Kết quả nổi bật (Headline results)  <!-- key metrics, exact numbers -->
  ## Có đáng đọc kỹ không? (Read deeper?)  <!-- verdict + which worker next -->
  ```
- **Chat preview:** 5–6 lines — one-liner + verdict + handoff (`→ paper-method` for
  the math, `→ paper-to-notebook` to run it) + saved path.

## Mode: `summary` (default) — faithful section-by-section condense
- **What to read:** the whole paper, section by section; ranged reads for long PDFs.
- **Template:**
  ```markdown
  ## Tóm tắt (Abstract in brief)
  ## Bối cảnh (Background)
  ## Phương pháp (Method)         <!-- faithful, names notation; no critique -->
  ## Thí nghiệm (Experiments)     <!-- datasets, baselines, exact metrics -->
  ## Kết quả & Ablation (Results) <!-- preserve all quantitative deltas -->
  ## Hạn chế tác giả nêu (Stated limitations)
  ## Thuật ngữ (Glossary)         <!-- | English | Tiếng Việt | Giải thích | -->
  ```
- **Fidelity:** condense, never invent; missing items → `bài báo không nêu (not
  stated)`. Critique belongs to `paper-method`, not here.
- **Chat preview:** 6–8 lines — method in 1 line + top 2–3 results + path.

## Mode: `eli5` — plain-language intuition
- **What to read:** abstract + method + one running example/figure; enough to ground
  ONE faithful analogy and ONE concrete toy example.
- **Template:**
  ```markdown
  ## Bài toán nói nôm na (The problem, plainly)
  ## Phép loại suy (The analogy)      <!-- one analogy, stated as analogy -->
  ## Ví dụ đồ chơi (Toy example)      <!-- small concrete walk-through -->
  ## Tại sao nó hiệu quả (Why it works)
  ## Analogy phá sản ở đâu (Where the analogy breaks)  <!-- honesty guard -->
  ```
- **Guard:** label the analogy AS an analogy; do not present it as the literal
  mechanism. Preserve the real term in `(English)` on first mention.
- **Chat preview:** 5–7 lines — analogy in 1–2 lines + the toy example's punchline.

## Mode: `mindmap` — Mermaid structure
- **What to read:** headings + abstract + method skeleton; build a hierarchy, not prose.
- **Output:** one Mermaid `mindmap` (root = paper) with branches Problem / Method /
  Experiments / Results / Limitations; leaves carry the specifics. A 3–5 line
  Vietnamese reading note follows the diagram.
- **Example:**
  ````markdown
  ```mermaid
  mindmap
    root((003 · Tên bài báo))
      Vấn đề
        Hạn chế baseline
        Động lực
      Phương pháp
        Kiến trúc
        Hàm mất mát (loss)
        Điểm mới (novelty)
      Thí nghiệm
        Datasets
        Baselines
      Kết quả
        Metric chính
        Ablation
      Hạn chế
  ```
  ````
- **Chat preview:** 5–6 lines — the 4–5 top-level branches as a bullet list + path
  (do NOT paste the Mermaid block into chat; it lives in the file).

---

## `all` — mode scaling by cardinality (§7)
When the target is `all` (every paper in `papers/`), do NOT run the full single-paper
template per paper. Scale per-item output DOWN so total output stays linear:

| Corpus size N | Per-paper output | Where it goes |
|---|---|---|
| **2–4 (Deep)** | one `notes/<id>-read-<mode>.md` per paper at full template | one file each |
| **5+ (Overview)** | ONE block per paper: one-liner + 2–3 bullets only | a single roll-up `notes/read-<mode>-all.md` |

- In Overview, prefer `gist`/`mindmap` granularity even if a heavier mode was named —
  state the downscale in the preview.
- Update `notes/INDEX.md` with one row per paper touched.
- Heavy per-paper deep reads across a big corpus are the **orchestrator's** parallel-
  subagent job, not a single `paper-read` pass — note the handoff and stop.

## Gotchas
- `gist` reading the full body defeats the mode — keep it to high-density regions.
- Never echo the whole artifact (or the Mermaid block) to chat; preview + path only.
- One mode per run; the mode is a parameter, not four separate skills.
