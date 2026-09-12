#!/usr/bin/env python3
"""Build a project skeleton (dirs + git governance files) from a compact JSON spec.

The calling skill emits only the spec; this script owns every boilerplate file so the
model never hand-writes .gitignore / CODEOWNERS / CONTRIBUTING / PR-template text.

Idempotent by design: an existing file is never overwritten, only reported as skipped.
.gitignore is the one exception -- missing lines are appended inside a marked block.

Usage:
    python scaffold_project.py <spec.json> [--dry-run]

Spec shape:
    {
      "project_name": "aion-lab",
      "profile": "research|web|agent|mixed",
      "root": ".",
      "team_size": 8,
      "visibility": "private|public",
      "default_branch": "main",
      "owners": {"apps/web": "@alice @bob"},
      "extra_dirs": ["services/worker"],
      "extra_ignore": ["*.parquet"]
    }

Output: a JSON report on stdout {created, skipped, dirs, warnings}.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Windows consoles default to cp1252 and would crash on Vietnamese diacritics in the report.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):  # pragma: no cover - very old interpreters
    pass

HERE = Path(__file__).resolve().parent
PROFILES_PATH = HERE / "profiles.json"
IGNORE_MARK_START = "# --- scaffold-project (managed block) ---"
IGNORE_MARK_END = "# --- end scaffold-project ---"


# --------------------------------------------------------------------------- templates

README_TMPL = """# {{PROJECT}}

> Bộ khung dự án do `scaffold-project` sinh ngày {{DATE}} — hồ sơ `{{PROFILE}}`, quy mô {{TEAM}} người.

## Bắt đầu (dành cho người mới vào nhóm)

```bash
git clone <URL-repo>
```

Sau đó đọc `CONTRIBUTING.md` **trước khi commit lần đầu**. Ba việc bắt buộc:

1. Sao chép `.env.example` thành `.env` và điền khóa của riêng bạn. **Không bao giờ commit `.env`.**
2. Dữ liệu thô không nằm trong repo — xem `data/raw/manifest.md` để biết lấy ở đâu.
3. Làm việc trên nhánh riêng, không commit thẳng vào `{{BRANCH}}`.

## Bản đồ thư mục

Mỗi thư mục trả lời được ba câu: **ai sở hữu · có vào git không · người hay máy sinh ra**.

{{DIRTABLE}}

Ký hiệu: `git=track` là commit bình thường · `git=ignore` là **cố ý** không đưa lên GitHub
(nhị phân, nhạy cảm, hoặc sinh lại được bằng script).

## Quy tắc không thương lượng

| Không làm | Vì sao |
|---|---|
| Commit `.env` hay khóa API | Đã push là nằm vĩnh viễn trong lịch sử git; phải hủy khóa và tạo lại |
| Commit file nhị phân (PDF, xlsx, checkpoint) | Git không merge được, repo phình và không xóa lại được |
| Commit thẳng vào `{{BRANCH}}` | Mất khả năng review, nhánh chính dễ hỏng |
| Sửa file trong `data/raw/` | Dữ liệu gốc là bất biến, dùng để đối chiếu khi sai |
| Để output AI sinh lẫn vào `data/` | Vòng sau AI sẽ đọc lại chính output của nó |
"""

CONTRIB_HEADER = """# Quy trình làm việc nhóm

> Sinh bởi `scaffold-project` ngày {{DATE}} cho nhóm **{{TEAM}} người**, nhánh chính `{{BRANCH}}`.

## 1. Mô hình git — sửa lại hiểu nhầm phổ biến

Git **không phải** tải file về rồi tải lên đè. Nếu là upload đè thì hai người sửa cùng lúc,
ai push sau sẽ xóa mất việc người trước. Git lưu **lịch sử thay đổi**.

| Lệnh | Nghĩa | Ở đâu |
|---|---|---|
| `clone` | Tải repo về **một lần duy nhất** | GitHub → máy bạn |
| `commit` | Đóng dấu mốc "tôi sửa những dòng này, vì lý do này" | **chỉ trên máy bạn** |
| `push` | Đẩy commit lên GitHub cho người khác thấy | máy bạn → GitHub |
| `pull` | Kéo việc người khác về máy mình | GitHub → máy bạn |

Commit mà chưa push thì **không ai thấy gì cả**.

## 2. Vòng lặp hằng ngày

```bash
git pull --rebase
```

