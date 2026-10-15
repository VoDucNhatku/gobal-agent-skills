# Pilot checkpoint — 2026-10-04

Current update 2026-10-05: **Task 10b source/completion FAIL; pilot đã gỡ**.
Lượt mới trong ảnh a5b534da lại thay official-document evidence bằng runtime paths và
báo Unverified không có. Activity thu gọn nên không kết luận không browse, không có
tool hay exact body/version. Không rollout 69 skill hoặc publish GitHub.

## Cleanup sau Task 10b — state hiện tại

- Precheck: exact 9 payload/ownership hashes khớp manifest cũ; uninstall dry-run exit 0,
  no writes. Dòng validated 0 của uninstall dry-run không phải xác minh 9 payload files.
- Real uninstall: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Pilot -Uninstall`,
  exit 0, 9 managed operations. Transaction:
  `C:\Users\Asus\.gemini\config\.gobal-agent-skills\transactions\577b1245-aae0-46f1-9247-5317f7166447`.
- Static verification 12:49:51.139100 UTC (19:49:51 Việt Nam): remaining managed files 0,
  ownership files 0, journal committed, **70 current SKILL.md entries**.
- Immediate before/after protected six-root inventories and existing MCP/settings hashes
  identical. Existing skills/rules, cv-maker and MCP untouched. Keep backups/state and
  source payload; no broad deletion. Committed uninstall is not undone by `-Recover`.
- Source-class/lane correction is prepared locally; it is not installed or Gemini-verified.

## Task 10c — local candidate checks (not product pass)

13:05 UTC: fresh full suite exit 0, 165 tests / 145.387s / OK; canonical 69 skills /
693 PASS / 0 FAIL/WARN. Generator drift check, both native/pilot quick_validate with
UTF-8, ledger structural check and nine-file pilot dry-run pass. Manifest SHA256:
`5f96b7f7c674e3a1ae00d1bf249847534ef4ef05b9502fb613a5377b2894d018`.
Preliminary Codex source/fallback tests are separate from Gemini; final Quick run used
one round / two queries / two opens / zero workers, but opened-source characters
25,729 > design ceiling 20,000 (overrun recorded, no further opens). No full budget,
cost/latency or product pass. Protected snapshot recheck unchanged; pilot remains absent.
Details and remaining human-ready candidate gate are in the evaluation note.

## Task 10b — lịch sử cài lại unmodified pilot lúc 12:30:20 UTC

- Fresh full suite: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`,
  exit 0, **165 tests / 147.805s / OK**, không skip. Các drift messages cuối là output
  của negative fixture tests, không phải generated distribution hiện tại bị lệch.
