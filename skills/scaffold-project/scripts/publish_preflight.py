#!/usr/bin/env python3
"""Read-only safety scan run BEFORE a project is pushed to GitHub for the first time.

This script never creates a repo, never commits, never pushes. It answers one question:
"if we committed everything right now, would we leak a secret or a huge binary?"

It is deliberately separate from the push itself so the irreversible commands stay visible
in the transcript instead of being buried inside a script.

Usage:
    python publish_preflight.py [--root .] [--json]

Exit code 0 = safe to proceed, 2 = blockers found (never push), 1 = script error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):  # pragma: no cover
    pass

# Filenames that must never be committed, matched on the path as posix.
SECRET_NAME_PATTERNS = [
    r"(^|/)\.env$",
    r"(^|/)\.env\.(?!example$|template$|sample$)[^/]+$",
    r"\.pem$",
    r"\.key$",
    r"\.p12$",
    r"\.pfx$",
    r"(^|/)id_rsa$",
    r"(^|/)id_ed25519$",
    r"(^|/)credentials\.json$",
    r"(^|/)service[-_]?account.*\.json$",
    r"(^|/)\.npmrc$",
    r"(^|/)\.pypirc$",
]

# Content signatures of live credentials.
SECRET_CONTENT_PATTERNS = [
    (r"sk-ant-[A-Za-z0-9_\-]{20,}", "Anthropic API key"),
    (r"\bsk-[A-Za-z0-9]{32,}", "OpenAI-style API key"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"\bgithub_pat_[A-Za-z0-9_]{50,}", "GitHub fine-grained token"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key id"),
    (r"\bAIza[0-9A-Za-z_\-]{35}\b", "Google API key"),
    (r"\bxox[baprs]-[A-Za-z0-9\-]{10,}", "Slack token"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----", "private key block"),
]

TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".ps1", ".sql", ".html", ".css",
    ".ipynb", ".tex", ".xml", ".gitignore", "",
}

BLOCK_MB = 50.0
WARN_MB = 10.0
SCAN_MAX_BYTES = 1_000_000


def run(cmd: list, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def ensure_repo(root: Path) -> list:
    """A local .git is required before check-ignore or add --dry-run mean anything.

    `git init` only creates a local .git directory -- it commits nothing and contacts
    no remote, so running it during a read-only scan is safe.
    """
    if (root / ".git").exists():
        return []
    res = run(["git", "init", "-q"], root)
    if res.returncode != 0:
        return ["git init thất bại: " + res.stderr.strip()]
    return ["đã chạy `git init` (chỉ tạo .git cục bộ, chưa commit gì)"]


def candidate_files(root: Path) -> tuple[list, list]:
    """Files git WOULD add, honouring .gitignore. Returns (paths, notes)."""
    notes = []
    res = run(["git", "add", "-A", "--dry-run"], root)
    if res.returncode != 0:
        return [], ["git add --dry-run thất bại: " + res.stderr.strip()]

    paths = []
    for line in res.stdout.splitlines():
        line = line.strip()
        if not line.startswith("add '"):
            continue
        paths.append(line[5:].rstrip("'"))
    return paths, notes


def scan_content(path: Path) -> list:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    try:
        if path.stat().st_size > SCAN_MAX_BYTES:
            return []
        blob = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    hits = []
    for pattern, label in SECRET_CONTENT_PATTERNS:
        if re.search(pattern, blob):
            hits.append(label)
    return hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true", help="machine-readable output only")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    report = {"root": root.as_posix(), "blockers": [], "warnings": [],
              "notes": [], "file_count": 0, "total_mb": 0.0, "remote": None}

    # --- tooling -----------------------------------------------------------
    for tool, flag in (("git", "--version"), ("gh", "--version")):
        res = run([tool, flag], root)
        if res.returncode != 0:
            report["blockers"].append("thiếu công cụ: {}".format(tool))
    auth = run(["gh", "auth", "status"], root)
    if auth.returncode != 0:
        report["blockers"].append("gh chưa đăng nhập — chạy `gh auth login`")

    if report["blockers"]:
        emit(report, args.json)
        sys.exit(2)

    # --- .gitignore is the hard gate --------------------------------------
    report["notes"].extend(ensure_repo(root))
    if not (root / ".gitignore").exists():
        report["blockers"].append(
            ".gitignore không tồn tại — chạy scaffold_project.py trước khi nghĩ tới push")
    else:
        # check-ignore works on a pathname whether or not the file exists yet.
        chk = run(["git", "check-ignore", "-q", ".env"], root)
        # git returns 0 when the path IS ignored; 1 when it is not.
        if chk.returncode != 0:
            report["blockers"].append(".gitignore không chặn `.env`")

    files, notes = candidate_files(root)
    report["notes"].extend(notes)
    report["file_count"] = len(files)

    existing_remote = run(["git", "remote", "get-url", "origin"], root)
    if existing_remote.returncode == 0:
        report["remote"] = existing_remote.stdout.strip()
        report["warnings"].append(
            "repo đã có remote origin ({}) — đây không phải lần push đầu".format(report["remote"]))

    total = 0
    for rel in files:
        p = root / rel
        if not p.is_file():
            continue
        size = p.stat().st_size
        total += size
        mb = size / 1_048_576

        posix = p.relative_to(root).as_posix()
        for pattern in SECRET_NAME_PATTERNS:
            if re.search(pattern, posix):
                report["blockers"].append("file bí mật sẽ bị commit: {}".format(posix))
                break

        for label in scan_content(p):
            report["blockers"].append("phát hiện {} trong {}".format(label, posix))

        if mb >= BLOCK_MB:
            report["blockers"].append("file quá lớn ({:.1f} MB): {}".format(mb, posix))
        elif mb >= WARN_MB:
            report["warnings"].append("file lớn ({:.1f} MB): {}".format(mb, posix))

        if posix.endswith(".ipynb"):
            try:
                if '"output_type"' in p.read_text(encoding="utf-8", errors="ignore"):
                    report["warnings"].append("notebook còn nhúng output: {}".format(posix))
            except OSError:
                pass

    report["total_mb"] = round(total / 1_048_576, 2)
    if report["total_mb"] > 100:
        report["warnings"].append(
            "tổng {} MB — repo nặng bất thường, kiểm tra lại .gitignore".format(report["total_mb"]))

    report["safe"] = not report["blockers"]
    emit(report, args.json)
    sys.exit(0 if report["safe"] else 2)


def emit(report: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
