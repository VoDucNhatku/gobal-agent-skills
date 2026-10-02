# Antigravity Evidence-First Admin Implementation Plan

> **Goal:** Build, verify, pilot, and roll out a native Antigravity distribution of all GOBAL skills with an evidence-grounded `/admin` workflow.
> **Architecture:** Keep `.claude/skills` as the canonical source, normalize and strictly validate it, then deterministically generate an Antigravity plugin containing portable manifests, translated paths, packaged rules, and companion resources. Gate the full local rollout behind an isolated `/admin-evidence-pilot` test that proves real Antigravity discovery and skill-body activation.
> **Tech Stack:** Python 3.11, PyYAML 6.x, `unittest`, PowerShell 5.1+, Git, Antigravity IDE 2.0.3, Markdown/YAML/JSON.

## Global Constraints

- Follow RED → GREEN → REFACTOR for executable behaviour.
- Use `apply_patch` for authored source edits; generators may write mechanical output.
- No external runtime dependency is required for users installing committed plugin output.
- Developer validation may depend on `PyYAML>=6.0.2,<7`.
- Antigravity skill manifests contain only `name` and `description`.
- Generated output must contain exactly 69 canonical skills plus one separately generated pilot skill that is excluded from the production plugin.
- Generated output must contain no unresolved `~/.claude` path and no Claude-only manifest field.
- Never overwrite unrelated global skills, rules, plugins, or MCP configuration.
- Preserve `cv-maker` during local rollout.
- A clean static check is not proof of slash-menu discovery or invocation.
- The full local rollout is forbidden until the isolated pilot passes all UI acceptance checks.

---

### Task 1: Establish the Python validation harness

**Files:**
- Create: `.gitignore`
- Create: `requirements-dev.txt`
- Create: `scripts/__init__.py`
- Create: `scripts/skill_manifest.py`
- Create: `tests/__init__.py`
- Create: `tests/test_skill_manifest.py`

**Interfaces:**
- Produces: `load_frontmatter(path)`, `split_frontmatter(text)`, `dump_skill(frontmatter, body)`, and `ManifestError`.
- Consumed by: normalizer, generator, validators, and tests in later tasks.

- [ ] **Step 1: Add the failing strict-parser tests**

```python
import tempfile
import unittest
from pathlib import Path

from scripts.skill_manifest import ManifestError, load_frontmatter


class SkillManifestTests(unittest.TestCase):
    def write_skill(self, text: str) -> Path:
        root = Path(tempfile.mkdtemp())
        path = root / "SKILL.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_rejects_unquoted_colon_in_description(self):
        path = self.write_skill("---\nname: demo\ndescription: Modes: quick\n---\n# Demo\n")
        with self.assertRaises(ManifestError):
            load_frontmatter(path)

    def test_requires_argument_hint_to_be_string_for_canonical_skill(self):
        path = self.write_skill(
            "---\nname: demo\ndescription: \"Use when testing.\"\nargument-hint: [quick]\nallowed-tools: Read\n---\n# Demo\n"
        )
        with self.assertRaisesRegex(ManifestError, "argument-hint"):
            load_frontmatter(path, canonical=True)

    def test_accepts_quoted_canonical_manifest(self):
        path = self.write_skill(
            "---\nname: demo\ndescription: \"Use when testing.\"\nargument-hint: \"[quick]\"\nallowed-tools: \"Read\"\n---\n# Demo\n"
        )
        data, body = load_frontmatter(path, canonical=True)
        self.assertEqual(data["name"], "demo")
        self.assertIn("# Demo", body)
```

- [ ] **Step 2: Verify RED**

Run:

```powershell
python -m unittest tests.test_skill_manifest -v
```

Expected: import failure because `scripts.skill_manifest` does not exist.

- [ ] **Step 3: Add dependencies and minimal parser implementation**

`.gitignore`:

```gitignore
.venv/
.tmp/
__pycache__/
*.pyc
.coverage
```

