#!/usr/bin/env python3
"""
GOBAL AGENT Skill Test Framework
Automated structural validation for all skills in gobal-skills/.

Checks:
1. YAML frontmatter validity (name, description, argument-hint, allowed-tools)
2. SKILL.md body line count (< 500)
3. Cross-reference integrity (referenced skills exist)
4. Provenance completeness (source attribution present)
5. Duplicate section detection
6. Anti-slop patterns (design skills only)
7. Frontmatter description format (third-person, trigger-focused)

Usage:
    python test_skills.py                    # Run all checks, print report
    python test_skills.py --json             # Output as JSON
    python test_skills.py --skill <name>     # Test single skill
    python test_skills.py --report <path>    # Write report to file
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict

# ─── Configuration ───────────────────────────────────────────────────────────

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent
MAX_BODY_LINES = 500
REPORT_DIR = SKILLS_DIR / "test-reports"

# Required frontmatter keys
REQUIRED_FM_KEYS = {"name", "description", "argument-hint", "allowed-tools"}

# Cross-reference patterns to detect
REF_PATTERNS = [
    r'`([a-z][a-z0-9-]+)`',           # backtick: `skill-name`
    r'\[\[([a-z][a-z0-9-]+)\]\]',      # wiki: [[skill-name]]
]

# Anti-slop patterns (design skills)
SLOP_PATTERNS = {
    "system_font": re.compile(r'font-family:\s*(Inter|Roboto|Arial|Helvetica|system-ui)', re.I),
    "purple_gradient": re.compile(r'#7C3AED|#DB2777|blurple', re.I),
    "emoji_icon": re.compile(r'[^\w\s]\s*(🚀|✨|🎯|🔥|💡|⚡|🎨|🛠️|📊|🎯)'),  # emoji as icons
}

# Provenance marker
PROVENANCE_MARKER = re.compile(r'> \*\*Source:\*\*', re.M)

# Duplicate section detector (look for repeated ## headings)
SECTION_HEADING = re.compile(r'^##\s+(.+)$', re.M)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def find_skill_dirs():
    """Return all skill directories (excluding special dirs)."""
    exclude = {"provenance", "references", "test-framework", "test-reports", "__pycache__"}
    dirs = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.is_dir() and d.name not in exclude and (d / "SKILL.md").exists():
            dirs.append(d)
    return dirs


def parse_frontmatter(content):
    """Extract YAML frontmatter between first pair of --- markers."""
    if not content.startswith("---"):
        return None
    end = content.find("---", 3)
    if end == -1:
        return None
    fm = content[3:end].strip()
    result = {}
    for line in fm.split("\n"):
        line = line.strip()
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip()
    return result


def get_body(content):
    """Return SKILL.md body (everything after frontmatter)."""
    if not content.startswith("---"):
        return content
    end = content.find("---", 3)
    if end == -1:
        return content
    return content[end + 3:].strip()


def find_cross_references(body):
    """Extract all skill-name references from backtick and wiki patterns."""
    refs = set()
    for pat in REF_PATTERNS:
        if isinstance(pat, str):
            pat = re.compile(pat)
        for m in pat.finditer(body):
            candidate = m.group(1)
            if len(candidate) > 2 and "_" not in candidate:
                refs.add(candidate)
    return refs


def find_duplicate_sections(body):
    """Detect repeated ## headings."""
    headings = SECTION_HEADING.findall(body)
    seen = {}
    dupes = []
    for h in headings:
        h_lower = h.lower().strip()
        count = seen.get(h_lower, 0) + 1
        seen[h_lower] = count
        if count > 1:
            dupes.append((h, count))
    return dupes


def check_slop(body, skill_name):
    """Check design skills for anti-slop patterns."""
    findings = []
    if "design" not in skill_name:
        return findings
    for pattern_name, pat in SLOP_PATTERNS.items():
        if pat.search(body):
            findings.append(pattern_name)
    return findings


