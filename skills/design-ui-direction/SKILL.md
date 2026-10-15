---
name: "design-ui-direction"
description: "DEPRECATED alias (2026-07-20) — design direction lives in design-web. The shared reference tables (anti-slop-bans, palettes, type-pairings, style-archetypes CSVs) and the Artifact preview template are owned by design-web (references/ and assets/). This stub only redirects; if invoked, immediately apply design-web instead."
---

# design-ui-direction — DEPRECATED alias → `design-web`

Skill này đã ngừng phát triển (2026-07-20). Toàn bộ việc chọn hướng thiết kế
(anti-slop tokens, type pairing, palette, HTML Artifact preview) nằm ở
**`design-web`** — file này chỉ tồn tại để các tham chiếu cũ không gãy.

## Nếu skill này bị gọi

Chuyển ngay sang `design-web` với cùng input. Mapping:

| Chức năng cũ (design-ui-direction) | Thay bằng (design-web) |
|---|---|
| Chọn hướng thiết kế + token set | `design-web` (toàn bộ procedure) |
| HTML Artifact preview | `design-web` Phase 4 (`../design-web/assets/artifact-preview-template.html`) |
| Bảng dữ liệu anti-slop / palettes / type-pairings / style-archetypes | `design-web/references/*.csv` (peer skill đọc trực tiếp) |

`review-frontend` cũng đọc CSV trực tiếp từ `../design-web/references` — không đi qua
stub này.

## Lý do deprecate

File này về sau chỉ còn là "data stub" trỏ sang chính các bảng CSV mà design-web sở
hữu — một tầng chuyển hướng không mang thêm dữ liệu. Bản asset trùng lặp
(`../design-web/assets/artifact-preview-template.html`, byte-identical với bản của
design-web) đã xóa; bản chuẩn duy nhất nằm ở `../design-web/assets`.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
