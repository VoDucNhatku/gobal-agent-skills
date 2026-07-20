---
name: audit-log
description: Append-only decision-moment log for AI/ML research. Captures only the 1–3 key decisions per thinking session (architecture change, debug direction, hallucination catch), not transcripts. Compact md entries with evidence. Triggers — log session, audit log, ghi quyết định, record decision.
argument-hint: <context | "summary" | "clear">
allowed-tools: Skill Agent Read Write Bash
---

# AI Audit Log — Decision Moment Capture

Append-only log of **material decisions** from AI/ML thinking sessions.
One session → 1–3 entries. Log what changed, why, your thinking, where's the proof.

## Principles

1. **Log quyết định, không log transcript.** Thinking session dài → extract
   decision moments. Ghi WHAT changed, WHY, Delta, Evidence.
2. **Materiality.** Chỉ log khi quyết định **thay đổi hướng dự án** — kiến trúc
   model, hướng debug, phát hiện hallucination. Syntax/formatting = skip.
3. **Không bịa.** Chỉ log quyết định THẬT. Evidence phải tồn tại; nếu chưa
   có → ghi `[chưa có evidence]`. Không bịa path, không bịa metric.

## Event Types

| Type | Khi ghi | Ví dụ |
|---|---|---|
| **DESIGN** | Chọn/đổi backbone, loss, architecture, pipeline, hướng chính | ResNet→EfficientNet; thêm contrastive loss; flatten→point cloud |
| **TROUBLE** | Hướng debug, optimize, regularization, fix sau gặp vấn đề | Overfit→dropout+wd; NaN loss→grad clip; data leak→loại feature |
| **VERIFY** | Phát hiện hallucination, sanity check, phản biện AI, verify claim | AI bịa "Smith 2023"→verify Scholar; AI đề xuất ViT cho 2K data→discard |

## Entry Format (~6 dòng / entry)

```md
### <entry_id> · <timestamp> · <TYPE>
**Decision:** <1 dòng — điều đã quyết/thay đổi>
**Why:** <1–2 dòng — lý do, context, số liệu>
**Delta:** <1 dòng — 3 phần: (1) phản biện AI đúng/sai, (2) sáng tạo thêm/giảm, (3) quyết định cuối + lý do>
**Evidence:** <path> hoặc [chưa có evidence]
```

Ví dụ:
```
### ae_a3f1c2 · 2026-07-20T14:30 · DESIGN
**Decision:** Chuyển backbone ResNet-50 → EfficientNet-B3
**Why:** Dataset 2K ảnh, ResNet overfit (train 99% val 72%). EfficientNet compound scaling phù hợp data-limited.
**Delta:** AI đề xuất ViT nhưng data quá ít → discard; thêm progressive resize; quyết định test 2 epoch trước commit.
**Evidence:** experiments/backbone_compare.csv
```

## Compression Rule

Khi user request "log session" / "audit":
1. Review conversation từ entry gần nhất (hoặc đầu session nếu chưa log).
2. Tìm các **decision moments** — khoảnh khắc ra quyết định material.
3. Mỗi moment → 1 entry. **Tối đa 3 entries/session.** Nếu hơn → chọn 3 quan trọng nhất.
4. Không có moment material → nói thẳng "không có quyết định đáng log", đừng ép log.

## Procedure

### Phase 0 — Parse `$ARGUMENTS`
- **context mô tả** hoặc model tự review session → extract decisions.
- **`summary`** → thống kê (số/tuyến/5 entry gần nhất).
- **`clear`** → archive `notes/audit-log-archive-<date>.md`, reset.

### Phase 1 — Materiality check
Mỗi candidate: thuộc {DESIGN, TROUBLE, VERIFY}? Không → skip.
Không rõ → hỏi user 1 câu duy nhất.

### Phase 2 — Offload to script
Ghi JSON spec tạm vào `.tmp/audit-log_<entry_id>.json` (project-relative, không bao giờ
`/tmp/` — xem conventions §9, path này silently fail trên Windows) → gọi `audit_append.py`
tự stamp + append:
```bash
python "<skill-path>/scripts/audit_append.py" .tmp/audit-log_<entry_id>.json
# --summary / --clear cũng qua script
```

### Phase 3 — Confirm
In 1 dòng: entry_id + type + decision. Đừng dump log.

## JSON Spec (model viết → script hoàn thiện)
```json
{
  "event_type": "DESIGN",
  "decision": "chuyển backbone ResNet → EfficientNet-B3",
  "why": "overfit (train 99% val 72%) do dataset nhỏ 2K",
  "delta": "AI đề xuất ViT → discard (data ít); thêm progressive resize; test 2 epoch trước commit",
  "evidence": "experiments/backbone_compare.csv"
}
```
Script tự thêm `entry_id` + `timestamp`. `evidence` optional.

## Gotchas

- **Materiality là điểm.** Log sai thứ → log vô dụng. 3 type, skip tất cả khác.
- **Compression.** 1 session ≤ 3 entries. Không gì đáng log → nói thẳng.
- **Evidence thật.** Path tồn tại, không bịa. Chưa có → `[chưa có evidence]`.
- **Append-only.** Không sửa/xóa cũ. `clear` = archive, không erase.
- **Được gọi, không tường thuật.** Orchestrator gọi tại decision point —
  không phải running commentary.
