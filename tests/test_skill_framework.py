import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = (
    REPO_ROOT
    / ".claude"
    / "skills"
    / "test-framework"
    / "scripts"
    / "test_skills.py"
)


class SkillFrameworkTests(unittest.TestCase):
    def test_invalid_utf8_returns_a_structured_failure(self):
        skill_dir = self.write_skill("alpha")
        (skill_dir / "SKILL.md").write_bytes(b"\xff\xfeinvalid text")
        completed = self.run_validator()
        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertEqual(report["summary"]["validated"], 0)
        self.assertTrue(any("UTF-8" in issue for issue in self.issues(report)))

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.skills_root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_skill(self, directory: str, *, name: str | None = None, body: str = "# Demo\n"):
        skill_dir = self.skills_root / directory
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_name = directory if name is None else name
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            f"name: {skill_name}\n"
            'description: "Use when testing the validator."\n'
            'argument-hint: "[quick]"\n'
            'allowed-tools: "Read"\n'
            "---\n\n"
            f"{body}",
            encoding="utf-8",
        )
        return skill_dir

    def run_validator(self, *arguments, validator=VALIDATOR, cwd=REPO_ROOT):
        return subprocess.run(
            [
                sys.executable,
                str(validator),
                "--skills-root",
                str(self.skills_root),
                "--json",
                *arguments,
            ],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def parse_report(self, completed):
        try:
            return json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            self.fail(
                f"validator did not emit JSON: {exc}\n"
                f"stdout={completed.stdout!r}\nstderr={completed.stderr!r}"
            )

    @staticmethod
    def issues(report):
        return [issue for skill in report["skills"] for issue in skill["issues"]]

    def test_nonexistent_root_returns_machine_readable_error(self):
        self.skills_root = self.skills_root / "missing"

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertEqual(report["errors"][0]["code"], "invalid_skills_root")
        self.assertEqual(report["summary"]["validated"], 0)

    def test_invalid_yaml_is_a_hard_failure(self):
        skill_dir = self.skills_root / "alpha"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: alpha\ndescription: Modes: quick\n---\n# Demo\n",
            encoding="utf-8",
        )

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertTrue(
            any("invalid YAML" in issue for issue in self.issues(report)),
            report,
        )

    def test_empty_root_returns_machine_readable_error(self):
        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertEqual(report["errors"][0]["code"], "empty_skills_root")

    def test_unknown_skill_returns_machine_readable_error(self):
        self.write_skill("alpha")

        completed = self.run_validator("--skill", "unknown")

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertEqual(report["errors"][0]["code"], "unknown_skill")
        self.assertIn("unknown", report["errors"][0]["message"])

    def test_nested_fixture_manifests_are_not_registered(self):
        self.write_skill("alpha")
        self.write_skill("alpha/tests/fixture", name="invalid-fixture")

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        report = self.parse_report(completed)
        self.assertEqual(report["summary"]["discovered"], 1)
        self.assertEqual([skill["skill"] for skill in report["skills"]], ["alpha"])

    def test_antigravity_schema_accepts_portable_fields(self):
        skill_dir = self.write_skill("alpha")
        (skill_dir / "SKILL.md").write_text(
            '---\nname: alpha\ndescription: "Use when testing."\n---\n# Demo\n',
            encoding="utf-8",
        )

        completed = self.run_validator("--host", "antigravity")

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        report = self.parse_report(completed)
        self.assertEqual(report["summary"]["validated"], 1)

    def test_antigravity_schema_rejects_extra_manifest_fields(self):
        for field in ("allowed-tools", "argument-hint", "unexpected"):
            with self.subTest(field=field):
                skill_dir = self.write_skill("alpha")
                (skill_dir / "SKILL.md").write_text(
                    '---\nname: alpha\ndescription: "Use when testing."\n'
                    f'{field}: "Read"\n---\n# Demo\n', encoding="utf-8",
                )

                completed = self.run_validator("--host", "antigravity")

                self.assertEqual(completed.returncode, 1)
                report = self.parse_report(completed)
                self.assertTrue(any(field in issue for issue in self.issues(report)), report)

    def test_test_framework_is_counted_when_it_has_a_skill_manifest(self):
        self.write_skill("alpha")
        self.write_skill("test-framework")

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        report = self.parse_report(completed)
        self.assertEqual(report["summary"]["discovered"], 2)
        self.assertEqual(report["summary"]["validated"], 2)

    def test_missing_local_resource_is_a_hard_failure(self):
        self.write_skill("alpha", body="Run `scripts/missing.py`.\n")

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertTrue(
            any("scripts/missing.py" in issue for issue in self.issues(report)),
            report,
        )

    def test_fenced_command_skill_root_path_checks_missing_resource(self):
        self.write_skill("alpha", body=(
            "```bash\npython '<skills>/alpha/scripts/missing.py' --json\n```\n"
        ))

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertTrue(any("alpha/scripts/missing.py" in issue for issue in self.issues(report)), report)

    def test_name_must_equal_directory(self):
        self.write_skill("alpha", name="beta")

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        diagnostic = "\n".join(self.issues(report))
        self.assertIn("alpha", diagnostic)
        self.assertIn("beta", diagnostic)

    def test_name_requires_kebab_case_even_when_directory_matches(self):
        for name in ("alpha_beta", "alpha.beta", "-alpha", "alpha-", "alpha--beta"):
            with self.subTest(name=name):
                self.write_skill(name)

                completed = self.run_validator(f"--skill={name}")

                self.assertEqual(completed.returncode, 1)
                report = self.parse_report(completed)
                self.assertTrue(any("kebab-case" in issue for issue in self.issues(report)), report)

    def test_wrong_canonical_field_type_is_a_hard_failure(self):
        skill_dir = self.write_skill("alpha")
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: alpha\n"
            'description: "Use when testing the validator."\n'
            "argument-hint: [quick]\n"
            'allowed-tools: "Read"\n'
            "---\n# Demo\n",
            encoding="utf-8",
        )

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertTrue(
            any("argument-hint" in issue and "string" in issue for issue in self.issues(report)),
            report,
        )

    def test_only_backticked_skill_local_resource_paths_are_checked(self):
        self.write_skill(
            "alpha",
            body=(
                "Ignore scripts/missing.py when it is not backticked.\n"
                "Ignore `docs/missing.md`, `README.md`, and `/scripts/missing.py`.\n"
                "Ignore non-literal `references/*.md`, `scripts/<name>.py`, and "
                "`templates/{kind}.md` examples.\n"
                "```bash\n"
                "python '<skills>/<skill-name>/scripts/tool.py'\n"
                "python '<skills>/alpha/scripts/<name>.py'\n"
                "python '<skills>/alpha/scripts/*.py'\n"
                "```\n"
            ),
        )

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_fenced_command_skill_root_path_resolves_existing_resource(self):
        skill_dir = self.write_skill("alpha", body=(
            "```bash\npython '<skills>/alpha/scripts/tool.py'\n```\n"
        ))
        (skill_dir / "scripts").mkdir()
        (skill_dir / "scripts" / "tool.py").write_text("", encoding="utf-8")

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_markdown_linked_local_resource_is_checked(self):
        self.write_skill(
            "alpha",
            body="Read the [local guide](references/missing-guide.md).\n",
        )

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertTrue(
            any("references/missing-guide.md" in issue for issue in self.issues(report)),
            report,
        )

    def test_existing_resource_file_and_directory_resolve_from_skill_directory(self):
        skill_dir = self.write_skill(
            "alpha",
            body=(
                "Use `scripts/tool.py`, `scripts/profiles.json`, `references/guide.md`, "
                "`assets/icons/`, `templates/page.md`, and `resources/examples/`.\n"
            ),
        )
        (skill_dir / "scripts").mkdir()
        (skill_dir / "scripts" / "tool.py").write_text("", encoding="utf-8")
        (skill_dir / "scripts" / "profiles.json").write_text("{}", encoding="utf-8")
        (skill_dir / "references").mkdir()
        (skill_dir / "references" / "guide.md").write_text("", encoding="utf-8")
        (skill_dir / "assets" / "icons").mkdir(parents=True)
        (skill_dir / "templates").mkdir()
        (skill_dir / "templates" / "page.md").write_text("", encoding="utf-8")
        (skill_dir / "resources" / "examples").mkdir(parents=True)

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_explicit_peer_skill_resource_resolves_from_referencing_skill(self):
        self.write_skill(
            "alpha",
            body="Use `../beta/references/shared.md` from the peer skill.\n",
        )
        peer_dir = self.write_skill("beta")
        (peer_dir / "references").mkdir()
        (peer_dir / "references" / "shared.md").write_text("", encoding="utf-8")

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_missing_explicit_peer_skill_resource_is_a_hard_failure(self):
        self.write_skill(
            "alpha",
            body="Use `../beta/templates/missing.md` from the peer skill.\n",
        )
        self.write_skill("beta")

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertTrue(
            any("../beta/templates/missing.md" in issue for issue in self.issues(report)),
            report,
        )

    def test_named_peer_skill_resource_resolves_from_skills_root(self):
        self.write_skill(
            "alpha",
            body="Use `beta/references/shared.md` from the peer skill.\n",
        )
        peer_dir = self.write_skill("beta")
        (peer_dir / "references").mkdir()
        (peer_dir / "references" / "shared.md").write_text("", encoding="utf-8")

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_missing_named_peer_skill_resource_is_a_hard_failure(self):
        self.write_skill(
            "alpha",
            body="Use `beta/references/missing.md` from the peer skill.\n",
        )
        self.write_skill("beta")

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 1)
        report = self.parse_report(completed)
        self.assertTrue(
            any("beta/references/missing.md" in issue for issue in self.issues(report)),
            report,
        )

    def test_bare_resource_directory_is_not_a_file_claim(self):
        self.write_skill(
            "alpha",
            body="Keep rarely used material in `references/`.\n",
        )

        completed = self.run_validator()

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_copied_skill_runs_without_repository_from_external_cwd(self):
        copied_skill = self.skills_root / "test-framework"
        shutil.copytree(VALIDATOR.parents[1], copied_skill, ignore=shutil.ignore_patterns("__pycache__"))
        external_cwd = self.skills_root / "unrelated-working-directory"
        external_cwd.mkdir()
        self.write_skill("alpha")

        completed = self.run_validator(
            validator=copied_skill / "scripts" / "test_skills.py", cwd=external_cwd,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        report = self.parse_report(completed)
        self.assertEqual(report["summary"]["validated"], 2)


if __name__ == "__main__":
    unittest.main()
