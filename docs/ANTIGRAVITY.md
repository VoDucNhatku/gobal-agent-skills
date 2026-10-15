# Cài và kiểm chứng GOBAL trong Antigravity IDE

Mục tiêu là Antigravity IDE, không phải Claude Code hay Gemini/Antigravity CLI.
`.claude/skills` là nguồn phát triển; bản IDE được sinh ở `skills/` và `rules/`.
Đừng bảo agent copy `.claude/skills` rồi tự suy ra nó đã xuất hiện trong menu.

## Trạng thái bản này

Bản đang triển khai: build/validator và installer phải qua kiểm thử; pilot IDE là gate
trước thay toàn bộ 69 skill. Chưa có kết quả product gate thì không gọi đây là bản đã
chạy đúng trên IDE. Native plugin và Direct/Global là hai cách cài cần thử riêng.

Checkpoint 2026-10-04: GitHub main chưa có bản này; hướng dẫn pilot hiện áp dụng cho
checkout local đang phát triển, không phải một clone mới từ main. Trên máy đang làm,
repo là `D:\Lich cong viec\gobal-agent-skills`, branch `feat/antigravity-evidence-first`.
Chỉ dùng lệnh bên dưới khi checkout thực sự có `scripts/install-antigravity.ps1`,
`pilot/manifest.json` và đã qua kiểm tra. Đừng suy diễn clone thành công là tải được bản
mới. Sau khi product gate đạt và SHA remote được xác nhận, cập nhật checkpoint này.

## 1. Tải repo và chọn đúng host

Mở PowerShell, chọn thư mục lưu repo:

```powershell
git clone https://github.com/VoDucNhatku/gobal-agent-skills.git
Set-Location .\gobal-agent-skills
git status --short
```

Nếu đã có repo, kiểm tra local changes trước khi `git pull --ff-only`. Không dùng
`reset --hard` để chữa lỗi tải. Lỗi Git, parser, dependency và discovery là các lỗi khác
nhau; giữ nguyên command/exit code/thông báo thật, không suy diễn lý do.

Vị trí IDE chính thức:

- Workspace: `<workspace>/.agents/skills/<skill>/`.
- Global: `~/.gemini/config/skills/<skill>/`; legacy `~/.gemini/antigravity/skills/`
  cũng được hỗ trợ. Kiểm tra trùng tên trước khi thay bản đang dùng.
- Global modular rules: `~/.gemini/config/rules/*.md`, cần frontmatter `trigger` hợp lệ.