- Canonical validator: 69 discovered/validated, 693 PASS, 0 FAIL/WARN, exit 0.
- Generator `--check`: distribution already matches, exit 0. Không generate lại payload.
- Ledger example: valid true / semantic_verified false, exit 0; không chứng minh nguồn.
- Sau khi làm rõ hướng dẫn new conversation, documentation tests chạy lại: 4 / OK.
- Dry-run pilot: 9 validated files, no writes, exit 0.
- Real install: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Pilot`,
  exit 0, 9 managed operations, **không Force**. Transaction/backup:
  `C:\Users\Asus\.gemini\config\.gobal-agent-skills\transactions\1c366e98-95e8-4e4d-abc1-93c964f78457`.
- Immediate pre/post protected path+SHA256 inventories ở sáu current/legacy/editor roots,
  cùng hai MCP files hiện hữu: exact unchanged. Chỉ loại trừ đúng pilot payload khỏi
  phép so sánh; installer state/backup là tài nguyên quản lý riêng, không phải MCP.
- Static check 12:30:20 UTC: exact 9 installed hashes và ownership bằng source manifest,
  8 skill/resource + 1 rule; schema 1/scope pilot; journal committed. Strict parser cho
  installed skill có đúng name/description, folder/name khớp; rule strict YAML có
  trigger always_on. Marker skill/rule đúng vị trí. Current SKILL.md count **70 → 71**.
- Pilot manifest SHA256 tại thời điểm cài giữ nguyên:
  `c3404f5feec5f5787591ce455d4a300316d7dcff4e482b545b70d8151d7c80be`.
- Khi cài này chưa sửa source policy/code hoặc guide chưa rõ ownership. Namespaced
  always_on rule có thể ảnh hưởng mọi chat trong cửa sổ thử; đã gỡ sau scoring như trên.

Human đã trả screenshot/answer của lượt riêng; source/completion fail. Không yêu cầu
thử lại payload không đổi. Một candidate-pilot mới cần cửa sổ thử riêng và activity;
một lượt pass vẫn không chứng minh mọi lane, latency/cost hay miễn nhiễm hallucination.

## Lịch sử cài 2026-10-04 (không phải lần reinstall)

Các mục bên dưới, kể cả chỉ dẫn thử/gỡ, là checkpoint lịch sử trước lần cleanup/reinstall,
không mô tả state hiện tại. Xem đánh giá ở
`notes/evaluation-antigravity-pilot-2026-10-05.md`; không dùng chúng để chấm Task 10b.

## Đã quan sát

- App executable: Antigravity IDE 2.0.3; chưa quan sát invoke trong chat.
- 12:54:26 UTC (19:54:26 giờ Việt Nam): real command
  `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Pilot`
  chạy từ `D:\Lich cong viec\gobal-agent-skills`, exit 0, 9 managed file operations.
- Target: `C:\Users\Asus\.gemini\config\skills\admin-evidence-pilot\` và
  `C:\Users\Asus\.gemini\config\rules\admin-evidence-pilot.md`.
- Transaction ID: `48af46eb-6a35-4c6e-b672-383a78bc672b`; backup/journal nằm trong
  `C:\Users\Asus\.gemini\config\.gobal-agent-skills\`. Journal committed, ownership
  schema 1/scope pilot, exact 9 hashes khớp manifest và bytes cài.
- Static post-check 12:54:58 UTC exit 0: SKILL chỉ name/description, tên khớp folder,
  rule trigger always_on; marker skill/rule tách nhau; exact inventory 8+1.
- Current global skill count tăng **70 → 71** (69 cũ + cv-maker + pilot).
- Trước/sau đối chiếu path+SHA256 inventory của mọi file ngoài pilot trong sáu roots
  current/legacy/editor và hashes hai MCP files hiện hữu: **unchanged**. `/admin` cũ,
  cv-maker và legacy skills/rules giữ nguyên. Current rules directory được tạo mới để
  chứa rule pilot; không có rule hiện hữu bị thay. Installer state/lock/journal là file
  mới ngoài payload, không phải MCP configuration.
- Snapshot chi tiết local nằm trong `.tmp/antigravity-profile-baseline.json` và
  `.tmp/antigravity-profile-after-pilot.json`, ignored, không đưa secret/config content
  lên GitHub. Bộ kiểm trước cài: 163 tests đạt, xem report chính.

## Chưa quan sát / không được coi pass

Discovery trong menu `/`, skill-body/rule activation, Gemini đọc tài liệu chính thức,
bác bỏ tiền đề sai, chống injection, citation support, product distinction, uncertainty,
budget thực tế: **unobserved**. Chưa có model/reasoning/answer/tool trace của lượt canary.
Mười hai fixture vẫn not_run; không có kết quả benchmark token/latency/cost.

Pilot hiện còn cài để người dùng thử. Rule always_on có thể ảnh hưởng các chat khác
khi còn cài; giữ cửa sổ thử ngắn, lưu trace rồi gỡ. Không thay toàn bộ 69 skill hoặc
publish GitHub trong checkpoint này. Không tự giả định thứ tự ưu tiên current/legacy.

## Bước cần người dùng

Mở chat mới, chọn skill thật trong menu, chạy prompt trong `docs/ANTIGRAVITY-PILOT.md`,
trả full answer và expanded activity/tool trace cùng model/reasoning. Không chép marker
vào prompt. Nếu menu không có pilot, ghi fail discovery và chẩn đoán từ log thật.

Gỡ sau khi ghi bằng chứng:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\Lich cong viec\gobal-agent-skills\scripts\install-antigravity.ps1' -Pilot -Uninstall
```

Đây chưa phải uninstall đã thực hiện trên profile thật. Installer từ chối drift nếu
file đã sửa; không dùng Force để bỏ qua khi chưa xem diagnostic/backup. Recovery dùng
`-Pilot -Recover` cho pending transaction. Không xóa rộng `.gemini`/skills/rules.
