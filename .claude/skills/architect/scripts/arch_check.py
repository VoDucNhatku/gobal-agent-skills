#!/usr/bin/env python3
"""Mechanical verification for an architecture document.

Checks only what a machine can actually decide, and says "unverifiable" instead of
guessing. Everything it reports carries the evidence it used, so the caller never has
to re-read the document to trust the result.

Checks performed:
  paths     every `backticked/path` claimed in the doc exists in the repo
  env       every `UPPER_SNAKE` env var claimed in the doc appears in code or .env*
  deps      every dependency named in the Tech Stack section appears in a manifest
  layering  ARCHITECTURE.md <= 200 lines, docs/arch/*.md <= 400 lines
  sections  every "## " section has real content or the literal "> Not Found"
  adr       every ADR carries the mandatory headings
  churn     files with the most git commits (where the architecture likely cuts wrong)

Usage:
  python arch_check.py --doc ARCHITECTURE.md --root .
  python arch_check.py --doc ARCHITECTURE.md --root . --only paths,env
"""

import argparse
import json
import os
import re
import subprocess
import sys

MAX_INDEX_LINES = 200
MAX_DETAIL_LINES = 400
MAX_EXAMPLES = 12
MAX_FILE_BYTES = 512 * 1024

SKIP_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build",
    ".next", ".nuxt", "coverage", "target", "vendor", ".turbo", ".cache",
}
CODE_EXT = {
    ".js", ".jsx", ".ts", ".tsx", ".py", ".go", ".rs", ".java", ".rb", ".php",
    ".yml", ".yaml", ".json", ".toml", ".env", ".example", ".sh", ".sql", ".prisma",
}
MANIFESTS = [
    "package.json", "requirements.txt", "pyproject.toml", "go.mod",
    "Cargo.toml", "Gemfile", "composer.json", "pom.xml",
]

BACKTICK = re.compile(r"`([^`\n]{2,120})`")
ENV_VAR = re.compile(r"^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+){1,6}$")
NOT_FOUND = re.compile(r">\s*Not Found", re.I)
SECTION = re.compile(r"^##\s+(.+?)\s*$", re.M)
ADR_REQUIRED = ["Bối cảnh", "Quyết định", "Phương án đã loại bỏ", "Điều kiện đảo ngược"]


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def walk_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield os.path.join(dirpath, name)


def looks_like_path(token):
    """A backticked token is a path claim only if it has a separator and a real segment."""
    if "/" not in token and "\\" not in token:
        return False
    if token.startswith(("http://", "https://", "//")):
        return False
    if any(c in token for c in " |<>*?\"") or token.endswith(("/", ":")):
        return False
    # strip a trailing :line reference — the doc is allowed to cite lines
    return bool(re.match(r"^[\w.@~-]+(?:/[\w.@ -]+)*[\w.]*(?::\d+)?$", token.replace("\\", "/")))


def collect_claims(doc_text):
    paths, envs = set(), set()
    for raw in BACKTICK.findall(doc_text):
        token = raw.strip()
        if ENV_VAR.match(token):
            envs.add(token)
        elif looks_like_path(token):
            paths.add(token.replace("\\", "/").split(":")[0])
    return sorted(paths), sorted(envs)


def check_paths(root, claims):
    missing = []
    for rel in claims:
        candidate = os.path.join(root, rel)
        if os.path.exists(candidate):
            continue
        # a glob-ish claim such as src/modules/*  counts as satisfied if the parent exists
        parent = os.path.dirname(candidate)
        if rel.endswith(("*", "*.md", "*.ts", "*.py")) and os.path.isdir(parent):
            continue
        missing.append(rel)
    return {
        "claimed": len(claims),
        "missing": len(missing),
        "examples": missing[:MAX_EXAMPLES],
    }


def check_env(root, claims):
    if not claims:
        return {"claimed": 0, "unreferenced": 0, "examples": []}
    haystack = []
    for path in walk_files(root):
        ext = os.path.splitext(path)[1].lower()
        base = os.path.basename(path)
        if ext not in CODE_EXT and not base.startswith(".env"):
            continue
        try:
            if os.path.getsize(path) > MAX_FILE_BYTES:
                continue
        except OSError:
            continue
        haystack.append(read_text(path))
    blob = "\n".join(haystack)
    unref = [v for v in claims if v not in blob]
    return {
        "claimed": len(claims),
        "unreferenced": len(unref),
        "examples": unref[:MAX_EXAMPLES],
    }


