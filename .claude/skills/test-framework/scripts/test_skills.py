#!/usr/bin/env python3
"""
GOBAL AGENT Skill Test Framework
Automated structural validation for all skills in gobal-skills/.

Checks (FAIL = the skill is broken; WARN = it is degraded):
1.  YAML frontmatter validity (name, description, argument-hint, allowed-tools)
1b. FAIL — `name:` matches its directory, or Claude Code cannot resolve the skill
1c. FAIL — `description:` within the 1024-char cap, past which it is truncated
2.  FAIL — SKILL.md body line count (< 500)
3.  Cross-reference integrity, read only from wiki links, "→ `skill`" handoffs,
    and Cross-References/Integration sections — a bare backtick is not a reference
4.  Provenance, required only where the skill claims an upstream source
5.  Duplicate section detection
6.  Anti-slop patterns (design skills only)
7.  Description format: third-person, and says when to fire ("Use when ..." or
    this suite's "Triggers — ..."); DEPRECATED stubs exempt
8.  Algorithm-justification vocabulary (implement-mode skills only)

Usage:
    python test_skills.py                    # Run all checks, print report
    python test_skills.py --json             # Output as JSON
    python test_skills.py --skill <name>     # Test single skill
    python test_skills.py --report <path>    # Write report to file
"""

import re
import sys
import json
import argparse
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent
MAX_BODY_LINES = 500
MAX_DESC_CHARS = 1024
REPORT_DIR = SKILLS_DIR / "test-reports"

# Required frontmatter keys
REQUIRED_FM_KEYS = {"name", "description", "argument-hint", "allowed-tools"}

# Cross-reference patterns. Only these three contexts denote a real skill
# handoff — see find_cross_references for why a bare backtick does not.
WIKI_REF = re.compile(r'\[\[([a-z][a-z0-9-]+)\]\]')
ARROW_REF = re.compile(r'(?:→|->)\s*`([a-z][a-z0-9-]+)`')
BACKTICK_REF = re.compile(r'`([a-z][a-z0-9-]+)`')
XREF_SECTION_HEADING = re.compile(
    r'^#{2,3}\s*(?:Cross[- ]?References?|Integration|Handoffs?|See also)\b.*$',
    re.I | re.M)

# Anti-slop patterns (design skills)
SLOP_PATTERNS = {
    "system_font": re.compile(r'font-family:\s*(Inter|Roboto|Arial|Helvetica|system-ui)', re.I),
    "purple_gradient": re.compile(r'#7C3AED|#DB2777|blurple', re.I),
    "emoji_icon": re.compile(r'[^\w\s]\s*(🚀|✨|🎯|🔥|💡|⚡|🎨|🛠️|📊|🎯)'),  # emoji as icons
}

# Provenance marker
PROVENANCE_MARKER = re.compile(r'> \*\*Source:\*\*', re.M)

# A skill only needs a provenance marker when it CLAIMS to be derived from an
# upstream repo. Original skills have nothing to attribute, and inventing a
# Source line to satisfy a linter is exactly the fabrication these skills forbid.
#
# The upstream name must sit on a line with an attribution verb. Matching the
# bare name flagged a CV template whose YAML has a `superpowers:` field, and a
# TikZ rule about captioning a figure "adapted from [x]" — neither is a claim
# about where the SKILL came from.
UPSTREAM = r'superpowers|addyosmani|gstack|AIL-Premium|mattpocock|anthropics/skills|obra'
ATTRIBUTION_VERB = r'borrow\w*|adapt\w*|port\w*|base[ds]? on|deriv\w*|inspired by|from'
# `Source:` counts only as a line-leading attribution, matching the repo's own
# `> **Source:** ...` convention. Unanchored, it also matched a CV skill's
# "Data source: (kaggle, ...)" — a project's data, not the skill's origin.
DERIVATION_CLAIM = re.compile(
    rf'^\s*>?\s*\*{{0,2}}Source:|'
    rf'^.*(?:{ATTRIBUTION_VERB})\b.*\b(?:{UPSTREAM})\b.*$|'
    rf'^.*\b(?:{UPSTREAM})\b.*(?:{ATTRIBUTION_VERB})\b.*$',
    re.I | re.M)

# Generic backticked vocabulary that is never a skill name. Bodies backtick any
# identifier-ish token, so these would otherwise read as broken references.
NON_SKILL_VOCAB = {
    # status / verdict values
    "yes", "no", "partial", "pass", "fail", "warn", "skip", "todo", "done",
    "match", "close", "diverge", "missing", "primary", "secondary", "inferred",
    "green", "red", "high", "medium", "low", "critical", "major", "minor",
    # frontmatter + template placeholders
    "name", "description", "argument-hint", "allowed-tools", "frontmatter",
    "slug", "candidate-slug", "timestamp", "date", "path", "id", "next",
    "field", "key", "value", "mode", "all", "none",
    # common prose nouns that happen to be backticked
    "notes", "papers", "scripts", "references", "templates", "assets", "output",
    "input", "logs", "src", "test", "tests", "main", "null", "true", "false",
}

