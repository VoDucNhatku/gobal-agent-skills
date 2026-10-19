# Section Catalog — 27 mục kiến trúc, đã phân bậc và gắn nguồn kiểm chứng

Dữ liệu tham chiếu của skill `architect`. Đọc **một mục** khi cần viết mục đó — không nạp cả file.
Ràng buộc: `../../_shared/rules/architecture-integrity.md`.

> **Source:** khung 27 phần từ bài "Bạn là kiến trúc sư, AI chỉ là thợ" (bản người dùng cung cấp,
> 2026-08-07), đã tái cấu trúc: thêm cột **tier**, cột **nguồn kiểm chứng**, cột **dấu hiệu filler**,
> và đảo mục 27 (quyết định kiến trúc) lên hạng mục hạng nhất theo `architecture-integrity` §4.

## Cách đọc bảng

- **Tier** — `D` = demo · `P` = product · `X` = platform. Mục gắn `P` chỉ viết khi tier ≥ product.
- **Nguồn kiểm chứng** — nơi PHẢI đọc để viết mục này ở mode `document`. Không tìm thấy → `> Not Found`.
- **Dấu hiệu filler** — nếu bản viết ra trông như cột này, mục đó vô giá trị, xóa hoặc viết lại.

---

## Tầng chỉ mục — luôn nằm trong `ARCHITECTURE.md` (≤ 200 dòng)

| # | Mục | Tier | Nguồn kiểm chứng | Dấu hiệu filler |
|---|---|---|---|---|
| 1 | **Project Overview** | D | `README`, `package.json:description`, entry point | Viết chung chung "hệ thống quản lý hiện đại"; không nói ai dùng và giải quyết vấn đề gì |
| 2 | **Tech Stack** | D | `package.json` / `requirements.txt` / `go.mod` / lockfile · Dockerfile · CI workflow | Liệt kê tên thư viện mà **không có phiên bản**; kê cả thứ không thực sự dùng |
| 3 | **Folder Structure** | D | `ls` thật của repo, `tsconfig paths`, alias import | Chép cây thư mục mà không nói **quy tắc đặt code mới ở đâu** |
| 4 | **System Architecture** | D | `docker-compose.yml` · nginx/gateway config · biến env trỏ service · sơ đồ Mermaid tự vẽ | Sơ đồ hộp-mũi-tên không ghi giao thức và cổng |
| 5 | **Module Breakdown** | D | Thư mục `src/modules/*` hoặc tương đương · router mount · export công khai | Liệt kê tên module mà không nói **trách nhiệm** và **ai phụ thuộc ai** |
| 22 | **Coding Convention** | P | `.eslintrc` · `.prettierrc` · `ruff.toml` · `.editorconfig` | Chép nguyên tài liệu ESLint; không nêu quy ước **riêng của dự án này** |
| — | **Invariants** *(mục thêm, không có trong khung gốc)* | D | Rút từ mục 7, 8, 17, và các ADR | Danh sách "best practice" chung thay vì ràng buộc thật của dự án |
| — | **ADR Index** *(mục thêm)* | D | `docs/arch/adr/` | Trống, trong khi dự án rõ ràng đã có quyết định lớn |

> Mục **Invariants** là danh sách "không bao giờ được làm" — mỗi dòng một câu mệnh lệnh, có nguồn.
> Ví dụ có giá trị: *"Không bao giờ cấp quyền dựa trên role phía client — mọi kiểm tra ở server
> (`src/middleware/authenticate.js:12`)"*. Đây là mục AI đọc nhiều nhất và cứu nhiều nhất.

---

## Tầng chi tiết — mỗi mục một file `docs/arch/<NN>-<slug>.md`

