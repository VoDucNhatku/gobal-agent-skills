# Skill Test Framework — GOBAL AGENT

Automated structural validation for all skills in `gobal-skills/`.

## Usage

```bash
# Run all checks (human-readable report)
python scripts/test_skills.py

# JSON output (for CI / tooling)
python scripts/test_skills.py --json

# Test single skill
python scripts/test_skills.py --skill code-reviewer

# Write report to file
python scripts/test_skills.py --report test-reports/latest.txt
```

Exit code: `0` = all pass, `1` = at least one failure.

## Checks Performed

| Check | What it verifies | Severity |
|-------|-----------------|----------|
| `frontmatter` | YAML frontmatter has all 4 required keys, name is kebab-case | WARN/FAIL |
| `body_lines` | SKILL.md body < 500 lines (token budget) | FAIL |
| `provenance` | Contains `> **Source:**` marker | WARN |
| `cross_refs` | Referenced skill names exist in gobal-skills/ | WARN |
| `duplicate_sections` | No repeated `##` headings (copy-paste detection) | FAIL |
| `anti_slop` | Design skills: no system fonts, purple gradients, emoji icons | WARN |
| `description_format` | Third-person, "Use when..." trigger format | WARN |
| `announce_line` | Contains "I'm using the..." announce pattern | WARN |

## Integration

- Run after any skill modification (pre-commit hook candidate)
- Run in CI to catch structural regressions
- Use `--json` output for programmatic quality tracking
