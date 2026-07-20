---
name: latex-math-renderer
description: DEPRECATED alias (2026-07-20) — math repair lives in latex-fix; the compatibility table lives in ~/.claude/rules/latex-katex-compat.md. The HTML render modes were dropped (CDN-script snippets are blocked by Artifact CSP and were never part of a real workflow). This stub only redirects; if invoked, immediately apply latex-fix instead.
argument-hint: (deprecated — use latex-fix)
allowed-tools: Skill Read
---

# latex-math-renderer — DEPRECATED alias → `latex-fix`

Skill này đã ngừng phát triển (2026-07-20). Việc làm cho công thức render đúng trên cả
hai engine nằm ở **`latex-fix`** (linter + fix theo
`~/.claude/rules/latex-katex-compat.md`) — file này chỉ tồn tại để các tham chiếu cũ
không gãy.

## Nếu skill này bị gọi

Chuyển ngay sang `latex-fix` với cùng input. Mapping mode cũ → mới:

| Mode cũ (latex-math-renderer) | Thay bằng |
|---|---|
| `preview` (liệt kê lệnh không tương thích + gợi ý thay thế) | `latex-fix` Phase 1 (linter flag) + bảng fix trong `latex-katex-compat.md` |
| `batch` (quét nhiều expression trong file) | `latex-fix` (vốn là batch repair trên `notes/`) |
| `render` (LaTeX → HTML snippet nhúng CDN) | ĐÃ BỎ — snippet nhúng CDN MathJax bị CSP của Artifact chặn (external hosts); web surface viết math theo thẳng luật `latex-katex-compat.md` |
| Bảng Engine Selection (surface nào chạy engine nào) | đã chuyển vào `latex-fix` §Engine context |

## Lý do deprecate

Hai skill cùng phục vụ một mục tiêu ("công thức hiện đúng trên KaTeX + MathJax") nhưng
tách đôi: bảng tương thích một nơi, repair một nơi, còn mode `render` sinh HTML không
dùng được ở surface nào của suite. Common-patterns table của skill này trùng nội dung
`latex-katex-compat.md` — nguồn chuẩn duy nhất là rules file đó.
