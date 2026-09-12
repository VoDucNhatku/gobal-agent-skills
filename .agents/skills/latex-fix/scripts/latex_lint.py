#!/usr/bin/env python3
"""latex_lint.py — flag math-rendering issues in notes/ Markdown so they render on
BOTH KaTeX (VS Code) and MathJax (GitHub). Called by the `latex-fix` skill
(script-offloading, workbench-conventions §9): the skill runs this to locate the
offending spans, then fixes ONLY those spans by hand against
~/.claude/rules/latex-katex-compat.md. This script does not edit files — it reports.

Usage:
    python latex_lint.py <file-or-glob> [<file-or-glob> ...]
    python latex_lint.py "notes/*.md"
    python latex_lint.py notes/003-method.md

Output: JSON lines, one finding per line:
    {"file": "...", "line": 42, "severity": "error", "rule": "legacy-delimiter",
     "match": "\\[ ... \\]", "fix": "replace \\[...\\] with $$...$$ (blank lines around)"}
Plus a final summary object. Skips fenced code (```), Mermaid blocks, and inline code spans.
"""
from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

# Windows consoles default to cp1252; force UTF-8 so Vietnamese / arrows in the
# JSON output never crash the process (UnicodeEncodeError).
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# (rule, severity, compiled pattern, human fix). Order matters only for reporting.
RULES = [
    ("fenced-math-block", "error", re.compile(r"^```math\s*$"),
     "replace ```math fence with $$ ... $$ (blank lines around)"),
    ("bracket-display-delim", "error", re.compile(r"\\\[|\\\]"),
     r"replace \[...\] with $$...$$ (blank lines around)"),
    ("paren-inline-delim", "error", re.compile(r"\\\(|\\\)"),
     r"replace \(...\) with $...$"),
    ("tag-macro", "error", re.compile(r"\\tag\b"),
     r"drop \tag{N}; append *(phương trình N trong paper)* after the $$ block"),
    ("label-ref-macro", "error", re.compile(r"\\(label|ref|eqref)\b"),
     r"drop \label/\ref/\eqref (KaTeX unsupported); use a plain number"),
    ("boldsymbol-macro", "warn", re.compile(r"\\boldsymbol\b"),
     r"prefer \mathbf{} (\boldsymbol is KaTeX-fragile)"),
    ("operatorname-macro", "warn", re.compile(r"\\operatorname\b"),
     r"use \mathrm{} for custom operators (\operatorname needs amsopn)"),
    ("middle-bar", "warn", re.compile(r"\\middle\\\|"),
     r"use \mid instead of \middle\| (KaTeX bug #683)"),
]

# Plain-text math heuristics (only checked OUTSIDE math spans).
PLAINTEXT_RULES = [
    ("plaintext-subscript", "warn", re.compile(r"\b[A-Za-z]+_[A-Za-z]{2,}\b"),
     "looks like plain-text subscript (e.g. L_total) — use $L_{total}$"),
    ("plaintext-norm", "warn", re.compile(r"\|\|[^|]+\|\|"),
     r"plain-text norm ||x|| — use $\|x\|$"),
    ("plaintext-argminmax", "warn", re.compile(r"\b(argmin|argmax)\b"),
     r"plain-text argmin/argmax — use $\arg\min$ / $\arg\max$"),
    ("plaintext-greek", "warn",
     re.compile(r"\b(alpha|beta|gamma|theta|lambda|sigma|epsilon)\b"),
     r"plain-text Greek — use $\theta$ etc. (only if this is math, not prose)"),
]


def iter_lines_skipping_code(text: str):
    """Yield (lineno, line, in_math_inline_ok) skipping fenced code & mermaid blocks."""
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            # a ```math fence is itself a finding, report before toggling
            yield i, line, in_fence
            in_fence = not in_fence
            continue
        yield i, line, in_fence


def _has_unspaced_display(text: str):
    """Find $$ display blocks not separated by blank lines (markdown-it requirement)."""
    findings = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        if line.strip() == "$$":
            prev = lines[i - 2].strip() if i - 2 >= 0 else ""
            nxt = lines[i].strip() if i < len(lines) else ""
            # opening $$ should have a blank line before; closing should have blank after.
            if prev not in ("",) and not prev.endswith("$$"):
                findings.append((i, "display-no-blank-before",
                                 "$$ display block needs a blank line before it"))
    return findings


def strip_inline_math(line: str) -> str:
    """Remove $...$ and `code` so plain-text heuristics don't fire inside real math/code."""
    line = re.sub(r"`[^`]*`", " ", line)
    line = re.sub(r"\$\$.*?\$\$", " ", line)
    line = re.sub(r"\$[^$]+\$", " ", line)
    return line


def lint_file(path: Path):
    findings = []
    text = path.read_text(encoding="utf-8", errors="replace")

    for lineno, line, in_fence in iter_lines_skipping_code(text):
        if line.lstrip().startswith("```math"):
            findings.append({"file": str(path), "line": lineno, "severity": "error",
                             "rule": "fenced-math-block", "match": line.strip(),
                             "fix": "replace ```math fence with $$ ... $$ (blank lines around)"})
            continue
        if in_fence:
            continue  # inside a code/mermaid fence — leave alone
        for rule, sev, pat, fix in RULES:
            if rule == "fenced-math-block":
                continue
            m = pat.search(line)
            if m:
                findings.append({"file": str(path), "line": lineno, "severity": sev,
                                 "rule": rule, "match": m.group(0), "fix": fix})
        # plain-text math only outside inline math/code
        bare = strip_inline_math(line)
        for rule, sev, pat, fix in PLAINTEXT_RULES:
            m = pat.search(bare)
            if m:
                findings.append({"file": str(path), "line": lineno, "severity": sev,
                                 "rule": rule, "match": m.group(0), "fix": fix})

    for lineno, rule, fix in _has_unspaced_display(text):
        findings.append({"file": str(path), "line": lineno, "severity": "warn",
                         "rule": rule, "match": "$$", "fix": fix})
    return findings


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: latex_lint.py <file-or-glob> [...]")
    paths = []
    for arg in sys.argv[1:]:
        hits = glob.glob(arg)
        paths.extend(hits if hits else [arg])

    total = 0
    files_with = set()
    for p in paths:
        path = Path(p)
        if not path.is_file():
            continue
        for f in lint_file(path):
            print(json.dumps(f, ensure_ascii=False))
            total += 1
            files_with.add(str(path))
    print(json.dumps({"summary": True, "findings": total,
                      "files_flagged": sorted(files_with),
                      "files_scanned": len([p for p in paths if Path(p).is_file()])},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
