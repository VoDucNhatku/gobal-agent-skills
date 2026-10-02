import tempfile
import unittest
from pathlib import Path

from scripts.skill_manifest import (
    ManifestError,
    dump_skill,
    load_frontmatter,
    split_frontmatter,
)


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
            "---\nname: demo\ndescription: \"Use when testing.\"\n"
            "argument-hint: [quick]\nallowed-tools: Read\n---\n# Demo\n"
        )
        with self.assertRaisesRegex(ManifestError, "argument-hint"):
            load_frontmatter(path, canonical=True)

    def test_accepts_quoted_canonical_manifest(self):
        path = self.write_skill(
            "---\nname: demo\ndescription: \"Use when testing.\"\n"
            "argument-hint: \"[quick]\"\nallowed-tools: \"Read\"\n---\n# Demo\n"
        )
        data, body = load_frontmatter(path, canonical=True)
        self.assertEqual(data["name"], "demo")
        self.assertIn("# Demo", body)

    def test_rejects_duplicate_yaml_keys(self):
        path = self.write_skill(
            "---\nname: demo\nname: duplicate\ndescription: \"Use when testing.\"\n"
            "---\n# Demo\n"
        )
        with self.assertRaisesRegex(ManifestError, "duplicate YAML key: name"):
            load_frontmatter(path)

    def test_requires_opening_frontmatter_delimiter(self):
        with self.assertRaisesRegex(ManifestError, "must start"):
            split_frontmatter("name: demo\n---\n# Demo\n")

    def test_requires_closing_frontmatter_delimiter(self):
        with self.assertRaisesRegex(ManifestError, "missing the closing"):
            split_frontmatter("---\nname: demo\n# Demo\n")

    def test_requires_frontmatter_to_be_mapping(self):
        path = self.write_skill("---\n- demo\n---\n# Demo\n")
        with self.assertRaisesRegex(ManifestError, "frontmatter must be a mapping"):
            load_frontmatter(path)

    def test_requires_name_to_be_non_empty_string(self):
        path = self.write_skill("---\nname: 123\ndescription: demo\n---\n# Demo\n")
        with self.assertRaisesRegex(ManifestError, "name must be a non-empty string"):
            load_frontmatter(path)

    def test_requires_description_to_be_non_empty_string(self):
        path = self.write_skill("---\nname: demo\ndescription: \"  \"\n---\n# Demo\n")
        with self.assertRaisesRegex(ManifestError, "description must be a non-empty string"):
            load_frontmatter(path)

    def test_requires_allowed_tools_to_be_string_for_canonical_skill(self):
        path = self.write_skill(
            "---\nname: demo\ndescription: demo\nallowed-tools: [Read]\n---\n# Demo\n"
        )
        with self.assertRaisesRegex(ManifestError, "allowed-tools"):
            load_frontmatter(path, canonical=True)

    def test_dump_skill_is_deterministic_and_normalizes_body(self):
        frontmatter = {
            "allowed-tools": "Read",
            "description": "Modes: quick",
            "name": "demo",
            "argument-hint": "[quick]",
        }
        body = "\r\n# Demo\r\n\r\nBody\r"

        first = dump_skill(frontmatter, body)
        second = dump_skill(frontmatter, body)

        self.assertEqual(first, second)
        self.assertEqual(
            first,
            "---\nname: demo\ndescription: 'Modes: quick'\nallowed-tools: Read\n"
            "argument-hint: '[quick]'\n---\n\n# Demo\n\nBody\n",
        )

    def test_dump_skill_uses_stable_key_order_independent_of_input_order(self):
        first = {
            "allowed-tools": "Read",
            "description": "Demo",
            "name": "demo",
            "argument-hint": "[quick]",
        }
        second = {
            "argument-hint": "[quick]",
            "name": "demo",
            "description": "Demo",
            "allowed-tools": "Read",
        }

        self.assertEqual(dump_skill(first, "# Demo"), dump_skill(second, "# Demo"))


if __name__ == "__main__":
    unittest.main()
