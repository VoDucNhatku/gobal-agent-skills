# Đánh giá bộ skill GOBAL — ngữ cảnh nghiên cứu flow xây dựng web (ReNER-VN, 09–15/10/2026)

**Ngày:** 15/10/2026 · **Phạm vi:** `.claude/skills` trong repo `gobal-agent-skills` (commit `f5f653a` + 17 thay đổi chưa commit của phiên khác), bản cài `~/.claude/skills`, settings người dùng, các cơ chế liên quan của Claude Code · **Người viết:** một phiên Claude Code làm dự án TMG301/ReNER-VN.

> **Ngữ cảnh của báo cáo này:** đánh giá được rút ra trong lúc **nghiên cứu flow xây dựng và vận hành một web thật** (đồ án ReNER-VN: web app + extension Chrome + pipeline NLP), gồm: nghiên cứu cách tổ chức repo web từ KusShoes và các repo mẫu, kiến trúc frontend/backend/worker, luồng dữ liệu từ extension tới thống kê, quy chuẩn giao việc cho AI, đặc tả sản phẩm và dựng repo làm việc trên GitHub. Vì vậy báo cáo nhìn bộ skill **từ góc độ làm web/sản phẩm có AI hỗ trợ**: những skill như `design-web`, `build-ui`, `backend-engineer`, `fullstack-builder`, `spec-writer`, `scaffold-project`, `admin` được xét kỹ; các skill nghiên cứu paper, LaTeX, học tập chỉ được xét ở mức cấu trúc và tần suất xuất hiện. Khi gộp với báo cáo từ ngữ cảnh khác (nghiên cứu paper thuần, code ML, học tập), cần đọc kết luận của file này **trong phạm vi flow web**.

**Dùng file này thế nào:** đây là **một trong nhiều báo cáo** sẽ được gộp để thiết kế lại bộ skill. Mỗi phát hiện có mã `F-xx`, mỗi đề xuất có mã `R-xx`, để các báo cáo khác dẫn chiếu và so sánh. Mỗi nhận định gắn một nhãn độ chắc:

| Nhãn | Nghĩa |
|---|---|
| **ĐO** | Đo trực tiếp bằng lệnh/script trong phiên này; có lệnh hoặc số liệu |
| **NGUỒN** | Đọc trực tiếp từ tài liệu chính thức hoặc bài báo (có link, có phiên bản) |
| **QUAN SÁT** | Thấy trong phiên làm việc này, một lần, chưa lặp lại để khẳng định |
| **SUY LUẬN** | Kết luận rút ra từ các điều trên; chưa kiểm chứng riêng |
| **CHƯA KIỂM** | Nghi vấn, cần kiểm trước khi hành động |

Mục 6 liệt kê **các nhận định sai mà phiên này đã nói rồi rút lại**. Khi gộp báo cáo, đừng lấy lại các nhận định đó từ lịch sử chat.

---

## 0. Vì sao có file này

**Chuyện gì xảy ra trước đó.** Sau 6 ngày dùng bộ skill để nghiên cứu flow web cho ReNER-VN, chủ bộ skill hỏi: "bộ skill hiện tại nên cập nhật và thay đổi thế nào cho hiện đại và quy chuẩn hơn?". Câu trả lời đầu tiên trong chat có 4 nhận định sai (mục 6). Chủ bộ skill phản biện và yêu cầu "suy nghĩ nghiêm túc hơn". Phiên này đã mở lại nguồn gốc, đo lại bộ skill và ghi kết quả vào file thay vì để trong chat.

**File này dùng để làm gì.**

1. **Lưu đánh giá có bằng chứng**, tách khỏi lịch sử chat (chat dễ mất, dễ lẫn nhận định đã rút lại).
2. **Làm một đầu vào** cho việc thiết kế lại bộ skill. Chủ bộ skill sẽ gom báo cáo từ nhiều phiên làm việc ở các ngữ cảnh khác nhau (web, nghiên cứu paper, code ML, học tập), so các phát hiện trùng nhau hoặc mâu thuẫn, rồi mới quyết sửa gì.
3. **Giữ một nơi để bổ sung dần**: các phiên sau có thêm quan sát trong ngữ cảnh flow web thì ghi tiếp vào đây theo cách ở mục 0.1, không tạo file rời.

**File này không phải:** kế hoạch đã được duyệt, hay lệnh sửa skill. Chưa skill nào bị sửa dựa trên file này.

## 0.1 Cách đóng góp vào file này

Áp dụng cho người hoặc phiên AI làm việc trong **ngữ cảnh flow web/sản phẩm**. Ngữ cảnh khác thì viết báo cáo riêng theo cùng khuôn, rồi gộp ở bước sau.

### Quy tắc chung

- **Thêm, không xóa.** Không sửa lời của mục cũ. Nếu một phát hiện sai hoặc lỗi thời, ghi vào mục 6 (nhận định đã rút lại) và thêm một dòng `Cập nhật <ngày>:` ngay dưới phát hiện đó.
- **Mã tiếp nối.** Phát hiện mới lấy mã `F-17`, `F-18`…; đề xuất mới `R-15`… Không dùng lại mã đã có.
- **Mỗi nhận định một nhãn độ chắc** (bảng ở đầu file). Không có bằng chứng thì ghi `CHƯA KIỂM`, không viết như sự thật.
- **Ghi rõ phiên/ngày/model** của người đóng góp trong nhật ký (cuối file).
- **Không dán dữ liệu cá nhân hay khóa** (memory cá nhân, token, đường dẫn chứa thông tin riêng) vào file.

### Khuôn một phát hiện mới

```markdown
### F-xx — <tên ngắn, nói thẳng vấn đề> · <NHÃN>

**Ngữ cảnh:** <đang làm việc gì, loại dự án, phiên/ngày>
**Thấy gì:** <hiện tượng cụ thể; skill nào; lệnh/đoạn văn nào>
**Bằng chứng:** <lệnh + kết quả / đường dẫn file:dòng / link tài liệu + phiên bản / trích log>
**Tác động:** <ảnh hưởng tới kết quả công việc như thế nào; mức độ>
**Không chắc ở đâu:** <điều chưa kiểm, cách kiểm>
**Liên quan:** <F-xx, R-xx khác>
```

### Khuôn một đề xuất mới

```markdown
| R-xx | <đề xuất> | <F-xx giải quyết> | <công sức: rất thấp/thấp/trung bình/cao> | <kiểm bằng gì để biết có hiệu quả> |
```

### Nên ghi những gì

| Loại quan sát | Ví dụ cần ghi | Vì sao đáng ghi |
|---|---|---|
| Skill **lẽ ra nên được dùng nhưng không được dùng** | Dựng repo đặc tả mà không ai gọi `spec-writer` | Dấu hiệu description mất hoặc định tuyến sai (F-01, F-02) |
| Skill **được gọi nhưng làm sai/thiếu** | Skill tạo cây thư mục không hợp dự án | Cho biết nội dung skill cần sửa chỗ nào |
| Skill **được gọi khi không nên** | Skill deploy tự chạy khi chỉ hỏi kiến thức | Cần `disable-model-invocation` hoặc description hẹp hơn |
| **Quy tắc bị bỏ qua** | Nói "xong" khi chưa chạy kiểm; thêm co-author trái memory | Ứng viên chuyển sang hook (F-04) |
| **Việc lặp lại không có skill nào phủ** | Viết đặc tả extension để bàn giao | Ứng viên skill mới (F-09) |
| **Nhận định sai của AI rồi phải rút lại** | Dẫn số liệu từ bản cũ của bài báo | Vào mục 6; bài học cho rule |
| **Số liệu harness** | Kết quả `/skill-doctor`, `/context`, `/doctor` | Căn cứ mạnh nhất để quyết giữ/bỏ/gộp |
| **So sánh có/không skill** | Cùng một task, lần có skill và lần không | Đo giá trị thật của skill (F-13) |

### Không nên ghi

- Cảm nhận chung chung không có ví dụ ("skill này hơi dài").
- Nội dung đã có ở mục khác; dẫn chiếu mã thay vì chép lại.
- Đề xuất công nghệ chỉ vì nhiều star hoặc đang thịnh hành, khi chưa gắn với một phát hiện cụ thể.

## 0.2 Cách nghiên cứu để có ghi chép chi tiết

Phần này hướng dẫn **thu bằng chứng** trong lúc làm việc thật, để phát hiện có độ chắc `ĐO`/`QUAN SÁT` thay vì `SUY LUẬN`.

### Trong lúc làm một việc

1. **Trước khi bắt đầu**, ghi một dòng: việc gì, ngữ cảnh gì, theo bạn skill nào nên được dùng.
2. **Trong lúc làm**, mỗi khi AI chọn skill hoặc tự làm, ghi: skill được gọi (nếu có), skill đã cân nhắc, lý do. Có thể yêu cầu AI tự nêu điều này ở cuối mỗi lượt.
3. **Khi có lỗi**, ghi ngay: lỗi gì, ai phát hiện (người, test, AI tự thấy), quy tắc/skill nào lẽ ra phải chặn.
4. **Sau khi xong**, so dòng đầu với thực tế: skill dự kiến có được dùng không; nếu không thì vì sao.

### Đo bằng công cụ của Claude Code

| Lệnh | Cho biết | Ghi vào đâu |
|---|---|---|
| `/skill-doctor` | Chi phí ngữ cảnh và tần suất dùng từng skill | Mục 3.1 hoặc phát hiện mới; kèm ngày, model |
| `/context` | Kích thước danh sách skill sau ngân sách | Mục 3.1 |
| `/doctor` | Ước tính chi phí danh sách và các phần lớn nhất | Mục 3.1 |
| `claude --debug` | Cảnh báo khi danh sách skill vượt ngân sách | F-01 |
| `claude plugin validate .claude/skills` | Frontmatter có parse được không | Mục 3.1 |
| Validator của repo (`test-framework/scripts/test_skills.py`) | Lỗi cấu trúc theo chuẩn GOBAL | Mục 3.1 |

### Thí nghiệm nhỏ để đo giá trị một skill

Áp dụng khi muốn chứng minh một skill có ích hay không (F-13):

1. Chọn **3–5 task thật** trong ngữ cảnh web, có cách kiểm đạt/không đạt rõ ràng (ví dụ: "viết đặc tả API cho màn Tìm trọ, phải có mã lỗi và phân quyền").
2. Chạy mỗi task **hai lần trong phiên mới**: một lần cho phép skill, một lần tắt skill đó (`skillOverrides: "off"`).
3. Chấm cùng tiêu chí đã viết **trước** khi chạy. Ghi thời gian, số lượt sửa, lỗi còn lại.
4. Ghi kết quả thành phát hiện mới với nhãn `ĐO`, kèm task, tiêu chí, kết quả từng lần.
5. Một vài task chỉ là tín hiệu ban đầu, chưa đủ để kết luận chung; ghi rõ cỡ mẫu.

### Thu bằng chứng từ dự án đã làm

- `WORK_LOG.md`, `notes/INDEX.md` của dự án: tìm các chỗ ghi "dùng skill X", "làm trực tiếp", "đính chính".
- Lịch sử git: commit sửa lỗi do AI gây ra; PR bị trả lại.
- Báo cáo audit (nếu có): lỗi nào do thiếu quy tắc trong skill.

---

## 1. Tóm tắt

