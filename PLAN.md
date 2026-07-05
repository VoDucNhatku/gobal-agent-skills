# Workbench v2 — Kế hoạch thiết kế lại (resumable)

> File này là BỘ NHỚ KẾ HOẠCH. Nếu phiên bị limit, phiên sau đọc file này + `notes/INDEX.md`
> (không có) → đọc `~/.claude/skills/PLAN.md` để tiếp tục không mất ngữ cảnh. Cập nhật phần
> "Tiến độ" sau mỗi bước hoàn thành.

## Bối cảnh & yêu cầu người dùng (chốt 2026-06-28)
Người dùng có bộ **Workbench** global ở `~/.claude/skills/` (11 skill research đã xong + nhánh web/UI
còn stub). Yêu cầu: **thiết kế lại / trộn / thêm** dựa trên các skill nổi tiếng, làm MỘT LẦN dùng luôn.

**Tiền đề xuyên suốt (BẮT BUỘC):** tiết kiệm token NHƯNG hiệu suất cao nhất — qua thiết kế tối ưu
từng tác vụ (progressive disclosure 3 tầng + 4 cơ chế AIL + chặn N lớn). Mọi skill phải tuân.

**NGUYÊN TẮC NGÔN NGỮ (chốt 2026-06-28 — áp cho TẤT CẢ skill v2):**
- TOÀN BỘ nội dung skill viết bằng TIẾNG ANH: SKILL.md body, frontmatter, references, scripts,
  comment, JSON key, đường dẫn, tên định danh, task spec mà orchestrator giao cho subagent.
  → để AI không bị lẫn ngữ cảnh khi suy luận.
- CHỈ prose GIAO TIẾP với người dùng mới dịch sang TIẾNG VIỆT: câu hỏi làm rõ, kế hoạch, preview
  trong chat, báo cáo cuối. (Đây đã là `workbench-conventions.md` §1 — giữ nguyên, không đổi.)
- ORCHESTRATOR SONG NGỮ: user chat tiếng Việt → orchestrator HIỂU tiếng Việt → DỊCH/viết task spec
  giao cho subagent bằng TIẾNG ANH → nhận kết quả → BÁO CÁO lại user bằng tiếng Việt.
- Trong artifact/output sản phẩm (web, doc): ngôn ngữ hiển thị theo project của user, không ép.

**NGUYÊN TẮC THIẾT KẾ LẠI (chốt 2026-06-28 — quan trọng nhất):**
GIỮ NGUYÊN bộ Workbench 11 skill đã hoàn thiện làm NỀN. KHÔNG đập đi xây lại. Chỉ:
(a) THÊM số ít skill thật sự thiếu (web/UI flagship, code-senior, có thể understand-codebase);
(b) TỐI ƯU thêm cái hay nhất học từ 8 repo vào skill/orchestrator hiện có;
(c) Thêm lệnh ngắn (alias) cho dễ gọi.
KHÔNG làm quá nhiều, KHÔNG lan man. Mỗi thay đổi phải trả lời được "cái này hay hơn ở đâu, đáng token không".
Ưu tiên: chỉ lấy 20% tinh túy tạo 80% giá trị; bỏ qua phần rườm rà của các repo.

### Mục tiêu người dùng (5)
1. **Taste / thẩm mỹ** — skill cho (a) WEB: biết thiết kế giao diện thế nào; (b) MARKDOWN: chỉ
   THAM KHẢO cách trình bày, KHÔNG tốn token vào thiết kế nặng. Tham khảo `taste-skill` + `ui-ux-pro-max`.
2. **Web skill là TRỌNG TÂM** — phải: hiểu thiết kế web/giao diện; project nhỏ (vd web tóm tắt kiến
   thức) thì GỌI THÊM skill research rồi tự thiết kế; tự học kiến trúc thiết kế mới từ web khác / mô
   tả người dùng; **BẮT BUỘC tương tác hỏi người dùng** lấy thông tin cụ thể, KHÔNG đoán mò — nhưng
   hiểu ngữ cảnh, hỏi đúng trọng tâm (agent tự quyết hỏi gì).
3. **Workflow** — học `superpowers` (Brainstorm→Plan→TDD→Execute→Review) + `Understand-Anything`
   (codebase → knowledge graph, multi-agent).
4. **Cách gọi skill rõ ràng, cá nhân hóa** — học `mattpocock/skills` + GStack: lệnh ngắn dễ nhớ
   (vd /plan, /tdd, /ship) + orchestrator. CẢ HAI.
5. **Code chuẩn senior + chống sửa nhầm** — học `addyosmani/agent-skills` (verification gates,
   anti-rationalization). Cơ chế chống: chạy code sai, sửa nhầm 1 đoạn thành sửa cả mã nguồn.
   Theme-neutral: agent tự đọc project để biết ngôn ngữ (TS/React/Next, Python/ML, Backend/API).
   **Agent chủ phải HIỂU CHI TIẾT công việc trước khi làm.**

