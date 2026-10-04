---
name: "scaffold-project"
description: "Designs the folder structure AND the team git workflow for a new project, scaled to team size — asks 3 blocking questions, picks a layout profile (research | web | agent | mixed), then offloads creation to a script that writes the tree plus its governance files. Modes — plan (blueprint only, default), apply (create for real), publish (secret-scan, then create the GitHub repo via gh and invite the team, only after an explicit yes), audit (score an existing repo), onboard (regenerate the teammate guide). Triggers — thiết kế thư mục, cấu trúc dự án, dựng khung dự án, tổ chức project, scaffold project, project structure, chia thư mục, làm việc nhóm trên github, quy trình git cho nhóm, nhiều người cùng repo, repo cho N người, onboard thành viên mới, tạo repo github, đẩy lên github, push lần đầu, mời thành viên vào repo. It decides layout + collaboration policy; it does NOT write framework code (use build-ui mode scaffold) or resolve a product stack (use scaffold-course-platform)."
allowed-tools: "Read Write Edit Bash Glob Grep AskUserQuestion"
argument-hint: "<project-name | path> [plan|apply|audit|onboard]"
---

# Scaffold Project (dựng khung dự án + quy trình nhóm)

> **Source:** nguyên bản Workbench — khởi từ bài viết "Cấu trúc 4 thư mục cho mọi dự án AI"
> và phần phê bình bài đó (phiên 2026-08-01: thiếu vùng output, chồng lấn prompts/skills,
> traces sai vị trí, bảo mật bị tính điểm thay vì chặn).
> **Purpose:** Một dự án mới cần **hai** thứ cùng lúc — bố cục thư mục và quy tắc để nhiều
> người làm chung mà không giẫm chân nhau. Skill này quyết định cả hai và tạo ra file thật.

Thông báo khi bắt đầu: *"Đang dùng skill `scaffold-project` để dựng khung dự án."*

## Iron Law — ba câu hỏi cho mọi thư mục

Mỗi thư mục phải trả lời được: **(1) ai sở hữu · (2) có vào git không · (3) người hay máy
sinh ra.** Không trả lời được cả ba → **không tạo thư mục đó**.

Ba câu này không phải hình thức: (1) sinh ra `CODEOWNERS`, (2) sinh ra `.gitignore`,
(3) quyết định vùng đó cần review hay chỉ cần tái tạo được. Thư mục vô chủ thành bãi rác.

## Hard Gate — hai việc không được bỏ qua

1. **`.gitignore` được ghi TRƯỚC mọi file khác.** Script đã làm đúng thứ tự này. Lý do:
   IDE dạng agent có thể "stage all → commit → sync" trong một lệnh và không phân biệt
   file nhạy cảm.
2. **Không tạo repo / commit / push khi chưa được người dùng đồng ý bằng lời trong phiên.**
   Chỉ mode `publish` được phép, và chỉ sau khi `publish_preflight.py` trả `safe: true`
   **và** người dùng xác nhận. Mặc định `--private`. Public phải xác nhận **lần thứ hai**,
   riêng biệt — đẩy repo public là hành vi công bố, có thể bị index và cache dù sau xóa.

## Conventions

Binding: `~/.claude/rules/workbench-conventions.md` — song ngữ §1 (prose tiếng Việt, tên
file/định danh tiếng Anh), preview-not-dump §3, script-offloading §9. **Đọc lúc chạy, không
inline.** Tri thức nặng nằm ở `references/`, danh sách thư mục nằm ở `scripts/profiles.json`.

## Modes

| Mode | Dùng khi | Output |
|---|---|---|
| `plan` (mặc định) | Trước khi tạo bất cứ gì | `notes/project-structure.md` + preview 6–9 dòng. **Không tạo thư mục** |
| `apply` | Blueprint đã chốt | Thư mục + file quản trị thật, qua script |
| `publish` | Khung đã tạo, muốn lên GitHub | Quét bí mật → xin xác nhận → tạo repo, mời người, bật bảo vệ nhánh |
| `audit` | Repo đã có, muốn chấm | Bảng pass/fail theo `references/team-workflow.md` §7 |
| `onboard` | Có người mới vào nhóm | Sinh lại `CONTRIBUTING.md` + checklist ngày đầu |

## Procedure

### Phase 0 — Resolve
Từ `$ARGUMENTS` lấy tên dự án / đường dẫn và mode. Đường dẫn tồn tại và đã có file →
nghiêng về `audit` trước, đừng đổ khung đè lên. Không rõ → hỏi một câu.

### Phase 1 — Ba câu hỏi chặn (BẮT BUỘC, không đoán)
Dùng `AskUserQuestion`. Chỉ hỏi những câu mà **câu trả lời làm đổi kết quả**:

1. **Sản phẩm cuối là gì?** → hồ sơ (`research` | `web` | `agent` | `mixed`).
   Phân vân giữa hai → `mixed`.
