import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from scripts.normalize_frontmatter import NormalizeError, main, normalize_text
from scripts.skill_manifest import load_frontmatter


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / ".claude" / "skills"


class NormalizeFrontmatterTests(unittest.TestCase):
    def parse_normalized(self, text: str):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "SKILL.md"
            path.write_text(text, encoding="utf-8", newline="\n")
            return load_frontmatter(path, canonical=True)

    def test_quotes_unquoted_description_containing_colon(self):
        source = (
            "---\n"
            "name: demo\n"
            "description: Modes: quick and safe\n"
            "argument-hint: <topic>\n"
            "allowed-tools: Read Write\n"
            "---\n\n"
            "# Demo\n"
        )

        normalized = normalize_text(source)

        data, _ = self.parse_normalized(normalized)
        self.assertEqual(data["description"], "Modes: quick and safe")
        self.assertIn('description: "Modes: quick and safe"\n', normalized)

    def test_restores_list_shaped_argument_hint_as_literal_string(self):
        source = (
            "---\n"
            "name: demo\n"
            "description: Use when testing.\n"
            "argument-hint: [quick|deep]\n"
            "allowed-tools: Read\n"
            "---\n# Demo\n"
        )

        normalized = normalize_text(source)

        data, _ = self.parse_normalized(normalized)
        self.assertEqual(data["argument-hint"], "[quick|deep]")
        self.assertIn('argument-hint: "[quick|deep]"\n', normalized)

    def test_preserves_boolean_and_other_scalar_types(self):
        source = (
            "---\n"
            "name: demo\n"
            "description: Use when testing.\n"
            "user_invocable: true\n"
            "retries: 3\n"
            "threshold: 1.5\n"
            "optional: null\n"
            "args: mode\n"
            "argument-hint: <topic>\n"
            "allowed-tools: Read\n"
            "---\n# Demo\n"
        )

        normalized = normalize_text(source)

        data, _ = self.parse_normalized(normalized)
        self.assertIs(data["user_invocable"], True)
        self.assertEqual(data["retries"], 3)
        self.assertEqual(data["threshold"], 1.5)
        self.assertIsNone(data["optional"])
        self.assertEqual(data["args"], "mode")

    def test_canonical_string_fields_remain_strings_when_scalar_shaped(self):
        source = (
            "---\n"
            "name: 123\n"
            "description: true\n"
            "args: null\n"
            "argument-hint: false\n"
            "allowed-tools: false\n"
            "---\n# Demo\n"
        )

        normalized = normalize_text(source)

        data, _ = self.parse_normalized(normalized)
        self.assertEqual(data["name"], "123")
        self.assertEqual(data["description"], "true")
        self.assertEqual(data["args"], "null")
        self.assertEqual(data["argument-hint"], "false")
        self.assertEqual(data["allowed-tools"], "false")

    def test_is_idempotent_and_normalizes_line_endings(self):
        source = (
            "---\r\n"
            "allowed-tools: Read\r\n"
            "description: Use when testing.\r\n"
            "name: demo\r\n"
            "argument-hint: [quick]\r\n"
            "---\r\n\r\n"
            "# Demo\r\n\r\nBody\r\n"
        )

        first = normalize_text(source)
        second = normalize_text(first)

        self.assertEqual(first, second)
        self.assertNotIn("\r", first)

    def test_preserves_complete_markdown_body_apart_from_line_endings(self):
        bodies = (
            "\n\n# Demo\n\nA hard break  \n\n\n  \n",
            "# Demo\r\n\r\nA hard break  \r\n\r\n\t\r\n",
            "\n\tIndented text\nNo final newline \t",
            "",
        )
        for body in bodies:
            with self.subTest(body=repr(body)):
                source = "---\nname: demo\ndescription: Use when testing.\n---\n" + body

                normalized = normalize_text(source)

                normalized_body = normalized.split("\n---\n", 1)[1]
                self.assertEqual(
                    normalized_body, body.replace("\r\n", "\n").replace("\r", "\n")
                )

    def test_preserves_long_quotes_backslashes_and_unicode_on_one_line(self):
        description = (
            "Use when testing: "
            + "x" * 1100
            + ' — giữ nguyên "quoted" text and folder\\file.'
        )
        source = (
            "---\n"
            "name: demo\n"
            f"description: {description}\n"
            "argument-hint: <đường-dẫn>\n"
            "allowed-tools: Read\n"
            "---\n# Demo\n"
        )

        normalized = normalize_text(source)

        data, _ = self.parse_normalized(normalized)
        self.assertEqual(data["description"], description)
        description_lines = [
            line for line in normalized.splitlines() if line.startswith("description:")
        ]
        self.assertEqual(len(description_lines), 1)
        self.assertGreater(len(description_lines[0]), 1000)

    def test_refuses_duplicate_keys_before_serializing(self):
        source = (
            "---\n"
            "name: demo\n"
            "name: duplicate\n"
            "description: Use when testing.\n"
            "---\n# Demo\n"
        )

        with self.assertRaisesRegex(NormalizeError, "duplicate frontmatter key: name"):
            normalize_text(source)

    def test_write_prevalidates_the_whole_batch_before_changing_any_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            sources = {
                "a-valid": b"---\nname: demo\ndescription: Use when testing.\n---\n# Demo\n",
                "z-invalid": b"---\nname: broken\nname: duplicate\n---\n# Broken\n",
            }
            for name, source in sources.items():
                path = root / name / "SKILL.md"
                path.parent.mkdir()
                path.write_bytes(source)
            errors = io.StringIO()

            with redirect_stderr(errors), redirect_stdout(io.StringIO()):
                result = main(["--skills-root", str(root), "--write"])

            self.assertEqual(result, 2)
            self.assertIn("duplicate frontmatter key", errors.getvalue())
            for name, source in sources.items():
                self.assertEqual((root / name / "SKILL.md").read_bytes(), source)

    def test_check_detects_crlf_and_bom_byte_drift_without_writing(self):
        canonical = normalize_text(
            "---\nname: demo\ndescription: Use when testing.\n---\n# Demo\n"
        ).encode("utf-8")
        fixtures = {
            "CRLF": canonical.replace(b"\n", b"\r\n"),
            "BOM": b"\xef\xbb\xbf" + canonical,
        }
        for label, source in fixtures.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                path = root / "SKILL.md"
                path.write_bytes(source)
                output = io.StringIO()

                with redirect_stdout(output):
                    result = main(["--skills-root", str(root), "--check"])

                self.assertEqual(result, 1)
                self.assertIn("1 of 1 skill manifests require normalization", output.getvalue())
                self.assertEqual(path.read_bytes(), source)

    def test_refuses_multiline_and_collection_constructs(self):
        fixtures = {
            "block scalar": (
                "---\nname: demo\ndescription: |\n  Use when testing.\n---\n# Demo\n"
            ),
            "indented continuation": (
                "---\nname: demo\ndescription: Use when testing.\n  continued\n---\n# Demo\n"
            ),
            "flow collection": (
                "---\nname: demo\ndescription: Use when testing.\ntags: [one, two]\n---\n# Demo\n"
            ),
        }

        for label, source in fixtures.items():
            with self.subTest(label=label):
                with self.assertRaises(NormalizeError):
                    normalize_text(source)

    def test_refuses_ambiguous_legacy_values_instead_of_guessing(self):
        fields = (
            "description: |2-",
            "description:",
            "description: Use when testing. # explanation",
            'description: "Use when testing." # "explanation"',
            "argument-hint: &hint [quick]",
            "tags: [one, two",
            "enabled: yes",
            "released: 2026-10-03",
            "duration: 1:20",
            "extra: key: value",
        )
        for field in fields:
            with self.subTest(field=field):
                key = field.split(":", 1)[0]
                description = "" if key == "description" else "description: Use when testing.\n"
                source = "---\nname: demo\n" + description + field + "\n---\n# Demo\n"

                with self.assertRaises(NormalizeError):
                    normalize_text(source)

    def test_complete_repository_round_trip_is_byte_idempotent(self):
        skill_paths = sorted(SKILLS_ROOT.rglob("SKILL.md"))
        inventory = (REPO_ROOT / "config/antigravity-skills.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(sorted(path.parent.name for path in skill_paths), inventory)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            for index, skill_path in enumerate(skill_paths):
                with self.subTest(skill=skill_path.parent.name):
                    source = skill_path.read_text(encoding="utf-8-sig")
                    first = normalize_text(source)
                    normalized_path = temp_root / str(index) / "SKILL.md"
                    normalized_path.parent.mkdir()
                    normalized_path.write_text(
                        first, encoding="utf-8", newline="\n"
                    )
                    load_frontmatter(normalized_path, canonical=True)
                    second = normalize_text(first)
                    self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))

    def test_normalizer_source_contains_no_machine_specific_path(self):
        normalizer_path = REPO_ROOT / "scripts" / "normalize_frontmatter.py"
        source = normalizer_path.read_text(encoding="utf-8")

        self.assertNotIn(str(REPO_ROOT), source)
        self.assertNotRegex(source, r"[A-Za-z]:[\\/]")


if __name__ == "__main__":
    unittest.main()