1. Kéo bản mới nhất **trước khi** làm bất cứ gì.
2. Tạo nhánh: `git checkout -b {{BRANCHEX}}`
3. Sửa, commit nhiều lần — mỗi commit **một ý**, message mô tả *vì sao*, không phải *cái gì*.
4. Đẩy lên: `git push -u origin <tên-nhánh>`
5. Mở Pull Request trên GitHub → đây là chỗ người khác kiểm tra.
6. Được duyệt → merge vào `{{BRANCH}}` → cả nhóm `git pull`.

## 3. Đặt tên nhánh

```
<loại>/<tên-bạn>-<việc>
```

`feat` tính năng mới · `fix` sửa lỗi · `exp` thí nghiệm · `docs` tài liệu · `chore` việc vặt.
Ví dụ: `feat/linh-rag-chunking`, `exp/nam-loss-ablation`.
"""

CONTRIB_SOLO = """## 4. Quy mô hiện tại: 1-3 người

- Nhánh + PR vẫn nên dùng, nhưng **được tự merge** sau khi CI xanh.
- Chưa cần CODEOWNERS. Khi lên 4 người thì bật.
"""

CONTRIB_TEAM = """## 4. Quy mô hiện tại: {{TEAM}} người — vận hành như một hệ thống

Ở quy mô này thứ giết dự án không phải là code dở, mà là **giẫm chân nhau**. Bốn cơ chế:

### 4.1 Phân vùng sở hữu (chống xung đột từ gốc)

`.github/CODEOWNERS` gán mỗi thư mục cho một người. Người sở hữu là người **bắt buộc duyệt**
PR chạm vào vùng đó. Nguyên tắc chia: **cắt theo thư mục, không cắt theo lớp kỹ thuật** —
nếu chia "một người làm frontend, một người làm backend" thì mọi tính năng đều đụng cả hai.

### 4.2 Bảo vệ nhánh chính

Bật trong GitHub → Settings → Branches → thêm rule cho `{{BRANCH}}`:

- Require a pull request before merging — **1 approval**
- Require status checks to pass
- Không cho force push

### 4.3 Giới hạn để review còn có nghĩa

| Giới hạn | Con số | Vì sao |
|---|---|---|
| Kích thước PR | ~400 dòng thay đổi | Vượt ngưỡng này chất lượng review tụt rõ rệt; PR to thường bị duyệt lấy lệ |
| Nhánh mở cùng lúc / người | 2 | Nhiều hơn là đang làm dở dang khắp nơi |
| Tuổi nhánh | 3 ngày | Nhánh sống lâu là nhánh sẽ conflict |
| Thời gian phản hồi PR | trong ngày làm việc | PR chờ lâu chặn cả dây chuyền |

### 4.4 Cấu trúc file phải phục vụ việc nhiều người

Đây là chỗ bố cục thư mục và làm việc nhóm dính vào nhau:

- **Một thứ một file.** Mỗi prompt một file, mỗi skill một thư mục, mỗi paper một note.
  Hai người hiếm khi chạm cùng file thì hiếm khi conflict.
- **File dùng chung là nam châm hút xung đột.** `INDEX.md`, sổ ghi chung, file cấu hình
  tổng: quy ước **chỉ thêm vào cuối**, không chèn giữa, không sắp xếp lại.
- **Notebook**: `.ipynb` là JSON có nhúng output, merge rất tệ. Xóa output trước khi commit
  (`nbstripout`), và giữ logic thật trong `src/` chứ không trong notebook.
- **File nhị phân**: không vào git. Để ở storage ngoài, trong repo chỉ giữ `manifest.md`
  ghi file nào ở đâu, ai tải lên, ngày nào.

## 5. Khi có agent AI tự commit

IDE dạng agent (Antigravity, Claude Code…) có thể "stage all → commit → sync" trong một lệnh.
Agent **không phân biệt** file nào nhạy cảm.

- `.gitignore` phải có **trước** commit đầu tiên. Repo này đã có sẵn.
- Mỗi agent chạy trên **nhánh riêng**. Nhiều agent cùng một nhánh là công thức gây xung đột.
- Đọc lại danh sách file đã stage trước khi để agent commit.
"""

CONTRIB_TAIL = """
## 6. Sự cố lộ khóa — làm gì

Đã push khóa API lên GitHub thì **xóa file đi là không đủ**: nó vẫn nằm trong lịch sử,
ai clone cũng đọc được.