2. **Bao nhiêu người, repo public hay private?** → bật/tắt CODEOWNERS, branch protection,
   mức cảnh báo bảo mật. Ngưỡng chuyển sang "hệ thống" là **4 người**, không phải 8.
3. **Một repo chung hay tách nhiều repo?** → monorepo là mặc định cho ≤8 người; tách repo
   chỉ khi các phần có chu kỳ phát hành thật sự độc lập.

Suy ra được thì đừng hỏi. Người dùng không trả lời → ghi rõ giả định vào blueprint.

### Phase 2 — Chọn hồ sơ + chia sở hữu
Đọc `references/layout-profiles.md` (§1 chọn hồ sơ, §3 vì sao track/ignore) và
`references/team-workflow.md` (§1 bật cơ chế theo quy mô, §2 cắt vùng sở hữu).

Nguyên tắc chia người quan trọng nhất: **cắt theo thư mục/tính năng, không cắt theo lớp
kỹ thuật**. Chia "một người frontend, một người backend" khiến mọi PR đều cần cả hai duyệt.

### Phase 3 — Blueprint (mode `plan` dừng ở đây)
Ghi `notes/project-structure.md`: cây thư mục · bảng ba câu hỏi cho từng vùng · bảng phân
công sở hữu · quy trình nhánh/PR theo quy mô · những gì **cố ý** không vào git kèm lý do.
In ra chat **6–9 dòng** + đường dẫn. Không dán cây thư mục đầy đủ vào chat.

### Phase 4 — Apply (script-offloaded, §9)
Viết spec rồi gọi script. **Không tự tay viết `.gitignore`, `CODEOWNERS`, `CONTRIBUTING`,
PR template, `.env.example`, `manifest.md`** — script sở hữu toàn bộ boilerplate đó.

```
python "<skills>/scaffold-project/scripts/scaffold_project.py" .tmp/scaffold_<slug>.json [--dry-run]
```

Spec (chỉ những khóa này):
```json
{"project_name":"aion-lab","profile":"mixed","root":".","team_size":8,
 "visibility":"private","default_branch":"main",
 "owners":{"apps/web":"@linh @nam"},"extra_dirs":[],"extra_ignore":[]}
```

Script trả JSON `{created, skipped, dirs, warnings, next}`. Nó **idempotent**: file đã có
thì báo `skipped`, không bao giờ ghi đè. `.gitignore` đã có thì chỉ nối thêm dòng thiếu.
Chạy `--dry-run` trước khi apply lên thư mục đã có nội dung.

**Script tự chèn sẵn** (đừng viết lại): cây thư mục theo hồ sơ · `.gitignore` (chung +
theo hồ sơ) · `README.md` kèm bảng bản đồ thư mục · `CONTRIBUTING.md` tiếng Việt co giãn
theo quy mô · `.env.example` · `.github/pull_request_template.md` · `.github/CODEOWNERS`
(khi ≥4 người) · `manifest.md` trong mọi vùng dữ liệu thô.

### Phase 5 — Bàn giao
In: 3–5 bước tiếp theo từ `report.next`, cảnh báo còn `@TODO-` trong CODEOWNERS. Hỏi người
dùng có muốn chạy tiếp mode `publish` không — **không tự chuyển sang Phase 6**.

### Phase 6 — Publish (mode `publish`, có rào chắn)

**6.1 Quét bắt buộc.** Không có bước này thì không có bước sau:
```
python "<skills>/scaffold-project/scripts/publish_preflight.py" --root .
```
Script chỉ đọc: nó chạy `git init` cục bộ (không commit, không kết nối mạng) rồi liệt kê
file git **sẽ** thêm, đối chiếu với danh sách tên file bí mật, chữ ký khóa trong nội dung
(`sk-ant-`, `AKIA…`, `gho_`, khối PRIVATE KEY…), kích thước, và notebook còn nhúng output.
Exit `2` = có blocker → **dừng hẳn**, báo từng blocker kèm cách xử lý. Exit `0` = đi tiếp.

**6.2 Xin xác nhận.** Trình bày đúng bốn con số rồi hỏi: **tên repo · private hay public ·
số file · tổng dung lượng**. Chờ câu trả lời rõ ràng. Public → hỏi lại lần hai, riêng.

**6.3 Thực thi** (chạy từng lệnh, hiện rõ trong transcript, không giấu trong script):
```
git add -A && git commit -m "chore: scaffold project structure"
```
```
gh repo create <name> --private --source=. --remote=origin --push
```

