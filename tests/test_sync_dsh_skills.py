"""Temporary-profile tests for scripts/sync-dsh-skills.ps1 (Windows PowerShell 5.1 only)."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "sync-dsh-skills.ps1"
POWERSHELL = shutil.which("powershell.exe")
VIETNAMESE = "Đọc một bài báo"


@unittest.skipUnless(POWERSHELL, "Windows PowerShell 5.1 is unavailable")
class SyncDshSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="gobal dsh sync ")
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.source = self.root / "claude skills"
        self.lab = self.root / "dsh lab"
        self.write(self.source / "paper-read/SKILL.md", f"---\nname: paper-read\ndescription: {VIETNAMESE}\n---\nBody\n")
        self.write(self.source / "paper-read/references/guide.md", "See ../../_shared/evidence.md\n")
        self.write(self.source / "study-forge/SKILL.md",
                   "---\nname: study-forge\ndisable-model-invocation: true\n---\nHidden pack\n")
        self.write(self.source / "_shared/evidence.md", "shared evidence\n")
        self.write(self.lab / "dsh-skills/read-docx-full/SKILL.md", "---\nname: read-docx-full\n---\nDocx\n")

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_sync(self):
        return subprocess.run([
            POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
            "-File", str(SCRIPT), "-Source", str(self.source), "-Lab", str(self.lab),
        ], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60, check=False)

    def skill(self, mirror, name):
        return (self.lab / "home" / mirror / name / "SKILL.md").read_text(encoding="utf-8")

    def test_builds_hidden_and_visible_mirrors_with_shared_folder(self):
        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        standard = self.skill("skills", "paper-read")
        self.assertTrue(standard.startswith("---\ndisable-model-invocation: true\n"), standard)
        self.assertIn(VIETNAMESE, standard)
        self.assertNotIn("disable-model-invocation", self.skill("skills", "read-docx-full"))
        self.assertNotIn("disable-model-invocation", self.skill("skills-admin", "paper-read"))
        self.assertEqual(self.skill("skills", "study-forge").count("disable-model-invocation"), 1)
        for mirror in ("skills", "skills-admin"):
            with self.subTest(mirror=mirror):
                base = self.lab / "home" / mirror
                self.assertEqual((base / "_shared/evidence.md").read_text(encoding="utf-8"), "shared evidence\n")
                guide = base / "paper-read/references/guide.md"
                self.assertEqual((guide.parent / "../../_shared/evidence.md").resolve().read_text(encoding="utf-8"),
                                 "shared evidence\n")

    def test_rerun_rebuilds_mirror_without_touching_the_source(self):
        self.assertEqual(self.run_sync().returncode, 0)
        before = {p.relative_to(self.source).as_posix(): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}

        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = {p.relative_to(self.source).as_posix(): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
        self.assertEqual(after, before)
        self.assertTrue((self.lab / "home/skills/_shared/evidence.md").is_file())

    def test_refuses_a_source_without_v2_shared_folder(self):
        shutil.rmtree(self.source / "_shared")

        result = self.run_sync()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("install_v2.mjs", result.stdout + result.stderr)
        self.assertFalse((self.lab / "home").exists())


if __name__ == "__main__":
    unittest.main()