1. **Hủy khóa cũ ở nhà cung cấp ngay** (rotate). Đây là bước bắt buộc và quan trọng nhất.
2. Tạo khóa mới, để trong `.env` (đã được gitignore).
3. Báo cả nhóm; nếu repo public, coi như khóa đã bị lộ công khai.

## 7. Trước khi commit lần đầu — danh sách kiểm

- [ ] Đã đọc mục 1 và 2 ở trên
- [ ] `.env` của tôi **không** hiện trong `git status`
- [ ] Tôi đang ở nhánh riêng, không phải `{{BRANCH}}`
- [ ] Không có file nhị phân nào trong danh sách stage
"""

PR_TMPL = """## Việc này làm gì

<!-- Một đoạn: thay đổi gì và VÌ SAO. Không liệt kê lại diff. -->

## Kiểm chứng thế nào

<!-- Lệnh đã chạy / test đã qua / ảnh chụp màn hình. "Chạy được trên máy tôi" không tính. -->

## Danh sách kiểm

- [ ] Không có khóa/bí mật nào trong diff
- [ ] Không có file nhị phân hay dữ liệu thô nào bị commit nhầm
- [ ] Notebook đã xóa output (nếu có)
- [ ] Dưới ~400 dòng thay đổi, hoặc đã giải thích vì sao phải to hơn
- [ ] Đã gán người duyệt theo CODEOWNERS
"""

ENV_TMPL = """# Sao chép file này thành .env rồi điền giá trị thật.
# .env đã được gitignore — KHÔNG BAO GIỜ commit nó.

# --- Model providers ---
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=

# --- Storage / database ---
DATABASE_URL=

# --- App ---
APP_ENV=development
"""

MANIFEST_TMPL = """# Manifest dữ liệu thô

`data/raw/` **không nằm trong git** (nhị phân + nhạy cảm). File này là bản đồ: ai muốn chạy
dự án thì đọc đây để biết tải dữ liệu ở đâu.

Quy tắc đặt tên: `YYYY-MM-DD_ten-tai-lieu_v01.<ext>` — ngày trước để sắp xếp tự nhiên.

| File | Nguồn / link | Người nạp | Ngày | Nhạy cảm | Ghi chú |
|---|---|---|---|---|---|
| _(ví dụ)_ 2026-08-01_survey-raw_v01.xlsx | Google Drive/… | @ai-do | 2026-08-01 | có (PII) | chưa ẩn danh |

> Dữ liệu chứa thông tin cá nhân: phải qua bước ẩn danh vào `data/interim/` trước khi dùng.
"""

CODEOWNERS_HEADER = """# Mỗi thư mục có một chủ sở hữu. Chủ sở hữu là người BẮT BUỘC duyệt PR chạm vào vùng đó.
# Cú pháp: <đường dẫn>  <@github-user ...>. Dòng khớp CUỐI CÙNG là dòng thắng.
# Thay các @TODO- bên dưới bằng username GitHub thật, nếu không GitHub sẽ bỏ qua dòng đó.

