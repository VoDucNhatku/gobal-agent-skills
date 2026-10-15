# Layout profiles — chọn hồ sơ và lý do từng vùng

> Danh sách thư mục **chính xác** nằm ở `../scripts/profiles.json` (script đọc file đó).
> File này chỉ giải thích **cách chọn** và **vì sao** mỗi vùng được đặt ở đó — đọc khi cần
> biện luận với người dùng hoặc khi mở rộng một hồ sơ.

## 1. Chọn hồ sơ

| Hồ sơ | Chọn khi | Dấu hiệu nhận biết |
|---|---|---|
| `research` | Sản phẩm cuối là **bài báo / kết quả thí nghiệm** | có `papers/`, cần `claims-ledger`, chạy GPU, viết LaTeX |
| `web` | Sản phẩm cuối là **ứng dụng người dùng truy cập** | có route, có UI, có deploy |
| `agent` | Sản phẩm cuối là **hệ agent / RAG** người khác gọi | có prompt, skill, eval, vector index |
| `mixed` | Từ **hai loại trở lên**, hoặc nhóm ≥4 người | mặc định cho nhóm công ty |

Nghi ngờ giữa hai hồ sơ → chọn `mixed`. Thừa một thư mục rỗng rẻ hơn nhiều so với việc
phải tái cấu trúc khi đã có 5 người đang làm dở.

## 2. Ba câu hỏi quyết định mọi vùng (Iron Law)

Mỗi thư mục phải trả lời được:

1. **Ai sở hữu?** → quyết định dòng trong `CODEOWNERS`.
2. **Có vào git không?** → quyết định `.gitignore`.
3. **Người hay máy sinh ra?** → quyết định có cần review không, và có tái tạo được không.

Không trả lời được cả ba → **đừng tạo thư mục đó**. Thư mục vô chủ là thư mục sẽ thành bãi rác.

## 3. Vì sao vùng này track, vùng kia ignore

| Vùng | Quyết định | Lý do |
|---|---|---|
| `papers/`, `data/raw/` | ignore + `manifest.md` được track | Nhị phân git không merge được; đã push là nằm vĩnh viễn trong lịch sử, repo phình không xóa lại. Manifest giữ lại *bản đồ* để người mới biết tải ở đâu |
| `data/interim/`, `data/processed/` | ignore | **Tái tạo được** bằng script. Commit script, đừng commit kết quả — nếu không sẽ có hai nguồn sự thật |
| `outputs/` | ignore | Sản phẩm AI sinh. Trộn vào `data/` là để vòng sau AI đọc lại chính output của nó |
| `.runs/` (traces) | ignore | Log máy sinh, append-only, hàng chục MB/ngày. Vòng đời khác hẳn `evals/tests/` viết tay |
| `evals/tests/`, `evals/scorecards/` | track | Viết tay, ít đổi, **phải được review** — đây là bằng chứng chất lượng |
| `notes/`, `research/notes/` | track | Text, merge tốt, một file một paper nên hiếm khi đụng nhau |
| `design/` | track | Design-record đã khóa từ `design-web` — `build-ui` đọc nó làm nguồn sự thật |
| `config/` | track | Tham số, **không chứa khóa**. Khóa nằm ở `.env` (ignore) + `.env.example` (track) |

### Vì sao `data/raw/*` chứ không phải `data/raw/`

Git **không thể** re-include một file nếu thư mục cha đã bị loại trừ. Viết `data/raw/`
thì `!data/raw/manifest.md` vô hiệu. Phải viết `data/raw/*` rồi mới phủ định được.
Đây là lỗi tinh vi và im lặng — đã kiểm chứng bằng `git check-ignore`.

## 4. `prompts/` và `agents/skills/` — ranh giới bắt buộc

Một `skill.md` (vai trò, quy trình, tiêu chuẩn đầu ra) **chính là** một system prompt.
Nếu để cả hai nơi cùng chứa nó, sẽ có hai bản, sửa một bản, và trôi lệch.

Chia theo **cơ chế gọi**, không theo nội dung:

- Agent **tự động nạp** → `agents/skills/<ten>/skill.md`. Đây là chủ sở hữu duy nhất.
- Người **dán tay** hoặc code gọi qua API → `prompts/tasks/<ten>.md`.

Dùng Claude Code / Antigravity thì gần như mọi thứ dồn về `agents/skills/`, `prompts/`
teo lại còn vài template.

## 5. Mở rộng một hồ sơ

Thêm vùng mới → thêm vào `extra_dirs` trong spec (không sửa `profiles.json` cho một dự án
đơn lẻ). Chỉ sửa `profiles.json` khi vùng đó đúng cho **mọi** dự án cùng hồ sơ.

Mỗi vùng thêm vào phải kèm câu trả lời cho ba câu ở §2, ghi vào bảng bản đồ trong `README.md`.
