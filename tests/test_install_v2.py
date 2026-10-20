"""Temporary-profile tests for scripts/install_v2.mjs (the Claude Code installer)."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install_v2.mjs"
NODE = shutil.which("node")


@unittest.skipUnless(NODE, "Node.js is unavailable")
class InstallV2Tests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="gobal install v2 ")
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        # A disposable checkout: the installer resolves its source next to its own path.
        self.repo = self.root / "repo"
        (self.repo / "scripts").mkdir(parents=True)
        shutil.copy2(INSTALLER, self.repo / "scripts" / "install_v2.mjs")
        self.write(self.repo / ".claude/skills/paper-read/SKILL.md", "---\nname: paper-read\n---\nv2\n")
        self.write(self.repo / ".claude/skills/paper-read/references/guide.md", "v2 guide\n")
        self.write(self.repo / ".claude/skills/_shared/evidence.md", "shared\n")
        self.write(self.repo / ".claude/rules/evidence-first.md", "v2 evidence rule\n")
        self.profile = self.root / "profile tiếng Việt"
        self.skills = self.profile / "skills"
        self.rules = self.profile / "rules"

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_installer(self, *arguments):
        result = subprocess.run(
            [NODE, str(self.repo / "scripts" / "install_v2.mjs"), "--target", str(self.skills), *arguments],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def snapshot(self):
        return {path.relative_to(self.profile).as_posix(): path.read_bytes()
                for path in self.profile.rglob("*") if path.is_file()}

    def backups(self):
        return list(self.profile.glob("skills-backup-*"))

    def test_dry_run_writes_nothing(self):
        self.write(self.rules / "workbench-conventions.md", "v1 rule\n")
        before = self.snapshot()

        output = self.run_installer("--dry-run", "--retire-rules", str(self.rules))

        self.assertIn("rules   retire workbench-conventions.md", output)
        self.assertIn("rules   add evidence-first.md", output)
        self.assertEqual(self.snapshot(), before)

    def test_fresh_profile_gets_skills_and_evidence_rule_without_existing_rules_dir(self):
        self.run_installer("--retire-rules", str(self.rules))

        self.assertEqual((self.skills / "paper-read/references/guide.md").read_text(encoding="utf-8"), "v2 guide\n")
        self.assertTrue((self.skills / "_shared/evidence.md").is_file())
        self.assertEqual(sorted(p.name for p in self.rules.iterdir()), ["evidence-first.md"])
        self.assertEqual((self.rules / "evidence-first.md").read_text(encoding="utf-8"), "v2 evidence rule\n")

    def test_upgrade_retires_v1_rules_keeps_evidence_rule_and_preserves_unrelated_files(self):
        self.write(self.skills / "paper-read/SKILL.md", "v1 paper-read\n")
        self.write(self.skills / "paper-method/SKILL.md", "absorbed v1 skill\n")
        self.write(self.skills / "my-own-skill/SKILL.md", "user skill\n")
        self.write(self.rules / "workbench-conventions.md", "v1 conventions\n")
        self.write(self.rules / "evidence-first.md", "v1 evidence rule\n")
        self.write(self.rules / "user-rule.md", "user rule\n")

        self.run_installer("--retire-rules", str(self.rules))

        self.assertEqual((self.skills / "paper-read/SKILL.md").read_text(encoding="utf-8"), "---\nname: paper-read\n---\nv2\n")
        self.assertFalse((self.skills / "paper-method").exists())
        self.assertEqual((self.skills / "my-own-skill/SKILL.md").read_text(encoding="utf-8"), "user skill\n")
        self.assertEqual(sorted(p.name for p in self.rules.iterdir()), ["evidence-first.md", "user-rule.md"])
        self.assertEqual((self.rules / "evidence-first.md").read_text(encoding="utf-8"), "v2 evidence rule\n")

        [backup] = self.backups()
        self.assertEqual((backup / "paper-read/SKILL.md").read_text(encoding="utf-8"), "v1 paper-read\n")
        self.assertEqual((backup / "paper-method/SKILL.md").read_text(encoding="utf-8"), "absorbed v1 skill\n")
        self.assertEqual((backup / "rules/workbench-conventions.md").read_text(encoding="utf-8"), "v1 conventions\n")
        self.assertEqual((backup / "rules/evidence-first.md").read_text(encoding="utf-8"), "v1 evidence rule\n")

    def test_rerun_leaves_an_up_to_date_evidence_rule_alone(self):
        self.run_installer("--retire-rules", str(self.rules))

        output = self.run_installer("--dry-run", "--retire-rules", str(self.rules))

        self.assertNotIn("rules   ", output)

    def test_back_to_back_upgrades_keep_separate_backups(self):
        self.run_installer()
        (self.skills / "paper-read/SKILL.md").write_text("edited once\n", encoding="utf-8")
        self.run_installer()
        (self.skills / "paper-read/SKILL.md").write_text("edited twice\n", encoding="utf-8")
        self.run_installer()

        saved = sorted((b / "paper-read/SKILL.md").read_text(encoding="utf-8") for b in self.backups())
        self.assertEqual(saved, ["edited once\n", "edited twice\n"])

    def test_without_retire_rules_the_rules_dir_is_untouched(self):
        self.run_installer()

        self.assertFalse(self.rules.exists())


@unittest.skipUnless(NODE, "Node.js is unavailable")
class InstallV2RepositoryTests(unittest.TestCase):
    def test_real_repository_dry_run_lists_the_full_suite(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "skills"
            result = subprocess.run([NODE, str(INSTALLER), "--target", str(target), "--dry-run"],
                                    capture_output=True, text=True, timeout=60, check=False)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            skills = [p for p in (REPO_ROOT / ".claude/skills").iterdir()
                      if (p / "SKILL.md").is_file() or p.name == "_shared"]
            self.assertIn(f"install {len(skills)} entries", result.stdout)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
