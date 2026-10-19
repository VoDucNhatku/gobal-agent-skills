---
name: "architect"
description: "Designs and maintains a project's architecture document as a layered, verifiable artifact — a thin ARCHITECTURE.md index plus on-demand detail files and append-only ADRs, scaled to project size (demo/product/platform) rather than a fixed 27-section template. Modes — blueprint (forward, before code exists; every item marked decided or open), document (reverse, from real source only; unfound sections written as Not Found), adr (one decision with the alternatives rejected and its reversal conditions), drift (compare document against real code, report contradictions, rewrite neither side silently). Triggers — thiết kế kiến trúc, kiến trúc dự án, ARCHITECTURE.md, tài liệu kiến trúc, sơ đồ hệ thống, chọn stack, quyết định kiến trúc, ADR, kiến trúc web app, kiến trúc demo, tài liệu lệch code, architecture drift, document the architecture. It decides and records architecture; it does NOT map symbols (use understand-codebase), write a feature spec (use spec-writer), or create folders (use scaffold-project)."
---

# Architect (kiến trúc dự án — bản vẽ, quyết định, và kiểm chứng)

> **Source:** khung 27 phần từ bài "Bạn là kiến trúc sư, AI chỉ là thợ" (bản người dùng cung cấp
> 2026-08-07) + prompt `/architecture-plan` của người dùng (quy tắc `> Not Found`) + `mattpocock/skills`
> (improve-codebase-architecture: churn git là tín hiệu kiến trúc sai; ADR khi bác một phương án).
> **Đã sửa so với nguồn:** thêm phân tầng token, thêm chiều xuôi (blueprint), co giãn theo tier,
> đưa quyết định lên hạng mục hạng nhất, và thêm cơ chế kiểm tra trôi.

Thông báo khi bắt đầu: *"Đang dùng skill `architect` mode `<mode>`."*

## Iron Law — không có nguồn thì không có câu

Ở mode `document`/`drift`, mỗi khẳng định phải trỏ được về `file:line`, một file config, hoặc một lệnh
đã chạy. Không tìm thấy → viết đúng chữ **`> Not Found`**. Cấm điền bằng cái mà "dự án kiểu này thường
làm". Một mục `> Not Found` là kết quả đúng — nó chỉ ra lỗ hổng thật; một mục văn xuôi trơn tru không
có nguồn là tài liệu giả.

## Conventions

Ràng buộc: `../_shared/rules/architecture-integrity.md` (neo nguồn §1 · phân tầng token §2 · tier §3 ·
ADR §4 · giữ tươi §5 · hai chiều §6) và `../_shared/rules/workbench-conventions.md` (song ngữ §1 —
prose tiếng Việt, tên file/định danh tiếng Anh; preview-not-dump §3; reuse-before-read §4; đọc chiến
lược §6; script-offloading §9). **Đọc lúc chạy, không inline.** Danh mục 27 mục nằm ở
`references/section-catalog.md`, khuôn sơ đồ nằm ở `references/diagram-templates.md` — đọc **từng
mục / từng khuôn** khi cần, không nạp cả file.

## Modes

| Mode | Dùng khi | Output |
|---|---|---|
| `blueprint` | **Chưa có code.** Web/app/demo mới, cần bản vẽ trước khi AI code | `ARCHITECTURE.md` (thì tương lai, gắn `[quyết định]`/`[chưa quyết]`) + ADR cho mỗi lựa chọn lớn |
| `document` | **Đã có code.** Cần tài liệu chính thức, onboard người mới, audit | `ARCHITECTURE.md` + `docs/arch/<NN>-*.md`, mọi câu có nguồn |
| `adr` | Vừa chốt một quyết định kiến trúc | Một file `docs/arch/adr/<NNNN>-<slug>.md` |
| `drift` | Nghi tài liệu và code đã lệch | Bảng mâu thuẫn — **không tự sửa bên nào** |

Không nêu mode: có source code → `document`, thư mục trống/chỉ có README → `blueprint`.

## Cấu trúc output (bắt buộc, §2)

```
ARCHITECTURE.md              ≤ 200 dòng — chỉ mục + ràng buộc chi phối MỌI thay đổi
docs/arch/<NN>-<slug>.md     ≤ 400 dòng/file — mục sâu, đọc theo yêu cầu
docs/arch/adr/<NNNN>-*.md    ≤ 80 dòng — một quyết định một file, append-only
```

`ARCHITECTURE.md` chứa tối đa 8 khối: tech stack + phiên bản · cấu trúc thư mục · sơ đồ hệ thống ·
module (một dòng mỗi module) · **Invariants** · quy ước code · chỉ mục ADR · bảng trỏ file chi tiết.
Mọi thứ khác xuống tầng dưới. Một `ARCHITECTURE.md` 3.000 dòng là tài liệu hỏng dù nội dung đúng —
agent không đủ context để nạp nó.

