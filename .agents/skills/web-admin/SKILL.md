---
name: web-admin
description: DEPRECATED alias (2026-08-02) — điều phối web đã bỏ. Stub này chỉ redirect, không tự điều phối. Gọi thẳng design-web (quyết hướng thiết kế) hoặc build-ui (dựng theo hệ token đã có); chuỗi design → build → review nay nằm trong chính build-ui.
---

# web-admin — DEPRECATED alias

Ngừng phát triển 2026-08-02. File này chỉ tồn tại để tham chiếu cũ không gãy.

## Gọi thẳng cái bạn cần

| Bạn muốn | Gọi |
|---|---|
| Quyết hướng thiết kế, chọn màu/chữ/bố cục | `design-web` |
| Dựng component / page / admin / scaffold | `build-ui` |
| Chấm anti-slop + a11y một site đã có | `review-frontend` |
| Backend, API, auth thật | `backend-engineer` |

Chuỗi **design → build → review** nay được ghi trong mục *"When to run the whole chain"* của
`build-ui`, cạnh chỗ thật sự dùng nó.

## Lý do bỏ

Thân skill này gần như chỉ là **một bảng tra**: *"Thiết kế giao diện X" → `design-web`*,
*"Dựng UI" → `build-ui`*. Nhưng Claude Code **đã tự khớp yêu cầu với description của từng skill** —
đó chính là thứ mà ~8k token description nạp mỗi phiên mua cho bạn. Đặt thêm một lớp tra cứu lên trên
là **trả tiền hai lần cho cùng một việc**, và bắt mỗi lượt dispatch đi qua hai skill thay vì một.

Phần duy nhất có giá trị thật — **thứ tự** design → build → review, và cảnh báo rằng
`build-admin-dashboard`/`scaffold-course-platform` là skill sống chứ không phải alias — đã được
chuyển vào `build-ui` và `admin`. Không mất gì.

> Bảng alias cũ ở đây từng khai sai rằng `build-admin-dashboard` và `scaffold-course-platform` đã bị
> gộp vào `build-ui`. **Sai** — cả hai là skill độc lập, có `references/` riêng. Đã sửa 2026-08-01.