`requirements-dev.txt`:

```text
PyYAML>=6.0.2,<7
```

Implementation requirements:

```python
from pathlib import Path

import yaml


class ManifestError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ManifestError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ManifestError("SKILL.md must start with a YAML frontmatter delimiter")
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])
    raise ManifestError("SKILL.md is missing the closing frontmatter delimiter")


def load_frontmatter(path: Path, canonical: bool = False) -> tuple[dict, str]:
    frontmatter_text, body = split_frontmatter(path.read_text(encoding="utf-8-sig"))
    try:
        data = yaml.load(frontmatter_text, Loader=UniqueKeyLoader)
    except (yaml.YAMLError, ManifestError) as exc:
        raise ManifestError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError(f"{path}: frontmatter must be a mapping")
    for required in ("name", "description"):
        if not isinstance(data.get(required), str) or not data[required].strip():
            raise ManifestError(f"{path}: {required} must be a non-empty string")
    if canonical:
        for field in ("argument-hint", "allowed-tools"):
            if field in data and not isinstance(data[field], str):
                raise ManifestError(f"{path}: {field} must be a string")
    return data, body


def dump_skill(frontmatter: dict, body: str) -> str:
    ordered = {key: frontmatter[key] for key in ("name", "description") if key in frontmatter}
    ordered.update({key: value for key, value in frontmatter.items() if key not in ordered})
    yaml_text = yaml.safe_dump(
        ordered,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    ).rstrip()
    normalized_body = body.replace("\r\n", "\n").replace("\r", "\n").lstrip("\n")
    return f"---\n{yaml_text}\n---\n\n{normalized_body.rstrip()}\n"
```

Use a `yaml.SafeLoader` subclass whose mapping constructor rejects duplicate keys.

- [ ] **Step 4: Create an isolated environment and verify GREEN**

Run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest tests.test_skill_manifest -v
```

Expected: all manifest unit tests pass.

- [ ] **Step 5: Commit**

```powershell
git add .gitignore requirements-dev.txt scripts tests
git commit -m "test: add strict skill manifest parser"
```

---

### Task 2: Make the existing skill validator truthful

**Files:**
- Modify: `.claude/skills/test-framework/scripts/test_skills.py`
- Modify: `.claude/skills/test-framework/SKILL.md`
- Modify: `.claude/skills/test-framework/README.md`
- Create: `tests/test_skill_framework.py`

**Interfaces:**
- Consumes: `scripts.skill_manifest.load_frontmatter`.
- Produces: truthful non-zero exit status and JSON counts for any configurable skills root.

- [ ] **Step 1: Add failing validator regression tests**

The tests create temporary skill roots and implement these exact assertions:

- `test_invalid_yaml_is_a_hard_failure`: write `description: Modes: quick`, run the
  validator, and assert exit code `1` plus an `invalid YAML` diagnostic.
- `test_test_framework_is_counted_when_it_has_a_skill_manifest`: create `alpha` and
  `test-framework` fixtures, run with `--json`, and assert `discovered == 2` and
  `validated == 2`.
- `test_missing_local_resource_is_a_hard_failure`: link to
  `scripts/missing.py`, run the validator, and assert exit code `1` plus the missing
  relative path in the error list.
- `test_name_must_equal_directory`: put `name: beta` inside `alpha/SKILL.md`, run the
  validator, and assert exit code `1` plus both names in the diagnostic.

Invoke the validator as a subprocess with `--skills-root <temp-root> --json` and assert
exit code `1` for invalid YAML/resources and `0` for a valid fixture.

- [ ] **Step 2: Verify RED**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_skill_framework -v
```

Expected: failures because the current parser hand-splits strings, excludes
`test-framework`, lacks `--skills-root`, and does not validate resources.

- [ ] **Step 3: Implement strict validation**

