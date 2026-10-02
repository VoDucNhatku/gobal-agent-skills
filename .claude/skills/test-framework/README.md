# Skill Test Framework — GOBAL AGENT

Automated structural validation for all skills in `gobal-skills/`.

## Usage

```bash
# From this skill directory, validate the complete canonical suite
python scripts/test_skills.py --skills-root ..

# JSON output (for CI / tooling)
python scripts/test_skills.py --skills-root .. --json

# Test single skill
python scripts/test_skills.py --skills-root .. --skill code-reviewer

# Write report to file
python scripts/test_skills.py --skills-root .. --report test-reports/latest.txt
```

Exit code: `0` = all pass, `1` = at least one failure.

## Checks Performed

| Check | What it verifies | Severity |
|-------|-----------------|----------|
| `frontmatter` | Strict YAML, unique keys, all 4 required keys, and canonical string types | FAIL |
| `name_matches_dir` | `name` exactly matches its containing directory | FAIL |
| `description_length` | Description is at most 1024 characters | FAIL |
| `body_lines` | SKILL.md body < 500 lines (token budget) | FAIL |
| `provenance` | Contains `> **Source:**` marker | WARN |
| `cross_refs` | Referenced skill names exist in gobal-skills/ | WARN |
| `local_resources` | Literal local or peer resource paths in backticks/Markdown links exist | FAIL |
| `duplicate_sections` | No repeated `##` headings (copy-paste detection) | FAIL |
| `anti_slop` | Design skills: no system fonts, purple gradients, emoji icons | WARN |
| `description_format` | Third-person, "Use when..." trigger format | WARN |
| `algorithm_justification` | Implement-mode skills document method-justification vocabulary | WARN |

## Integration

- Run after any skill modification (pre-commit hook candidate)
- Run in CI to catch structural regressions
- Use `--json` output for programmatic quality tracking
- Use `--skills-root <path>` for fixtures or generated distributions; JSON reports include
  separate `discovered` and strictly `validated` counts.
