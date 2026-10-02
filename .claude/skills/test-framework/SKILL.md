---
name: test-framework
description: Automated structural validation for all skills in gobal-skills/. Verifies frontmatter, line limits, cross-references, and anti-slop rules.
argument-hint: [all|single-skill <name>]
allowed-tools: Read Bash
---

# Test Framework

> **Purpose:** Automated structural validation for GOBAL AGENT skills.

## Usage

```bash
# Run all checks (human-readable report)
python scripts/test_skills.py --skills-root ..

# JSON output (for CI / tooling)
python scripts/test_skills.py --skills-root .. --json

# Test single skill
python scripts/test_skills.py --skills-root .. --skill <skill-name>
```

## Checks Performed
- `frontmatter`: Strict YAML, unique keys, required fields, and canonical field types.
- `name_matches_dir`: Manifest name exactly matches the containing skill directory.
- `description_length`: Description stays within the supported character limit.
- `body_lines`: SKILL.md body < 500 lines (token budget).
- `provenance`: Contains `> **Source:**` marker.
- `cross_refs`: Referenced skill names exist.
- `local_resources`: Literal local/peer resource paths in backticks or Markdown links exist.
- `duplicate_sections`: No repeated headings.
- `anti_slop`: Design skills follow aesthetics rules.
- `description_format`: Correct trigger format.
- `algorithm_justification`: Implement-mode skills (argument-hint contains `implement`)
  carry method-justification vocabulary (complexity / Big-O / invariant / convergence /
  provenance) — guards fabricated METHOD, not just fabricated results. N/A for
  non-implementation skills.

Invalid YAML, wrong canonical types, name mismatches, missing resources, oversized bodies,
duplicate sections, and oversized descriptions are hard failures and return exit code `1`.
Style and provenance findings remain warnings.
