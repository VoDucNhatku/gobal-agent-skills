# Antigravity Evidence-First Admin Implementation Plan

> **Goal:** Build, verify, pilot, and roll out a native Antigravity distribution of all GOBAL skills with an evidence-grounded `/admin` workflow.
> **Architecture:** Keep `.claude/skills` as the canonical source, normalize and strictly validate it, then deterministically generate an Antigravity plugin containing portable manifests, translated paths, packaged rules, and companion resources. Gate the full local rollout behind an isolated `/admin-evidence-pilot` test that proves real Antigravity discovery and skill-body activation.
> **Tech Stack:** Python 3.11, pinned PyYAML 6.0.3, `unittest`, PowerShell 5.1, Git, Antigravity IDE 2.0.3, Markdown/YAML/JSON.

## Global Constraints

- Follow RED → GREEN → REFACTOR for executable behaviour.
- Use `apply_patch` for authored source edits; generators may write mechanical output.
- Copying the committed IDE distribution and registering slash skills needs no Python dependency. Executable workers have explicit optional runtime requirements; the structural validator requires Python and pinned PyYAML, packaged with its own parser.
- Developer validation uses `PyYAML==6.0.3` so serialization cannot drift between patch releases.
- Antigravity skill manifests contain only `name` and `description`.
- Generated output must match a committed exact-name inventory of 69 canonical skills, not merely a count, plus one separately generated pilot skill and rule excluded from the production plugin.
- Generated output must contain no unresolved `~/.claude` path and no Claude-only manifest field.
- Never overwrite unrelated global skills, rules, plugins, or MCP configuration.
- Preserve `cv-maker` during local rollout.
- A clean static check is not proof of slash-menu discovery or invocation.
- The full local rollout is forbidden until the isolated pilot passes all UI acceptance checks.
- Generated text uses repository-governed LF endings on every platform; binary assets are copied byte-for-byte.
- The PowerShell installer targets Direct/Global IDE paths. Native IDE plugin installation uses the documented filesystem/Customizations flow and must have a separate product check. `/plugin install` is documented for the interactive TUI, not established as an IDE command.

## Preflight amendment — 2026-10-03 (takes precedence)

The user authorized continuing after `notes/review-antigravity-preflight.md`. Keep the architecture, but execute the repairs and minimal product experiment before broad rollout. Work on the existing feature branch; preserve all in-progress edits. No profile replacement or GitHub publication before the product gates pass.

Execution order: Tasks 2–3 repairs → Task 5 minimal evidence contract → Task 4 minimal/full generated bundles → Task 7 pilot-safe installer tests → Task 10 real IDE canary → remaining Tasks 6–9/full installer checks → Tasks 11–12. Independent repair units may run concurrently with disjoint file ownership and targeted RED/GREEN checks.

Additional acceptance contract:

- Empty/missing roots and unknown skill filters fail with a non-zero exit and machine-readable diagnostic. Discover only immediate skill directories; nested fixture manifests are not registrations.
- Move the reusable parser into the canonical `test-framework/scripts/` bundle; the repository helper imports that implementation. Test copying the skill outside the repository. Document its PyYAML requirement.
- Normalization is schema-aware, preserves Markdown content except specified line-ending normalization, validates the entire batch before writing, and detects byte-level LF drift.
- Install all generated canonical rules plus `evidence-first`, not just the new rule. Inventory legacy/current global roots; never guess duplicate-name precedence or delete unmanaged legacy folders.
- Separate `USER_REPORTED` from `OBSERVED_VERIFIED`. Counter-evidence reopens claims and dependent deductions; it does not automatically establish the correction. Retrieved/attached content and worker evidence are untrusted data, not instructions.
- Update `admin/references/dispatch-protocol.md`, related research dispatch policy and `token-budget`; use one coordinator/worker-shared budget and verified host capabilities with sequential fallback. Remove unsupported fixed Claude context and parallel-cost assumptions from the portable policy.
- Keyword contract tests prove instruction presence only. Separate authored cases, offline structural evaluation and real IDE executions in reports. The semantic reviewer needs an inspected passage/reproducible locator and claim-level evidence stance.
- Ledger negatives cover dangling/cyclic derivations, derivation from NEI, invalid status/evidence combinations and reviewer-record gaps; deterministic validation never claims to prove entailment.
- Pilot temporarily installs one namespaced skill and a concise namespaced `always_on` rule with the production activation shape. It changes no existing skill/rule and is removed after scoring; its global rule affects other chats while installed, so keep the canary window bounded and disclose that lifecycle. No assertion of slash-specific rule activation.
- Installer uses staging, per-file ownership hashes, backups, a lock and a recovery journal; it is a recoverable multi-path transaction, not a single atomic filesystem swap. Test caught errors and interrupted-install recovery only on explicit temporary targets before real profile mutation.
- Record actual calls/time/token usage where available before any performance claim. Release tests never run on each `/admin` request. A single canary does not prove every research lane or eliminate hallucinations.

