# Architecture Integrity (binding cho mọi skill sinh/sửa tài liệu kiến trúc)

Rules file vệ tinh, đọc **lúc chạy** bởi `architect`, `requirement-ladder`, và bất kỳ skill nào
khẳng định điều gì về kiến trúc một hệ thống (`code-reviewer`, `self-evaluator`,
`understand-codebase`). Phụ thuộc `~/.claude/rules/workbench-conventions.md`; xung đột thì
conventions thắng. Skill trích một dòng và đọc lúc chạy — **không inline**.

Quy tắc gốc: **tài liệu kiến trúc chỉ được nói những gì kiểm chứng được, và phải rẻ đủ để đọc.**
Một tài liệu sai còn tệ hơn không có tài liệu — vì AI sẽ tin nó và xây tiếp trên nền sai.

---

## 1. CRITICAL — không đoán, không lấp chỗ trống

- Mọi câu khẳng định về hệ thống **đã tồn tại** phải truy được về `path/file:line`, một file config,
  hoặc một lệnh đã chạy. Không có nguồn → viết đúng chữ `> Not Found`, **không** viết cái mà "dự án
  kiểu này thường làm".
- **Cấm suy diễn theo mẫu ngành.** "Đa số dự án Node dùng JWT" không phải bằng chứng dự án NÀY dùng
  JWT. Framework mô tả *chỗ cần điền*, nó không cung cấp *nội dung*.
- **Mọi con số phải chép từ code/config**: TTL, timeout, pool size, coverage threshold, rate limit,
  port. Con số không có nguồn là số bịa — vi phạm nặng ngang bịa kết quả thực nghiệm
  (`paper-writing-integrity` §3).
- Suy luận có cơ sở nhưng chưa xác minh → gắn `[suy luận]` và nêu căn cứ. Không gắn nhãn = đang
  trình bày phỏng đoán như sự thật.
- Mục "> Not Found" **là kết quả hợp lệ và hữu ích** — nó chỉ ra lỗ hổng thật của dự án. Lấp đầy 27
  mục bằng văn xuôi trơn tru là thất bại, không phải thành công.

## 2. Ngân sách token — tài liệu phải đọc được, không chỉ viết được

Tài liệu kiến trúc mà agent không đủ context để nạp thì vô dụng. Bắt buộc **phân tầng**:

| Tầng | File | Trần | Nội dung |
|---|---|---|---|
| Chỉ mục | `ARCHITECTURE.md` | **≤ 200 dòng** | Mục lục + đúng những ràng buộc chi phối MỌI thay đổi |
| Chi tiết | `docs/arch/<NN>-<slug>.md` | ≤ 400 dòng/file | Từng mục sâu, đọc theo yêu cầu |
| Quyết định | `docs/arch/adr/<NNNN>-<slug>.md` | ≤ 80 dòng/ADR | Một quyết định một file, append-only |

Tầng chỉ mục chứa tối đa 8 thứ: tech stack + phiên bản · cấu trúc thư mục · sơ đồ hệ thống · danh
sách module (một dòng mỗi module) · **danh sách bất biến "không bao giờ được làm"** · quy ước code ·
chỉ mục ADR · bảng trỏ tới các file chi tiết. Mọi thứ khác xuống tầng dưới.

> Đây chính là progressive disclosure mà conventions §11 đã bắt buộc cho skill — áp dụng lại cho
> tài liệu dự án. Một `ARCHITECTURE.md` 3.000 dòng vi phạm nguyên tắc này dù nội dung đúng.

## 3. Co giãn theo quy mô — số mục là hệ quả, không phải mục tiêu

| Tier | Khi nào | Số mục |
|---|---|---|
| `demo` | Demo sản phẩm, hackathon, POC, 1–3 người, ≤ 3 tuần | 7 |
| `product` | Có người dùng thật, dữ liệu thật, hoặc tiền thật | 16–19 |
| `platform` | Team ≥ 5, nhiều service, có SLO/on-call | tối đa 27 |

Viết mục không áp dụng được cho tier hiện tại → **bỏ hẳn mục đó**, không viết "N/A". Mục N/A tốn token
và che lấp mục thật. Nâng tier là quyết định của người dùng, ghi thành ADR.

## 4. Quyết định là hạng mục hạng nhất, không phải phụ lục

Mỗi ADR bắt buộc có đủ: **bối cảnh · quyết định · phương án ĐÃ LOẠI BỎ kèm lý do · hệ quả chấp nhận ·
điều kiện đảo ngược (khi nào quyết định này nên bị xét lại)**.

Thiếu "phương án đã loại bỏ" thì đó không phải ADR, chỉ là mô tả. Phần *tại sao không chọn cái kia* là
thứ duy nhất AI không tự suy được từ source code — mọi thứ khác nó đọc code là ra.

ADR **append-only**: quyết định đổi thì viết ADR mới `Supersedes: <id>`, đánh dấu bản cũ
`Superseded by: <id>`. Không sửa đè, không xóa — lịch sử quyết định chính là giá trị.

## 5. Giữ tươi — tài liệu phải kiểm chứng lại được

- Mỗi tài liệu mang header: ngày sinh (`YYYY-MM-DD`) · commit/trạng thái nguồn · tier · người/skill sinh ra.
- Khẳng định nào kiểm được bằng máy thì phải kiểm bằng máy (đường dẫn có tồn tại · dependency có trong
  manifest · biến env có xuất hiện trong code), không kiểm bằng mắt.
- **Trôi (drift) là finding, không phải ghi chú.** Doc nói A, code làm B → báo mâu thuẫn kèm cả hai
  nguồn, và **không tự sửa doc theo code**: một trong hai đang sai, chọn cái nào là việc của người dùng.
- Tín hiệu tìm chỗ kiến trúc hỏng: file bị sửa nhiều lần nhất trong lịch sử git thường là chỗ kiến trúc
  đặt sai đường cắt (ý từ `mattpocock/skills` — improve-codebase-architecture).

## 6. Trung thực về chiều đang chạy

Có đúng hai chiều, không được lẫn:

- **Xuôi (blueprint)** — chưa có code. Mọi thứ là *dự định*, đánh dấu `[quyết định]` (đã chốt) hoặc
  `[chưa quyết]` (còn mở). **Cấm** viết bằng thì hiện tại như thể đã tồn tại.
- **Ngược (document)** — đã có code. Mọi thứ là *quan sát*, chịu §1. Cấm viết điều mong muốn.

Dự án có code một phần → chạy `document` cho phần đã có, `blueprint` cho phần chưa có, và **đánh dấu
rõ ranh giới**. Trộn hai chiều mà không phân định là cách sinh ra tài liệu nửa thật nửa mơ — nguy hiểm
nhất, vì không ai biết phần nào kiểm được.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Giải thích ngắn |
|---|---|---|
| architecture drift | trôi kiến trúc | Tài liệu và code nói khác nhau; một trong hai đã lỗi thời |
| ADR (Architecture Decision Record) | biên bản quyết định kiến trúc | Một quyết định + phương án đã loại bỏ + điều kiện đảo ngược |
| tier | bậc quy mô | demo / product / platform — quyết định số mục cần viết |
| progressive disclosure | tiết lộ tăng dần | Chỉ mục mỏng luôn nạp, chi tiết đọc theo yêu cầu |
| tracer bullet | đạn vạch đường | Lát cắt dọc mỏng nhất chạy được đầu-cuối, dùng để chứng minh kiến trúc |
| grounding | neo nguồn | Mỗi khẳng định truy được về file:line hoặc một lệnh đã chạy |
