---
name: "reuse-checker"
description: "DEPRECATED alias (2026-07-20) — absorbed into artifact-manager. Its staleness table and check/suggest/diff modes now live there (modes reuse/suggest/diff). This stub only redirects; if invoked, immediately apply artifact-manager instead."
---

# reuse-checker — DEPRECATED alias → `artifact-manager`

Skill này đã được sáp nhập vào **`artifact-manager`** (2026-07-20). File này chỉ tồn
tại để các tham chiếu cũ không gãy.

## Nếu skill này bị gọi

Chuyển ngay sang `artifact-manager` với cùng input. Mapping mode cũ → mới:

| Mode cũ (reuse-checker) | Thay bằng (artifact-manager) |
|---|---|
| `check` (tìm artifact + staleness) | mode `reuse` (đã kèm bảng staleness + output format) |
| `suggest` (artifact liên quan) | mode `suggest` |
| `diff` (artifact cũ vs yêu cầu mới) | mode `diff` |

## Lý do deprecate

Hai skill cùng giữ một protocol REUSE-BEFORE-READ (workbench-conventions §4) nhưng
bảng staleness chỉ nằm ở một bên còn INDEX.md nằm ở bên kia — mỗi lần check phải nhảy
qua lại. Sáp nhập về `artifact-manager` (chủ sở hữu `notes/INDEX.md`) để một skill
làm trọn một việc.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