# Duplicate section detector (look for repeated ## headings)
SECTION_HEADING = re.compile(r'^##\s+(.+)$', re.M)

# Algorithm-justification check (implement-mode skills): the skill body must carry
# method-justification vocabulary so fabricated-METHOD is guarded, not just results.
IMPLEMENT_MODE_HINT = re.compile(r'\bimplement\b', re.I)
ALGO_JUSTIFY_KEYWORDS = re.compile(
    r'Algorithm Justification|complexity|Big-?O|O\(\?\)|invariant|convergence|'
    r'provenance|correctness idea', re.I)

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


def collect_mode_vocabulary(skill_files):
    """Every mode / profile / variant token any skill declares about itself.

    Bodies write these in backticks exactly like skill names (`implement`,
    `corpus`, `scaffold`, `mixed`), so without this the reference check flags
    every mode in the suite as a broken skill.

    Harvested from three places, because skills declare their vocabulary in all
    three: the `argument-hint`, a `Modes — a (…), b (…)` clause, and any
    pipe-enumeration such as `(research | web | agent | mixed)`.
    """
    modes = set()
    for f in skill_files:
        try:
            fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        except OSError:
            continue
        if not fm:
            continue

        hint = fm.get("argument-hint", "")
        modes.update(re.findall(r'[a-z][a-z0-9-]{2,}', hint.lower()))

        desc = fm.get("description", "")
        # "Modes — plan (…), apply (…), publish (…)" → the words before each "("
        for clause in re.findall(r'Modes?\s*[—:-]\s*(.+?)(?:\.\s|$)', desc):
            modes.update(re.findall(r'\b([a-z][a-z0-9-]{2,})\s*\(', clause.lower()))
            modes.update(re.findall(r'[a-z][a-z0-9-]{2,}', clause.lower()))
        # "(research | web | agent | mixed)" anywhere in the description
        for group in re.findall(r'\(([^()]*\|[^()]*)\)', desc):
            modes.update(re.findall(r'[a-z][a-z0-9-]{2,}', group.lower()))
    return modes


def collect_rule_names(rules_dir):
    """Basenames of `~/.claude/rules/*.md`, which bodies cite in backticks."""
    if not rules_dir.is_dir():
        return set()
    return {p.stem for p in rules_dir.glob("*.md")}


def _xref_section_text(body):
    """Text of the sections where this suite lists its skill handoffs."""
    chunks = []
    for m in XREF_SECTION_HEADING.finditer(body):
        rest = body[m.end():]
        nxt = re.search(r'^#{1,3}\s', rest, re.M)
        chunks.append(rest[:nxt.start()] if nxt else rest)
    return "\n".join(chunks)


def find_cross_references(body, known_non_skills=frozenset()):
    """Extract skill-name references from explicit cross-reference contexts.

    A bare backtick match is far too broad here: these bodies backtick every
    identifier-ish token — modes (`implement`), enum values (`verified`), LaTeX
    macros (`tikzpicture`), file types (`bib`), even ordinary words (`and`).
    Enumerating that vocabulary is endless, so instead this reads only the three
    places a real handoff is written:

      * a wiki link, `[[skill-name]]`
      * an arrow handoff, "→ `skill-name`"
      * a backticked name inside a Cross-References / Integration section

    `known_non_skills` then removes modes and rule basenames, which legitimately
    appear in those same positions.
    """
    refs = set()
    sources = [
        (WIKI_REF, body),
        (ARROW_REF, body),
        (BACKTICK_REF, _xref_section_text(body)),
    ]
    for pat, text in sources:
        for m in pat.finditer(text):
            candidate = m.group(1)
            if len(candidate) <= 2 or "_" in candidate:
                continue
            if candidate in known_non_skills:
                continue
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


def validate_description(desc, skill_name=""):
    """A description must be third-person and must say when the skill fires.

    Two conventions satisfy the trigger requirement: the upstream 'Use when...'
    phrasing, and this suite's own 'Triggers — <bilingual keyword list>', which
    carries the same information in a form the router can match on directly.
    DEPRECATED stubs are exempt: they exist so old references resolve, and are
    meant NOT to fire.
    """
    issues = []
    if not desc:
        return ["empty description"]
    low = desc.lower()
    if "deprecated" in low:
        return issues
    if desc[0].islower():
        issues.append("starts with lowercase (should be capitalized)")
    has_trigger = any(k in low for k in ("use when", "use for", "trigger"))
    if not has_trigger:
        issues.append("no trigger guidance ('Use when...' or 'Triggers — ...')")
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


def check_name_matches_dir(fm, dir_name):
    """`name:` must equal the containing directory.

    Claude Code registers a skill under its directory name; a mismatched `name:`
    makes every routing table that calls the skill by directory silently miss.
    This is a hard failure, not a style warning.
    """
    declared = (fm or {}).get("name")
    if declared is None:
        return None
    if declared != dir_name:
        return f"name: '{declared}' does not match directory '{dir_name}' — skill will not resolve"
    return None