1. **Nền tốt, nên giữ:** kỷ luật bằng chứng (`evidence-first`, NOT RUN), `design-web`/`build-ui` xoay quanh kiểm chứng thật, validator cấu trúc pass 100%, chính sách song ngữ. Nghiên cứu độc lập (SkillsBench) cho thấy skill **được tuyển chọn** giúp agent làm đúng nhiều hơn; bộ này thuộc loại đó (F-16).
2. **Vấn đề lớn nhất không phải "nhiều skill tốn token" mà là "skill bị mất description nên không được chọn".** Claude Code giới hạn danh sách skill ở khoảng 1% cửa sổ ngữ cảnh; vượt thì bỏ description của skill ít dùng. Trong phiên này, **37 skill của bộ chỉ hiện tên/tiêu đề, không có mô tả khi nào dùng**, gồm cả `design-web`, `spec-writer`, `security-review`, `verification-before-completion` (F-01).
3. `admin` chọn worker **dựa đúng vào danh sách đó**, nên các skill mất description gần như vô hình với admin (F-02). Trong phiên này, 4 lần gọi `/admin` đều tự làm, không gọi worker, kể cả khi việc khớp skill (F-02, QUAN SÁT).
4. **Quy tắc bắt buộc đang chỉ là chữ.** Không có hook, không có subagent, không skill nào dùng `disable-model-invocation` hay `paths` (F-04 đến F-06).
5. **Thiếu một số năng lực đã cần thật:** biến proposal thành repo làm việc (F-09), quy tắc khi một tài liệu có nhiều phiên bản (F-10), chuẩn đầu ra cho dự án web (F-11).
6. **Nhóm skill trí nhớ:** `project-memory` và `learnings-db` chưa từng tạo thư mục lưu trữ trong hai workspace đã quét; auto memory của Claude Code đang dùng thật. Không nên thay skill bằng auto memory, vì auto memory không chia sẻ qua git (F-12).
7. **Gần như chưa có eval hành vi** (1 bộ), nên chưa đo được skill có giúp hay không (F-13).
8. **Ba bản sao + bản Antigravity, 17 thay đổi chưa commit:** dễ lệch (F-14).

---

## 2. Bối cảnh: đánh giá này dựa trên công việc nào

Từ 09 đến 15/10/2026, các phiên Claude Code (VS Code, model Opus/Fable) làm đồ án TMG301 đề tài 8 (ReNER-VN: trích xuất giá thuê trọ từ bài Facebook) với bộ skill này:

| Việc | Đầu ra | Skill liên quan lẽ ra dùng | Thực tế |
|---|---|---|---|
| Đọc proposal, nghiên cứu nền, phản biện | `notes/` trong TMG301, audit 13 lỗi | paper-read, hallucination-guard, ieee-q1-devil-advocate | Một số phiên dùng (ghi trong log); phiên này làm trực tiếp |
| Khảo sát KusShoes + 10 repo + 8 repo | Sổ kiến thức, thiết kế v0.2 | understand-codebase, domain-modeling | Làm trực tiếp |
| Quy chuẩn prompt giao việc cho AI | `PROMPT-KIEN-TRUC-GIAO-VIEC-AI.md` (v1.2 sau phản biện) | spec-writer, writing-plans | Làm trực tiếp |
| Repo làm việc `VoDucNhatku/rener-vn` | 56 file: đặc tả sản phẩm, dữ liệu, API, CSDL, extension, đánh giá, 6 ADR, JSON Schema, 7 fixture, 16 issue | spec-writer, scaffold-project, domain-modeling | Làm trực tiếp; không skill nào phủ trọn việc này |
| Repo handbook nghiên cứu | 198 file, 4 issue | scaffold-project (publish) | Một phiên khác dùng; ghi trong log L0–L5 |

Đây là góc nhìn từ **một loại dự án** (đồ án học thuật có phần web + NLP). Các báo cáo khác nên bổ sung góc nhìn từ dự án nghiên cứu thuần, code thuần, học tập.

---

## 3. Hiện trạng đo được

### 3.1 Số liệu tổng (ĐO)

| Chỉ số | Giá trị | Cách đo |
|---|---|---|
| Thư mục skill có `SKILL.md` hợp lệ | 69 (71 thư mục, gồm cả file phụ) | Validator + script kiểm kê (phụ lục A) |
| Skill là alias "DEPRECATED" | 7: `build-ui-component`, `design-ui-direction`, `latex-math-renderer`, `reuse-checker`, `skill-router`, `web-admin`, `workbench-admin` | Description bắt đầu bằng `DEPRECATED` |
| Tổng ký tự description | 34.475 ký tự (giá trị YAML); 37.440 nếu tính cả dòng `description:` | Script + `grep` |
| Description dài nhất | `backend-engineer` 1.020, `security-review` 1.012, `code-senior` 1.004 | Phụ lục A |
| Tổng dòng thân SKILL.md | 8.443 | Phụ lục A |
| Skill có `scripts/` / `references/` | 9 / 16 | Phụ lục A |
| Validator cấu trúc (canonical) | 69 skill, 0 FAIL, 0 WARN, 100% | `test_skills.py --host canonical` ngày 15/10 |
| Skill dùng `paths:` hoặc `disable-model-invocation:` | 0 | `grep` frontmatter |
| Hook trong settings người dùng/dự án | 0 | `~/.claude/settings.json` chỉ có `model`, `effortLevel`, `modelSettings` |
| `skillOverrides`, `skillListingBudgetFraction` | Chưa đặt | Như trên |
| Subagent tùy chỉnh (`.claude/agents/`, `~/.claude/agents/`) | 0 | `ls` |
| Bộ eval hành vi | 1 (`evals/admin-research`) | `ls evals` |
| Thay đổi chưa commit trong repo | 17 file (của phiên Antigravity khác) | `git status --short` |
| `plugin.json` | Schema Antigravity; chưa có manifest plugin Claude Code | Đọc file |

### 3.2 Ba nơi chứa skill (ĐO)

| Nơi | Vai trò | Tình trạng |
|---|---|---|
| `gobal-agent-skills/.claude/skills/` | Nguồn | Có thay đổi chưa commit |
| `gobal-agent-skills/skills/` | Bản phân phối Antigravity (sinh bằng script) | Khác nguồn ở frontmatter và đoạn "Antigravity resource execution" |
| `~/.claude/skills/` | Bản đang chạy | Khớp nguồn về nội dung; khác cách quote frontmatter; có thêm thư mục `synced/` và 2 symlink sang `~/.codex/skills` (`latex-fix`, `study-forge`) |

**Cập nhật 15/10/2026 (phiên NCKH, ĐO):** so sánh phần thân SKILL.md giữa `~/.claude/skills` và repo HEAD `f5f653a`, bỏ frontmatter và ký tự CR:

- 55/69 skill giống nhau.
- **14/69 skill khác nhau**, trong đó có `admin`, `research-admin`, `hallucination-guard` và `self-evaluator`.
- Bản cài có ngày sửa 08/09/2026.
- `~/.claude/rules` không có `evidence-first.md`.

Vì vậy câu "Khớp nguồn về nội dung" ở bảng trên không đúng với 14 skill này. Chi tiết ở F-17.

### 3.3 Nhóm skill trí nhớ dùng thực tế ra sao (ĐO, phạm vi quét có hạn)

Quét hai workspace (`d:\Lich cong viec`, thư mục kế hoạch kì 5), sâu 6 cấp:

| Cơ chế | Nơi lưu | Dùng thực tế |
|---|---|---|
| `project-memory` (skill) | `project-memory/` gồm context, decisions, preferences, known-issues, progress | **Không tìm thấy thư mục nào** |
| `learnings-db` (skill) | `learnings-db/` gồm successes, failures, corrections, by-domain | **Không tìm thấy** |
| `audit-log` (skill) | `notes/audit-log.md` | 1 file, 2 mục (09/10) |
| `artifact-manager` (skill) | `notes/INDEX.md` | Được dùng như quy ước; các phiên cập nhật INDEX bằng tay |
| WORK_LOG tự đặt | `notes/kusshoes-to-rener-vn/WORK_LOG.md` | Dùng liên tục, các lượt C0 → M3 |
| Auto memory của Claude Code | `~/.claude/projects/d--Lich-cong-viec/memory/` | 10 file, 9 mục index, cập nhật nhiều lần |

---

## 4. Cơ chế Claude Code liên quan (NGUỒN, đọc ngày 14–15/10/2026)