---

## Procedure

### Phase 0 — Resolve mode + tier

Xác định mode theo bảng trên. Kiểm `notes/INDEX.md` và `ARCHITECTURE.md` sẵn có trước (§4) — đã có
tài liệu tươi thì nghiêng về `drift`, đừng viết đè.

Chọn tier bằng **`ask the user a focused question`, chỉ hỏi khi chưa suy ra được** từ repo:

| Tier | Dấu hiệu | Số mục |
|---|---|---|
| `demo` | Không có CI, không có test, không có auth thật, ≤ 3 người | 7 |
| `product` | Có người dùng/dữ liệu/tiền thật, có CI hoặc deploy | 16–19 |
| `platform` | Nhiều service, có SLO/on-call, team ≥ 5 | tối đa 27 |

Viết mục không thuộc tier → **bỏ hẳn**, không viết "N/A" (§3).

### Phase 1 — Thu thập nền (khác nhau theo chiều)

**Chiều ngược (`document`, `drift`):** đọc chiến lược (§6), không đọc cả repo.
Thứ tự bắt buộc, dừng khi đủ cho tier:

1. Manifest + lockfile → mục 2 (phiên bản là **bắt buộc**, không có phiên bản thì mục 2 vô giá trị)
2. `ls` thật + config alias → mục 3
3. `docker-compose.yml` / gateway config / biến env trỏ service → mục 4
4. Thư mục module + nơi mount router → mục 5
5. Schema/migration → mục 9
6. Đọc **một** đường đi thật đầu-cuối (một endpoint, một trang) → mục 6 và 11
7. Còn thiếu quan hệ phụ thuộc → `→ dùng understand-codebase mode scan`, đọc kết quả, **không tự crawl**

**Chiều xuôi (`blueprint`):** không có code để đọc, nên nền là **yêu cầu**. Chưa có danh sách
Feature → `→ dùng requirement-ladder` trước; kiến trúc chọn mà không biết cần đỡ năng lực gì là
kiến trúc đoán. Có Feature rồi thì mỗi lựa chọn stack phải chỉ ra nó phục vụ Feature nào.

### Phase 2 — Viết

Với **từng** mục thuộc tier: đọc dòng tương ứng trong `references/section-catalog.md` (cột *nguồn kiểm
chứng* và *dấu hiệu filler*), viết, rồi tự đối chiếu cột filler. Trông giống cột filler → viết lại
hoặc xóa mục.

Ba quy tắc không nhân nhượng:

- **Con số phải chép** — TTL, timeout, pool size, port, coverage. Không có nguồn thì `> Not Found`,
  không ước lượng.
- **Sơ đồ theo khuôn sẵn.** Đọc khuôn tương ứng trong `references/diagram-templates.md` (mục 4
  flowchart · 9 erDiagram · 11 sequenceDiagram · 6 request flow · 12 dependency · enum `status` →
  stateDiagram). Mọi cạnh phải mang nhãn giao thức/cổng/đường dẫn — mũi tên trần là filler.
  **Mỗi trường enum `status` trong DB phải có một `stateDiagram`**: đó là luật chuyển trạng thái,
  thứ AI vi phạm nhiều nhất khi viết code.
- **Mục Invariants viết ở thể mệnh lệnh + kèm nguồn.** Ví dụ đạt: *"Không cấp quyền dựa trên role phía
  client — mọi kiểm tra ở server (`src/middleware/authenticate.js:12`)"*. Đây là mục AI đọc nhiều nhất.

Ở `blueprint`, mỗi mục gắn **`[quyết định]`** (đã chốt, kèm ADR) hoặc **`[chưa quyết]`** (còn mở, kèm
câu hỏi cần trả lời). Cấm viết thì hiện tại như thể hệ thống đã tồn tại (§6).

### Phase 3 — Kiểm chứng bằng máy (script-offloaded, §9)

**Không tự mắt kiểm.** Chạy:

```
python "scripts/arch_check.py" --doc ARCHITECTURE.md --root .
```

Script trả JSON: đường dẫn được nhắc mà không tồn tại · biến env không xuất hiện trong code ·
dependency nêu ở Tech Stack mà không có trong manifest · vi phạm trần dòng · mục rỗng mà không có
`> Not Found` · ADR thiếu heading bắt buộc · **file bị sửa nhiều nhất trong lịch sử git**.

Bạn chỉ đọc JSON đó, **không đọc lại tài liệu**. Mọi finding phải sửa trước khi báo xong. Ở `blueprint`
chỉ chạy `--only layering,sections` (chưa có code để đối chiếu).

File churn cao là **gợi ý**, không phải kết luận: file sửa nhiều thường là chỗ kiến trúc cắt sai
đường, nhưng cũng có thể chỉ là file cấu hình. Nêu như giả thuyết kèm số commit, đừng khẳng định.

