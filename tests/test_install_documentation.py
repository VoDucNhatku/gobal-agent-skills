"""Checks for concrete install paths, not IDE or model behavior."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallDocumentationTests(unittest.TestCase):
    def test_claude_quick_start_dependency_path_exists_in_canonical_bundle(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        paths = re.findall(r"pip install -r ~/.claude/(\S+)", readme)
        self.assertTrue(paths, "Copied-skill optional dependency command is missing")
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue((ROOT / ".claude" / path).is_file(), path)

    def test_pilot_documentation_explicitly_labels_local_unpublished_checkout(self):
        guide = (ROOT / "docs/ANTIGRAVITY.md").read_text(encoding="utf-8")
        self.assertTrue("GitHub main chưa có bản này" in guide, "Unpublished release status is missing")
        self.assertTrue("checkout local" in guide, "Local checkout scope is missing")

    def test_current_vietnamese_intro_matches_rule_inventory_and_no_fixed_cost(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        current = readme.split("# Tiếng Việt", 1)[1]
        rules = list((ROOT / ".claude/rules").glob("*.md"))
        self.assertTrue(f"{len(rules)} file quy tắc" in current, "Shared rule count is stale")
        for obsolete in ("1.9k tok", "5.8k tok", "gấp 10 lần", "giá trị ≥ 2k token",
                         "`web-admin` lo cả chuỗi", "ép chạy song song"):
            self.assertTrue(obsolete not in current, f"Obsolete current policy: {obsolete}")

    def test_copied_validator_examples_explicitly_select_the_host(self):
        for name in ("SKILL.md", "README.md"):
            text = (ROOT / ".claude/skills/test-framework" / name).read_text(encoding="utf-8")
            for line in text.splitlines():
                if line.startswith("python scripts/test_skills.py"):
                    self.assertIn("--host", line, f"Ambiguous host in {name}")


if __name__ == "__main__":
    unittest.main()