def validate_description(desc):
    """Check description follows 'Use when...' third-person format."""
    issues = []
    if not desc:
        issues.append("empty description")
        return issues
    if desc[0].islower():
        issues.append("starts with lowercase (should be capitalized)")
    if "use when" not in desc.lower() and "use for" not in desc.lower():
        issues.append("missing 'Use when...' trigger phrase")
    if any(desc.startswith(p) for p in ("I ", "We ", "This skill")):
        issues.append("first-person (should be third-person)")
    return issues


# ─── Checks ──────────────────────────────────────────────────────────────────

def check_frontmatter(fm):
    issues = []
    missing = REQUIRED_FM_KEYS - set(fm.keys())
    if missing:
        issues.append(f"missing keys: {', '.join(sorted(missing))}")
    if "name" in fm:
        if fm["name"] != fm["name"].lower().replace(" ", "-"):
            issues.append(f"name not kebab-case: {fm['name']}")
        if "/" in fm.get("name", "") or "\\" in fm.get("name", ""):
            issues.append(f"name contains path separator: {fm['name']}")
    return issues


def check_body_lines(body):
    lines = body.split("\n")
    count = len(lines)
    return count if count > MAX_BODY_LINES else 0


def check_provenance(body):
    return 1 if PROVENANCE_MARKER.search(body) else 0


def check_cross_refs(refs, all_skill_names):
    broken = []
    for ref in refs:
        if ref not in all_skill_names:
            broken.append(ref)
    return broken


# ─── Main Test Runner ────────────────────────────────────────────────────────