## Repair checkpoint — 2026-10-04

The user requested starting the fixes after the fresh audit: 130 tests ran, with one
failure and one error in the generator; the actual profile had no installed pilot.
These items extend Tasks 4, 7 and 8 before the Task 10 product gate:

- [x] Pilot vendors only rule dependencies reachable from the admin bundle and temporary
  evidence policy, handling cycles without unrelated domain resources.
- [x] Generator rejects source/output reparse points and divergent unowned or user-modified
  expected outputs before any mutation; unchanged owned output may regenerate.
- [x] Installer avoids staging an unchanged transaction and checks drift immediately before
  recovery writes; temporary-profile tests include external process termination.
- [x] Correct concrete dependency paths in install docs; explicitly distinguish the local
  unpublished checkout from what a fresh GitHub main clone currently contains.
- [x] Run a fresh full suite and independent review, generate the exact distribution, then
  snapshot and install only the reversible namespaced pilot.
- [ ] Obtain the new-chat IDE response and activity trace before full rollout/publication.

Execution status 2026-10-04: foundation and pilot installer pass the fresh 165-test
suite; the nine-file pilot is installed and byte-verified, not IDE-verified. Historical
step checklists below are the original TDD recipe, not a completion ledger. Current
evidence and remaining gates are in `notes/verification-antigravity-evidence-first.md`
and `notes/verification-antigravity-pilot.md`. Task 7 is **pilot-only**; full installer,
full rollout, remote CI and publication remain pending. Do not infer completion from
the generated 69-skill bundle or the local checkpoint commit.

Update 2026-10-05: user returned answer text but not activity trace. Visible official
source/completion gate fails, activation/budget remain unobserved. Per Task 10, isolated
pilot has been uninstalled (9 managed files; baseline count 70; protected bytes unchanged).
Task 10 product acceptance and Tasks 11–12 remain pending. Next prerequisite is the old
run's expanded trace before changing protocol or reinstalling; see evaluation note.

Further update 2026-10-05: old-run activity and Router guide content received. A later
web prompt was appended in the same conversation, not the proposed new-chat control;
UI shows a PowerShell fetch-finished status, without raw command/source output. This
resolves the apparent canary persistence as compatible with retained chat context,
not proof of cache or current pilot activation. Continue Task 10 with a separately
recorded unchanged-payload reinstall and genuine new-chat retest (Task 10b below).
No policy/code repair or 69-skill rollout is authorized by a false clean-test verdict.

Latest update 2026-10-05: Task 10b returned a separate welcome-screen conversation
with the pilot chip and original official-document request. Its answer again substituted
runtime paths for official evidence and reported nothing unverified. Source/completion
FAIL is visible; collapsed activity does not establish retrieval capability or exact body.
Pilot was removed with ownership checks (transaction 577b1245-aae0-46f1-9247-5317f7166447);
baseline 70 entries and protected profile/MCP hashes are restored/unchanged.
Task 10c repairs the explicit evidence-class/completion contract inside the approved
Task 5 design, not a new architecture or a proven fix. No repeated unchanged retest.

---

### Task 1: Establish the Python validation harness

