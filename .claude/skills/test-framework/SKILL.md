---
name: "test-framework"
description: "Use when validating skill structure in gobal-skills/. Verifies host-specific frontmatter, line limits, cross-references, bundled resources, and anti-slop rules."
allowed-tools: "Read Bash"
argument-hint: "[all|single-skill <name>]"
---

# Test Framework

> **Purpose:** Automated structural validation for GOBAL AGENT skills.

## Usage

The executable validator requires Python 3.11+ and optional `PyYAML==6.0.3`.
Install that dependency with `python -m pip install -r requirements.txt` from
this skill directory when running validation. Copying/registering the skill's
instructions does not require Python. Both validator and parser are bundled
under `scripts/`; the repository's helper delegates to this parser.

```bash
# Canonical source bundle: run all checks (human-readable report)
python scripts/test_skills.py --skills-root .. --host canonical

# JSON output (for CI / tooling)
python scripts/test_skills.py --skills-root .. --host canonical --json

# Test single skill
python scripts/test_skills.py --skills-root .. --host canonical --skill <skill-name>

# Validate a generated portable Antigravity skills root
python scripts/test_skills.py --skills-root <generated-skills-root> --host antigravity --json
```

Select the schema of the skills being checked, not the editor's default. Resolve the
validator and skills-root to absolute observed paths before execution; keep the project
working directory for report/artifact paths. Do not run canonical defaults on native
two-field manifests. The optional dependency path above is relative to this skill directory.

## Checks Performed
- `frontmatter`: Strict YAML, unique keys, kebab-case names and host-specific fields.
  Canonical requires string `name`, `description`, `argument-hint`, `allowed-tools`;
  Antigravity requires only string `name`, `description` and rejects extra keys.
- `name_matches_dir`: Manifest name exactly matches the containing skill directory.
- `description_length`: Description stays within the supported character limit.
- `body_lines`: SKILL.md body < 500 lines (token budget).
- `provenance`: Contains `> **Source:**` marker.
- `cross_refs`: Referenced skill names exist.
- `local_resources`: Literal local/peer paths in backticks or Markdown links exist;
  fenced command paths using `<skills>/skill-name/scripts/file.py` also resolve.
- `duplicate_sections`: No repeated headings.
- `anti_slop`: Design skills follow aesthetics rules.
- `description_format`: Correct trigger format.
- `algorithm_justification`: Implement-mode skills (argument-hint contains `implement`)
  carry method-justification vocabulary (complexity / Big-O / invariant / convergence /
  provenance) — guards fabricated METHOD, not just fabricated results. N/A for
  non-implementation skills and portable metadata without an argument-hint. Report these
  omitted metadata-based checks separately; native and canonical totals are not equal coverage.

Invalid YAML, wrong canonical types, name mismatches, missing resources, oversized bodies,
duplicate sections, and oversized descriptions are hard failures and return exit code `1`.
Style and provenance findings remain warnings.
Missing/empty roots and unknown `--skill` filters return exit code `1`; `--json`
includes an `errors` array with diagnostic `code` and `message`. Discovery reads
only immediate child skill directories, excluding nested test fixtures.
These checks establish structural validity, not host discovery or invocation.
