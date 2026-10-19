---
name: "requirement-ladder"
description: "Turns a business goal into a three-rung requirement ladder — Epic (why, the business outcome), Feature (what capability the system must have), Story (one user need, sprint-sized and testable) — with Given/When/Then acceptance criteria on every story and exactly one tracer-bullet story per epic to de-risk the architecture early. Enforces a size gate that catches a Feature disguised as a Story. Modes — ladder (default, full decomposition), split (break one oversized story), audit (score an existing backlog). Triggers — chia nhỏ yêu cầu, epic feature story, user story, phân rã yêu cầu, backlog, acceptance criteria, tiêu chí nghiệm thu, story quá to, làm gì trước, tracer bullet, cần build gì, yêu cầu sản phẩm, break down requirements. It decomposes requirements; it does NOT choose the architecture (use architect), write an implementation spec (use spec-writer), or model entities (use domain-modeling)."
---

# Requirement Ladder (thang yêu cầu — Epic → Feature → Story)

> **Source:** bài "Epic, Feature, User Story — BA phân biệt thế nào?" (bản người dùng cung cấp
> 2026-08-07) cho ba bậc và bộ checklist; khái niệm *tracer bullet* từ **The Pragmatic Programmer**,
> gặp lại trong `mattpocock/skills` (to-tickets: chẻ plan thành tracer-bullet ticket có dependency).
> **Đã thêm so với nguồn:** bậc tracer bullet, cổng chặn kích thước có ngưỡng đo được, ràng buộc
> Given/When/Then, và vị trí trong chuỗi so với `architect`.

Thông báo khi bắt đầu: *"Đang dùng skill `requirement-ladder` mode `<mode>`."*

## Iron Law — Story không test được thì không phải Story

Mỗi Story phải mang **acceptance criteria dạng Given/When/Then** viết đủ cụ thể để `tdd-enforcer` biến
thẳng thành test đỏ. Không viết nổi tiêu chí nghiệm thu → yêu cầu chưa đủ rõ, **hỏi lại**, đừng đẩy
xuống backlog. Story mơ hồ là chỗ AI tự bịa hành vi.

## Conventions

Ràng buộc: `../_shared/rules/workbench-conventions.md` (song ngữ §1 — prose tiếng Việt, tên định danh
tiếng Anh; preview-not-dump §3; reuse-before-read §4; scope §10) và
`../_shared/rules/architecture-integrity.md` §6 (không viết yêu cầu như thể đã tồn tại). Đọc lúc chạy.

## Ba bậc

| Bậc | Trả lời | Đơn vị | Kiểm tra "đúng bậc" |
|---|---|---|---|
| **Epic** | *Vì sao làm?* — kết quả kinh doanh | Quá lớn cho một sprint | Nêu được outcome đo được (doanh thu / chi phí / rủi ro / trải nghiệm)? Không nêu được → chưa phải Epic, chỉ là mong muốn |
| **Feature** | *Cần xây năng lực gì?* | Nhóm chức năng, nhiều sprint | Tự nó giao được một phần giá trị dùng thật? Không → nó là task kỹ thuật, không phải Feature |
| **Story** | *Người dùng nào cần gì, để làm gì?* | Một sprint, test được | Qua **cổng kích thước** dưới đây? |

Story viết đúng khuôn: `As a <vai trò>, I want <mục tiêu>, so that <lý do>.`
Vai trò phải là **một** vai trò có thật trong hệ thống, không phải "user" chung chung.

## Cổng kích thước — bắt Feature đội lốt Story

Story **vi phạm bất kỳ ngưỡng nào** dưới đây là Feature trá hình → phải chẻ:

| Ngưỡng | Vi phạm khi |
|---|---|
| Màn hình / surface | Chạm > 1 màn hình |
| Endpoint | Cần > 3 endpoint mới |
| Acceptance criteria | Có > 5 tiêu chí |
| Liên từ | Tiêu đề chứa "và" nối **hai hành vi** khác nhau |
| Vai trò | Phục vụ > 1 vai trò người dùng |

Ví dụ trượt cổng: *"As a customer, I want to checkout securely so that I can buy products safely"* —
gộp thêm thẻ, xác thực, tóm tắt đơn, mã giảm giá, xác nhận, xử lý thất bại. Sáu Story, không phải một.

Không chắc → hỏi đúng một câu: **"Story này làm và test xong trong một sprint được không?"** Không →
chẻ.

## Bậc thứ tư — tracer bullet (mỗi Epic đúng một)

Chọn **đúng một** Story mỗi Epic làm *đạn vạch đường*: lát cắt **dọc** mỏng nhất chạy được đầu-cuối
(UI → API → service → DB → phản hồi về UI), làm **trước tiên**.