Trên Windows, `~` là user profile đang chạy IDE. Không nhầm `.antigravity-ide`,
`.claude`, CLI profile hoặc một tài khoản Administrator khác với profile đang hoạt động.
[Tài liệu skills](https://antigravity.google/docs/skills?tab=ide),
[tài liệu rules](https://antigravity.google/docs/rules?tab=ide).

## 2. Kiểm tra repo trước cài

Chỉ phần phát triển/validation cần Python 3.11+ và PyYAML; copy bundle và menu IDE không
cần cài Python. Worker thực thi có dependency riêng, không tự cài chúng khi chưa cần.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts\build_antigravity.py --check
.\.venv\Scripts\python.exe .claude\skills\test-framework\scripts\test_skills.py --skills-root .claude\skills --host canonical --json
.\.venv\Scripts\python.exe skills\test-framework\scripts\test_skills.py --skills-root skills --host antigravity --json
```

Không có skill, root sai, filter sai, YAML/resource/hash lỗi phải trả exit khác 0.
Số 69 phải khớp danh sách tên trong `config/antigravity-skills.txt`; đếm 69 thư mục
không đủ nếu có tên sai hoặc resource thiếu. `--check` không tạo/sửa output.

## 3. Pilot có thể gỡ, trước khi thay 69 skill

Installer giai đoạn đầu chỉ cho phép pilot. Full rollout chưa được mở chỉ vì static
tests xanh; cần chấm IDE canary trước.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Pilot -DryRun
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Pilot
```

Pilot chỉ thêm `admin-evidence-pilot` và một rule namespaced ngắn `always_on`; không sửa
`/admin`, skill hiện hữu, `cv-maker`, rule ngoài bộ hay MCP. Rule tạm thời có hiệu lực
ở các chat khác khi còn cài, nên chỉ giữ trong cửa sổ thử rồi gỡ.
Không dùng `-Force` như cách mặc định để bỏ qua collision; đọc diagnostic và backup trước.

Mở chat mới trong IDE, kiểm Customizations và menu `/`, chọn `/admin-evidence-pilot`.
Dán prompt của case `IDE-FALSE-PREMISE` trong `evals/admin-research/cases.yml`.
Ghi version app, model/reasoning, câu trả lời đầy đủ và mở rộng activity/tool trace.
Không chép marker vào prompt. Marker chỉ giúp nhận diện; trace mới kiểm được nguồn body,
rule và thao tác đọc tài liệu. Screenshot câu trả lời không chứng minh budget hoặc activation.

Sau khi lưu bằng chứng, gỡ:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Pilot -Uninstall
```

Nếu giao dịch bị dừng đột ngột, đọc vị trí journal mà installer báo và dùng `-Pilot -Recover`.
Không xóa cả `.gemini`, `skills` hay `rules` để chữa lỗi. Installer phải từ chối phục hồi
đè lên file đã bị người dùng sửa sau transaction; trường hợp đó cần kiểm từng target.

## 4. Sau khi pilot đạt

Chỉ mở full installer sau khi đủ gate trong plan: đủ generated rules/resources,
install/update/uninstall/recovery trên profile tạm đạt, nguồn nào chạy được chứng minh,
baseline profile thật được kiểm kê và có backup. Full bundle gồm đúng 69 skill quản lý;
`cv-maker` là dữ liệu ngoài bộ phải được giữ nguyên.

Không để hai bản cùng tên ở current/legacy/plugin/workspace rồi suy đoán thứ tự ưu tiên.
Chỉ xử lý bản trùng đã xác định thuộc bộ này, có backup và theo từng đường dẫn cụ thể.
Không công bố GitHub đã cập nhật khi chưa kiểm SHA remote.

## 5. Native plugin — kiểm riêng

Repo root có `plugin.json`, `skills/`, `rules/`. Tài liệu IDE hướng dẫn global plugin
ở `~/.gemini/config/plugins/<name>/` hoặc workspace `.agents/plugins/<name>/`, rồi kiểm
Customizations. `/plugin install` nằm trong hướng dẫn interactive TUI; không coi đó
là lệnh standalone IDE đã kiểm. Không đồng thời cài Direct và Plugin cùng tên.
[Tài liệu plugins](https://antigravity.google/docs/plugins?tab=ide).

## 6. `/admin` mới làm gì?

- Yêu cầu sáng tạo/chuyển đổi/file local: làm thẳng, không chạy nghiên cứu web mặc định.
- Tra cứu factual: đọc đoạn nguồn thật, ưu tiên primary và nguồn phù hợp thời điểm/phạm vi.
- Nghiên cứu lớn: tách claim, kiểm nguồn gốc trùng, phản chứng và mâu thuẫn; tổng hợp bằng
  tiếng Việt, citation ngay cạnh phát biểu và không biến `NEI` thành chắc chắn.
- `admin nhanh`: không subagent; hết budget thì nói rõ giới hạn. `admin sâu`: tăng độ sâu
  trong khả năng host, không tự đổi model hoặc giả vờ có công cụ.
- Kiểm thử phát hành không chạy mỗi request. Trần thao tác là chính sách ban đầu, không
  phải số tiết kiệm hay tốc độ đã đo.

## 7. Nếu không thấy slash skill

Kiểm theo thứ tự: đúng host/profile → bundle/hash/parser → đúng thư mục/name → duplicate
roots → chat mới/Customizations → activity log. Không sửa YAML ngẫu nhiên hoặc copy bộ
Claude sang mọi thư mục. Rule thiếu `trigger` có thể bị bỏ qua; skill file hợp lệ vẫn
chưa chứng minh được đăng ký hoặc invoke. Báo chính xác bước đã đạt và bước chưa quan sát.

Không thể bảo đảm model hết hallucination từ một prompt hoặc một canary. Kết quả thử nằm
trong `notes/verification-antigravity-*.md`; fixtures `not_run` không phải regression pass.