def run_tests(skill_filter=None, json_output=False, report_path=None):
    skill_dirs = find_skill_dirs()
    all_skill_names = {d.name for d in skill_dirs}

    results = []
    total_pass = 0
    total_fail = 0
    total_warn = 0

    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        if skill_filter and skill_name != skill_filter:
            continue

        skill_file = skill_dir / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        body = get_body(content) if fm else content
        body_lines = body.split("\n")

        finding = {
            "skill": skill_name,
            "path": str(skill_file.relative_to(SKILLS_DIR)),
            "checks": {},
            "issues": [],
            "warnings": [],
        }

        # Check 1: Frontmatter
        if fm is None:
            finding["checks"]["frontmatter"] = "FAIL"
            finding["issues"].append("No YAML frontmatter found")
        else:
            fm_issues = check_frontmatter(fm)
            if fm_issues:
                finding["checks"]["frontmatter"] = "WARN"
                finding["warnings"].extend(fm_issues)
            else:
                finding["checks"]["frontmatter"] = "PASS"

        # Check 2: Body line count
        line_count = len(body_lines)
        if line_count > MAX_BODY_LINES:
            finding["checks"]["body_lines"] = "FAIL"
            finding["issues"].append(f"Body is {line_count} lines (max {MAX_BODY_LINES})")
        else:
            finding["checks"]["body_lines"] = "PASS"

        # Check 3: Provenance
        has_prov = check_provenance(content) > 0
        if not has_prov:
            finding["checks"]["provenance"] = "WARN"
            finding["warnings"].append("No provenance marker (> **Source:**) found")
        else:
            finding["checks"]["provenance"] = "PASS"

        # Check 4: Cross-references
        refs = find_cross_references(body)
        broken = check_cross_refs(refs, all_skill_names)
        if broken:
            finding["checks"]["cross_refs"] = "WARN"
            finding["warnings"].append(f"Broken refs: {', '.join(sorted(broken))}")
        else:
            finding["checks"]["cross_refs"] = "PASS"

        # Check 5: Duplicate sections
        dupes = find_duplicate_sections(body)
        if dupes:
            finding["checks"]["duplicate_sections"] = "FAIL"
            finding["issues"].append(f"Duplicate headings: {dupes}")
        else:
            finding["checks"]["duplicate_sections"] = "PASS"

        # Check 6: Anti-slop (design skills only)
        slop = check_slop(body, skill_name)
        if slop:
            finding["checks"]["anti_slop"] = "WARN"
            finding["warnings"].append(f"Slop patterns: {', '.join(slop)}")
        else:
            finding["checks"]["anti_slop"] = "PASS"

        # Check 7: Description format
        if fm and "description" in fm:
            desc_issues = validate_description(fm["description"])
            if desc_issues:
                finding["checks"]["description_format"] = "WARN"
                finding["warnings"].extend(desc_issues)
            else:
                finding["checks"]["description_format"] = "PASS"

        # Check 8: Announce line
        if "I'm using the" in body or "Announce at start" in body:
            finding["checks"]["announce_line"] = "PASS"
        else:
            finding["checks"]["announce_line"] = "WARN"
            finding["warnings"].append("Missing announce line ('I'm using the...')")

        # Tally
        for check, status in finding["checks"].items():
            if status == "PASS":
                total_pass += 1
            elif status == "FAIL":
                total_fail += 1
            elif status == "WARN":
                total_warn += 1

        results.append(finding)

    # ─── Report ──────────────────────────────────────────────────────────────

    if json_output:
        report = {
            "summary": {
                "total_skills": len(results),
                "total_checks": total_pass + total_fail + total_warn,
                "pass": total_pass,
                "fail": total_fail,
                "warn": total_warn,
                "pass_rate": f"{total_pass / max(1, total_pass + total_fail) * 100:.1f}%",
            },
            "skills": results,
        }
        output = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        lines = []
        lines.append("=" * 70)
        lines.append("GOBAL AGENT — Skill Test Report")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Skills tested: {len(results)}")
        lines.append(f"Total checks:  {total_pass + total_fail + total_warn}")
        lines.append(f"  ✅ PASS: {total_pass}")
        lines.append(f"  ❌ FAIL: {total_fail}")
        lines.append(f"  ⚠️  WARN: {total_warn}")
        if total_pass + total_fail > 0:
            lines.append(f"  Pass rate: {total_pass / max(1, total_pass + total_fail) * 100:.1f}%")
        lines.append("")

        # Group by status
        failures = [r for r in results if any(s == "FAIL" for s in r["checks"].values())]
        warnings_only = [r for r in results if r not in failures and r["warnings"]]

        if failures:
            lines.append("─" * 70)
            lines.append(f"FAILURES ({len(failures)} skills)")
            lines.append("─" * 70)
            for f in failures:
                lines.append(f"\n❌ {f['skill']}")
                for issue in f["issues"]:
                    lines.append(f"   • {issue}")

        if warnings_only:
            lines.append("")
            lines.append("─" * 70)
            lines.append(f"WARNINGS ({len(warnings_only)} skills)")
            lines.append("─" * 70)
            for f in warnings_only[:10]:  # Cap at 10
                lines.append(f"\n⚠️  {f['skill']}")
                for w in f["warnings"][:5]:
                    lines.append(f"   • {w}")
            if len(warnings_only) > 10:
                lines.append(f"\n   ... and {len(warnings_only) - 10} more (use --json for full report)")

        if not failures and not warnings_only:
            lines.append("✅ All checks passed. No issues found.")

        lines.append("")
        lines.append("─" * 70)
        lines.append("Per-Skill Summary")
        lines.append("─" * 70)
        for r in results:
            statuses = [f"{k}={v[0].upper()}" for k, v in r["checks"].items()]
            icon = "✅" if not r["issues"] else "❌" if any("FAIL" in v for v in r["checks"].values()) else "⚠️"
            lines.append(f"  {icon} {r['skill']:<35} {' | '.join(statuses)}")

        lines.append("")
        output = "\n".join(lines)

    # Write report
    if report_path:
        Path(report_path).write_text(output, encoding="utf-8")
        print(f"Report written to {report_path}")
    elif not json_output:
        print(output)

    if json_output:
        print(output)

    return results


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GOBAL Skill Test Framework")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--skill", help="Test single skill by name")
    parser.add_argument("--report", help="Write report to file path")
    args = parser.parse_args()

    results = run_tests(
        skill_filter=args.skill,
        json_output=args.json,
        report_path=args.report,
    )

    # Exit code: 0 if no failures, 1 if any
    has_fail = any(
        any(v == "FAIL" for v in r["checks"].values())
        for r in results
    )
    sys.exit(1 if has_fail else 0)
