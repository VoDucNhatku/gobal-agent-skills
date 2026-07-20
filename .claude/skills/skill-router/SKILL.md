---
name: skill-router
description: DEPRECATED alias (2026-07-20) — routing lives in gobal-orchestrator. This stub only redirects; it performs no routing itself. If invoked, immediately apply gobal-orchestrator instead (modes classify/route cover everything this skill did).
argument-hint: (deprecated — use gobal-orchestrator)
allowed-tools: Skill Read
---

# skill-router — DEPRECATED alias → `gobal-orchestrator`

Skill này đã ngừng phát triển (2026-07-20). Toàn bộ chức năng routing nằm ở
**`gobal-orchestrator`** — file này chỉ tồn tại để các tham chiếu cũ không gãy.

## Nếu skill này bị gọi

Chuyển ngay sang `gobal-orchestrator` với cùng input. Mapping mode cũ → mới:

| Mode cũ (skill-router) | Thay bằng (gobal-orchestrator) |
|---|---|
| `route` (tìm skill tối ưu) | mode `classify` rồi `route` |
| `discover` (liệt kê skill) | Domain Registry trong gobal-orchestrator |
| `suggest` (gợi ý workflow đa skill) | mode `classify` (complexity + routing) |
| `recommend` / `analyze` (phân tích usage từ logs/) | ĐÃ BỎ — hạ tầng log không tồn tại; nếu cần suite-health, dùng `test-framework` |

## Lý do deprecate

Tách "router chọn skill" khỏi "orchestrator invoke skill" khiến mỗi dispatch đi qua
2 skill mà không thêm giá trị — gobal-orchestrator vốn đã classify → route → dispatch
trong một lượt. Hai mode meta (`recommend`/`analyze`) dựa trên `logs/token-usage-*.md`
và learnings-db chưa từng được sinh ra ở định dạng đó.