### Phase 4 — Preview (§3)

In **6–9 dòng** tiếng Việt + đường dẫn đã lưu: tier đã chọn · số mục viết được / số mục `> Not Found` ·
số ADR · kết quả `arch_check` (số finding từng loại) · rủi ro lớn nhất. **Không dump nội dung tài liệu
vào chat.**

---

## Mode `adr`

Một quyết định → một file `docs/arch/adr/<NNNN>-<slug>.md` theo mẫu ở cuối
`references/section-catalog.md`. Bắt buộc đủ: bối cảnh · quyết định · **phương án đã loại bỏ kèm lý do
cụ thể** · hệ quả chấp nhận · **điều kiện đảo ngược**.

Thiếu "phương án đã loại bỏ" thì không phải ADR, chỉ là mô tả — và mô tả thì đọc code là ra, viết làm
gì. Phần *tại sao không chọn cái kia* là thứ duy nhất AI không tự suy được.

Đổi quyết định cũ → ADR **mới** ghi `Supersedes: ADR-<n>`, đánh dấu bản cũ `Superseded by`. Append-only,
không sửa đè, không xóa.

## Mode `drift`

1. Chạy `arch_check.py` (đủ mọi check) → lấy phần kiểm được bằng máy.
2. Với mỗi Invariant và mỗi khẳng định về auth/authorization/luồng lỗi, `text search capability` code để xác nhận.
3. Trả bảng:

| Khẳng định | Doc nói | Code làm | Nguồn code | Verdict |
|---|---|---|---|---|

Verdict ∈ `khớp` / `lệch` / `doc thiếu` / `không kiểm được`.

**Không tự sửa bên nào.** Doc nói A, code làm B — một trong hai đang sai, và chọn cái nào là quyết định
sản phẩm, không phải quyết định của skill. Báo mâu thuẫn, đề xuất, chờ người dùng chốt. Sau khi chốt:
sửa doc → chạy lại Phase 3; sửa code → `→ dùng code-senior`.

---

## Vị trí trong chuỗi

```
Ý tưởng → requirement-ladder (Epic→Feature) → architect blueprint (+adr)
                                                      │
        scaffold-project (thư mục) ←──────────────────┤
                                                      ▼
       requirement-ladder (Story) → spec-writer → code-senior / build-ui / backend-engineer
                                                      │
                                                      ▼
                                          architect drift (định kỳ)
```

Epic/Feature đi **trước** kiến trúc (phải biết cần đỡ năng lực gì mới chọn được kiến trúc);
Story đi **sau** (phải biết đường nối ở đâu mới cắt story đúng chỗ).

## Gotchas

- **Trần 200 dòng là ràng buộc cứng**, không phải gợi ý. Vượt trần → đẩy nội dung xuống `docs/arch/`,
  đừng nén chữ. Tài liệu agent không nạp nổi thì không ai đọc.
- **`> Not Found` là tính năng.** Sức ép hoàn thành đủ 27 mục chính là thứ sinh ra tài liệu bịa.
- **Đừng crawl repo bằng tay.** Cần quan hệ phụ thuộc → `understand-codebase`; cần kiểm cơ học →
  `arch_check.py`. Đọc cả repo vào context là thất bại kiểu điển hình.
- **Đừng trộn hai chiều mà không phân định** (§6). Dự án nửa có code → ghi rõ ranh giới từng mục.
- **Bảo mật:** phát hiện secret thật trong config khi đọc nền → **không chép vào tài liệu**, chỉ ghi
  tên biến. `→ dùng security-review` nếu secret đã bị commit.
- **Giữ trong phạm vi (§10):**
  - `→ dùng understand-codebase cho` bản đồ symbol/import/call.
  - `→ dùng requirement-ladder cho` Epic → Feature → Story.
  - `→ dùng spec-writer cho` spec một feature cụ thể + chia task.
  - `→ dùng scaffold-project cho` tạo thư mục thật và quy trình git.
  - `→ dùng domain-modeling cho` entity/aggregate/invariant mức dữ liệu.
  - `→ dùng backend-engineer cho` hợp đồng API chi tiết; `design-web`/`build-ui` cho giao diện.
  - `→ dùng code-reviewer cho` chất lượng code; `security-review` cho audit bảo mật.


## Antigravity resource execution
Resolve relative skill/resource paths against the containing loaded file's observed location.
Before invoking a bundled command from the project working directory, resolve its entrypoint
to an absolute quoted path; resolve bundled imports/resources from their own containing file.
Do not change the working directory into the installed skill. Inputs and outputs such as
`.tmp/` and `notes/` remain relative to the current project, unless the user specifies otherwise.
Do not invent the installed location; if the host does not expose it, discover the actual file
using available file capabilities or ask for its location before running the command.