**Files:**
- Create: `.gitignore`
- Create: `.gitattributes`
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
PyYAML==6.0.3
```

`.gitattributes`:

```gitattributes
* text=auto
*.md text eol=lf
*.py text eol=lf
*.ps1 text eol=lf
*.json text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
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
git add .gitignore .gitattributes requirements-dev.txt scripts tests
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
- Validate unambiguous local and peer-skill resource paths in Markdown links and backticks,
  including `scripts/`, `references/`, `assets/`, `templates/`, and `resources/` with
  any extension. Do not treat generic prose tokens as paths.
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
- preserves one-line long descriptions, quotes, backslashes, and Unicode;
- makes the complete 69-skill normalize → parse → normalize cycle byte-idempotent;
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
- Create: `config/antigravity-skills.txt`
- Create: `config/antigravity-compatibility.yml`
- Create: `scripts/build_antigravity.py`
- Create: `tests/test_build_antigravity.py`
- Generate: `skills/`
- Generate: `rules/`
- Generate: `pilot/skills/admin-evidence-pilot/SKILL.md`
- Generate: `pilot/rules/admin-evidence-pilot.md`
- Generate: `pilot/manifest.json`

**Interfaces:**
- Consumes: strict canonical skills and `.claude/rules`.
- Produces: complete Antigravity plugin tree, a production-shaped namespaced pilot,
  exact file inventories, and a `--check` drift gate.

- [ ] **Step 1: Add failing generator tests**

Tests assert that a fixture build:

- emits only `name` and `description` in generated frontmatter;
- recursively copies companion files;
- maps rule and peer-skill paths relative to each generated text file;
- rewrites runtime/path tokens only through the committed compatibility table and rejects
  unresolved `~/.claude`, missing resources, and unsupported Claude-only tool identifiers;
- vendors the manifest parser beside the installed `test-framework` script and proves that
  script starts outside the repository;
- produces byte-identical output twice;
- normalizes every generated text file to LF while preserving binary bytes;
- rejects stale/orphan generated files after an add, remove, or rename;
- excludes `references/` and `test-reports/` as top-level skills;
- matches the exact 69-name inventory for the real repository;
- emits a pilot skill, a concise namespaced `always_on` pilot rule, and a manifest of their hashes.

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
rules are `model_decision` with descriptions. The pilot rule has the production `always_on`
shape, is namespaced and temporary, and affects all chats while installed; it is not part of the
production plugin. Fail instead of guessing an unknown path or tool ABI. Compare the complete expected
file set, so `--check` fails on both missing output and orphan output.

- [ ] **Step 4: Generate and verify GREEN**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_build_antigravity -v
.\.venv\Scripts\python.exe scripts/build_antigravity.py
.\.venv\Scripts\python.exe scripts/build_antigravity.py --check
```

Expected: the exact 69 generated skill names plus the isolated pilot artifact; deterministic
check exits `0`; no generated `~/.claude`; installed `test-framework` smoke starts without
repository-root imports.

- [ ] **Step 5: Commit**

```powershell
git add plugin.json config scripts/build_antigravity.py tests/test_build_antigravity.py skills rules pilot
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
- Modify: `.claude/skills/admin/references/dispatch-protocol.md`
- Modify: `.claude/skills/token-budget/SKILL.md`
- Modify: `.claude/skills/research-admin/SKILL.md`
- Create: `tests/test_evidence_skill_contract.py`

**Interfaces:**
- Produces: lane selection, task/fact/progress ledgers, source qualification, claim-level
  citation gate, calibrated synthesis, and bounded runtime budgets.

- [ ] **Step 1: Add failing contract tests**

Tests inspect the authored files and assert instruction presence only, not model adherence:

```python
required_admin_terms = {
    "Fast non-research", "Quick evidence", "Standard evidence", "Deep evidence",
    "OBSERVED_VERIFIED", "USER_REPORTED", "LOOKUP", "DERIVE", "ASSUMPTION_OR_UNKNOWN",
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
- Produces: transactional Direct/Global IDE installation, content-hash ownership manifest,
  recoverable backups, and pilot-only installation. Native IDE plugin installation has its
  own filesystem/Customizations workflow and product gate documented in Task 8.

- [ ] **Step 1: Add failing installer integration tests**

From Python, invoke PowerShell against a temporary `-ProfileRoot` and assert:

- `-Pilot` installs only `admin-evidence-pilot` and a concise namespaced temporary `always_on` rule;
- pilot mode installs the namespaced pilot rule and verifies the pilot manifest hashes;
- full mode installs the exact 69-skill inventory and every generated shared rule;
- unrelated `cv-maker` survives update and uninstall;
- unmanaged collision fails without `-Force`;
- forced collision is copied to a timestamped backup;
- update/uninstall refuses to delete a managed file whose content drifted since install,
  unless `-Force` first backs it up;
- invalid source aborts before destination mutation;
- dry run performs no writes;
- injected mid-install failure restores the complete pre-install tree;
- corrupt ownership manifests and junction/reparse-point escapes fail closed;
- paths containing spaces and Unicode work under Windows PowerShell Desktop 5.1.

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
  [string]$SourcePath = (Split-Path -Parent $PSScriptRoot),
  [string]$ProfileRoot = $env:USERPROFILE,
  [switch]$Pilot,
  [switch]$Force,
  [switch]$Uninstall,
  [switch]$DryRun
)
```

Use `-LiteralPath`, resolved target containment checks, and reparse-point rejection. Build a
same-volume staging tree, validate its exact file set and hashes, then swap managed paths with
rollback on caught failures, a lock, a recovery journal and an explicit recovery operation. Record per-file installed hashes; updates and uninstall are
drift-aware. Never touch `mcp_config.json`.

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

Use the complete `IDE-FALSE-PREMISE` fixture in `evals/admin-research/cases.yml`; it adds
the source-instruction trust-boundary probe. The skill body supplies `Protocol: AG-EF-PILOT-1`
and the temporary rule separately supplies `Rule Canary: AG-EF-RULE-1`. Do not put either
marker in the user prompt. Stay within the Quick ceiling of one round, three queries and
two source opens; markers without loaded-source/tool trace are not an activation verdict.

- [ ] **Step 2: Document exact install and verification commands**

Include:

- clone and native IDE filesystem/Customizations plugin installation (not an unverified TUI command);
- direct standalone IDE install via PowerShell;
- update and uninstall;
- strict parser/count diagnostics;
- new-chat `/` and `/admin` checks;
- distinction between static validity, discovery, and invocation;
- rollback location and preservation of unrelated skills.
- an explicit statement that the installer supports Direct/Global only; Workspace and native
  Plugin installs use Antigravity's documented paths/commands rather than untested script modes.

- [ ] **Step 3: Add CI**

Use both Ubuntu and `windows-latest`. The Windows job explicitly asserts Windows PowerShell
Desktop 5.1 and executes the Unicode/space-path installer cases with `powershell.exe`. Both jobs
install the pinned `requirements-dev.txt`, run `python -m unittest discover -s tests -v`, the
canonical skill validator, generator `--check`, exact-inventory/orphan checks, and evidence
example validation.

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
- Install only: `C:\Users\Asus\.gemini\config\rules\admin-evidence-pilot.md` (temporary global rule)
- Record: `notes/verification-antigravity-pilot.md`

**Interfaces:**
- Consumes: verified repository output.
- Produces: real product discovery/invocation verdict without changing existing skills.