### Quyết định người dùng
- Loại code: web/FE + Python/ML + backend/API → **theme-neutral, tự suy ra ngôn ngữ**.
- Gọi skill: **lệnh ngắn + orchestrator**.
- Phạm vi: **tôi (Claude) tự quyết số skill**, trộn + thêm + chỉnh. Làm 1 lần dùng luôn.

## Các repo cần nghiên cứu (KIỂM CHỨNG — số star user đưa có thể phóng đại)
1. obra/superpowers — workflow Brainstorm→Plan→TDD→Execute→Review
2. anthropics/skills — chuẩn chính thức (đã có dữ liệu phiên trước)
3. mattpocock/skills — PRD→plan, TDD, triage-debug, gọi skill gọn
4. garrytan/gstack — 25 skills, slash command /plan-*, /design-html, /qa, /ship, /canary-deploy
5. nextlevelbuilder/ui-ux-pro-max-skill — design intelligence
6. Egonex-AI/Understand-Anything — codebase → knowledge graph, multi-agent, dashboard
7. addyosmani/agent-skills — 22 lifecycle skills, verification gates, anti-rationalization
8. Leonxlnx/taste-skill — chống UI nhàm chán, layout/typography/motion/spacing
(+ tra internet: token-economy best practices cho skill)

## RESUME (nếu phiên bị ngắt)
- Workflow nghiên cứu đang chạy: runId `wf_33ae306d-388`
  - scriptPath: `C:\Users\DELL\.claude\projects\d--CPV-VIP\5bd7dd15-03cc-4f04-a43e-f9a95dee3633\workflows\scripts\research-skill-ecosystem-wf_33ae306d-388.js`
  - output khi xong: `tasks\wt41aua4d.output` (đọc `result.repoFindings / .tokenBest / .architecture`)
- Phiên trước đã build xong 6 stub research + 5 builder script + README + artifact v1 (xem [[workbench-suite-completed]]).

## YÊU CẦU LƯU FINDINGS (user nhấn mạnh 2026-06-28)
BẮT BUỘC: ghi findings chi tiết từ 8 repo (kể cả thông tin tưởng không cần) vào MỘT file tham khảo
`~/.claude/skills/references/ecosystem-research.md` — đọc on-demand, KHÔNG nằm trong context thường
trực (progressive disclosure → tiết kiệm token). Mục đích: sau này resume / thiết kế lại thì có
sẵn tư liệu, không phải nghiên cứu lại. Ghi NGUYÊN VĂN findings (repo, star thật, skill list,
workflow pattern, cơ chế token/safety, ideas-to-steal, quotes) khi workflow `wt41aua4d` xong.

## TIẾN ĐỘ
- [x] Chốt yêu cầu với user (AskUserQuestion)
- [x] Ghi PLAN.md khởi đầu (file này)
- [~] Nghiên cứu 8 repo + token best-practices (workflow `wf_33ae306d-388` đang chạy)
- [x] Ghi findings NGUYÊN VĂN vào `references/ecosystem-research.md` (527 dòng) ✓
- [x] Chốt kiến trúc v2 vào PLAN.md + user DUYỆT (2026-06-28): "OK làm hết theo thứ tự đề xuất"
- [ ] Viết /design (flagship) ← ĐANG LÀM
- [ ] Viết /code, /ui, /review-fe, /understand
- [ ] Nâng orchestrator + alias 10 skill cũ
- [ ] Test scripts + kiểm định + artifact
- [ ] Chốt kiến trúc Workbench v2 (danh sách skill cuối + lệnh ngắn + handoff) → ghi vào PLAN.md
- [ ] Viết/sửa skill (taste, ui/web, understand-codebase, code-senior, workflow orchestrator…)
- [ ] Test các builder script mới
- [ ] Kiểm định (desc ≤1024, body <500, compile)
- [ ] Artifact trình bày style mới

## Phát hiện về hiện trạng (đã rà 2026-06-28)
- 11 skill research: ĐÃ XONG, tốt → GIỮ NGUYÊN.
- Nhánh web/UI: 5 stub (`design-ui-direction`, `build-ui-component`, `build-admin-dashboard`,
  `review-frontend`, `scaffold-course-platform`) đều RỖNG (chỉ có references/assets), và gắn cứng
  chủ đề "course platform". → Đây là chỗ làm web flagship THEME-NEUTRAL cho user.
- `~/.claude/rules/frontend-aesthetics.md`: ĐÃ TỐT (anti-slop checklist, type/color/motion, review
  rubric). → TÁI DÙNG làm "taste rule", KHÔNG viết lại. Đây chính là taste-skill content có sẵn.
- Hướng web (theo yêu cầu user): skill web phải (a) hiểu thiết kế giao diện; (b) project nhỏ gọi
  thêm research skill lấy content rồi tự thiết kế; (c) tự học kiến trúc mới từ web khác/mô tả;
  (d) BẮT BUỘC hỏi user đúng trọng tâm, không đoán mò.