**6.4 Sau khi có repo** — hỏi username GitHub của từng người rồi mời:
```
gh api -X PUT repos/<owner>/<repo>/collaborators/<username> -f permission=push
```
Nhóm ≥4 người thì bật bảo vệ nhánh bằng `gh api -X PUT
repos/<owner>/<repo>/branches/<branch>/protection --input <file>.json` với payload
`{"required_status_checks":null,"enforce_admins":false,
"required_pull_request_reviews":{"required_approving_review_count":1},"restrictions":null}`.
**Nếu trả về 403:** gói tài khoản không cho bảo vệ nhánh trên repo private — báo thẳng,
đưa hai lựa chọn (chuyển public, hoặc dựa vào CODEOWNERS + quy ước) chứ đừng im lặng bỏ qua.

### Mode `audit`
Chạy checklist `references/team-workflow.md` §7. Mục 1–2 (`.env` bị lộ, bí mật đã commit)
là **cổng chặn** — fail thì báo trước mọi thứ khác, kèm thứ tự xử lý sự cố (§6: **hủy khóa
cũ trước**, viết lại lịch sử chỉ là bước phụ). Không tự sửa; báo phát hiện + lệnh khắc phục.

## Rules

| Quy tắc | Chi tiết |
|---|---|
| Nhị phân không vào git | PDF, xlsx, checkpoint, ảnh lớn → storage ngoài + `manifest.md` |
| `data/raw/*` chứ không `data/raw/` | Git không re-include được file nếu thư mục cha bị loại trừ; `!data/raw/manifest.md` sẽ vô hiệu. Đã kiểm chứng bằng `git check-ignore` |
| Output AI tách khỏi `data/` | Trộn vào là vòng sau AI đọc lại chính output của nó |
| `traces` là log, không phải test | `.runs/` (ignore), tách khỏi `evals/tests/` (viết tay, track) |
| Bảo mật là cổng, không phải điểm | Rò rỉ / bịa nguồn / sai định dạng bắt buộc = **fail thẳng**. Tính 5/100 điểm nghĩa là agent làm lộ dữ liệu vẫn đạt 95 và được duyệt |
| Một chủ sở hữu cho mỗi vùng | Nhiều vùng một người thì được; vùng vô chủ thì không |
| Tên file tiếng Anh | Theo conventions §1 — prose tiếng Việt, định danh tiếng Anh |

## Anti-patterns

| Ngụy biện | Thực tế |
|---|---|
| "Tạo `.gitignore` sau cũng được" | Agent stage-all commit `.env` trước đó. Đã push là phải hủy khóa, không xóa được khỏi lịch sử |
| "Cứ commit `data/raw` cho tiện, sau xóa" | Nhị phân nằm vĩnh viễn trong lịch sử; clone chậm mãi mãi; GitHub chặn >100MB |
| "Nhóm nhỏ chưa cần PR" | Ngưỡng là 4 người. Bật muộn thì phải sửa thói quen đã hình thành |
| "Chia frontend/backend cho gọn" | Mọi tính năng chạm cả hai → mọi PR cần cả hai duyệt → tắc |
| "Cứ commit thẳng `main` cho nhanh" | Mất khả năng review, và không rollback được từng thay đổi |
| "Đổ khung đè lên repo cũ cho sạch" | Chạy `audit` + `--dry-run` trước. Script không ghi đè, nhưng người thì có thể |
| "Prompt để cả `prompts/` lẫn `agents/skills/`" | Hai bản, sửa một bản, trôi lệch. Chia theo **cơ chế gọi** (`references/layout-profiles.md` §4) |
| "Có eval là đủ, chấm tay cũng được" | Chấm tay thì không ai chạy lại lần hai. Tách `tests/auto` (script chấm) và `tests/judge` |
| "Người dùng bảo dựng repo tức là cho phép push luôn" | Không. Tạo repo và push là hành vi hướng ra ngoài — xin xác nhận riêng ở 6.2, mỗi lần |
| "Preflight cảnh báo thôi, cứ push rồi sửa sau" | Blocker là **dừng hẳn**. Khóa đã push thì phải hủy khóa, xóa file không cứu được |
| "Để public cho tiện chia sẻ" | Public là công bố, có thể bị index/cache dù sau xóa. Mặc định private; public cần xác nhận lần hai |
| "Bật bảo vệ nhánh thất bại thì thôi bỏ qua" | Báo thẳng lỗi 403 và đưa lựa chọn. Im lặng bỏ qua khiến nhóm tưởng đang được bảo vệ |

## Integration

- `admin` → người gọi chính (nhánh 2: đúng một skill phủ được).
- `design-web` → sau khi có khung, quyết định giao diện; design-record ghi vào `design/`.
- `build-ui` mode `scaffold` → dựng code framework **bên trong** `apps/web` đã có.
- `scaffold-course-platform` → chọn stack sản phẩm; skill này chỉ lo bố cục + quy trình.
- `security-review` → chạy sau `audit` nếu phát hiện bí mật đã commit.
- `artifact-manager` → ghi blueprint vào `notes/INDEX.md`.