| Cơ chế | Nội dung trích/tóm tắt | Nguồn |
|---|---|---|
| Danh sách skill | "skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked" | [Skills](https://code.claude.com/docs/en/skills) |
| Ngân sách danh sách | Danh sách luôn có mọi **tên**; nhiều skill thì "drops some descriptions to fit the listing's character budget". Ngân sách "scales at 1% of the model's context window"; bỏ description "starting with the skills you invoke least" | Skills — *Skill descriptions are cut short* |
| Giới hạn mỗi skill | `description` + `when_to_use` bị cắt ở 1.536 ký tự trong danh sách; nên đặt tình huống dùng chính lên đầu | Skills — frontmatter |
| Công cụ đo | `/doctor` ước tính chi phí danh sách; `/skill-doctor` xem chi phí và tần suất dùng từng skill; `/context` hiện kích thước danh sách sau ngân sách | Skills |
| Điều chỉnh | `skillListingBudgetFraction` (ví dụ 0.02), `skillOverrides` với `"name-only"` / `"off"`, `skillListingMaxDescChars` | Skills |
| `disable-model-invocation: true` | Claude không tự gọi; chỉ chạy khi người dùng gõ `/tên`. Dùng cho quy trình có tác dụng phụ | Skills; [Best practices](https://code.claude.com/docs/en/best-practices) |
| `paths:` | Glob giới hạn khi nào skill tự kích hoạt | Skills |
| Quy tắc phải luôn đúng | "Claude skipped a rule that must hold every time: move the rule into a hook." Hook có thể khai báo trong frontmatter `hooks` của skill | Skills — *Troubleshooting*; [Hooks](https://code.claude.com/docs/en/hooks) |
| CLAUDE.md | Khuyên dưới 200 dòng mỗi file; là ngữ cảnh, không phải cấu hình bắt buộc; Claude có thể đọc `AGENTS.md` thay `CLAUDE.md` | [Memory](https://code.claude.com/docs/en/memory) |
| Auto memory | Claude tự ghi; lưu ở `~/.claude/projects/<project>/memory/`; nạp mỗi phiên (200 dòng đầu hoặc 25 KB); theo repository, dùng chung giữa các worktree; **nằm trên máy, không trong repo** | Memory |
| Dự án lớn | CLAUDE.md theo thư mục, skill theo thư mục, đóng gói quy ước dùng chung thành plugin | [Large codebases](https://code.claude.com/docs/en/large-codebases) |
| Eval skill | Viết eval với grader `tool_used: Skill`, chạy `claude plugin eval`; `claude plugin validate .claude/skills` kiểm frontmatter | Skills — *Skill not triggering* |
| Chuẩn mở | Agent Skills (SKILL.md) do Anthropic phát triển, công bố chuẩn mở tại agentskills.io; nhiều công cụ khác hỗ trợ (số lượng chính xác khác nhau giữa các nguồn) | [agentskills.io](https://agentskills.io/) |
| Hiệu quả skill | SkillsBench **bản hiện tại**: 87 tác vụ, 18 cấu hình; skill tuyển chọn nâng tỉ lệ đạt từ 33,9% lên 50,5% (+16,6 điểm %), dao động +4,1 đến +25,7 theo cấu hình; skill tập trung tối đa 3 phần tốt hơn bộ lớn. **Bản v1** (khác số): 86 tác vụ, 7 cấu hình, +16,2 điểm, và có điều kiện "self-generated Skills" không giúp trung bình | [arXiv 2602.12670](https://arxiv.org/abs/2602.12670), [v1](https://arxiv.org/abs/2602.12670v1) |
| Rủi ro skill bên thứ ba | Snyk quét 3.984 skill từ ClawHub/skills.sh, báo 13,4% có lỗi mức nghiêm trọng (báo cáo của hãng, chưa bình duyệt) | [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub) |

---

## 5. Phát hiện

### F-01 — Một nửa bộ skill mất description trong danh sách · QUAN SÁT + NGUỒN

Trong danh sách skill phiên này nhận được, **37 skill của bộ** chỉ hiện tên hoặc dòng tiêu đề, không có câu "dùng khi nào" (phụ lục B). Một số skill quan trọng nằm trong đó: `design-web`, `spec-writer`, `security-review`, `verification-before-completion`, `research-admin`, `writing-plans`, `tdd-enforcer`, `fullstack-builder`. Theo docs, Claude Code bỏ description của skill ít được gọi nhất trước, nên danh sách này phản ánh **tần suất dùng** theo thống kê của Claude Code.

**Tác động:** skill mất description thì Claude khó nhận ra nó hợp với yêu cầu, dù tên đúng. Số 37 là của một phiên với cửa sổ ngữ cảnh 1M token; phiên có cửa sổ nhỏ hơn sẽ có ngân sách nhỏ hơn. **CHƯA KIỂM:** con số trên `/skill-doctor`.

### F-02 — `admin` định tuyến dựa vào chính danh sách bị cắt · NGUỒN + QUAN SÁT

`admin/SKILL.md` ghi: không liệt kê worker vì "description của cả 66 skill đã nằm sẵn trong context". Giả định này đúng khi danh sách đủ ngân sách; sai với F-01.

Quan sát thêm: trong phiên này, 4 lần gọi `/admin` (quy chuẩn prompt + skill; tạo repo `rener-vn`; nhận xét bộ skill; câu hỏi về skill/memory) đều tự làm, không gọi worker, kể cả khi việc khớp skill (dựng repo đặc tả ↔ `spec-writer`/`scaffold-project`). Các phiên khác có gọi worker: log J0 (11/10) ghi dùng `admin` cùng `hallucination-guard`. Nguyên nhân chưa rõ: có thể do F-01, do nhánh 1 được đặt làm mặc định, hoặc do việc không khớp trọn skill nào. **CHƯA KIỂM**.

### F-03 — 7 alias deprecated vẫn chiếm danh sách · ĐO

Chúng được giữ có chủ đích để tham chiếu cũ không gãy (README repo nói rõ). Đổi lại, mỗi alias chiếm một dòng tên và có thể đẩy description của skill thật ra khỏi ngân sách. Cách thay: bảng chuyển hướng trong README, hoặc `skillOverrides: "off"`.

### F-04 — Quy tắc bắt buộc chỉ nằm trong văn bản · ĐO + QUAN SÁT

Không có hook. Ví dụ trong đợt này:
- **Lỗi phán đoán:** `evidence-first` đã có, nhưng phiên này vẫn ghi "proposal v1.3 **đã nộp**" khi chưa kiểm (sửa ở PR #17 repo `rener-vn`). Hook **không** bắt được loại lỗi này; cần quy tắc rõ hơn (F-10) và reviewer độc lập.
- **Quy tắc máy móc:** memory người dùng "không thêm Co-Authored-By Claude" xung đột với nhắc nhở hệ thống yêu cầu thêm trailer. Phiên này tuân memory vì đọc được nó. Một hook `commit-msg`/PreToolUse sẽ **bảo đảm** điều đó.

Các quy tắc máy móc khác hợp với hook: không commit `.env`/khóa, chạy lệnh verify trước khi kết thúc lượt (Stop hook), chặn lệnh phá hủy.

### F-05 — Skill có tác dụng ra bên ngoài vẫn để model tự gọi · ĐO

`scaffold-project` (mode `publish` tạo repo GitHub, mời người), `deploy-admin`, `rollback-manager`, `finishing-a-development-branch`, `run-on-modal` (tốn chi phí GPU) không có `disable-model-invocation`. Bản thân skill có cổng hỏi "yes", nhưng cơ chế harness mạnh hơn và còn giải phóng chỗ trong danh sách.

### F-06 — Chưa giới hạn skill theo loại file · ĐO

`latex-fix` (math trong `notes/*.md`), `build-ui` (thư mục frontend), `paper-*` (khi có `papers/`) có thể dùng `paths:` để chỉ tự kích hoạt đúng ngữ cảnh. **SUY LUẬN:** giảm chọn nhầm; cần thử.

### F-07 — `fullstack-builder` có lỗi cấu trúc nội dung · ĐO

Lặp heading "Project Structure", "Stack Detection", "Generated Items"; có mục `Mode: setup` không khai báo trong description (chỉ có scaffold/add-feature/integrate); cây thư mục chung chung. Validator pass vì chỉ kiểm heading `##` trùng ở một mức. Thiếu những gì đợt ReNER cần: contract-first (OpenAPI sinh client), tách 3 loại state ở frontend, fixture-first, hồ sơ demo/pilot, job bền trong DB.

### F-08 — Skill đặc tả/kế hoạch chưa theo kịp cách làm đã chốt · SUY LUẬN

- `spec-writer` thiếu: thuật ngữ có "không phải/tránh dùng", luật nghiệp vụ có ví dụ đạt/không đạt, state machine kèm "trạng thái không chứng minh điều gì", tách Locked/Open/Explore, allowed paths, ví dụ nghiệm thu. Các khuôn này đã có trong `PROMPT-KIEN-TRUC-GIAO-VIEC-AI.md` v1.2 (TMG301).
- `writing-plans` yêu cầu code đầy đủ trong mọi bước. Người dùng đã xác nhận (12/10): AI tự quyết chi tiết dễ đảo ngược, chỉ hỏi về nghĩa dữ liệu/quyền/nghiệm thu. Hai điều này mâu thuẫn ở task ít rủi ro.

### F-09 — Thiếu năng lực "proposal → repo làm việc" · QUAN SÁT

Repo `rener-vn` (56 file) phải dựng tay: đọc proposal → người dùng/hành trình/màn hình → từ điển dữ liệu + enum → pipeline → API/CSDL → đặc tả bàn giao (extension) → kế hoạch đánh giá → ADR → JSON Schema + fixture + script kiểm → backlog GitHub có milestone. `scaffold-project` lo cây thư mục + quy trình git; `spec-writer` lo spec một tính năng; không skill nào lo chuỗi này. Loại việc này lặp lại ở nhiều đồ án và dự án nhận khách.

### F-10 — Thiếu quy tắc khi một nguồn có nhiều phiên bản · QUAN SÁT

Hai proposal v1.2 và v1.3 cùng ngày; memory ghi bản nộp là v1.2; mọi phiên từ 09/10 dùng v1.3 mà không so; phiên này gắn nhãn "đã nộp" không kiểm. `evidence-first` nói "source existence is insufficient" nhưng không nói gì về **phiên bản**. Đề xuất quy tắc: thấy nhiều bản thì liệt kê, so, ghi bản đang dùng và lý do; không gắn nhãn "đã nộp/bản cuối/đã duyệt" khi người dùng chưa xác nhận.

### F-11 — Quy ước đầu ra thiên về nghiên cứu · NGUỒN (rule nội bộ)

`workbench-conventions.md` §3a đặt đầu ra ở `notes/<id>-<skill>.md` (mã paper). Dự án web/sản phẩm cần `docs/` theo mảng, `docs/decisions/` (ADR), `spec/` (schema, fixture), `AGENTS.md`. Đợt ReNER phải tự đặt các quy ước này.

### F-12 — Nhóm trí nhớ: chồng chéo về khái niệm, phần lớn chưa dùng · ĐO + SUY LUẬN

- Bốn skill có mục trùng ý: `project-memory/decisions.md` ↔ `audit-log` (quyết định); `project-memory/preferences.md` ↔ `learnings-db/corrections.md` ↔ loại `feedback` của auto memory.
- `project-memory`, `learnings-db` chưa tạo thư mục ở hai workspace đã quét (§3.3).
- **Không thay bằng auto memory:** auto memory nằm trên máy, không vào git, chỉ Claude Code đọc. Người khác clone repo không thấy. Skill ghi file vào dự án thì chia sẻ được qua git và dùng được ở Antigravity. Đây là giá trị cần giữ.
- **SUY LUẬN:** chọn **một** bố cục file trong dự án (ví dụ `notes/INDEX.md` + `notes/WORK_LOG.md` + `notes/decisions/` + `notes/claims-ledger.md`, như đợt ReNER đã dùng thật) và gom bốn skill về bố cục đó; auto memory giữ phần cá nhân (sở thích, cách làm việc).

### F-13 — Gần như không đo hiệu quả hành vi · ĐO

Validator kiểm cấu trúc, không kiểm skill có được chọn đúng lúc hay có làm đúng việc. Chỉ `admin-research` có eval. Cảm nhận "skill giúp giảm ảo giác khi nghiên cứu" của người dùng phù hợp với SkillsBench (skill tuyển chọn có ích), nhưng **chưa có số đo riêng cho bộ này**.

### F-14 — Nhiều bản sao, phân phối chưa thống nhất · ĐO

Ba nơi chứa skill (§3.2), 17 thay đổi treo, `plugin.json` chỉ cho Antigravity. Mỗi lần sửa phải đồng bộ tay; dễ chạy bản cũ mà tưởng bản mới.

**Cập nhật 15/10/2026:** rủi ro này đã xảy ra thật và có tác động đo được. Phiên nghiên cứu 14–15/10 chạy `admin`, `research-admin` và `hallucination-guard` bản ngày 08/09, không phải bản evidence-first trong repo. Xem F-17.

### F-15 — Chưa có chính sách khi lấy skill từ bên ngoài · NGUỒN + SUY LUẬN

Xu hướng dùng skill từ thư viện/chợ là có thật (chuẩn mở, nhiều nơi phân phối), nhưng chất lượng và bảo mật không đều (báo cáo Snyk). Bộ hiện tại không có quy trình nhận skill ngoài: đọc trước khi cài, ghim phiên bản, fork về repo, quét script, chạy eval.

### F-16 — Điểm mạnh cần giữ · ĐO + NGUỒN

- `evidence-first` + NOT RUN + claims ledger: chặn được nhiều lỗi nói quá. Audit 11/10 trong TMG301 sửa 13 nhóm lỗi nhờ kỷ luật này.
- `design-web`/`build-ui`: bảng "lỗi tìm được bằng cách nào" (9 lỗi, 0 lỗi tìm bằng "nghĩ kỹ hơn") là bằng chứng nội bộ tốt cho việc bắt render, chụp, đo.
- Validator strict, 100% pass; script offloading (9 skill có `scripts/`).
- Chính sách song ngữ, preview-not-dump, reuse-before-read.

---

## 6. Nhận định sai đã rút lại trong phiên này

| Đã nói | Vì sao sai | Đúng là |
|---|---|---|
| "Skill do model tự viết không giúp gì" (đặt cạnh lời khuyên gọn bộ skill) | Lấy số SkillsBench **v1** qua bản tóm tắt tìm kiếm; bản hiện tại không còn điều kiện này; "self-generated" là model tự viết skill cho tác vụ, không phải bộ người dùng tuyển chọn qua nhiều tuần | Bộ này gần với "skill tuyển chọn", loại mà bài báo cho thấy có ích |
| "Khoảng 37 nghìn ký tự description bị nạp mỗi phiên" | 37.440 là tổng trong file nguồn; Claude Code giới hạn danh sách khoảng 1% ngữ cảnh | Phần vượt bị **bỏ**, gây mất description (F-01), không phải nạp hết |
| "Gộp 4 skill trí nhớ vì Claude Code đã có auto memory" | Auto memory không chia sẻ qua git, chỉ Claude Code đọc | Giữ cách lưu file trong dự án; chỉ xét gộp về một bố cục (F-12) |
| "Proposal v1.3 đã nộp" (trong repo `rener-vn`) | Chưa có xác nhận; memory ghi v1.2 | Đã sửa ở PR #17: "chưa xác nhận bản đã nộp" |
| "`~/.claude/skills/` khớp nguồn về nội dung" (§3.2) — *bổ sung 15/10 bởi phiên NCKH* | Phép đo ngày 15/10 cho thấy 14/69 skill có phần thân khác repo HEAD. Bản cài có ngày 08/09 | Chỉ 55/69 skill giống. Bản cài thiếu các thay đổi evidence-first ngày 04/10 (F-17) |

**Bổ sung 15/10/2026:** các nhận định sai mà phiên nghiên cứu NCKH đã rút lại (venue, toán, nhân quả, nguồn) nằm ở §10.6. Khi gộp báo cáo, cũng không lấy lại các nhận định đó.

---

## 7. Đề xuất

Thứ tự theo giá trị trên công sức. "Kiểm bằng" là cách biết đề xuất có hiệu quả.

| Mã | Đề xuất | Giải quyết | Công sức | Kiểm bằng |
|---|---|---|---|---|
| **R-01** | Chạy `/skill-doctor` và `/context`; ghi số liệu thật về chi phí danh sách và tần suất dùng từng skill vào báo cáo gộp | F-01, F-02 | Rất thấp | Có bảng số liệu |
| **R-02** | Viết lại description theo mẫu: câu đầu là **tình huống dùng** + từ khóa người dùng hay nói; giữ dưới ~300 ký tự; bỏ phần "Modes —" dài vào thân skill | F-01 | Thấp | `/context` giảm; eval kích hoạt (R-10) tăng |
| **R-03** | Gỡ 7 alias khỏi danh sách: bảng chuyển hướng trong README, hoặc `skillOverrides: "off"`; đặt `name-only` cho skill dùng hiếm | F-03, F-01 | Thấp | Số skill mất description giảm |
| **R-04** | `admin`: thêm một bảng ánh xạ ngắn "loại việc → skill" (khoảng 20 dòng) thay vì dựa hoàn toàn vào danh sách; giữ nhánh 1 nhưng bắt buộc nêu skill đã cân nhắc | F-02 | Thấp | Eval định tuyến (R-10) |
| **R-05** | Thêm `disable-model-invocation: true` cho skill có tác dụng ra ngoài: `scaffold-project` (publish), `deploy-admin`, `rollback-manager`, `finishing-a-development-branch`, `run-on-modal` | F-05 | Rất thấp | Không bị gọi tự động |
| **R-06** | Chuyển quy tắc máy móc sang hook: chặn co-author trong commit; chặn file `.env`/khóa; Stop hook chạy lệnh verify của dự án nếu có | F-04 | Trung bình | Thử commit vi phạm bị chặn |
| **R-07** | Thêm quy tắc "nhiều phiên bản nguồn" vào `evidence-first` (F-10) | F-10 | Rất thấp | Ca eval: hai file v1/v2 |
| **R-08** | Sửa `fullstack-builder` (F-07); nâng `spec-writer` theo khuôn prompt v1.2; nới `writing-plans` theo mức rủi ro của task | F-07, F-08 | Trung bình | Validator + eval sinh spec |
| **R-09** | Skill mới `project-repo-spec`: proposal/brief → repo đặc tả (docs theo mảng, ADR, `spec/` schema + fixture + checker, `AGENTS.md`) → backlog GitHub (chỉ khi người dùng đồng ý). Dùng `rener-vn` làm ví dụ mẫu | F-09, F-11 | Cao | Dựng lại `rener-vn` từ proposal, so độ phủ |
| **R-10** | Eval hành vi cho khoảng 8 skill dùng nhiều: admin (định tuyến), spec-writer, design-web, build-ui, backend-engineer, paper-read, hallucination-guard, latex-fix. Mỗi skill có ca "nên kích hoạt" và "không nên"; thêm ca có/không skill để đo giá trị | F-13 | Trung bình–cao | `claude plugin eval` hoặc runner hiện có |
| **R-11** | Gom nhóm trí nhớ về một bố cục file trong dự án; phân vai rõ với auto memory | F-12 | Trung bình | Một phiên mới tìm được bối cảnh chỉ từ file dự án |
| **R-12** | Một nguồn duy nhất → sinh bản Claude Code (plugin) + bản Antigravity; commit hoặc tách 17 thay đổi treo trước khi sửa gì | F-14 | Trung bình | Không còn sửa tay ở bản cài |
| **R-13** | Quy trình nhận skill ngoài: đọc hết, ghim phiên bản, fork vào repo, quét script, chạy eval trước khi bật | F-15 | Thấp | Checklist trong README |
| **R-14** | Thêm hồ sơ đầu ra "product/web" vào `workbench-conventions` (docs/, decisions/, spec/, AGENTS.md) bên cạnh hồ sơ research | F-11 | Thấp | Skill web/spec tuân theo |

**Không nên làm** (SUY LUẬN): thay skill ghi file bằng auto memory; xóa skill chỉ vì ít dùng khi chưa có số liệu R-01; thêm nhiều skill mới trước khi giải F-01 (sẽ làm mất thêm description).

---

## 8. Phác thảo cấu trúc bộ skill mới (đề xuất, chưa kiểm)

```text
Tầng 0 — Cơ chế ép (không phải skill)
  hooks: commit, secrets, verify-on-stop        settings: skillOverrides, budget
  rules: evidence-first (+ phiên bản nguồn), workbench-conventions (research + product)

Tầng 1 — Điểm vào
  admin (có bảng ánh xạ việc → skill)

Tầng 2 — Quy trình lõi, model tự gọi (~12–15 skill, description ngắn, rõ)
  đặc tả: project-repo-spec, spec-writer          kế hoạch/thực thi: writing-plans, executing-plans
  kiểm: verification-before-completion, hallucination-guard, code-reviewer
  web: design-web, build-ui, review-frontend, backend-engineer
  trí nhớ dự án: một skill + một bố cục file

Tầng 3 — Gói theo miền (plugin hoặc paths:, chỉ hiện khi đúng ngữ cảnh)
  research: paper-*, citation-guard, claim-forge, latex-*
  học tập: study-*, knowledge-quiz, concept-explainer
  deploy/GPU: deploy-admin, run-on-modal (disable-model-invocation)
  (sau này) robotics: ROS 2, LeRobot, mô phỏng trước khi chạy thật

Tầng 4 — Thủ công (disable-model-invocation)
  scaffold-project publish, rollback, finishing-branch, ai-cv-forge
```

Mục tiêu: số skill **hiện description** trong danh sách nằm gọn trong ngân sách; các gói miền chỉ xuất hiện khi cần.

---

## 9. Gợi ý khi gộp với báo cáo các phiên khác

1. **So theo mã:** với mỗi `F-xx`, các báo cáo khác xác nhận, phản bác hay chưa thấy? Phát hiện được nhiều phiên độc lập xác nhận nên ưu tiên.
2. **Ưu tiên số liệu R-01** (`/skill-doctor`) trước khi quyết bỏ/gộp skill nào. Tần suất dùng thật quan trọng hơn ấn tượng của từng phiên.
3. **Tách loại dự án:** báo cáo này đến từ ngữ cảnh **nghiên cứu flow xây dựng web** (đồ án web + extension + NLP). Phiên nghiên cứu thuần có thể thấy `paper-*` dùng nhiều; phiên code có thể thấy khác.
4. **Lọc nhận định đã rút lại:** mục 6 của mỗi báo cáo.
5. **Câu hỏi cần chủ bộ skill quyết:**
   - Giữ hay gỡ 7 alias deprecated?
   - Phân phối chính: Claude Code plugin, Antigravity, hay cả hai từ một nguồn?
   - 17 thay đổi Antigravity đang treo: commit hay tách nhánh?
   - Bộ skill có chia sẻ cho người khác không? Nếu có, ngôn ngữ mô tả, giấy phép và mức phụ thuộc vào rule cá nhân cần xem lại.

---

## 10. Bổ sung từ ngữ cảnh nghiên cứu paper — NCKH nhóm 7, đề tài #7 (14–15/10/2026)

> **Phạm vi.** Theo §0.1, ngữ cảnh khác flow web nên viết báo cáo riêng. Ở đây chủ bộ skill yêu cầu đóng góp thẳng vào file này, nên mục 10 giữ đúng khuôn của file và gắn nhãn ngữ cảnh **nghiên cứu paper** để bước gộp lọc ra được.
>
> Phân tích chi tiết từng lỗi (nguyên văn câu đã viết, file:dòng, kiểm lại bằng mô phỏng) nằm ở [`phan-tich-phien-nckh-t07-2026-10-15.md`](phan-tich-phien-nckh-t07-2026-10-15.md). Mục này chỉ ghi phần liên quan tới bộ skill.

### 10.1 Bối cảnh và skill được dùng thực tế

**Phiên:** Claude Code trên VS Code, Opus 5.5 (một lượt chạy Sonnet 5), ngày 14–15/10/2026.

**Việc đã làm:** bốn lượt `/admin` trên dự án NCKH (phát hiện vật thể tí hon trong ảnh trên không, YOLO-OBB):

1. Đánh giá một hướng có đủ khả thi cho Q4/Q3 không.
2. Tìm đường lên Q2.
3. Quét rộng các hướng nghiên cứu.
4. Báo cáo lại.

Đầu ra là 3 note và 3 dòng ledger (C-16, C-17, C-18).

**Phản biện:** sau đó một chat khác audit lại kết quả, dùng worker gpt-6.1-sol ×2 và gpt-6-astra ×1, và ghi C-19. Tôi đếm được **14 lỗi** đã được xác nhận. Phiên này tự kiểm lại mọi lỗi kiểm được bằng mô phỏng hoặc bằng cách mở lại nguồn (file phân tích, §1).

**Skill được gọi** (ĐO, đếm lời gọi `Skill`/`Agent` trong transcript):

| Skill | Số lần gọi | Ghi chú |
|---|---:|---|
| `admin` (qua lệnh `/admin`) | 3 | Lần nào cũng chuyển sang `research-admin` |
| `research-admin` | 3 | Tự làm hết, không gọi worker nào |
| `hallucination-guard` | 3 | Có ở cả ba note. Không bắt được lỗi nào trong 14 lỗi |
| `paper-method`, `paper-synthesize`, `ieee-q1-devil-advocate`, `self-evaluator` | 0 | Xem F-20 → F-22 |
| Agent / subagent | 0 | Xem F-23 |

### 10.2 Đối chiếu với các phát hiện đã có

| Mã | Từ ngữ cảnh nghiên cứu | Ghi chú |
|---|---|---|
| F-01 | Chưa thấy | Không ghi lại danh sách skill của phiên, nên không đối chiếu được |
| F-02 | **Phản bác một phần** | `/admin` chuyển đúng sang `research-admin` cả 3 lần. Vấn đề "tự làm, không gọi worker" nằm ở tầng sub-admin (F-20), không nằm ở `admin` |
| F-04 | Xác nhận | Venue Claim Card và việc đọc lại ledger đều chỉ là chữ. Lỗi ở đây là lỗi phán đoán, hook không bắt được, cần reviewer (F-23) |
| F-10 | Xác nhận, mở rộng | Ngoài "phiên bản của nguồn" còn có "phiên bản của claim": một claim kỹ thuật đã sửa ở note sau vẫn bị chép lại từ note cũ (F-25) |
| F-13 | Xác nhận | `evals/admin-research/cases.yml` có 12 ca. Không ca nào về venue/tier, không ca nào kiểm tính đúng của suy luận (ĐO, grep) |
| F-14 | **Xác nhận, có tác động đo được** | F-17 |
| F-16 | Xác nhận | Ledger, REVISION và hộp đính chính giúp audit truy từng lỗi về đúng §/dòng |

### 10.3 Phát hiện mới

### F-17 — Bản Claude Code đang chạy cũ hơn nguồn 5 tuần, gồm cả 4 skill nghiên cứu cốt lõi · ĐO

**Ngữ cảnh:** khi tìm vì sao các quy tắc evidence-first không có tác dụng trong phiên NCKH 14–15/10.

**Thấy gì:** transcript ghi "Base directory for this skill: …\.claude\skills\…" cho `admin`, `research-admin` và `hallucination-guard`. Đây là bản cài ngày 08/09/2026, không phải repo. Commit `0ef12b5` (04/10, "evidence-first pilot") đã sửa `admin` trong repo, nhưng bản sửa không tới được `~/.claude`.

**Bằng chứng:** so phần thân SKILL.md (bỏ frontmatter, bỏ CR) giữa `~/.claude/skills/<s>` và `git show HEAD:.claude/skills/<s>/SKILL.md`:

- 55/69 skill giống.
- **14/69 skill khác**. Số dòng HEAD/bản cài: `admin` 114/81, `research-admin` 233/197, `hallucination-guard` 126/106, `self-evaluator` 119/102, `writing-skills` 163/143, `test-framework` 59/31, `token-budget` 72/75, `understand-codebase` 56/61. Sáu skill còn lại khác nội dung nhưng cùng số dòng: `ai-cv-forge`, `build-ui-component`, `code-admin`, `design-ui-direction`, `paper-method`, `using-git-worktrees`.
- `~/.claude/rules` không có `evidence-first.md`.
- `research-proposal-integrity.md` và `workbench-conventions.md` ở bản cài giống HEAD.

**Tác động:** các cải tiến evidence-first chưa từng chạy trong Claude Code. Một số cải tiến đó đúng là loại có thể chặn lỗi của phiên này: bản HEAD của `hallucination-guard` có "Split material factual claims and deductions" và "entails the exact claim's … scope"; bản HEAD của `research-admin` có "Unseen body/AI summaries are not support". **SUY LUẬN:** nếu đã cài, chúng có thể chặn 4/14 lỗi (về độ sâu đọc và loại bài toán). Chúng không chặn được các lỗi về venue, phạm vi định lý hay nhân quả. Từ nay, mọi câu kiểu "skill X đã có quy tắc Y" phải kiểm trên **bản cài**, không kiểm trên repo.

**Không chắc ở đâu:** chưa biết việc chỉ đưa pilot sang Antigravity có phải chủ ý không (**CHƯA KIỂM**, hỏi chủ bộ skill). Chưa kiểm bản Antigravity đang chạy bản nào. Nếu so với working tree (gồm 17 thay đổi treo) thay vì HEAD, số skill lệch còn lớn hơn.

**Liên quan:** F-14, R-12, R-15.

**Cập nhật 15/10/2026 (cùng phiên, ĐO):** tiêu đề "cũ hơn nguồn 5 tuần" bị sai, vì tôi suy ra từ ngày sửa file (08/09). Khi so phần thân với từng commit, bản cài **khớp commit `e51683d` (02/10/2026) ở 68/69 skill**; chỉ `test-framework` khác. Bản cài vì vậy chỉ thiếu các commit từ `0ef12b5` (04/10, evidence-first) trở đi, khoảng 2 ngày. Nội dung còn lại của F-17 vẫn đúng.

**Cập nhật 15/10/2026 — đã xử lý (ĐO):** sau khi `main` của repo `gobal-agent-skills` được merge ở `8053e95` (PR #1), bản cài đã được đồng bộ lại:

- **Skill:** 67/69 thư mục giống hệt repo từng byte.
- **Hai skill dùng chung với Codex** (`latex-fix`, `study-forge`, junction sang `~/.codex/skills`): chỉ thay `SKILL.md`. Riêng `study-forge` trước đó có frontmatter YAML không hợp lệ.
- **Rule:** đủ 7 rule, đã có `evidence-first.md`.
- **Validator trên bản cài:** 99,6%. 3 lỗi còn lại là báo nhầm "escapes skills root" do junction; các file được nhắc tới đều tồn tại.
- **Sao lưu:** `~/.claude/backups/skills-rules-2026-10-15/`.
- **Chưa làm:** R-15 (script tự báo lệch) vẫn còn mở.

Đo thêm về các bản đang có:
- `origin/main` của repo `gobal-agent-skills` (`20de9e1`, tháng 08) dùng bố cục cũ và cũ nhất.
- Repo `gobal-agent-skills-antigravity` (05/10) có `skills/` và `rules/` khớp working tree local, chỉ khác 4 file README/test.

### F-18 — Rule venue toàn cục buộc phải gắn band và lấn quyết định của dự án · NGUỒN + QUAN SÁT

**Ngữ cảnh:** câu hỏi "hướng này đủ Q4 chưa, lên Q3/Q2 được không" trong dự án NCKH. Ledger của dự án đã chốt "No venue band" (C-13 → C-15).

**Thấy gì:** `research-proposal-integrity.md` có hai quy định:

- §1 là bảng tier → band ("T1 … Q4. **NEVER Q1 alone**"; "T2 … Q2–Q3").
- §2 bắt mọi đề xuất phải có Venue Claim Card với ô "Venue band" ("A proposal note without this card is incomplete").

Ba skill cùng thực thi rule này: bảng định tuyến của `research-admin`, mẫu lỗi "Venue overclaim → Grade per §1" của `hallucination-guard`, và `ieee-q1-devil-advocate` (§1 là binding). Rule **không nói gì về thứ tự ưu tiên** khi dự án có quyết định khác. Kết quả là thẻ venue của phiên này **qua được** guard, chính vì nó có tier kèm điều kiện.

**Bằng chứng:**

- Note của phiên: "Rubric §1: T1 → workshop / hội nghị Scopus / Q4; T2 → Q2–Q3", và "Q2 cần thêm ≥ 3 dataset độc lập nguồn … (trần Q3)".
- Ledger dự án C-13: "T1/T2 labels describe intervention only, not journal quartile". C-15: "Journal quartile is not a deterministic per-paper method grade".
- Giao thức nghiên cứu của dự án (`RESEARCH-PROMPT.md` §3) cấm nói "đủ Q1/Q2" khi chưa có bằng chứng.
- Audit C-19 phải rút lại cả mapping lẫn "luật ba dataset", và ghi chỉ sửa trong dự án, "không sửa skill/rule toàn cục".

**Tác động:** trực tiếp gây ra 2 trong 14 lỗi, nhưng đây là hai lỗi chi phối kết luận chính của 2/3 note. Rule sinh ra từ một sự cố thật (07/07, project 034: nói quá rồi phải rút), và mục tiêu chống nói quá vẫn đúng. Vấn đề nằm ở cơ chế: một bảng tất định, bắt buộc điền band, đã tạo ra lỗi theo chiều ngược lại. Vì audit không sửa rule, **phiên sau sẽ lặp lại lỗi này**.

**Không chắc ở đâu:** chưa biết ở dự án khác rule này gây lỗi thường xuyên đến đâu (**CHƯA KIỂM**). Chưa biết bỏ bảng thì có mất tác dụng chống nói quá không; cần eval R-24 có cả ca 07/07.

**Liên quan:** F-04, F-19, F-22, R-16.

### F-19 — `hallucination-guard` kiểm nguồn và nhãn, không kiểm suy luận, nhưng kết quả "sạch" được báo như "đúng" · ĐO + NGUỒN

**Ngữ cảnh:** cổng bắt buộc cuối cùng của `admin` (Phase 6) và `research-admin` (Step 7), đã chạy trên cả ba note.

**Thấy gì:** quy tắc của bản đang chạy là "Every factual claim needs a source". Bước scan hỏi "can it be verified from available context?". Ba lần scan bắt sửa 14 chỗ, gồm ba loại:

- chi tiết nguồn (số epoch, số mức, số lần thử, số đếm);
- nhãn độ sâu đọc;
- gắn nhãn [suy luận] cho câu chưa có nhãn.

Có một lần guard sửa lĩnh vực của nguồn (HODet). **Không chỗ nào kiểm suy luận đúng hay sai**, và 11/14 lỗi mà audit tìm ra thuộc loại suy luận hoặc khung câu hỏi. Sau scan, phiên này báo người dùng: "Lỗi phát hiện đã sửa và kiểm lại, **không còn lỗi**".

**Bằng chứng:** SKILL.md bản cài, phần Core Rules và Mode scan; transcript 14/10 lúc 14:33 và 17:43; bảng lỗi ở file phân tích §2.

Các lỗi lọt qua guard:

- "Cùng diện tích ⇒ hiệu ứng hình dạng chỉ bậc hai". Phản ví dụ, ĐO bằng mô phỏng: P(rỗng) là 0 so với 0,4995.
- "√2·s dự báo mức sàn AP tối ưu".
- "arctan(2δ/L) là giới hạn khả năng xác định".
- "A8 đủ ứng viên mà recall thấp ⇒ nguyên nhân ở đặc trưng".

**Tác động:** guard tạo cảm giác an toàn sai đúng ở loại lỗi gây hại nhất cho đề xuất nghiên cứu. Bản HEAD đã có "Split … deductions" (F-17), nhưng chưa có các bước cụ thể:

- (a) định lý bảo đảm gì, và claim đang dùng nó để nói gì;
- (b) cận trên, cận dưới hay kỳ vọng;
- (c) thử một phản ví dụ nhỏ bằng số;
- (d) claim nhân quả có can thiệp đối chứng không;
- (e) nguồn trích có cùng loại bài toán không;
- (f) độ sâu đọc có đủ cho mức chắc của claim không.

**Không chắc ở đâu:** chưa chạy bản HEAD trên ba note cũ để đếm nó bắt được bao nhiêu lỗi. R-24 sẽ đo việc này.

**Liên quan:** F-13, F-26, R-17, R-24.

### F-20 — `research-admin` không có mode "thẩm định một đề xuất", trong khi đây là việc lặp lại nhiều nhất của dự án · ĐO + QUAN SÁT

**Ngữ cảnh:** cả ba yêu cầu `/admin` của phiên đều thuộc loại "đánh giá một hướng hoặc đề xuất so với prior và tiêu chuẩn".

**Thấy gì:** `research-admin` có các mode scope, pipeline, triage, read, synthesize. Dòng định tuyến cho "Đề xuất hướng / novelty / venue" trỏ tới `paper-synthesize gaps/expand`, mà skill này suy luận trên "INDEX gists" của `papers/`. Không mode nào vừa với việc thẩm định. Trong dự án NCKH, việc cùng loại đã xảy ra ít nhất 4 lần trong 11–15/10 (`t07-critique-q2-2026-10-11`, `t07-venue-assessment-2026-10-14`, `t07-q2-path-2026-10-14`, audit C-19). Mỗi lần đều dựng quy trình bằng tay.

**Bằng chứng:** SKILL.md của `research-admin` (Modes, Routing Rules); transcript có 0 lời gọi worker; danh sách file trong `notes/` của dự án.

**Tác động:** mọi bước (đọc prior, kiểm toán, phản biện, chấm venue) dồn vào một ngữ cảnh duy nhất, không có điểm dừng nào để kiểm. Hiện tượng giống F-09 ở ngữ cảnh web: việc lặp lại không có skill nào phủ.

**Không chắc ở đâu:** chưa biết dự án nghiên cứu khác có gặp loại việc này nhiều như vậy không.

**Liên quan:** F-02, F-09, R-18.

### F-21 — `paper-method` chỉ nhận bài trong `./papers/`, nên bài tải từ web phải đọc bằng grep · NGUỒN + QUAN SÁT

**Ngữ cảnh:** đọc sâu O2-DETR, OSCAR, MCSA, tải về trong lúc làm.

**Thấy gì:** Phase 0 của `paper-method` chuyển đầu vào thành "a concrete file under `./papers/`". Phiên này tải các bài vào scratchpad (một phần do tôi chọn, vì repo dự án là public) rồi đọc O2-DETR bằng grep từ khóa ("size/small/scale"). Note gắn nhãn "toàn văn, quét từ khóa"; ledger C-17 ghi "full-text check". Claim "phân phối **không phụ thuộc kích thước**" là sai: Eq.(1) là `Dol = Do0 + (Wr, Hr)·A(n)Pol(n)` và Eq.(2) nhân với `(Wr, Hr, Wr, Hr)`. Grep theo từ không bắt được sự phụ thuộc viết bằng ký hiệu.

**Bằng chứng:** SKILL.md của `paper-method` Phase 0; bản text của bài, dòng 271 và 325; ledger C-17.

**Tác động:** một claim sai đi vào ledger với nhãn đọc toàn văn.

**Không chắc ở đâu:** việc `paper-method critique` (bước "Key equations — copied faithfully") sẽ bắt được lỗi này là **SUY LUẬN**.

**Liên quan:** F-26, R-19.

### F-22 — Skill phản biện duy nhất nằm cuối chuỗi viết bài và dùng đúng rubric đã gây lỗi · NGUỒN + SUY LUẬN

**Ngữ cảnh:** tìm xem skill nào lẽ ra phải phản biện đề xuất trước khi giao cho người dùng.

**Thấy gì:** `ieee-q1-devil-advocate` có ba đặc điểm:

- nhận đầu vào là "paper draft" và chạy "áp chót" trong chuỗi viết bản thảo;
- lấy §1 của rule venue làm binding ("T1 mà target Q1 = FAIL thẳng");
- ghi "Không nhận kiến thức từ LLM training; mọi claim phải đè vào nội dung văn bản đầu vào", nên không mở nguồn gốc.

**Bằng chứng:** SKILL.md; `paper-writing-integrity.md` §6.

**Tác động:** không có phản biện nào ở giai đoạn đề xuất. **SUY LUẬN:** kể cả khi được gọi, skill này sẽ **củng cố** lỗi venue (F-18) và không bắt được lỗi cần mở nguồn gốc (F-21) hay lỗi sai loại bài toán. Đây cũng là lời tự sửa của phiên này: giả thuyết ban đầu "không gọi devil-advocate là một nguyên nhân" là sai hướng (§10.6).

**Liên quan:** F-18, F-23, R-20.

### F-23 — Không có reviewer độc lập ở giai đoạn đề xuất, và cấu hình subagent tự mâu thuẫn · QUAN SÁT + NGUỒN

**Ngữ cảnh:** cùng một model vừa viết vừa tự kiểm, inline, không có subagent.

**Thấy gì:** hai bên nói ngược nhau:

- Harness Claude Code dặn "Do not spawn agents unless the user asks".
- `admin/references/dispatch-protocol.md` dặn "Việc độc lập → nhiều `Task` call". Bản HEAD của `research-admin` thêm "If subagents are unavailable, execute sequentially".

Chưa nơi nào nói `/admin sâu` có được tính là người dùng đã yêu cầu dùng subagent hay không.

**So sánh có/không phản biện độc lập** (QUAN SÁT, n = 1). Đây không phải so sánh có/không skill. Phân loại "lỗi tìm được bằng cách nào" (theo §0.1, cùng kiểu bảng trong `design-web`):

| Cách tìm ra lỗi | Lỗi |
|---|---|
| Tìm phản ví dụ toán | 3 (cùng diện tích, √2·s ⇒ tối ưu, arctan ⇒ khả năng xác định) |
| Mở lại nguồn gốc ở mức method/bảng | 2 (O2-DETR, AQE) |
| Đối chiếu tài liệu dự án (ledger phạm vi, giao thức, issue #21) | 3 (mapping venue, luật ba dataset, CSCWD) |
| Phản biện logic nhân quả/đo lường | 3 (cặp nhãn HBB/OBB, A8 ⇒ đặc trưng, "ngân sách lỗi") |
| Kiểm manifest/cache | 1 ("khoảng 45 nguồn") |
| Đối chiếu tên trong dự án | 1 (hai nghĩa của "hướng A") |
| Người dùng chỉ ra | 1 (ghi sai nguồn gốc của audit) |
| `hallucination-guard` của phiên | **0** |

**Không chắc ở đâu:** audit được đọc kết quả của phiên này trước khi phản biện, và dùng model khác. Vì vậy bảng này không đo được giá trị của skill. Nó chỉ cho biết **loại kiểm tra nào** bắt được loại lỗi nào.

**Liên quan:** F-13, F-19, F-22, R-20.

### F-24 — Đọc lại ledger theo chuỗi claim, bỏ qua các dòng quy định phạm vi và giao thức của dự án · ĐO

**Ngữ cảnh:** quy tắc §3 của `research-proposal-integrity`: "re-read `notes/claims-ledger.md` + the proposal note" trước mọi câu hỏi tiếp nối.

**Thấy gì:** phiên này chỉ đọc lại các dòng cha-con của claim đang xét. Mục "nguồn nội bộ đã đọc lại" của note 1 chỉ có C-10 → C-12. Note 2 chỉ có C-11, C-12, C-16. Phiên bỏ qua:

- C-13 → C-15 (quy định phạm vi, "no venue band");
- tài liệu điểm vào và giao thức nghiên cứu của dự án.

Giao thức của dự án đã cảnh báo đúng hai lỗi: "Phân biệt rõ bài này với phát hiện chính chiếc drone…" và "Không tuyên bố … đủ Q1/Q2". Báo cáo lượt 1 của chính phiên này còn ghi đã thấy "hai hướng nghiên cứu đang chạy song song".

**Bằng chứng:** header của hai note; ledger; `RESEARCH-PROMPT.md` §1 và §3 của dự án.

**Tác động:** gây ra lỗi venue, luật ba dataset, CSCWD sai loại bài toán, và lỗi chọn nghĩa "hướng A" mà không hỏi lại.

**Không chắc ở đâu:** câu chữ của rule để ngỏ cách hiểu "đọc lại toàn bộ" hay "đọc lại phần liên quan". Phiên khác có thể hiểu khác.

**Liên quan:** F-18, F-27, R-21.

### F-25 — Đính chính kỹ thuật không có nơi tra, nên claim đã sửa bị chép lại · ĐO

**Ngữ cảnh:** claim "cùng diện tích ⇒ hiệu ứng hình dạng chỉ bậc hai" (Hệ quả 2 trong proposal v2 §6).

**Thấy gì:** dự án đã sửa claim này ở issue #21, ở digest §5.3, và ở `t07-dl-from-slides-VI.md:682` với đúng phản ví dụ 8×8 so với 16×4. Nhưng proposal v2 vẫn giữ bản cũ, và phiên này chép lại từ proposal. Ledger chỉ ghi claim về venue và novelty, không ghi claim toán hay kỹ thuật.

**Bằng chứng:** grep "Hệ quả 2" trên `notes/` của dự án; hai note của phiên.

**Tác động:** tốn một vòng audit để sửa lại một điều đã được sửa trước đó.

**Liên quan:** F-10, R-22.

### F-26 — Không có cổng "độ sâu đọc ↔ độ mạnh claim", và nhãn độ sâu bị trộn · QUAN SÁT

**Thấy gì:** ba ví dụ:

- Nhãn "toàn văn, quét từ khóa" (thực chất là grep) trở thành "full-text check" trong ledger.
- Một REVISION (C-18) ghi "abstract only" nhưng kết luận "phần còn lại **chỉ là** điều kiện theo kích thước pixel".
- Con số "khoảng 45 nguồn mới" không có bảng chọn nguồn để tái dựng. Manifest của audit đếm được 298 bản ghi và 174 ID arXiv.

Giao thức của dự án có sẵn quy tắc "Không biến abstract thành full-method audit". Bộ rule toàn cục thì chưa có.

**Tác động:** ba lỗi trong 14 lỗi; hai trong số đó đi vào ledger.

**Liên quan:** F-19, F-21, R-17, R-19.

### F-27 — Không kiểm tiền đề và loại bài toán trước khi trả lời · QUAN SÁT

**Thấy gì:** ba trường hợp:

- "Hướng A" có hai nghĩa trong dự án, nhưng phiên tự chọn một nghĩa.
- Câu hỏi đặt sẵn khung Q4/Q3/Q2, phiên trả lời trong khung đó dù dự án đã bỏ việc gắn band.
- CSCWD là bài phát hiện drone (anti-UAV) nhưng bị coi là đối thủ của bài phát hiện vật từ UAV.

`workbench-conventions` §2 ("ask once" khi mơ hồ) chỉ nói về việc phân giải `$ARGUMENTS` (id paper, đường dẫn), không nói về khái niệm mơ hồ. Ca eval `IDE-FALSE-PREMISE` kiểm tiền đề **dữ kiện** sai, không kiểm khung câu hỏi hay loại bài toán.

**Liên quan:** F-24, R-18, R-24.

### F-28 — Ledger nhận REVISION dựa trên bằng chứng suy luận, với nhịp quá nhanh · ĐO

**Thấy gì:** ba REVISION trong khoảng một ngày: C-16 và C-17 ngày 14/10, C-18 ngày 15/10. Cả ba đều ghi lý do "new evidence", nhưng thực chất:

- C-18 dựa trên abstract.
- C-17 dựa trên grep từ khóa.
- Các điều kiện suy ra (≥3 dataset, ≥2 họ detector) bị ghi thành điều kiện venue.

Quy trình revision (§3) bắt nêu nguyên nhân nhưng không bắt nêu **loại bằng chứng**, nên "new evidence" che được cả abstract.

**Tác động:** ledger, vốn để chống trôi claim, lại ghi chính sự trôi đó. C-19 phải sửa lại; memory của phiên cũng ghi theo.

**Liên quan:** F-18, F-26, R-23.

### 10.4 Đề xuất mới

| Mã | Đề xuất | Giải quyết | Công sức | Kiểm bằng |
|---|---|---|---|---|
| **R-15** | Script kiểm lệch giữa bản cài và nguồn: so phần thân SKILL.md và rules giữa `~/.claude` và repo, báo tên từng skill lệch. Chạy trong validator hoặc hook SessionStart. Nếu chủ ý chỉ đưa pilot sang Antigravity thì ghi rõ trong README | F-17, F-14 | Thấp | Sau khi đồng bộ, script báo 0 lệch; sửa thử 1 file thì báo đúng 1 |
| **R-16** | Sửa `research-proposal-integrity.md`: (a) thêm thứ tự ưu tiên: quyết định phạm vi trong ledger hoặc giao thức của dự án đứng trên rubric; (b) cho phép Venue Claim Card ghi "Venue band: chưa gán — lý do + điều kiện để gán"; (c) đổi bảng tier → band thành mô tả loại can thiệp, ghi rõ "không phải bằng chứng editorial; venue cụ thể phải dùng tiêu chí chính thức của venue đó"; (d) giữ quy tắc chống nói quá: không hứa band khi không có điều kiện. Sửa đồng bộ `ieee-q1-devil-advocate` và mẫu lỗi của `hallucination-guard` | F-18 | Thấp | Eval: dự án có ledger "no band" và câu hỏi "đủ Q2 chưa" → đầu ra không gán band, không viện bảng tier. Ca 07/07 (nói quá) vẫn bị chặn |
| **R-17** | Thêm phần **kiểm suy luận** vào `hallucination-guard` (mode riêng hoặc trong scan), xây trên bước "deductions" của HEAD. Với mỗi claim [derived] hoặc nhân quả, trả lời 6 câu: định lý bảo đảm gì, claim dùng nó nói gì; cận trên, cận dưới hay kỳ vọng; một phản ví dụ bằng số đã chạy thử; có can thiệp đối chứng không; nguồn có cùng loại bài toán không; độ sâu đọc có đủ cho "không có / chỉ còn / không phụ thuộc" không. Báo kết quả **kèm phạm vi**: "đã kiểm nguồn; đã / chưa kiểm suy luận". Không báo "không còn lỗi" | F-19, F-26 | Trung bình | Replay R-24: cờ được ≥10/14 lỗi; trên các note đã sửa sau C-19, số cờ sai thấp |
| **R-18** | Thêm mode `assess` (thẩm định hướng hoặc đề xuất) cho `research-admin`. Bước 0: nạp phạm vi dự án (header và mọi dòng active của ledger, tài liệu điểm vào và giao thức) và kiểm tiền đề; nhãn mơ hồ thì hỏi 1 câu. Bước 1: đọc prior gần nhất qua `paper-method`. Bước 2: phản biện độc lập (R-20). Bước 3: guard cả nguồn lẫn suy luận. Đầu ra: claim, điều chưa biết, phép thử phân biệt các hướng. Chỉ nói về venue khi dự án cho phép | F-20, F-24, F-27 | Trung bình | 3 ca từ NCKH (venue, đường Q2, quét rộng), chấm theo 14 lỗi đã xác nhận |
| **R-19** | Cho `paper-method` nhận URL hoặc đường dẫn bất kỳ (bài tải từ web), lưu text vào cache local của dự án (không commit khi repo public). Dùng 3 mức nhãn độ sâu cố định: abstract / grep từ khóa / method và bảng | F-21, F-26 | Thấp | Chạy trên O2-DETR: phải chép được Eq.1–2 có (Wr, Hr) |
| **R-20** | Phản biện độc lập ở giai đoạn đề xuất: tách `ieee-q1-devil-advocate` thành mode `proposal` và `manuscript`, hoặc làm skill mới. Mode `proposal` được mở nguồn gốc, không dùng rubric venue làm bằng chứng, phải thử phản ví dụ và đối chiếu giao thức của dự án, chạy trong ngữ cảnh mới (subagent). Ghi trong `admin`: `/admin sâu` hoặc câu "phản biện độc lập" được tính là người dùng đồng ý dùng subagent | F-22, F-23 | Trung bình | Chạy trên 3 note trước C-19: so số lỗi bắt được giữa mode `proposal` và bản hiện tại |
| **R-21** | Quy tắc đọc lại trước câu trả lời về venue hoặc novelty: đọc header ledger, mọi dòng active (không chỉ chuỗi cha-con) và tài liệu điểm vào/giao thức của dự án. Ledger cho phép gắn nhãn `SCOPE` cho các dòng quy định phạm vi | F-24 | Rất thấp | Eval: ledger có dòng SCOPE nằm ngoài chuỗi claim → đầu ra dẫn đúng dòng đó |
| **R-22** | Sổ đính chính kỹ thuật: thêm loại claim `T-` (toán/kỹ thuật) vào ledger, hoặc tạo `notes/corrections.md`. Guard tra sổ này trước khi dùng lại một claim lấy từ note cũ hơn | F-25, F-10 | Thấp | Ca: proposal cũ có claim đã sửa ở note sau → đầu ra dùng bản đã sửa |
| **R-23** | Quy trình revision: mỗi REVISION ghi **loại bằng chứng** (kết quả chạy / đọc method / abstract / suy luận / phản biện của người dùng). Nếu chỉ có abstract hoặc suy luận thì không đổi điều kiện venue, chỉ ghi "đề xuất sửa" trong note | F-28 | Rất thấp | Sau 1 tháng, đếm số REVISION có loại bằng chứng "suy luận" |
| **R-24** | Bộ eval hồi cứu từ sự cố này. Đầu vào: 3 note trước C-19 cùng tài liệu dự án. Đáp án: 14 lỗi đã xác nhận (file phân tích §2). Ca âm: các note sau C-19, không được cờ. Dùng để chấm guard, mode `assess` và critic | F-13, F-19 | Trung bình | Là thước đo chung cho R-16 → R-20 |
| **R-25** | Khi tóm tắt một báo cáo do phiên hoặc model khác làm (audit, kết quả worker), chép người làm từ header của file. Memory về việc bên ngoài phải ghi nguồn đó | §10.6 | Rất thấp | Kiểm tay khi ghi memory |

**Không nên làm** (SUY LUẬN):

- Chỉ thêm `ieee-q1-devil-advocate` vào chuỗi mà không sửa rubric (R-16). Làm vậy sẽ củng cố chính lỗi venue.
- Coi "nhiều agent hơn" là cách sửa. Audit hiệu quả nhờ tiền đề khác, đọc nguồn gốc và tìm phản ví dụ, không nhờ số agent. Giao thức của dự án cũng ghi: ba agent không phải ba thí nghiệm độc lập.
- Thêm bước bắt buộc vào guard trước khi có R-24. Mỗi lượt sẽ tốn thêm chi phí mà chưa biết bắt thêm được bao nhiêu lỗi.
- Bỏ hẳn quy tắc chống nói quá. Sự cố 07/07 (project 034) vẫn là rủi ro thật. R-16 chỉ đổi cơ chế, không đổi mục tiêu.

### 10.5 Câu hỏi cho chủ bộ skill

1. Bản cài `~/.claude` chưa có evidence-first: đây là chủ ý (pilot chỉ cho Antigravity) hay quên đồng bộ? Câu trả lời quyết định R-15 là "sửa lỗi" hay "ghi chính sách".
2. Giữ hay bỏ bảng tier → band? Nếu giữ, có chấp nhận thứ tự ưu tiên "dự án đứng trên rubric" (R-16a) không?
3. `/admin sâu` có được tính là đồng ý dùng subagent không? Câu này cần trả lời trước R-20.
4. Mode `assess` (R-18) nên nằm trong `research-admin` hay thành skill riêng? Thêm skill riêng sẽ làm tăng áp lực lên ngân sách danh sách skill (F-01).

### 10.6 Nhận định sai đã rút lại — phiên NCKH 14–15/10

Không lấy lại các nhận định dưới đây khi gộp báo cáo. Cột "Đúng là" theo audit C-19 và phần tự kiểm của phiên này.

| Đã nói | Vì sao sai | Đúng là |
|---|---|---|
| "Thuật toán gán nhãn vẫn là T1 … T1 → Q4; muốn Q2 phải đổi head (T2)" | Dự án đã bỏ mapping (C-13, C-15). Loại can thiệp không quyết định quartile; ATSS (CVPR 2020) là phản ví dụ | Đánh giá insight, prior và bằng chứng. Chưa có band (C-19) |
| "Q2 cần ≥3 dataset độc lập nguồn và ≥2 họ detector; thiếu thì trần Q3" | Không có quy định editorial nào như vậy. Đây là mục tiêu thiết kế trong một note cũ, bị nâng thành luật | Độ rộng bằng chứng phải khớp với claim |
| "√2·s phải dự báo mức sàn AP tối ưu" | Định lý chỉ bảo đảm có ứng viên, không nói về positive sau top-k/xung đột hay AP | Hình chữ nhật đóng có cạnh ngắn ≥ √2·s chứa ≥1 điểm lưới (ĐO: đúng); tối ưu AP là câu hỏi thực nghiệm |
| "Cùng diện tích ⇒ hiệu ứng hình dạng chỉ bậc hai" | Cùng kỳ vọng nhưng khác phân phối. Dự án đã sửa ở issue #21 | s×s: P(rỗng) = 0; 2s×s/2: P(rỗng) = 0,5 (ĐO) |
| "Δθ_max = arctan(2δ/L) là giới hạn khả năng xác định góc" | Đây là cận trên độ nhạy khi endpoint lệch vuông góc; lệch 2D thì dùng asin. Không phải sàn sai số | Gọi là "độ nhạy hoặc độ tin cậy góc theo scale" (ĐO: 21,76° ≤ 21,80°; 23,30° ≤ 23,58°) |
| "O2-DETR: phân phối không phụ thuộc kích thước" (nhãn "full-text check") | Kết luận từ grep từ khóa. Eq.1–2 nhân với (Wr, Hr) | Có chuẩn hóa theo kích thước hình học; chưa thấy cổng độ tin cậy theo số pixel tuyệt đối |
| "Phần còn lại của C-17 chỉ là điều kiện theo kích thước pixel" | Kết luận từ abstract của AQE | Chưa kết luận được novelty. AQE còn có loss theo aspect ratio |
| Dùng độ lệch giữa HBB và envelope OBB làm phép đo nhiễu nhãn | OBB được sinh từ HBB (H2RBox-v2) rồi sửa tay, nên không độc lập | Chỉ là độ bất nhất giữa hai biểu diễn, dùng để chọn mẫu audit |
| "CSCWD xử lý cùng triệu chứng, là đối thủ cho hướng A" | CSCWD phát hiện drone (anti-UAV), khác bài toán | Chỉ là prior về cơ chế transfer, cần kiểm lại trên bài toán của dự án |
| "A8 đủ ứng viên mà recall vẫn thấp ⇒ nguyên nhân ở đặc trưng" | Một chỉ số không xác định được nguyên nhân | Cần can thiệp có đối chứng |
| "Ngân sách lỗi cho biết mỗi nguyên nhân chiếm bao nhiêu" | Các nguyên nhân có tương tác, nên không có cách chia duy nhất | "Dấu hiệu lỗi có thể chồng nhau"; dùng factorial |
| "Khoảng 45 nguồn mới" | Không có bảng chọn nguồn để tái dựng | 298 bản ghi, 174 ID arXiv trả về; chưa phải số bài đã đọc |
| "Mỗi file đã qua kiểm bịa … không còn lỗi" | Guard chỉ kiểm nguồn và nhãn | "Không còn claim dữ kiện thiếu nguồn; chưa kiểm suy luận" |
| Memory: "C-19 là self-audit qua 3 subagent" | Audit do một chat khác làm (gpt-6.1-sol, gpt-6-astra); phiên này có 0 lời gọi Agent | Đã sửa memory ngày 15/10 |
| F-17 (tiêu đề ban đầu): "bản cài cũ hơn nguồn 5 tuần" | Suy ra từ ngày sửa file (08/09), không từ nội dung | Bản cài khớp commit `e51683d` (02/10) ở 68/69 skill; chỉ cũ hơn bản evidence-first khoảng 2 ngày |
| (Giả thuyết ban đầu khi chuẩn bị báo cáo này) "Không gọi `ieee-q1-devil-advocate` là một nguyên nhân" | Skill đó dùng chính rubric gây lỗi và không mở nguồn gốc | Thiếu phản biện **độc lập** ở giai đoạn đề xuất (F-22, F-23) |

---

## Nguồn

Đọc ngày 14–15/10/2026:

- Claude Code: [Skills](https://code.claude.com/docs/en/skills) (danh sách, ngân sách, frontmatter, troubleshooting), [Memory](https://code.claude.com/docs/en/memory), [Large codebases](https://code.claude.com/docs/en/large-codebases), [Best practices](https://code.claude.com/docs/en/best-practices), [Hooks](https://code.claude.com/docs/en/hooks)
- [agentskills.io](https://agentskills.io/)
- SkillsBench: [bản hiện tại](https://arxiv.org/abs/2602.12670), [v1](https://arxiv.org/abs/2602.12670v1)
- [Snyk — ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub) (báo cáo của hãng)

Bằng chứng nội bộ: repo `gobal-agent-skills` (commit `f5f653a`); `~/.claude/settings.json`; TMG301 `notes/kusshoes-to-rener-vn/WORK_LOG.md` (C0 → M3), `notes/quy-chuan-ai-dev/PROMPT-KIEN-TRUC-GIAO-VIEC-AI.md`; repo `VoDucNhatku/rener-vn` (commit `07a78c2`, PR #17).

**Giới hạn:** chưa chạy `/skill-doctor`; chưa đọc kỹ thân của mọi skill (đọc kỹ: admin, fullstack-builder, spec-writer, writing-plans, executing-plans, design-web, build-ui, writing-skills; đọc lướt nhóm trí nhớ, scaffold-project); quét thư mục trí nhớ chỉ ở hai workspace, sâu 6 cấp; danh sách skill mất description (phụ lục B) là của một phiên.

---

## Nhật ký đóng góp

| Ngày | Người/phiên | Thay đổi |
|---|---|---|
| 15/10/2026 | Phiên Claude Code (Opus 5.5 → Fable 5.1), dự án TMG301/ReNER-VN | Tạo file: F-01 → F-16, R-01 → R-14, mục 6, phụ lục A–B |
| 15/10/2026 | Như trên, theo yêu cầu chủ bộ skill | Thêm ngữ cảnh "nghiên cứu flow xây dựng web"; thêm mục 0 (vì sao có file), 0.1 (cách đóng góp), 0.2 (cách nghiên cứu để ghi chi tiết) |
| 15/10/2026 | Phiên Claude Code (VS Code, Opus 5.5; một lượt Sonnet 5), dự án NCKH nhóm 7 — **ngữ cảnh nghiên cứu paper**, theo yêu cầu chủ bộ skill | Thêm §10: F-17 → F-28, R-15 → R-25, bảng đối chiếu F cũ (§10.2), nhận định đã rút lại (§10.6). Thêm dòng "Cập nhật" dưới §3.2 và F-14, thêm một hàng và một dòng trỏ ở §6. Phân tích chi tiết ở `notes/phan-tich-phien-nckh-t07-2026-10-15.md`. Chưa sửa skill nào |

---

## Phụ lục A — Kiểm kê skill (ĐO, 15/10/2026)

Cột: số ký tự description · số dòng thân SKILL.md · có `scripts/` · có `references/` · alias deprecated.

| Skill | Ký tự description | Dòng thân | scripts | references | Deprecated | Mất description (phụ lục B) |
|---|---:|---:|:-:|:-:|:-:|:-:|
| `admin` | 367 | 128 |  | ✓ |  | ✓ |
| `ai-cv-forge` | 445 | 476 |  | ✓ |  |  |
| `artifact-manager` | 562 | 141 |  |  |  | ✓ |
| `audit-log` | 288 | 93 | ✓ |  |  |  |
| `backend-engineer` | 1020 | 139 |  |  |  |  |
| `brainstorming` | 421 | 125 |  |  |  | ✓ |
| `build-admin-dashboard` | 275 | 47 |  | ✓ |  | ✓ |
| `build-ui` | 885 | 120 |  | ✓ |  |  |
| `build-ui-component` | 252 | 29 |  |  | ✓ |  |
| `citation-guard` | 370 | 86 |  |  |  |  |
| `claim-forge` | 974 | 199 |  | ✓ |  |  |
| `code-admin` | 357 | 70 |  |  |  | ✓ |
| `code-reviewer` | 322 | 169 |  |  |  |  |
| `code-senior` | 1004 | 131 |  |  |  |  |
| `concept-explainer` | 438 | 94 |  |  |  | ✓ |
| `context-compressor` | 414 | 115 |  |  |  | ✓ |
| `debug-investigator` | 500 | 184 |  |  |  | ✓ |
| `deploy-admin` | 382 | 151 |  |  |  | ✓ |
| `design-ui-direction` | 323 | 26 |  |  | ✓ |  |
| `design-web` | 963 | 141 | ✓ | ✓ |  | ✓ |
| `domain-modeling` | 243 | 185 |  |  |  |  |
| `executing-plans` | 366 | 76 |  |  |  |  |
| `finishing-a-development-branch` | 202 | 141 |  |  |  |  |
| `fullstack-builder` | 392 | 180 |  |  |  | ✓ |
| `hallucination-guard` | 441 | 126 |  |  |  |  |
| `ieee-q1-devil-advocate` | 329 | 81 |  |  |  |  |
| `knowledge-graph` | 902 | 86 | ✓ | ✓ |  |  |
| `knowledge-quiz` | 423 | 83 |  |  |  |  |
| `latex-fix` | 894 | 92 | ✓ |  |  |  |
| `latex-math-renderer` | 304 | 25 |  |  | ✓ |  |
| `latex-tikz-generator` | 333 | 80 |  | ✓ |  |  |
| `learnings-db` | 400 | 130 |  |  |  | ✓ |
| `monitor-setup` | 389 | 169 |  |  |  | ✓ |
| `paper-method` | 848 | 130 |  | ✓ |  |  |
| `paper-read` | 970 | 103 |  | ✓ |  |  |
| `paper-storytelling` | 554 | 141 |  | ✓ |  |  |
| `paper-submission` | 641 | 100 |  |  |  | ✓ |
| `paper-synthesize` | 879 | 132 |  |  |  |  |
| `paper-to-notebook` | 841 | 90 | ✓ | ✓ |  |  |
| `paper-triage` | 812 | 122 |  |  |  |  |
| `project-memory` | 386 | 132 |  |  |  | ✓ |
| `receiving-code-review` | 203 | 151 |  |  |  |  |
| `requesting-code-review` | 218 | 139 |  |  |  |  |
| `research-admin` | 652 | 233 |  |  |  | ✓ |
| `reuse-checker` | 237 | 22 |  |  | ✓ |  |
| `review-frontend` | 889 | 97 |  |  |  |  |
| `rollback-manager` | 339 | 119 |  |  |  | ✓ |
| `run-on-modal` | 737 | 90 | ✓ | ✓ |  |  |
| `scaffold-course-platform` | 223 | 56 |  | ✓ |  | ✓ |
| `scaffold-project` | 989 | 178 | ✓ | ✓ |  |  |
| `security-review` | 1012 | 76 |  |  |  | ✓ |
| `self-evaluator` | 411 | 119 |  |  |  | ✓ |
| `ship-validator` | 357 | 148 |  |  |  | ✓ |
| `skill-router` | 212 | 23 |  |  | ✓ | ✓ |
| `spec-writer` | 366 | 208 |  |  |  | ✓ |
| `study-forge` | 922 | 271 | ✓ | ✓ |  | ✓ |
| `study-tutor` | 355 | 111 |  |  |  | ✓ |
| `style-humanizer` | 425 | 108 |  |  |  | ✓ |
| `tdd-enforcer` | 507 | 256 |  |  |  | ✓ |
| `test-framework` | 160 | 59 | ✓ |  |  | ✓ |
| `token-budget` | 580 | 72 |  |  |  | ✓ |
| `understand-codebase` | 381 | 56 |  |  |  | ✓ |
| `using-git-worktrees` | 221 | 147 |  |  |  | ✓ |
| `verification-before-completion` | 258 | 121 |  |  |  | ✓ |
| `vi-translate` | 774 | 136 |  |  |  | ✓ |
| `web-admin` | 241 | 30 |  |  | ✓ | ✓ |
| `workbench-admin` | 254 | 35 |  |  | ✓ | ✓ |
| `writing-plans` | 242 | 151 |  |  |  | ✓ |
| `writing-skills` | 199 | 163 |  |  |  | ✓ |

## Phụ lục B — Skill hiện không có description trong danh sách của phiên này (QUAN SÁT, 15/10/2026)

Danh sách skill mà phiên này nhận được hiển thị các skill dưới đây chỉ bằng tên hoặc dòng tiêu đề, không có câu "dùng khi nào". Theo docs, Claude Code bỏ description của skill **ít được gọi nhất** trước khi danh sách vượt ngân sách (khoảng 1% cửa sổ ngữ cảnh). Phiên khác, máy khác hoặc model có cửa sổ khác có thể cho kết quả khác.

**37 skill:** `admin`, `artifact-manager`, `brainstorming`, `build-admin-dashboard`, `code-admin`, `concept-explainer`, `context-compressor`, `debug-investigator`, `deploy-admin`, `design-web`, `fullstack-builder`, `learnings-db`, `monitor-setup`, `paper-submission`, `project-memory`, `research-admin`, `rollback-manager`, `scaffold-course-platform`, `security-review`, `self-evaluator`, `ship-validator`, `skill-router`, `spec-writer`, `study-forge`, `study-tutor`, `style-humanizer`, `tdd-enforcer`, `test-framework`, `token-budget`, `understand-codebase`, `using-git-worktrees`, `verification-before-completion`, `vi-translate`, `web-admin`, `workbench-admin`, `writing-plans`, `writing-skills`.

Không nằm trong repo nhưng có trong `~/.claude/skills`: thư mục `synced/` (skill đồng bộ từ claude.ai) và 2 symlink sang `~/.codex/skills` (`latex-fix`, `study-forge`).