def check_deps(root, doc_text):
    manifests = [m for m in MANIFESTS if os.path.exists(os.path.join(root, m))]
    if not manifests:
        return {"status": "unverifiable", "reason": "no manifest found", "examples": []}
    blob = "\n".join(read_text(os.path.join(root, m)) for m in manifests).lower()
    section = ""
    for match in SECTION.finditer(doc_text):
        if "tech stack" in match.group(1).lower():
            start = match.end()
            nxt = SECTION.search(doc_text, start)
            section = doc_text[start:nxt.start() if nxt else len(doc_text)]
            break
    if not section:
        return {"status": "unverifiable", "reason": "no Tech Stack section", "examples": []}
    named = {t.strip() for t in BACKTICK.findall(section)}
    named = {t for t in named if not looks_like_path(t) and not ENV_VAR.match(t) and len(t) > 2}
    absent = sorted(t for t in named if t.split("@")[0].lower() not in blob)
    return {
        "status": "checked",
        "manifests": manifests,
        "named": len(named),
        "absent": len(absent),
        "examples": absent[:MAX_EXAMPLES],
    }


def check_layering(root, doc_path):
    findings = []
    n = len(read_text(doc_path).splitlines())
    if n > MAX_INDEX_LINES:
        findings.append(f"{os.path.basename(doc_path)}: {n} dòng (trần {MAX_INDEX_LINES})")
    arch_dir = os.path.join(root, "docs", "arch")
    detail = 0
    if os.path.isdir(arch_dir):
        for path in walk_files(arch_dir):
            if not path.endswith(".md"):
                continue
            detail += 1
            m = len(read_text(path).splitlines())
            if m > MAX_DETAIL_LINES:
                rel = os.path.relpath(path, root).replace("\\", "/")
                findings.append(f"{rel}: {m} dòng (trần {MAX_DETAIL_LINES})")
    return {
        "index_lines": n,
        "detail_files": detail,
        "violations": len(findings),
        "examples": findings[:MAX_EXAMPLES],
    }


def check_sections(doc_text):
    matches = list(SECTION.finditer(doc_text))
    empty = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(doc_text)
        body = doc_text[start:end].strip()
        if NOT_FOUND.search(body):
            continue
        # a one-line section can still be a real section; only genuinely thin bodies count
        if len(body) < 60 or body.lower() in {"tbd", "todo"}:
            empty.append(match.group(1))
    return {
        "sections": len(matches),
        "empty": len(empty),
        "examples": empty[:MAX_EXAMPLES],
    }


def check_adrs(root):
    adr_dir = os.path.join(root, "docs", "arch", "adr")
    if not os.path.isdir(adr_dir):
        return {"status": "absent", "count": 0, "incomplete": 0, "examples": []}
    bad = []
    count = 0
    for path in sorted(walk_files(adr_dir)):
        if not path.endswith(".md"):
            continue
        count += 1
        text = read_text(path)
        missing = [h for h in ADR_REQUIRED if h not in text]
        if missing:
            rel = os.path.relpath(path, root).replace("\\", "/")
            bad.append(f"{rel}: thiếu {', '.join(missing)}")
    return {
        "status": "checked",
        "count": count,
        "incomplete": len(bad),
        "examples": bad[:MAX_EXAMPLES],
    }


def git_churn(root, top=10):
    try:
        out = subprocess.run(
            ["git", "-C", root, "log", "--pretty=format:", "--name-only"],
            capture_output=True, text=True, timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return {"status": "unavailable", "hot_files": []}
    if out.returncode != 0:
        return {"status": "not a git repo", "hot_files": []}
    counts = {}
    for line in out.stdout.splitlines():
        line = line.strip()
        if not line or line.split("/")[0] in SKIP_DIRS:
            continue
        counts[line] = counts.get(line, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: -kv[1])[:top]
    return {
        "status": "checked",
        "hot_files": [{"file": f, "commits": c} for f, c in ranked],
    }


def main():
    # Windows consoles default to cp1252; Vietnamese findings would raise UnicodeEncodeError.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", default="ARCHITECTURE.md")
    ap.add_argument("--root", default=".")
    ap.add_argument("--only", default="", help="comma list: paths,env,deps,layering,sections,adr,churn")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    doc_path = args.doc if os.path.isabs(args.doc) else os.path.join(root, args.doc)
    if not os.path.exists(doc_path):
        json.dump({"error": f"document not found: {doc_path}"}, sys.stdout, ensure_ascii=False)
        print()
        return

    doc_text = read_text(doc_path)
    wanted = {w.strip() for w in args.only.split(",") if w.strip()}
    run = (lambda name: not wanted or name in wanted)

    path_claims, env_claims = collect_claims(doc_text)
    report = {"doc": os.path.relpath(doc_path, root).replace("\\", "/"), "root": root}

    if run("paths"):
        report["paths"] = check_paths(root, path_claims)
    if run("env"):
        report["env"] = check_env(root, env_claims)
    if run("deps"):
        report["deps"] = check_deps(root, doc_text)
    if run("layering"):
        report["layering"] = check_layering(root, doc_path)
    if run("sections"):
        report["sections"] = check_sections(doc_text)
    if run("adr"):
        report["adr"] = check_adrs(root)
    if run("churn"):
        report["churn"] = git_churn(root)

    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
