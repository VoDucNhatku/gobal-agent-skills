---
name: "build-ui-component"
description: "DEPRECATED alias (2026-07-20) — absorbed into build-ui. One-component builds are build-ui mode component; the component catalog moved to build-ui/references/component-catalog.md. This stub only redirects; if invoked, immediately apply build-ui instead."
---

# build-ui-component — DEPRECATED alias → `build-ui`

Skill này đã được sáp nhập vào **`build-ui`** (2026-07-20). File này chỉ tồn tại để
các tham chiếu cũ không gãy. Tài sản duy nhất
(`../build-ui/references/component-catalog.md`) đã chuyển về `build-ui`; bản ở đây đã xóa.

## Nếu skill này bị gọi

Chuyển ngay sang `build-ui` với cùng input. Mapping mode cũ → mới:

| Mode cũ (build-ui-component) | Thay bằng |
|---|---|
| `component` (dựng 1 component từ design tokens) | `build-ui` mode `component` |
| `variant` (thêm variant cho component có sẵn) | `build-ui` mode `component` (nêu rõ variant cần thêm trong yêu cầu) |
| `audit` (kiểm a11y / slop một component) | `review-frontend` |

Các guardrail a11y (focus-visible, đủ state, reduced-motion, không truyền state bằng
màu đơn thuần) và Anti-Runaway Contract (Edit over Write, verify trước khi claim done)
đã nằm sẵn trong `build-ui` Phase 1 + quality floor §7 của
`../../rules/frontend-aesthetics.md` — không mất nội dung khi chuyển.

## Lý do deprecate

`build-ui` đã gộp build-ui-component / build-admin-dashboard / scaffold-course-platform
thành một skill 4 mode (`component`/`page`/`admin`/`scaffold`) đọc chung một
design-record. Giữ skill lẻ này tạo 2 đường vào cho cùng một việc, và tách
component catalog khỏi chính skill dùng nó (build-ui từng tham chiếu `references/`
mà không sở hữu file — tham chiếu ma, đã sửa 2026-07-20).


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