| # | Mục | Tier | Nguồn kiểm chứng | Dấu hiệu filler |
|---|---|---|---|---|
| 6 | **Request Flow** | P | Middleware chain trong app entry · một controller thật đọc từ đầu đến cuối | Mô tả lý thuyết MVC thay vì lần theo **một request có thật** |
| 7 | **Authentication** | P | Module auth · thư viện token · nơi lưu token · TTL trong env | Nói "dùng JWT" mà không nêu thuật toán ký, nơi lưu, TTL, cách thu hồi |
| 8 | **Authorization** | P | Middleware phân quyền · bảng role/permission · RLS policy | Nói "có RBAC" mà không chỉ ra **nơi kiểm tra thực sự chạy** |
| 9 | **Database** | D | `schema.prisma` / migration files / `models.py` · sơ đồ ER sinh từ schema | Vẽ ER mà bỏ qua index, cascade, và chiến lược migration |
| 10 | **API Architecture** | P | Router definitions · schema validation · format response thật | Nói "RESTful" mà không nêu quy ước versioning và format lỗi |
| 11 | **Business Flow** | D | Service layer · test e2e · sequence diagram lần theo code | Kể lại use case bằng lời mà không gắn tên hàm/endpoint cụ thể |
| 12 | **Dependency Graph** | P | Output của `understand-codebase` mode scan | Vẽ đồ thị mà không chỉ ra **cycle** hoặc hub nguy hiểm |
| 13 | **External Services** | P | SDK imports · biến env chứa key · client wrapper | Liệt kê dịch vụ mà bỏ timeout, rate limit, và fallback khi nó chết |
| 14 | **Configuration** | D | `.env.example` · config loader · `docker-compose environment` | Chép `.env.example` mà không nói biến nào **bắt buộc** và mặc định là gì |
| 15 | **Logging** | P | Logger setup · format · nơi log được gửi tới | Nói "có logging" mà không nêu trường bắt buộc (request_id, user_id) |
| 16 | **Error Handling** | P | Global error handler · lớp exception · mã lỗi | Không nêu **hình dạng response lỗi** mà client phải parse |
| 17 | **Security** | P | Helmet/CORS config · validation layer · rate limiter · secret handling | Chép OWASP Top 10 thay vì nói dự án này **thật sự** chặn gì ở đâu |
| 18 | **Performance** | X | Cache layer · index DB · kết quả benchmark đã chạy | Nêu con số SLO chưa từng đo — vi phạm `architecture-integrity` §1 |
| 19 | **Scalability** | X | Replica config · load balancer · sharding key | Bàn lý thuyết scale cho hệ thống chưa có người dùng |
| 20 | **Deployment** | P | CI/CD workflow files · Dockerfile · script deploy | Mô tả pipeline lý tưởng thay vì pipeline **đang chạy** |
| 21 | **Testing** | P | Test config · coverage threshold · thư mục test thật | Nêu mục tiêu coverage mà không nói **con số hiện tại** |
| 23 | **Design Pattern** | P | Đọc code thật để nhận diện pattern đang dùng | Liệt kê pattern GoF mà code không hề dùng |
| 24 | **Strengths** | P | Rút từ các mục trên, có dẫn chiếu | Tự khen chung chung, không dẫn được bằng chứng |
| 25 | **Technical Debt** | P | `TODO`/`FIXME` grep · test bị skip · ADR bị supersede | Danh sách nợ mơ hồ, không có vị trí file và không xếp ưu tiên |
| 26 | **Improvement Proposal** | X | Từ mục 25 + ADR có điều kiện đảo ngược đã chạm | Danh sách mong ước không gắn với nợ hay ràng buộc thật |
| 27 | **Appendix** | X | Glossary · sơ đồ phụ · link tài liệu ngoài | Bãi rác chứa thứ không xếp được chỗ khác |

---

## Bộ mục theo tier (dùng trực tiếp, không phải tự suy)

- **`demo` (7 mục)** — 1, 2, 3, 4, 9, 11, 14 + Invariants. Thêm mục 7 **chỉ khi** demo có đăng nhập.
  Lý do chọn bộ này: đây đúng những chỗ AI hay tự tiện bịa ra — thêm thư viện lạ, đặt file sai chỗ,
  đổi hình dạng dữ liệu, đoát tên biến env.
- **`product` (16–19 mục)** — bộ `demo` + 5, 6, 7, 8, 10, 13, 15, 16, 17, 20, 21, 22.
- **`platform` (tối đa 27)** — thêm 12, 18, 19, 23, 24, 25, 26, 27.

## Mẫu ADR (`docs/arch/adr/<NNNN>-<slug>.md`, ≤ 80 dòng)

```markdown
# ADR-<NNNN>: <quyết định, viết ở thể khẳng định>

- Ngày: YYYY-MM-DD · Trạng thái: accepted | superseded by ADR-<n> | proposed
- Liên quan: <mục kiến trúc số mấy>

## Bối cảnh
<Ràng buộc thật buộc phải quyết. Có số liệu/nguồn thì dẫn.>

## Quyết định
<Một câu. Thể khẳng định, hiện tại.>

## Phương án đã loại bỏ
| Phương án | Vì sao loại |
|---|---|
| <A> | <lý do cụ thể, không phải "phức tạp hơn"> |

## Hệ quả chấp nhận
<Cái giá đã biết và đồng ý trả.>

## Điều kiện đảo ngược
<Dấu hiệu cụ thể khiến quyết định này phải được xét lại.>
```

Thiếu bảng **Phương án đã loại bỏ** hoặc **Điều kiện đảo ngược** → chưa phải ADR (§4).
