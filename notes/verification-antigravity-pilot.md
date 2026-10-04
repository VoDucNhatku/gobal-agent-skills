# Pilot checkpoint — 2026-10-04

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
