---
name: "test-framework"
description: "Automated structural validation for all skills in gobal-skills/. Verifies frontmatter, line limits, cross-references, and anti-slop rules."
argument-hint: "[all|single-skill <name>]"
allowed-tools: "Read Bash"
---

# Test Framework

> **Purpose:** Automated structural validation for GOBAL AGENT skills.

## Usage

```bash
# Run all checks (human-readable report)
python scripts/test_skills.py

# JSON output (for CI / tooling)
python scripts/test_skills.py --json

# Test single skill
python scripts/test_skills.py --skill <skill-name>
```

## Checks Performed
- `frontmatter`: YAML frontmatter has all required keys.
- `body_lines`: SKILL.md body < 500 lines (token budget).
- `provenance`: Contains `> **Source:**` marker.
- `cross_refs`: Referenced skill names exist.
- `duplicate_sections`: No repeated headings.
- `anti_slop`: Design skills follow aesthetics rules.
- `description_format`: Correct trigger format.
- `announce_line`: Contains announce pattern.
