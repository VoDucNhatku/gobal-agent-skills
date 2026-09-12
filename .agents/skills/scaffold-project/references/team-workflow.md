# Team workflow — quy tắc quyết định theo quy mô nhóm

> `CONTRIBUTING.md` sinh ra trong dự án đã chứa phần hướng dẫn cho **thành viên**.
> File này là phần **skill cần để ra quyết định**: chia sở hữu thế nào, bật cơ chế nào ở
> quy mô nào, và checklist cho mode `audit`.

## 1. Bật cơ chế theo quy mô

| Quy mô | Nhánh + PR | Review bắt buộc | CODEOWNERS | Branch protection | Ghi chú |
|---|---|---|---|---|---|
| 1 người | nên | không | không | không | Nhánh vẫn hữu ích để rollback |
| 2–3 | có | tự merge sau CI | không | chỉ chặn force-push | Chưa cần bộ máy |
| **4–8** | **có** | **1 approval** | **có** | **có** | Ngưỡng chuyển sang "hệ thống" |
| 9+ | có | 1–2 approval | có | có + release branch | Cần cả người điều phối |

Ngưỡng thật nằm ở **4 người**, không phải 8: từ 4 trở lên không ai còn nắm hết mọi thay đổi
trong đầu, nên phải có cơ chế thay cho trí nhớ.

## 2. Cắt vùng sở hữu — nguyên tắc quan trọng nhất

**Cắt theo thư mục (theo tính năng), không cắt theo lớp kỹ thuật.**

Chia "một người frontend, một người backend" nghe hợp lý nhưng sai: mọi tính năng đều chạm
cả hai, nên mọi PR đều cần cả hai duyệt, và hai người luôn chờ nhau. Cắt dọc theo vùng
chức năng thì phần lớn PR chỉ chạm một vùng, một người duyệt là xong.

Gợi ý cho nhóm 8 người trên hồ sơ `mixed`:

| Vùng | Số người | Vai trò |
|---|---|---|
| `apps/web` + `packages/ui` + `design` | 2–3 | Giao diện, đi cùng `design-web` → `build-ui` |
| `apps/api` + `packages/core` + `infra` | 2 | Backend, dữ liệu, triển khai |
| `agents/` + `prompts/` + `evals/` | 2 | Chất lượng AI — người viết prompt phải là người viết eval |
| `research/` + `data/` | 1–2 | Nghiên cứu, quản lý dữ liệu và manifest |

Một người có thể sở hữu nhiều vùng; một vùng **không được** vô chủ.

## 3. Giới hạn để review còn có nghĩa

| Giới hạn | Con số | Vì sao |
|---|---|---|
| Kích thước PR | ~400 dòng thay đổi | Vượt ngưỡng, chất lượng review tụt rõ; PR to thường bị duyệt lấy lệ |
| Nhánh mở / người | 2 | Nhiều hơn là đang làm dở dang khắp nơi |
| Tuổi nhánh | 3 ngày | Nhánh sống lâu là nhánh sẽ conflict |
| Phản hồi PR | trong ngày làm việc | PR chờ lâu chặn cả dây chuyền |

Đây là **quy tắc kinh nghiệm để vận hành**, không phải kết quả đo đạc — trình bày đúng như vậy.

## 4. Chống xung đột bằng cấu trúc

Cấu trúc thư mục tốt là cấu trúc khiến **hai người hiếm khi chạm cùng một file**:

- **Một thứ một file** — mỗi prompt một file, mỗi skill một thư mục, mỗi paper một note.
- **File dùng chung là nam châm hút xung đột** (`INDEX.md`, sổ ghi chung, config tổng):
  quy ước **chỉ thêm vào cuối**, không chèn giữa, không sắp xếp lại. Nếu vẫn đụng nhiều →
  tách theo người (`INDEX-<ten>.md`) rồi gộp định kỳ.
- **Notebook** `.ipynb` là JSON nhúng output, merge rất tệ → `nbstripout`, và giữ logic thật
  trong `src/`.
- **File nhị phân** không vào git — storage ngoài + `manifest.md`.

## 5. Khi có agent AI tự commit (Antigravity, Claude Code…)

- `.gitignore` phải tồn tại **trước** commit đầu tiên. Agent "stage all" không phân biệt
  file nhạy cảm.
- **Mỗi agent một nhánh.** Nhiều agent cùng một nhánh là công thức gây xung đột.
- Commit message do AI sinh mô tả *cái gì đã đổi*; người vẫn phải bổ sung *vì sao*.

## 6. Sự cố lộ khóa

Đã push khóa lên GitHub thì xóa file **không đủ** — nó nằm trong lịch sử, ai clone cũng đọc
được. Thứ tự xử lý: **(1) hủy khóa cũ ở nhà cung cấp ngay** → (2) tạo khóa mới trong `.env`
→ (3) báo cả nhóm. Viết lại lịch sử (`filter-repo`) là bước phụ, không thay thế bước 1.

## 7. Checklist cho mode `audit`

Chấm repo đang có, mỗi dòng là pass/fail kèm bằng chứng (đường dẫn hoặc lệnh):

| # | Kiểm | Lệnh xác minh | Mức |
|---|---|---|---|
| 1 | Có `.gitignore` và nó chặn `.env` | `git check-ignore -v .env` | **chặn** |
| 2 | Không có bí mật nào **đã** bị commit | `git log --all --diff-filter=A --name-only \| grep -Ei '\.env$\|credential\|secret'` | **chặn** |
| 3 | Không có nhị phân lớn trong lịch sử | `git rev-list --objects --all` + `git cat-file --batch-check` sắp theo size | cao |
| 4 | Nhánh chính được bảo vệ (nhóm ≥4) | GitHub Settings → Branches | cao |
| 5 | Có `CODEOWNERS`, không còn `@TODO-` | đọc `.github/CODEOWNERS` | cao |
| 6 | Mọi thư mục trả lời được 3 câu (Iron Law) | đối chiếu bảng trong `README.md` | trung bình |
| 7 | Notebook không nhúng output | `grep -l '"output_type"' **/*.ipynb` | trung bình |
| 8 | Có `evals/` với ít nhất 1 scorecard tách gate/điểm | đọc `evals/scorecards/` | trung bình |
| 9 | `data/raw` không bị sửa tại chỗ (có manifest) | đọc `data/raw/manifest.md` | thấp |

Mục 1–2 là **cổng chặn**: fail thì báo trước mọi thứ khác, kèm hướng dẫn hủy khóa (§6).