def check_description_length(fm):
    """`description:` is capped at MAX_DESC_CHARS; past that it is truncated."""
    desc = (fm or {}).get("description")
    if not desc:
        return None
    n = len(desc)
    if n > MAX_DESC_CHARS:
        return f"description is {n} chars (max {MAX_DESC_CHARS}) — will be truncated"
    return None


def check_body_lines(body):
    lines = body.split("\n")
    count = len(lines)
    return count if count > MAX_BODY_LINES else 0


def check_provenance(body, description=""):
    """Provenance is required only where derivation is claimed.

    Returns 1 (satisfied) for an original skill that claims no upstream, 1 for a
    derived skill that carries the marker, and 0 only when a skill says it came
    from somewhere but never says where.
    """
    if PROVENANCE_MARKER.search(body):
        return 1
    claims_derivation = DERIVATION_CLAIM.search(f"{description}\n{body}")
    return 0 if claims_derivation else 1


def check_cross_refs(refs, all_skill_names):
    broken = []
    for ref in refs:
        if ref not in all_skill_names:
            broken.append(ref)
    return broken


def check_algorithm_justification(fm, body):
    """Implement-mode skills must carry algorithm-justification vocabulary.

    Returns None when not applicable (skill has no implement mode), [] when the
    vocabulary is present, or a list of issues when it is missing.
    """
    hint = (fm or {}).get("argument-hint", "")
    has_implement_mode = bool(IMPLEMENT_MODE_HINT.search(hint))
    if not has_implement_mode:
        return None
    if ALGO_JUSTIFY_KEYWORDS.search(body):
        return []
    return ["implement-mode skill lacks algorithm-justification vocabulary "
            "(complexity/Big-O/invariant/convergence/provenance)"]


# ─── Main Test Runner ────────────────────────────────────────────────────────

def run_tests(skill_filter=None, json_output=False, report_path=None):
    skill_dirs = find_skill_dirs()
    # Every directory holding a SKILL.md is a resolvable skill, including the
    # ones find_skill_dirs() declines to TEST. Building this from the tested set
    # alone made a reference to `test-framework` read as broken.
    all_skill_names = {
        d.name for d in SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    }

    results = []
    total_pass = 0
    total_fail = 0
    total_warn = 0

    # Vocabulary that is backticked like a skill name but never is one: every
    # mode any skill declares, every rule basename, plus generic tokens.
    known_non_skills = (
        collect_mode_vocabulary(d / "SKILL.md" for d in skill_dirs)
        | collect_rule_names(SKILLS_DIR.parent / "rules")
        | NON_SKILL_VOCAB
    )

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

        # Check 1b: name must match its directory (hard failure — breaks routing)
        name_issue = check_name_matches_dir(fm, skill_file.parent.name)
        if name_issue:
            finding["checks"]["name_matches_dir"] = "FAIL"
            finding["issues"].append(name_issue)
        else:
            finding["checks"]["name_matches_dir"] = "PASS"

        # Check 1c: description length cap
        desc_issue = check_description_length(fm)
        if desc_issue:
            finding["checks"]["description_length"] = "FAIL"
            finding["issues"].append(desc_issue)
        else:
            finding["checks"]["description_length"] = "PASS"

        # Check 2: Body line count
        line_count = len(body_lines)
        if line_count > MAX_BODY_LINES:
            finding["checks"]["body_lines"] = "FAIL"
            finding["issues"].append(f"Body is {line_count} lines (max {MAX_BODY_LINES})")
        else:
            finding["checks"]["body_lines"] = "PASS"

        # Check 3: Provenance
        has_prov = check_provenance(content, (fm or {}).get("description", "")) > 0
        if not has_prov:
            finding["checks"]["provenance"] = "WARN"
            finding["warnings"].append("No provenance marker (> **Source:**) found")
        else:
            finding["checks"]["provenance"] = "PASS"

        # Check 4: Cross-references
        refs = find_cross_references(body, known_non_skills)
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
            desc_issues = validate_description(fm["description"], skill_name)
            if desc_issues:
                finding["checks"]["description_format"] = "WARN"
                finding["warnings"].extend(desc_issues)
            else:
                finding["checks"]["description_format"] = "PASS"

        # Check 8 (removed 2026-08-01): announce line.
        #
        # This matched the literal English string "I'm using the ..." — a
        # convention from obra/superpowers that arrived with the six skills
        # imported from it and was never adopted suite-wide. The other 58 skills
        # write their bodies in Vietnamese, so the check was flagging a language
        # mismatch as a defect, and the harness already shows the user which
        # skill fired. Adopt it deliberately or drop it; silently warning 58
        # times taught nobody anything.

        # Check 9: Algorithm justification (implement-mode skills only)
        algo_issues = check_algorithm_justification(fm, body)
        if algo_issues is not None:
            if algo_issues:
                finding["checks"]["algorithm_justification"] = "WARN"
                finding["warnings"].extend(algo_issues)
            else:
                finding["checks"]["algorithm_justification"] = "PASS"

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
    # Windows consoles default to cp1252, which cannot print the report's
    # emoji status icons — force UTF-8 so the script runs everywhere.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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
