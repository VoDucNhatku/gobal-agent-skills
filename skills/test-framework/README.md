# Skill Test Framework — GOBAL AGENT

Automated structural validation for all skills in `gobal-skills/`.

## Usage

Running the optional validator requires Python 3.11+ and `PyYAML==6.0.3`.
From this copied skill directory, install its optional dependency with
`python -m pip install -r requirements.txt`. Registration of the Markdown skill
itself needs no Python. The sibling parser in `scripts/skill_manifest.py` makes
the validator runnable outside the repository, including from an unrelated cwd
when the script and `--skills-root` paths are explicit.

```bash
# From this skill directory, validate the complete canonical suite
python scripts/test_skills.py --skills-root .. --host canonical

# JSON output (for CI / tooling)
python scripts/test_skills.py --skills-root .. --host canonical --json

# Test single skill
python scripts/test_skills.py --skills-root .. --host canonical --skill code-reviewer

# Write report to file
python scripts/test_skills.py --skills-root .. --host canonical --report test-reports/latest.txt

# Generated portable Antigravity distribution
python scripts/test_skills.py --skills-root <generated-skills-root> --host antigravity --json
```

Exit code: `0` = all pass, `1` = at least one failure.
Missing/empty roots and unknown `--skill` selections also return `1`.
With `--json`, input errors have an `errors` array containing `code` and `message`.
Only immediate child directories containing `SKILL.md` are registrations;
nested fixture manifests are excluded.

## Checks Performed

| Check | What it verifies | Severity |
|-------|-----------------|----------|
| `frontmatter` | Strict YAML, unique keys, kebab-case name; canonical requires all 4 string fields, Antigravity only name/description and no extra keys | FAIL |
| `name_matches_dir` | `name` exactly matches its containing directory | FAIL |
| `description_length` | Description is at most 1024 characters | FAIL |
| `body_lines` | SKILL.md body < 500 lines (token budget) | FAIL |
| `provenance` | Contains `> **Source:**` marker | WARN |
| `cross_refs` | Referenced skill names exist in gobal-skills/ | WARN |
| `local_resources` | Literal local/peer paths in backticks/links and fenced `~/.gemini/config/skills/skill-name/...` commands exist; glob/placeholder examples excluded | FAIL |
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
- Canonical metadata beyond the four required fields is preserved; the portable
  Antigravity schema explicitly permits only `name` and `description`.
- A structural pass does not prove host discovery, skill invocation, instruction
  adherence, or claim accuracy; those require independent product/content checks.