Tiêu chí chọn: chạm được nhiều tầng kiến trúc nhất với ít nghiệp vụ nhất. Nó không phải Story dễ nhất,
cũng không phải Story giá trị nhất — nó là Story **chứng minh kiến trúc đứng được**. Sai kiến trúc thì
lộ ở đây, khi sửa còn rẻ; phát hiện ở Story thứ 20 thì đã muộn.

Cắt ngang theo tầng ("làm hết database trước, rồi hết API") là phản mẫu: không có gì chạy được cho tới
tận cuối, và mọi giả định kiến trúc chỉ được kiểm chứng khi đã quá muộn để đổi.

---

## Procedure

### Phase 0 — Resolve
Xác định mode: `ladder` (mặc định) | `split <story>` | `audit <backlog-path>`. Kiểm `notes/INDEX.md`
và `notes/requirements-*.md` sẵn có trước (§4). Đầu vào mơ hồ tới mức không rõ ai là người dùng →
hỏi **một** câu bằng `ask the user a focused question`, không đoán.

### Phase 1 — Epic
Viết 1–3 Epic. Mỗi Epic: outcome đo được + vì sao quan trọng bây giờ. Không viết nổi outcome đo được →
ghi `[chưa đo được]` và nêu câu hỏi cần trả lời; **không** bịa chỉ số.

### Phase 2 — Feature
Với mỗi Epic, liệt kê năng lực cần có. Mỗi Feature một dòng mục đích + phần giá trị nó giao được.
Dừng ở mức năng lực — **chưa** chẻ Story ở bước này.

> **Chốt chặn:** đây là điểm bàn giao sang `architect` mode `blueprint`. Kiến trúc phải được chọn để
> đỡ **danh sách Feature này**. Chọn kiến trúc trước khi biết cần đỡ gì là chọn bừa. Quay lại Phase 3
> sau khi có bản vẽ.

### Phase 3 — Story (sau khi đã có kiến trúc)
Với mỗi Feature, viết Story theo khuôn, chạy **cổng kích thước** cho từng cái, gắn acceptance criteria:

```markdown
### S-<n> — <tiêu đề>
As a <vai trò>, I want <mục tiêu>, so that <lý do>.

**Acceptance criteria**
- Given <bối cảnh>, when <hành động>, then <kết quả quan sát được>.
- Given <ca lỗi>, when <hành động>, then <thông báo/hành vi cụ thể>.

**Phụ thuộc:** S-<x> · **Tracer bullet:** có/không · **Feature:** F-<n>
```

Ca lỗi là **bắt buộc** ít nhất một dòng. Story chỉ mô tả đường hạnh phúc là Story viết một nửa — và
nửa còn lại sẽ do AI tự nghĩ ra.

### Phase 4 — Thứ tự
Xếp theo phụ thuộc, tracer bullet lên đầu. Có chu trình phụ thuộc → chẻ tiếp cho tới khi hết.

### Phase 5 — Preview (§3)
Ghi `notes/requirements-<slug>.md`. In **5–8 dòng** tiếng Việt: số Epic/Feature/Story · tracer bullet
là cái nào · số Story bị chẻ do trượt cổng · điểm mơ hồ còn lại · bước kế tiếp. Không dump file.

---

## Mode `split`
Nhận một Story quá lớn, chẻ theo **hành vi** (không theo tầng kỹ thuật). Trục chẻ ưu tiên: từng bước
quy trình → từng vai trò → hạnh phúc vs ca lỗi → từng quy tắc nghiệp vụ. Mỗi mảnh phải tự nó giao được
giá trị quan sát được; mảnh nào không → đó là task kỹ thuật, gộp vào Story cần nó.

## Mode `audit`
Chấm backlog sẵn có, pass/fail từng dòng: Epic có outcome đo được? · Feature có phải năng lực (không
phải task)? · Story qua cổng kích thước? · có acceptance criteria? · có ca lỗi? · có truy ngược lên
Feature/Epic? Trả bảng finding, **không tự sửa backlog** — sửa yêu cầu là quyết định của người dùng.

## Gotchas
- **Cấm bịa chỉ số.** "Tăng chuyển đổi 30%" mà không có nguồn là số bịa — ghi `[chưa đo được]`.
- **Story sau kiến trúc, Feature trước kiến trúc.** Đảo thứ tự sinh ra Story cắt sai đường nối.
- **Đừng chẻ theo tầng.** "Làm DB trước" là phản mẫu — xem phần tracer bullet.
- **Giữ trong phạm vi (§10):**
  - `→ dùng architect cho` chọn kiến trúc và ghi ADR.
  - `→ dùng spec-writer cho` spec chi tiết + chia task của **một** Story đã chốt.
  - `→ dùng domain-modeling cho` entity/aggregate/invariant.
  - `→ dùng tdd-enforcer cho` biến acceptance criteria thành test đỏ.
  - `→ dùng brainstorming cho` giai đoạn còn chưa biết muốn làm gì.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
