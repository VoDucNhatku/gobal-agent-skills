import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.build_antigravity import BuildError, TEXT_SUFFIXES, build
from scripts.skill_manifest import load_frontmatter


REPO_ROOT = Path(__file__).resolve().parents[1]


class BuildAntigravityTests(unittest.TestCase):
    def fixture(self, root):
        config = root / "config"
        config.mkdir()
        (config / "antigravity-skills.txt").write_text("admin\ndemo\n", encoding="utf-8")
        shutil.copyfile(REPO_ROOT / "config/antigravity-compatibility.yml", config / "antigravity-compatibility.yml")
        for name in ("admin", "demo"):
            self.source(root, f"skills/{name}/SKILL.md", (
                f'---\nname: "{name}"\ndescription: "Use when testing."\n'
                'argument-hint: "<topic>"\nallowed-tools: "Read Task Skill"\n---\n'
                f"\n# {name}\n\nA hard break  \n\nNo final newline  "
            ))
        for name in yaml.safe_load((config / "antigravity-compatibility.yml").read_text())["rules"]:
            self.source(root, f"rules/{name}", f"# {name}\n\nKeep the evidence policy.\n")

    def source(self, root, path, value):
        target = root / ".claude" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value.encode("utf-8") if isinstance(value, str) else value)
        return target

    def test_emits_portable_manifest_and_preserves_markdown_body(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            _, source_body = load_frontmatter(root / ".claude/skills/demo/SKILL.md", canonical=True)

            self.assertEqual(build(root), 0)

            data, body = load_frontmatter(root / "skills/demo/SKILL.md", host="antigravity")
            self.assertEqual(set(data), {"name", "description"})
            self.assertTrue(body.startswith(source_body))
            self.assertIn("## Antigravity resource execution", body)
            self.assertIn("absolute quoted path", body)
            self.assertIn("Do not change the working directory", body)
            self.assertIn("`.tmp/` and `notes/` remain relative to the current project", body)

    def test_portable_resource_command_runs_absolute_entrypoint_from_project_cwd(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "bundle"
            root.mkdir()
            self.fixture(root)
            self.source(root, "skills/admin/scripts/resolve.py", (
                "from pathlib import Path\nimport sys\n"
                "Path('notes').mkdir(exist_ok=True)\n"
                "Path('notes/result.txt').write_text(Path(sys.argv[1]).read_text(encoding='utf-8'), encoding='utf-8')\n"
            ))
            source = root / ".claude/skills/admin/SKILL.md"
            source.write_bytes(source.read_bytes() + b'\nRun python "scripts/resolve.py" ".tmp/input.txt".\n')
            build(root)
            _, body = load_frontmatter(root / "skills/admin/SKILL.md", host="antigravity")
            self.assertIn("containing loaded file's observed location", body)
            self.assertIn("Do not invent the installed location", body)
            project = Path(temp_dir) / "project có spaces"
            (project / ".tmp").mkdir(parents=True)
            (project / ".tmp/input.txt").write_text("observed fixture input", encoding="utf-8")
            entrypoint = (root / "skills/admin/scripts/resolve.py").resolve()

            result = subprocess.run([sys.executable, "-B", str(entrypoint), ".tmp/input.txt"],
                                    cwd=project, capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((project / "notes/result.txt").read_text(), "observed fixture input")
            self.assertFalse((root / "skills/admin/notes").exists())

    def test_copies_recursive_resources_with_lf_and_preserves_code_and_binary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            self.source(root, "skills/demo/references/nested/guide.md", "# Guide\r\n\r\nHard break  \r\n")
            self.source(root, "skills/demo/scripts/example.py", "class Task:\r\n    Read = 1\r\n")
            binary = b"\x00\xff\r\n\x89PNG"
            self.source(root, "skills/demo/assets/example.bin", binary)
            self.source(root, "skills/demo/scripts/__pycache__/ignored.pyc", binary)
            self.source(root, "skills/references/fixture/SKILL.md", "not a registration")
            self.source(root, "skills/test-reports/SKILL.md.txt", "not a registration")

            build(root)

            self.assertEqual((root / "skills/demo/references/nested/guide.md").read_bytes(), b"# Guide\n\nHard break  \n")
            self.assertEqual((root / "skills/demo/scripts/example.py").read_bytes(), b"class Task:\n    Read = 1\n")
            self.assertEqual((root / "skills/demo/assets/example.bin").read_bytes(), binary)
            self.assertEqual(sorted(path.name for path in (root / "skills").iterdir()), ["admin", "demo"])
            self.assertFalse(any((root / "skills").rglob("*.pyc")))

    def test_actual_known_dotfiles_are_normalized_to_lf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            for name in (".gitignore", ".gitattributes"):
                self.source(root, f"skills/demo/resources/{name}", b"# dotfile\r\nfixture\r\n")

            build(root)

            for name in (".gitignore", ".gitattributes"):
                self.assertEqual((root / f"skills/demo/resources/{name}").read_bytes(), b"# dotfile\nfixture\n", name)

    def test_maps_rule_peer_and_runtime_paths_relative_to_each_output_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            self.source(root, "skills/admin/scripts/helper.py", "print('hello')\n")
            skill = root / ".claude/skills/demo/SKILL.md"
            skill.write_bytes(skill.read_bytes() + (
                "\n`~/.claude/rules/workbench-conventions.md`\n"
                "`~/.claude/rules`\n"
                "`~/.claude/skills/admin/scripts/helper.py`\n"
                'python "<skills>/admin/scripts/helper.py"\n'
            ).encode("utf-8"))
            self.source(root, "skills/demo/references/guide.md", "`~/.claude/rules/workbench-conventions.md`\n")
            self.source(root, "rules/research-proposal-integrity.md", "`~/.claude/rules/workbench-conventions.md`\n")

            build(root)

            output = (root / "skills/demo/SKILL.md").read_text()
            self.assertIn("`../../rules/workbench-conventions.md`", output)
            self.assertIn("`../../rules`", output)
            self.assertIn("`../admin/scripts/helper.py`", output)
            self.assertIn('python "../admin/scripts/helper.py"', output)
            self.assertIn("`../../../rules/workbench-conventions.md`", (root / "skills/demo/references/guide.md").read_text())
            self.assertIn("`workbench-conventions.md`", (root / "rules/research-proposal-integrity.md").read_text())
            for name in yaml.safe_load((root / "config/antigravity-compatibility.yml").read_text())["rules"]:
                header = (root / "rules" / name).read_text().split("\n---\n", 1)[0][4:]
                metadata = yaml.safe_load(header)
                self.assertEqual(metadata["trigger"], "always_on" if name == "evidence-first.md" else "model_decision")
                self.assertTrue(metadata["description"])

    def test_maps_explicit_tools_to_capabilities_without_renaming_code(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            tools = ("Read", "Task", "Skill", "WebSearch", "WebFetch", "AskUserQuestion", "TodoWrite")
            skill = root / ".claude/skills/demo/SKILL.md"
            skill.write_bytes(skill.read_bytes() + ("\n" + " ".join(f"`{tool}`" for tool in tools) +
                "\nTask calls may run independently.\n```python\nclass Task:\n    Read = 1\n```\n").encode("utf-8"))

            build(root)

            output = (root / "skills/demo/SKILL.md").read_text()
            compatibility = yaml.safe_load((root / "config/antigravity-compatibility.yml").read_text())
            for tool in tools:
                self.assertIn(f'`{compatibility["tools"][tool]}`', output)
            self.assertIn("use sequential execution if unavailable", output)
            self.assertIn("```python\nclass Task:\n    Read = 1\n```", output)

    def test_maps_bare_known_tool_phrases_but_preserves_plain_names_and_code(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            source = root / ".claude/skills/demo/SKILL.md"
            source.write_bytes(source.read_bytes() + (
                "\nUse the Read tool, Write tool, Edit tool, and Grep calls.\n"
                "Read the data; Write is an entity name.\n"
                "```python\nRead tool = 1\nWrite tool = 2\n```\n"
            ).encode("utf-8"))

            build(root)

            output = (root / "skills/demo/SKILL.md").read_text()
            self.assertIn("file reading capability tool", output)
            self.assertIn("file writing capability tool", output)
            self.assertIn("targeted file editing capability tool", output)
            self.assertIn("text search capability calls", output)
            self.assertIn("Read the data; Write is an entity name.", output)
            self.assertIn("```python\nRead tool = 1\nWrite tool = 2\n```", output)

    def test_rejects_unsupported_tools_paths_and_phantom_resources_before_writing(self):
        cases = {
            "unknown allowed tool": ("", 'allowed-tools: "MysteryTool"'),
            "unsupported body tool": ("Use `NotebookEdit`.", None),
            "unknown explicit body tool": ("Use `MysteryTool` tool.", None),
            "unknown home path": ("`~/.claude/settings.json`", None),
            "wildcard rule": ("`~/.claude/rules/*.md`", None),
            "missing peer": ('python "<skills>/admin/scripts/missing.py"', None),
            "missing local": ("Read `references/missing.md`.", None),
        }
        for label, (body, replacement) in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.fixture(root)
                path = root / ".claude/skills/demo/SKILL.md"
                source = path.read_text()
                if replacement:
                    source = source.replace('allowed-tools: "Read Task Skill"', replacement)
                path.write_bytes((source + "\n" + body).encode("utf-8"))

                with self.assertRaises(BuildError):
                    build(root)
                self.assertFalse((root / "skills").exists())

    def test_metadata_canonical_home_path_is_rejected_before_output_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            source = root / ".claude/skills/demo/SKILL.md"
            source.write_bytes(source.read_bytes().replace(
                b'description: "Use when testing."',
                b'description: "Use ~/.claude/rules/workbench-conventions.md when testing."',
            ))

            with self.assertRaisesRegex(BuildError, "metadata.*canonical home"):
                build(root)

            self.assertFalse((root / "skills").exists())

    def test_requires_exact_skill_and_rule_inventory_not_only_a_count(self):
        for label in ("extra skill", "same count wrong name", "duplicate inventory", "extra rule"):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.fixture(root)
                if label == "extra skill":
                    self.source(root, "skills/rogue/SKILL.md", (root / ".claude/skills/demo/SKILL.md").read_bytes())
                elif label == "same count wrong name":
                    (root / ".claude/skills/demo").rename(root / ".claude/skills/impostor")
                elif label == "duplicate inventory":
                    (root / "config/antigravity-skills.txt").write_text("admin\nadmin\n", encoding="utf-8")
                else:
                    self.source(root, "rules/unknown.md", "# Unknown\n")

                with self.assertRaises(BuildError):
                    build(root)
                self.assertFalse((root / "skills").exists())

    def test_check_reports_byte_drift_without_mutating_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            build(root)
            target = root / "skills/demo/SKILL.md"
            target.write_bytes(b"modified generated file\r\n")

            self.assertEqual(build(root, check=True), 1)

            self.assertEqual(target.read_bytes(), b"modified generated file\r\n")

    def test_refuses_unowned_collision_before_creating_any_other_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            target = root / "skills/demo/SKILL.md"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"user-owned skill\n")

            with self.assertRaisesRegex(BuildError, "unowned or modified"):
                build(root)

            self.assertEqual(target.read_bytes(), b"user-owned skill\n")
            self.assertFalse((root / "skills/admin").exists())
            self.assertFalse((root / "distribution-manifest.json").exists())

    def test_required_output_directory_file_collision_blocks_every_write(self):
        for directory in ("skills", "rules", "pilot"):
            with self.subTest(directory=directory), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.fixture(root)
                collision = root / directory
                collision.write_bytes(b"user file, not a directory\n")

                with self.assertRaises((BuildError, OSError)):
                    build(root)

                self.assertEqual(collision.read_bytes(), b"user file, not a directory\n")
                self.assertFalse((root / "plugin.json").exists())
                self.assertFalse((root / "distribution-manifest.json").exists())
                for other in {"skills", "rules", "pilot"} - {directory}:
                    self.assertFalse((root / other).exists())

    def test_owned_expected_output_drift_is_preserved_and_blocks_all_writes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            build(root)
            target = root / "skills/demo/SKILL.md"
            target.write_bytes(b"user revision\n")
            self.source(root, "skills/admin/resources/new.txt", "new source\n")
            manifest = (root / "distribution-manifest.json").read_bytes()

            with self.assertRaisesRegex(BuildError, "unowned or modified"):
                build(root)

            self.assertEqual(target.read_bytes(), b"user revision\n")
            self.assertEqual((root / "distribution-manifest.json").read_bytes(), manifest)
            self.assertFalse((root / "skills/admin/resources/new.txt").exists())

    def test_equal_unowned_output_can_be_adopted_then_owned_source_updates_work(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            from scripts.build_antigravity import PLUGIN
            (root / "plugin.json").write_bytes((json.dumps(PLUGIN, indent=2) + "\n").encode())
            build(root)
            source = root / ".claude/skills/demo/SKILL.md"
            source.write_bytes(source.read_bytes() + b"\nNew canonical content.\n")

            self.assertEqual(build(root), 0)
            self.assertIn(b"New canonical content.", (root / "skills/demo/SKILL.md").read_bytes())
            self.assertEqual(build(root, check=True), 0)

    def test_source_file_symlink_is_rejected_before_outputs_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            root.mkdir()
            self.fixture(root)
            outside = Path(temp_dir) / "private.txt"
            outside.write_bytes(b"outside data\n")
            link = root / ".claude/skills/demo/private.txt"
            try:
                link.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"file symlinks unavailable: {exc}")

            with self.assertRaisesRegex(BuildError, "reparse|symlink"):
                build(root)

            self.assertFalse((root / "skills").exists())
            self.assertEqual(outside.read_bytes(), b"outside data\n")

    def directory_link(self, link, target, *, junction=False):
        if junction:
            if os.name != "nt":
                self.skipTest("Windows junction test")
            quote = lambda value: "'" + str(value).replace("'", "''") + "'"
            result = subprocess.run([
                "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                f"New-Item -ItemType Junction -Path {quote(link)} -Target {quote(target)} | Out-Null",
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlinks unavailable: {exc}")

    def test_source_directory_links_and_junctions_are_rejected(self):
        for junction in (False, True):
            with self.subTest(junction=junction), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir) / "repo"
                root.mkdir()
                self.fixture(root)
                outside = Path(temp_dir) / "outside"
                outside.mkdir()
                (outside / "secret.bin").write_bytes(b"not distributable")
                link = root / ".claude/skills/demo/resources"
                self.directory_link(link, outside, junction=junction)

                with self.assertRaisesRegex(BuildError, "reparse|symlink"):
                    build(root)

                self.assertFalse((root / "skills").exists())
                self.assertEqual((outside / "secret.bin").read_bytes(), b"not distributable")

    def test_missing_outputs_beneath_destination_links_are_rejected_without_external_writes(self):
        for junction in (False, True):
            with self.subTest(junction=junction), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir) / "repo"
                root.mkdir()
                self.fixture(root)
                outside = Path(temp_dir) / "outside"
                outside.mkdir()
                self.directory_link(root / "skills", outside, junction=junction)

                with self.assertRaisesRegex(BuildError, "reparse|symlink"):
                    build(root)
                with self.assertRaisesRegex(BuildError, "reparse|symlink"):
                    build(root, check=True)

                self.assertEqual(list(outside.iterdir()), [])
                self.assertFalse((root / "rules").exists())
                self.assertFalse((root / "distribution-manifest.json").exists())

    def test_repository_ancestor_junction_is_rejected_before_mutation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            outside = Path(temp_dir) / "outside"
            outside.mkdir()
            real_root = outside / "repo"
            real_root.mkdir()
            self.fixture(real_root)
            link = Path(temp_dir) / "ancestor"
            self.directory_link(link, outside, junction=True)

            with self.assertRaisesRegex(BuildError, "reparse|symlink"):
                build(link / "repo")

            self.assertFalse((real_root / "skills").exists())

    def test_equal_destination_file_symlink_is_not_adopted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            root.mkdir()
            self.fixture(root)
            from scripts.build_antigravity import PLUGIN
            outside = Path(temp_dir) / "plugin.json"
            outside.write_bytes((json.dumps(PLUGIN, indent=2) + "\n").encode())
            try:
                (root / "plugin.json").symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"file symlinks unavailable: {exc}")

            with self.assertRaisesRegex(BuildError, "reparse|symlink"):
                build(root)

            self.assertFalse((root / "skills").exists())

    def test_file_manifest_is_byte_deterministic_and_excludes_itself(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            (root / "user-notes.txt").write_bytes(b"unowned root file\r\n")
            build(root)
            manifest = json.loads((root / "distribution-manifest.json").read_text())
            self.assertEqual(manifest["schema_version"], 1)
            self.assertNotIn("distribution-manifest.json", manifest["files"])
            self.assertEqual(set(manifest["files"]), {"plugin.json"} | {
                path.relative_to(root).as_posix()
                for directory in ("skills", "rules")
                for path in (root / directory).rglob("*") if path.is_file()
            })
            first = {path: (root / path).read_bytes() for path in manifest["files"]}
            first["distribution-manifest.json"] = (root / "distribution-manifest.json").read_bytes()
            for path, digest in manifest["files"].items():
                self.assertEqual(hashlib.sha256(first[path]).hexdigest(), digest)

            build(root)

            self.assertEqual(first, {path: (root / path).read_bytes() for path in first})
            self.assertEqual((root / "user-notes.txt").read_bytes(), b"unowned root file\r\n")
            self.assertEqual(build(root, check=True), 0)

    def test_orphans_require_ownership_and_modified_stale_files_are_preserved(self):
        for label in ("unowned added", "owned removed", "owned renamed", "modified removed"):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.fixture(root)
                source = self.source(root, "skills/demo/references/old.md", "original\n")
                build(root)
                orphan = root / "skills/demo/references/old.md"
                if label == "unowned added":
                    orphan = root / "skills/demo/references/user.md"
                    orphan.write_bytes(b"user data")
                else:
                    source.unlink()
                    if label == "owned renamed":
                        self.source(root, "skills/demo/references/new.md", "original\n")
                    if label == "modified removed":
                        orphan.write_bytes(b"user data")

                self.assertEqual(build(root, check=True), 1)
                if label in ("unowned added", "modified removed"):
                    with self.assertRaises(BuildError):
                        build(root)
                    self.assertEqual(orphan.read_bytes(), b"user data")
                else:
                    self.assertEqual(build(root), 0)
                    self.assertFalse(orphan.exists())
                    self.assertEqual(build(root, check=True), 0)

    def test_pilot_clones_admin_resources_with_local_rules_and_distinct_canaries(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            admin = root / ".claude/skills/admin/SKILL.md"
            admin.write_bytes(admin.read_bytes() + b"\n`~/.claude/rules/workbench-conventions.md`\n`references/deep/dispatch.md`\n")
            self.source(root, "skills/admin/references/deep/dispatch.md", "`~/.claude/rules/research-proposal-integrity.md`\n")
            self.source(root, "skills/admin/resources/ledger.yml", "source: observed\r\n")

            build(root)

            pilot = root / "pilot"
            data, body = load_frontmatter(pilot / "skills/admin-evidence-pilot/SKILL.md", host="antigravity")
            self.assertEqual(data["name"], "admin-evidence-pilot")
            self.assertIn("Protocol: AG-EF-PILOT-1", body)
            self.assertNotIn("AG-EF-RULE-1", body)
            self.assertIn("`references/shared-rules/workbench-conventions.md`", body)
            self.assertIn("`../shared-rules/research-proposal-integrity.md`", (pilot / "skills/admin-evidence-pilot/references/deep/dispatch.md").read_text())
            self.assertEqual((pilot / "skills/admin-evidence-pilot/resources/ledger.yml").read_bytes(), b"source: observed\n")
            rule = (pilot / "rules/admin-evidence-pilot.md").read_text()
            self.assertIn('trigger: "always_on"', rule)
            self.assertIn("Rule Canary: AG-EF-RULE-1", rule)
            self.assertNotIn("AG-EF-PILOT-1", rule)
            self.assertEqual([path.name for path in (pilot / "rules").iterdir()], ["admin-evidence-pilot.md"])
            manifest = json.loads((pilot / "manifest.json").read_text())
            self.assertEqual(manifest["schema_version"], 1)
            self.assertEqual(set(manifest["files"]), {path.relative_to(pilot).as_posix() for path in pilot.rglob("*") if path.is_file() and path.name != "manifest.json"})
            for path, digest in manifest["files"].items():
                self.assertEqual(hashlib.sha256((pilot / path).read_bytes()).hexdigest(), digest)

    def test_cli_resolves_repository_inputs_from_an_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            command = [sys.executable, "-B", str(REPO_ROOT / "scripts/build_antigravity.py"), "--repo-root", str(root)]

            result = subprocess.run(command, cwd=temp_dir, capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            check = subprocess.run(command + ["--check"], cwd=temp_dir, capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_pilot_bundles_only_transitive_rule_dependencies_even_with_a_cycle(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            admin = root / ".claude/skills/admin/SKILL.md"
            admin.write_bytes(admin.read_bytes() + b"\n`~/.claude/rules/workbench-conventions.md`\n")
            self.source(root, "rules/workbench-conventions.md", "`~/.claude/rules/research-proposal-integrity.md`\n")
            self.source(root, "rules/research-proposal-integrity.md", "`~/.claude/rules/workbench-conventions.md`\n")

            build(root)

            directory = root / "pilot/skills/admin-evidence-pilot/references/shared-rules"
            self.assertEqual(sorted(path.name for path in directory.iterdir()), ["research-proposal-integrity.md", "workbench-conventions.md"])

    def test_real_inventory_and_bundled_validator_work_outside_repository(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shutil.copytree(REPO_ROOT / ".claude", root / ".claude", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copytree(REPO_ROOT / "config", root / "config")
            names = (root / "config/antigravity-skills.txt").read_text().splitlines()
            self.assertEqual(len(names), 69)

            build(root)

            self.assertEqual(sorted(path.name for path in (root / "skills").iterdir()), names)
            for name in names:
                load_frontmatter(root / "skills" / name / "SKILL.md", host="antigravity")
            command = [sys.executable, "-B", str(root / "skills/test-framework/scripts/test_skills.py"),
                       "--skills-root", str(root / "skills"), "--host", "antigravity", "--json"]
            result = subprocess.run(command, cwd=temp_dir, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["summary"]["discovered"], 69)
            self.assertEqual(report["summary"]["validated"], 69)
            self.assertEqual(report["summary"]["fail"], 0)
            self.assertEqual(build(root, check=True), 0)

    def test_pilot_rule_dag_includes_rule_canary_dependencies_not_unrelated_rules(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.fixture(root)
            self.source(root, "skills/admin/references/guide.md", "`~/.claude/rules/research-proposal-integrity.md`\n")
            self.source(root, "rules/research-proposal-integrity.md", "`~/.claude/rules/workbench-conventions.md`\n")
            self.source(root, "rules/evidence-first.md", "`~/.claude/rules/latex-katex-compat.md`\n")
            self.source(root, "rules/latex-katex-compat.md", "latex-fix bundles `scripts/latex_lint.py`; `~/.claude/rules/workbench-conventions.md`\n")

            build(root)

            directory = root / "pilot/skills/admin-evidence-pilot/references/shared-rules"
            self.assertEqual(sorted(path.name for path in directory.iterdir()), [
                "latex-katex-compat.md", "research-proposal-integrity.md", "workbench-conventions.md",
            ])
            self.assertIn("`scripts/latex_lint.py`", (directory / "latex-katex-compat.md").read_text())

    def test_normal_portable_validator_runtime_cache_does_not_become_an_orphan(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            shutil.copytree(REPO_ROOT / ".claude", root / ".claude", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copytree(REPO_ROOT / "config", root / "config")
            build(root)
            command = [sys.executable, str(root / "skills/test-framework/scripts/test_skills.py"),
                       "--skills-root", str(root / "skills"), "--host", "antigravity", "--json"]

            result = subprocess.run(command, cwd=temp_dir, capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            cache = root / "skills/test-framework/scripts/__pycache__"
            cache_bytes = {path.name: path.read_bytes() for path in cache.glob("*.pyc")}
            self.assertTrue(cache_bytes, "normal Python invocation must exercise bytecode caching")
            self.assertEqual(build(root, check=True), 0)
            self.assertEqual(build(root), 0)
            self.assertEqual(cache_bytes, {path.name: path.read_bytes() for path in cache.glob("*.pyc")})

    def test_ignored_runtime_cache_still_rejects_reparse_entries_before_writing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            root.mkdir()
            self.fixture(root)
            build(root)
            outside = Path(temp_dir) / "outside"
            outside.mkdir()
            (outside / "cached.pyc").write_bytes(b"external cache")
            self.directory_link(root / "skills/demo/__pycache__", outside, junction=True)
            before = (root / "distribution-manifest.json").read_bytes()
            self.source(root, "skills/demo/references/new.md", "new source\n")

            with self.assertRaisesRegex(BuildError, "reparse|symlink"):
                build(root, check=True)
            with self.assertRaisesRegex(BuildError, "reparse|symlink"):
                build(root)

            self.assertEqual((outside / "cached.pyc").read_bytes(), b"external cache")
            self.assertEqual((root / "distribution-manifest.json").read_bytes(), before)
            self.assertFalse((root / "skills/demo/references/new.md").exists())

    def test_windows_autocrlf_clone_preserves_every_generated_text_suffix_and_binary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "source"
            root.mkdir()
            self.fixture(root)
            shutil.copyfile(REPO_ROOT / ".gitattributes", root / ".gitattributes")
            for suffix in sorted(TEXT_SUFFIXES):
                self.source(root, f"skills/demo/resources/sample{suffix}", "plain fixture text\nsecond line\n")
            binary = b"\x00\xff\r\n\x89PNG"
            self.source(root, "skills/demo/assets/sample.bin", binary)
            opaque = b"opaque noNUL\r\nmixedLF\n"
            self.source(root, "skills/demo/assets/opaque.bin", opaque)
            for name in (".gitignore", ".gitattributes"):
                self.source(root, f"skills/demo/resources/{name}", b"# dotfile\r\nfixture\r\n")
            build(root)

            def git(*args, cwd=root):
                result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return result

            git("init", "--quiet")
            git("config", "core.autocrlf", "true")
            git("add", "--all")
            git("-c", "user.name=Build Fixture", "-c", "user.email=build-fixture@example.invalid",
                "commit", "--quiet", "-m", "Generated line-ending fixture")
            clone = Path(temp_dir) / "clone"
            git("-c", "core.autocrlf=true", "clone", "--quiet", str(root), str(clone), cwd=temp_dir)

            self.assertEqual((clone / "skills/demo/assets/opaque.bin").read_bytes(), opaque)
            self.assertEqual(build(clone, check=True), 0)
            self.assertEqual((clone / "skills/demo/assets/sample.bin").read_bytes(), binary)
            for suffix in sorted(TEXT_SUFFIXES):
                self.assertEqual((clone / f"skills/demo/resources/sample{suffix}").read_bytes(),
                                 b"plain fixture text\nsecond line\n", suffix)
            for name in (".gitignore", ".gitattributes"):
                self.assertEqual((clone / f"skills/demo/resources/{name}").read_bytes(),
                                 b"# dotfile\nfixture\n", name)


if __name__ == "__main__":
    unittest.main()