- [x] **Step 1: Install pilot only**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Pilot
```

Expected: one new pilot skill plus its namespaced temporary `always_on` rule; production `/admin`,
all 69 current skills, `cv-maker`, production rules, and MCP files remain unchanged.

- [x] **Step 2: Run static pilot gate**

Strictly parse the installed pilot and rule with the repository-pinned parser, verify
folder/name equality, exact manifest/hash equality with the generated pilot, and installed
skill baseline increase by one. The IDE discovery result—not an undocumented bundled parser—is
the product-authority check.

- [ ] **Step 3: Run the product gate in a new Antigravity chat**

The human user opens a new Antigravity chat, records the exact app version, confirms the pilot
in `/`, invokes the case from Task 8, and returns the complete output plus activity/tool trace.
This step cannot be replaced by the editor CLI because Antigravity IDE 2.0.3 exposes no
supported slash-skill invoke command. A final-answer screenshot alone cannot prove the operation
budget.

- [ ] **Step 4: Score all eight pilot conditions**

Pass only if discovery, protocol marker, false-premise rejection, correct official path,
official-source support, product distinction, uncertainty labelling, and operation budget
all pass. Otherwise roll back the isolated pilot and return to the failing task.

- [x] **Step 5: Remove or archive the pilot**

Use installer uninstall/pilot rollback so installed skill count returns to its baseline.

---

### Task 10b: Repeat the unchanged pilot in a genuinely new conversation

This repeats Task 10, not a candidate policy fix. Scope remains nine managed pilot files
and one bounded new-chat case; global pilot rule is temporary and removed after scoring.
Existing profile skills, cv-maker, rules, MCP, source policy and GitHub stay unchanged.

- [x] Re-run the complete suite, generated drift check, canonical validation and ledger
  structural check; require all exits 0. Dry-run the existing pilot-only installer.
- [x] Immediately snapshot protected bytes; install without Force; check the nine payload
  and ownership hashes, exact inventory, strict metadata, committed journal and 70→71
  SKILL.md entries. Compare protected profile/MCP hashes before/after.
- [x] Receive separate-conversation answer/screenshot; expanded activity, exact loaded
  body and operation budget remain unobserved. Do not call that missing trace a pass.
- [x] Score visible source/completion FAIL separately from prior same-chat responses,
  record limits/budget, then uninstall
  the temporary pilot with protected bytes and baseline skill count verified.

---

### Task 10c: Narrow evidence-class correction after the reproduced failure

Scope: canonical admin entrypoint, research reference and concise evidence-first rule;
regenerate their native/pilot counterparts. Preserve lane ceilings, zero Quick workers,
existing profile and the full-rollout gate. This is a candidate compliance correction,
not a demonstrated internal root cause or a Gemini pass.

- [x] Record the observed RED: official-document request answered with runtime metadata
  and false closure. Separate it from unknown source-loading/capability causes.
- [x] Bind requested evidence class at intake and final acceptance; official publisher
  passage/URL/locator cannot be replaced by local catalog/path checks. Retrieval failure
  retains NEI/Unverified. Ancillary product claims require their own support.
- [x] Strengthen the authored case's grading criteria without relabelling fixtures as runs.
- [x] Regenerate, run fresh structural/integration checks and independent forward tests;
  record failures and costs/operation counts without claiming Gemini adherence.
- Local result: 165 tests / 145.387s / OK; canonical 693 PASS; generator, quick_validate,
  ledger structural check and pilot dry-run pass. Final Codex Quick test meets operation
  count ceilings but reports 25,729 opened-source characters against 20,000; no aggregate
  performance or Gemini claim. See evaluation note for exact candidate hash and limits.
- [ ] Arrange a bounded candidate-pilot window with the human, then install/check only
  namespaced payload, obtain one new-chat result and score/remove it. No rollout on
  static checks, Codex forward tests or canary markers alone.

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
- Rollback: if static or new-chat product verification fails, restore the pre-install snapshot
  transactionally and preserve the failed install evidence for diagnosis.

- [ ] **Step 1: Capture baseline hashes and counts**

Record the 70 current `SKILL.md`, unrelated skill names, active rules, plugin paths, and
MCP hashes before mutation.

- [ ] **Step 2: Run full managed install with backup**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\install-antigravity.ps1 -Force
```

- [ ] **Step 3: Run static post-install verification**

Require 69 managed generated skills plus preserved `cv-maker`; strict-parse every
installed manifest; compare managed hashes; confirm evidence rule parses; confirm MCP hash
is unchanged; confirm backup and ownership manifest exist.

- [ ] **Step 4: Run new-chat product verification**

Confirm `/admin` appears and invoke one short official-source fact check. If product-level
verification cannot be observed, report static installation separately and do not call
activation verified. If discovery or invocation fails, execute rollback before any completion
claim.

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