- Replace the hand-written frontmatter parser with `load_frontmatter`.
- Add `--skills-root` and resolve the repository helper import from the repo root.
- Include every directory containing `SKILL.md`, including `test-framework`.
- Validate local backticked `references/*.md`, `scripts/*.py`, and `assets/*` paths.
- Treat invalid YAML, wrong types, missing resources, and name mismatch as hard failures.
- Keep description/cross-reference/style warnings distinct from failures.
- Update the skill and README so documented checks match actual checks.

- [ ] **Step 4: Verify GREEN and observe the real integration failure**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_skill_framework -v
.\.venv\Scripts\python.exe .claude\skills\test-framework\scripts\test_skills.py --skills-root .claude\skills --json
```

Expected: unit tests pass; repository validation exits `1` and identifies the 26 strict
YAML failures plus real missing-resource references.

- [ ] **Step 5: Commit**

```powershell
git add .claude/skills/test-framework tests/test_skill_framework.py
git commit -m "fix: make skill validation strict"
```

---

### Task 3: Normalize all canonical manifests and repair phantom resources

**Files:**
- Create: `scripts/normalize_frontmatter.py`
- Create: `tests/test_normalize_frontmatter.py`
- Modify: all `.claude/skills/*/SKILL.md` frontmatter mechanically
- Modify: `.claude/skills/understand-codebase/SKILL.md`
- Modify: `.claude/skills/paper-method/SKILL.md`
- Modify: `.claude/skills/research-admin/SKILL.md`
- Modify: `.claude/skills/design-ui-direction/SKILL.md`
- Delete: `fix_yaml.py`
- Delete: `fix_all_yaml.py`

**Interfaces:**
- Produces: strict, deterministic canonical manifests and no false bundled-resource claims.
- Consumed by: Antigravity generator.

- [ ] **Step 1: Add failing normalizer tests**

Test that `normalize_text`:

- quotes `description` values containing `: `;
- converts list-shaped `argument-hint` syntax back to its original string notation;
- preserves booleans such as `user_invocable: true`;
- is idempotent on the second run;
- never contains a hard-coded machine path.

- [ ] **Step 2: Verify RED**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_normalize_frontmatter -v
```

Expected: import failure because the normalizer does not exist.

- [ ] **Step 3: Implement the safe normalizer**

The CLI accepts only explicit paths:

```powershell
python scripts/normalize_frontmatter.py --skills-root .claude/skills --check
python scripts/normalize_frontmatter.py --skills-root .claude/skills --write
```

It extracts the current one-line frontmatter fields without interpreting unquoted scalar
contents, serializes string fields safely, writes UTF-8/LF, and refuses duplicate keys or
multiline structures it cannot preserve.

- [ ] **Step 4: Normalize and repair references**

- Run the normalizer across all canonical skill manifests.
- Replace the nonexistent `understand-codebase/scripts/cb_builder.py` workflow with a
  bounded `rg --files`/`rg` discovery workflow and an explicit fallback when `rg` is absent.
- Point `paper-method` explicitly to the peer resource
  `paper-read/references/depth-modes.md`.
- Point `research-admin` explicitly to
  `knowledge-graph/scripts/kg_builder.py`.
- Make the deprecated `design-ui-direction` alias point to the real
  `design-web` resource or remove the false local asset path.
- Remove the two hard-coded legacy fixer scripts.

- [ ] **Step 5: Verify GREEN and canonical integration**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_normalize_frontmatter -v
.\.venv\Scripts\python.exe scripts/normalize_frontmatter.py --skills-root .claude/skills --check
.\.venv\Scripts\python.exe .claude\skills\test-framework\scripts\test_skills.py --skills-root .claude\skills
```

Expected: 69 skills parse; no strict YAML, type, name, or missing-resource failure.

- [ ] **Step 6: Commit**

```powershell
git add .claude/skills scripts/normalize_frontmatter.py tests/test_normalize_frontmatter.py fix_yaml.py fix_all_yaml.py
git commit -m "fix: normalize canonical skill manifests"
```

---

### Task 4: Build the deterministic Antigravity plugin

**Files:**
- Create: `plugin.json`
- Create: `scripts/build_antigravity.py`
- Create: `tests/test_build_antigravity.py`
- Generate: `skills/`
- Generate: `rules/`

**Interfaces:**
- Consumes: strict canonical skills and `.claude/rules`.
- Produces: complete Antigravity plugin tree and `--check` drift gate.

- [ ] **Step 1: Add failing generator tests**

Tests assert that a fixture build:

- emits only `name` and `description` in generated frontmatter;
- recursively copies companion files;
- maps rule and peer-skill paths relative to each generated text file;
- rejects unresolved `~/.claude`, missing resources, and unknown Claude tool identifiers;
- produces byte-identical output twice;
- excludes `references/` and `test-reports/` as top-level skills;
- produces 69 skills for the real repository.

- [ ] **Step 2: Verify RED**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_build_antigravity -v
```

Expected: import failure because the generator does not exist.

- [ ] **Step 3: Implement generator and manifest**

`plugin.json`:

```json
{
  "$schema": "https://antigravity.google/schemas/v1/plugin.json",
  "name": "gobal-agent-skills",
  "description": "Evidence-grounded GOBAL AGENT skills for Antigravity IDE."
}
```

Generator commands:

```powershell
python scripts/build_antigravity.py
python scripts/build_antigravity.py --check
```

Use explicit mappings for canonical rules and peer resources. Generated rules receive
valid Antigravity frontmatter; `evidence-first` is `always_on`, while detailed domain
rules are `model_decision` with descriptions. Fail instead of guessing an unknown path or
tool ABI.

- [ ] **Step 4: Generate and verify GREEN**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_build_antigravity -v
.\.venv\Scripts\python.exe scripts/build_antigravity.py
.\.venv\Scripts\python.exe scripts/build_antigravity.py --check
```

Expected: 69 generated skills; deterministic check exits `0`; no generated `~/.claude`.

- [ ] **Step 5: Commit**

```powershell
git add plugin.json scripts/build_antigravity.py tests/test_build_antigravity.py skills rules
git commit -m "feat: add native Antigravity plugin distribution"
```

---

### Task 5: Implement Evidence-First `/admin`

**Files:**
- Create: `.claude/rules/evidence-first.md`
- Modify: `.claude/skills/admin/SKILL.md`
- Create: `.claude/skills/admin/references/research-protocol.md`
- Create: `.claude/skills/admin/references/source-quality.md`
- Create: `.claude/skills/admin/references/claim-ledger.md`
- Create: `.claude/skills/admin/resources/claim-ledger.example.yml`
- Modify: `.claude/skills/hallucination-guard/SKILL.md`
- Modify: `.claude/skills/self-evaluator/SKILL.md`
- Create: `tests/test_evidence_skill_contract.py`

**Interfaces:**
- Produces: lane selection, task/fact/progress ledgers, source qualification, claim-level
  citation gate, calibrated synthesis, and bounded runtime budgets.

- [ ] **Step 1: Add failing contract tests**

Tests inspect the authored files and assert the presence of enforceable invariants:

```python
required_admin_terms = {
    "Fast non-research", "Quick evidence", "Standard evidence", "Deep evidence",
    "VERIFIED_OR_GIVEN", "LOOKUP", "DERIVE", "ASSUMPTION_OR_UNKNOWN",
    "SUPPORTED", "REFUTED", "CONTESTED", "NEI",
}
```

Also assert that the always-on rule is concise, that detailed protocols are references,
that search snippets are forbidden as evidence, and that a real URL without entailment is
a failure.

- [ ] **Step 2: Verify RED**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_evidence_skill_contract -v
```

Expected: missing rule/reference failures.

- [ ] **Step 3: Author the behaviour layer using progressive disclosure**

- Keep `admin/SKILL.md` below 500 body lines and route factual work to the on-demand
  protocol.
- Encode the four evidence lanes and operation ceilings.
- Require full-source reading, `origin_id` deduplication, counter-evidence by risk, the
  four claim statuses, evidence-bound synthesis, and stall detection.
- Extend `hallucination-guard` with source identity, entailment, independence, currency,
  and claim-coverage checks.
- Extend `self-evaluator` with static-vs-product verification and citation correctness
  versus completeness.

- [ ] **Step 4: Rebuild and verify GREEN**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_evidence_skill_contract -v
.\.venv\Scripts\python.exe scripts/build_antigravity.py
.\.venv\Scripts\python.exe scripts/build_antigravity.py --check
```

Expected: all evidence contract tests pass and generated output stays deterministic.

- [ ] **Step 5: Commit**

```powershell
git add .claude/rules .claude/skills/admin .claude/skills/hallucination-guard .claude/skills/self-evaluator tests/test_evidence_skill_contract.py skills rules
git commit -m "feat: make admin evidence first"
```

---

### Task 6: Add deterministic claim-ledger validation

**Files:**
- Create: `scripts/validate_evidence.py`
- Create: `tests/test_validate_evidence.py`

**Interfaces:**
- Consumes: YAML claim-ledger documents.
- Produces: human or JSON report and non-zero exit code for structural provenance gaps.

- [ ] **Step 1: Add failing validator tests**

Cover:

- valid supported claim with a source edge;
- supported claim without evidence;
- unknown source ID;
- duplicate claim/source IDs;
- supported claim with a fatal flag;
- corroboration that repeats one `origin_id`;
- output citation pointing to absent evidence;
- explicit `NEI` accepted without fake support.

- [ ] **Step 2: Verify RED**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_validate_evidence -v
```

Expected: import failure because the validator does not exist.

- [ ] **Step 3: Implement structural validation**

CLI:

```powershell
python scripts/validate_evidence.py path\to\ledger.yml
python scripts/validate_evidence.py path\to\ledger.yml --json
```

The report explicitly says semantic entailment is reviewer-supplied and not proven by the
script.

- [ ] **Step 4: Verify GREEN**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_validate_evidence -v
.\.venv\Scripts\python.exe scripts/validate_evidence.py .claude\skills\admin\resources\claim-ledger.example.yml
```

Expected: all unit tests and the example ledger pass.

- [ ] **Step 5: Commit**

```powershell
git add scripts/validate_evidence.py tests/test_validate_evidence.py
git commit -m "feat: validate claim evidence ledgers"
```

---

### Task 7: Add safe Windows install, pilot, update, and rollback

**Files:**
- Create: `scripts/install-antigravity.ps1`
- Create: `tests/test_installer.py`

**Interfaces:**
- Consumes: generated plugin root.
- Produces: managed plugin or direct IDE installation, ownership manifest, backups, and
  pilot-only installation.

- [ ] **Step 1: Add failing installer integration tests**

From Python, invoke PowerShell against a temporary `-ProfileRoot` and assert:

- `-Pilot` installs only `admin-evidence-pilot` and no always-on global rule;
- direct full mode installs 69 skills and evidence rule;
- unrelated `cv-maker` survives update and uninstall;
- unmanaged collision fails without `-Force`;
- forced collision is copied to a timestamped backup;
- uninstall removes only manifest-owned paths;
- invalid source aborts before destination mutation;
- dry run performs no writes.

- [ ] **Step 2: Verify RED**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_installer -v
```

Expected: failure because the installer does not exist.

- [ ] **Step 3: Implement PowerShell installer**

Supported parameters:

```powershell
param(
  [ValidateSet('Direct','Plugin')] [string]$Mode = 'Direct',
  [ValidateSet('Global','Workspace')] [string]$Scope = 'Global',
  [string]$WorkspacePath,
  [string]$SourcePath = (Split-Path -Parent $PSScriptRoot),
  [string]$ProfileRoot = $env:USERPROFILE,
  [switch]$Pilot,
  [switch]$Force,
  [switch]$Uninstall,
  [switch]$DryRun
)
```

Use `-LiteralPath`, resolved target containment checks, per-file ownership manifests, and
recoverable backups. Never touch `mcp_config.json`.

- [ ] **Step 4: Verify GREEN**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_installer -v
```

Expected: all temporary-profile install/update/uninstall tests pass.

- [ ] **Step 5: Commit**

```powershell
git add scripts/install-antigravity.ps1 tests/test_installer.py
git commit -m "feat: add safe Antigravity installer"
```

---

### Task 8: Add documentation, regression cases, and CI

**Files:**
- Modify: `README.md`
- Create: `docs/ANTIGRAVITY.md`
- Create: `evals/admin-research/cases.yml`
- Create: `evals/admin-research/rubric.md`
- Create: `.github/workflows/validate.yml`
- Modify: `notes/INDEX.md`

**Interfaces:**
- Produces: Windows-first user workflow, update/uninstall/diagnostics, one pilot case, and
  twelve release-time regression cases.

- [ ] **Step 1: Add the twelve concrete cases**

Each case defines `id`, prompt, lane, material claims, required behaviours, forbidden
behaviours, source policy, and pass rule. The first executable pilot is:

```text
/admin-evidence-pilot Kiểm chứng phát biểu này:
"Antigravity IDE dùng ~/.claude/skills làm thư mục global skills."
Chỉ dùng nguồn chính thức/primary source. Tách rõ Observed, Inferred và
Unverified. Nếu phát biểu sai, hãy bác bỏ và nêu đúng đường dẫn.
```

The pilot must end with `Protocol: AG-EF-PILOT-1` and stay within one search batch and two
opened authoritative sources.

- [ ] **Step 2: Document exact install and verification commands**

Include:

- clone and `/plugin install <local-path>`;
- direct standalone IDE install via PowerShell;
- update and uninstall;
- strict parser/count diagnostics;
- new-chat `/` and `/admin` checks;
- distinction between static validity, discovery, and invocation;
- rollback location and preservation of unrelated skills.

- [ ] **Step 3: Add CI**

Workflow installs `requirements-dev.txt`, runs `python -m unittest discover -s tests -v`,
the canonical skill validator, generator `--check`, and evidence example validation.

- [ ] **Step 4: Run documentation and CI-equivalent checks**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe .claude\skills\test-framework\scripts\test_skills.py --skills-root .claude\skills
.\.venv\Scripts\python.exe scripts/build_antigravity.py --check
.\.venv\Scripts\python.exe scripts/validate_evidence.py .claude\skills\admin\resources\claim-ledger.example.yml
git diff --check
```

Expected: all commands exit `0`.

- [ ] **Step 5: Commit**

```powershell
git add README.md docs evals .github notes/INDEX.md
git commit -m "docs: add Antigravity install and evidence evals"
```

---

### Task 9: Code review and full pre-pilot verification

**Files:**
- Review: all branch changes
- Write: `notes/verification-antigravity-evidence-first.md`

**Interfaces:**
- Produces: evidence-backed verification record before touching the active profile.

- [ ] **Step 1: Review tests before implementation**

Run a code review focused on unsafe path handling, unmanaged overwrite/deletion,
frontmatter parsing, transformation ambiguity, false-green validation, and test quality.

- [ ] **Step 2: Fix every high/medium finding with a regression test**

For each code defect, reproduce RED, apply the smallest fix, and verify GREEN.

- [ ] **Step 3: Run the complete fresh suite**

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe .claude\skills\test-framework\scripts\test_skills.py --skills-root .claude\skills --json
.\.venv\Scripts\python.exe scripts/build_antigravity.py --check
.\.venv\Scripts\python.exe scripts/validate_evidence.py .claude\skills\admin\resources\claim-ledger.example.yml --json
git diff --check
```

Record exact command, timestamp, exit code, and counts in the verification note.

- [ ] **Step 4: Commit**

```powershell
git add tests scripts notes/verification-antigravity-evidence-first.md
git commit -m "test: verify Antigravity evidence distribution"
```

---

### Task 10: Install and validate the isolated Antigravity pilot

**Files:**
- Install only: `C:\Users\Asus\.gemini\config\skills\admin-evidence-pilot\`
- Record: `notes/verification-antigravity-pilot.md`

**Interfaces:**
- Consumes: verified repository output.
- Produces: real product discovery/invocation verdict without changing existing skills.

- [ ] **Step 1: Install pilot only**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Mode Direct -Scope Global -Pilot
```

Expected: one new pilot skill; production `/admin`, all 69 current skills, `cv-maker`,
rules, and MCP files remain unchanged.

- [ ] **Step 2: Run static pilot gate**

Strictly parse the installed pilot with Antigravity's bundled `js-yaml`, verify folder/name
equality, hash equality with source, and installed skill baseline increase by one.

- [ ] **Step 3: Run the product gate in a new Antigravity chat**

The human user opens a new Antigravity chat, confirms the pilot in `/`, invokes the case
from Task 8, and returns the complete output or screenshot. This step cannot be replaced
by the editor CLI because Antigravity IDE 2.0.3 exposes no supported slash-skill invoke
command.

- [ ] **Step 4: Score all eight pilot conditions**

Pass only if discovery, protocol marker, false-premise rejection, correct official path,
official-source support, product distinction, uncertainty labelling, and operation budget
all pass. Otherwise roll back the isolated pilot and return to the failing task.

- [ ] **Step 5: Remove or archive the pilot**

Use installer uninstall/pilot rollback so installed skill count returns to its baseline.

---

### Task 11: Roll out all generated skills to the active Antigravity profile

**Files:**
- Update: `C:\Users\Asus\.gemini\config\skills\<69 managed skills>\`
- Create: `C:\Users\Asus\.gemini\config\rules\evidence-first.md`
- Preserve: `C:\Users\Asus\.gemini\config\skills\cv-maker\`
- Create: managed backup and ownership manifest

**Interfaces:**
- Consumes: a passing pilot verdict.
- Produces: full local Evidence-First GOBAL skill set.

- [ ] **Step 1: Capture baseline hashes and counts**

Record the 70 current `SKILL.md`, unrelated skill names, active rules, plugin paths, and
MCP hashes before mutation.

- [ ] **Step 2: Run full managed install with backup**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Mode Direct -Scope Global -Force
```

- [ ] **Step 3: Run static post-install verification**

Require 69 managed generated skills plus preserved `cv-maker`; strict-parse every
installed manifest; compare managed hashes; confirm evidence rule parses; confirm MCP hash
is unchanged; confirm backup and ownership manifest exist.

- [ ] **Step 4: Run new-chat product verification**

Confirm `/admin` appears and invoke one short official-source fact check. If product-level
verification cannot be observed, report static installation separately and do not call
activation verified.

---

### Task 12: Finish, merge, and push

**Files:**
- Review: branch diff against `main`
- Update: verification note with final local rollout state

**Interfaces:**
- Produces: reviewed Git history on `main` and updated GitHub repository.

- [ ] **Step 1: Run final verification after local rollout**

Re-run the complete suite and generated drift check. Confirm repository status contains
only intended changes.

- [ ] **Step 2: Fast-forward `main` after review**

```powershell
git switch main
git merge --ff-only feat/antigravity-evidence-first
```

- [ ] **Step 3: Push and verify the remote commit**

```powershell
git push origin main
git ls-remote origin refs/heads/main
```

Require the remote SHA to equal local `main` before reporting GitHub updated.