## KIẾN TRÚC WORKBENCH v2 — CHỐT (2026-06-28, sau research wf_33ae306d-388)

Findings nguyên văn: `~/.claude/skills/references/ecosystem-research.md`.
Star (theo trang hiển thị lúc fetch): superpowers 240k · anthropic/skills 156k · mattpocock 148k ·
gstack 117k · ui-ux-pro-max 97k · Understand-Anything 68k · addyosmani 67k · taste 52k.

### GIỮ NGUYÊN 10 skill research (đã tốt)
paper-read, paper-method, paper-synthesize, reading-triage, knowledge-graph, vi-translate,
paper-to-notebook, run-on-modal, latex-fix, audit-log. → chỉ thêm ALIAS lệnh ngắn (frontmatter).

### THÊM 5 skill (thay 5 stub web rỗng + 1 mới), theme-neutral, body tiếng Anh
1. **design-web** (`/design`) — FLAGSHIP. Thay design-ui-direction.
   Modes: direction (default) | learn (học kiến trúc từ web/URL khác hoặc mô tả) |
   content-site (gọi reading-triage→paper-read/synth lấy content rồi thiết kế) | directions N.
   - Taste rules: tái dùng `frontend-aesthetics.md` + artifact-design two-pass loop.
   - GATE BẮT BUỘC: hỏi user 2-3 câu chặn (blocking) trước khi thiết kế, KHÔNG đoán mò; agent tự
     quyết hỏi gì (hiểu ngữ cảnh). Self-review-for-slop trước khi present (superpowers).
   - Knowledge nặng để trong CSV on-disk (palettes/type-pairings/style-archetypes/anti-slop-bans)
     + `scripts/design_search.py` (BM25+regex top-3) → coverage sâu, gần như 0 token thường trực.
   - Output: HTML Artifact preview + `notes/design-<slug>.md` (locked source-of-truth).
2. **build-ui** (`/ui`) — gộp build-ui-component + build-admin-dashboard + scaffold-course-platform.
   Modes: component | page | admin (CRUD role-gated, authz server-side) | scaffold (theme-neutral).
   Đọc `notes/design-<slug>.md` đã khóa làm nguồn token.
3. **review-frontend** (`/review-fe`) — populate stub: §1/§8 slop rubric pass/fail + a11y + token
   consistency. Modes: audit (default) | fix (sửa surgical bằng Edit, không rewrite).
4. **code-senior** (`/code`) — theme-neutral, tự suy ngôn ngữ từ project.
   Modes: implement (understand→plan minimal-diff→edit surgical→verify) | debug (reproduction-first:
   phải có lệnh fail đỏ TRƯỚC khi đặt giả thuyết — mattpocock) | review (diff-only, severity-coded).
   - ANTI-RUNAWAY-EDIT: ưu tiên Edit hơn Write; read-before-edit staleness; old_string tối thiểu
     duy nhất; SMALL-FIX-STAYS-SMALL (sửa nhỏ chạm nhiều dòng/cả file → STOP, re-scope).
   - Verification gate + anti-rationalization table (addyosmani): definition-of-done, không tự bịa.
5. **understand-codebase** (`/understand`) — NEW (Understand-Anything). Token-bounded KG của codebase.
   Modes: scan (default, incremental) | explain <file|fn> | onboard | diff (impact analysis).
   - Offload merge sang script (như kg_builder), KHÔNG đọc master graph ngược vào context.

### NÂNG workbench-orchestrator (giữ core decompose→fan-out→synthesize)
Thêm lifecycle GATE (không phải advice): BRAINSTORM → PLAN → (UNDERSTAND) → BUILD → VERIFY → REVIEW.
- BRAINSTORM: việc build phi-tầm-thường phải trình design + user duyệt TRƯỚC khi code; self-review
  spec tìm placeholder/mâu thuẫn trước. Next chỉ được là PLAN.
- PLAN: ghi spec ngày-tháng vào notes/design-<slug>.md, chia vertical slice (mattpocock).
- Mỗi worker nêu "skill kế tiếp DUY NHẤT được phép" (superpowers terminal-state) = refusal-gate.
- ORCHESTRATOR SONG NGỮ: user VN → hiểu → task spec EN cho subagent → báo cáo lại VN.

### LỆNH NGẮN (command map — user-invoked entry verbs)
/understand /triage /read /method /synth /kg /translate /notebook /modal
/design /ui /review-fe /code /latex /audit · /wb (orchestrator)
RULE chống đệ quy: lệnh ngắn do user gọi; một lệnh user-invoked có thể gọi worker (model-invoked)
nhưng KHÔNG gọi lệnh user-invoked khác. Chỉ orchestrator là multi-agent dispatcher.

### Tổng: 10 giữ + 5 mới = 15 skill. Mỗi thay đổi đều "hay hơn ở đâu" rõ ràng, không lan man.