"""


# --------------------------------------------------------------------------- helpers


def die(msg: str) -> None:
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
    sys.exit(1)


def render(tmpl: str, mapping: dict) -> str:
    out = tmpl
    for key, val in mapping.items():
        out = out.replace("{{" + key + "}}", str(val))
    return out


def dir_table(dirs: list) -> str:
    rows = ["| Thư mục | git | Ai sinh ra | Vai trò |", "|---|---|---|---|"]
    for d in dirs:
        origin = "người" if d.get("origin") == "human" else "máy"
        rows.append(
            "| `{}/` | {} | {} | {} |".format(
                d["path"], d.get("git", "track"), origin, d.get("note", "")
            )
        )
    return "\n".join(rows)


def write_if_absent(path: Path, content: str, report: dict, dry: bool) -> None:
    rel = path.as_posix()
    if path.exists():
        report["skipped"].append(rel)
        return
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    report["created"].append(rel)


def merge_gitignore(path: Path, lines: list, report: dict, dry: bool) -> None:
    block = [IGNORE_MARK_START] + lines + [IGNORE_MARK_END]
    if not path.exists():
        if not dry:
            path.write_text("\n".join(block) + "\n", encoding="utf-8", newline="\n")
        report["created"].append(path.as_posix())
        return

    existing = path.read_text(encoding="utf-8").splitlines()
    missing = [ln for ln in lines if ln not in existing]
    if not missing:
        report["skipped"].append(path.as_posix() + " (đã đủ)")
        return
    if not dry:
        with path.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write("\n" + "\n".join([IGNORE_MARK_START] + missing + [IGNORE_MARK_END]) + "\n")
    report["created"].append(path.as_posix() + " (+{} dòng)".format(len(missing)))


# --------------------------------------------------------------------------- main


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", help="path to the JSON spec")
    ap.add_argument("--dry-run", action="store_true", help="report only, touch nothing")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.is_file():
        die("không tìm thấy spec: {}".format(spec_path))
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die("spec JSON hỏng: {}".format(exc))

    profiles_doc = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    profile_key = spec.get("profile", "mixed")
    if profile_key not in profiles_doc["profiles"]:
        die("profile không hợp lệ: {} (có: {})".format(
            profile_key, ", ".join(profiles_doc["profiles"])))
    profile = profiles_doc["profiles"][profile_key]

    root = Path(spec.get("root", ".")).resolve()
    project = spec.get("project_name") or root.name
    team = int(spec.get("team_size", 1))
    branch = spec.get("default_branch", "main")
    dry = args.dry_run

    report = {"ok": True, "root": root.as_posix(), "profile": profile_key,
              "created": [], "skipped": [], "dirs": [], "warnings": []}

    if spec.get("visibility") == "public":
        report["warnings"].append(
            "Repo public: kiểm tra lại data/ và config/ không chứa dữ liệu định danh trước khi push."
        )

    # 1. directories -------------------------------------------------------
    dirs = list(profile["dirs"])
    for extra in spec.get("extra_dirs", []):
        dirs.append({"path": extra, "git": "track", "origin": "human", "note": "thêm theo yêu cầu"})

    for d in dirs:
        target = root / d["path"]
        report["dirs"].append(d["path"])
        if dry:
            continue
        target.mkdir(parents=True, exist_ok=True)
        # .gitkeep only for tracked dirs -- ignored dirs must not be committed at all
        if d.get("git", "track") == "track":
            keep = target / ".gitkeep"
            if not keep.exists() and not any(target.iterdir()):
                keep.write_text("", encoding="utf-8")

    # 2. .gitignore FIRST (hard gate: before any file that could hold a secret)
    ignore_lines = list(profiles_doc["common_ignore"]) + list(profile.get("ignore", []))
    ignore_lines += list(spec.get("extra_ignore", []))
    seen, deduped = set(), []
    for ln in ignore_lines:
        if ln not in seen:
            seen.add(ln)
            deduped.append(ln)
    merge_gitignore(root / ".gitignore", deduped, report, dry)

    # 3. governance + docs -------------------------------------------------
    subs = {"PROJECT": project, "DATE": date.today().isoformat(), "TEAM": team,
            "BRANCH": branch, "PROFILE": profile_key,
            "BRANCHEX": "feat/ten-ban-viec-can-lam", "DIRTABLE": dir_table(dirs)}

    write_if_absent(root / "README.md", render(README_TMPL, subs), report, dry)

    contrib = CONTRIB_HEADER + (CONTRIB_SOLO if team <= 3 else CONTRIB_TEAM) + CONTRIB_TAIL
    write_if_absent(root / "CONTRIBUTING.md", render(contrib, subs), report, dry)

    write_if_absent(root / ".env.example", ENV_TMPL, report, dry)
    write_if_absent(root / ".github" / "pull_request_template.md", PR_TMPL, report, dry)

    if team >= 4:
        owners = spec.get("owners", {})
        lines = [CODEOWNERS_HEADER, "* @TODO-tech-lead", ""]
        for d in dirs:
            if d.get("git") != "track":
                continue
            who = owners.get(d["path"], "@TODO-" + d["path"].replace("/", "-"))
            lines.append("/{}/ {}".format(d["path"], who))
        write_if_absent(root / ".github" / "CODEOWNERS", "\n".join(lines) + "\n", report, dry)

    # 4. data manifest where a raw zone exists -----------------------------
    for d in dirs:
        if d["path"].endswith("data/raw") or d["path"].endswith("papers"):
            write_if_absent(root / d["path"] / "manifest.md", MANIFEST_TMPL, report, dry)

    report["next"] = [
        "git init && git add . && git commit -m \"chore: scaffold project structure\"",
        "Sửa @TODO- trong .github/CODEOWNERS thành username GitHub thật",
        "Bật branch protection cho nhánh {} trên GitHub".format(branch) if team >= 4 else "",
    ]
    report["next"] = [n for n in report["next"] if n]

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
