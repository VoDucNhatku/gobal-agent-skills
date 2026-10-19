import base64
import hashlib
import json
import os
import queue
import shutil
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install-antigravity.ps1"
POWERSHELL = shutil.which("powershell.exe")


@unittest.skipUnless(POWERSHELL, "Windows PowerShell 5.1 is unavailable")
class PilotInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="gobal pilot ")
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.source = self.root / "source package"
        self.profile = self.root / "profile tiếng Việt"
        self.profile.mkdir()
        self.payload = {
            "skills/admin-evidence-pilot/SKILL.md": b"---\nname: admin-evidence-pilot\ndescription: Test pilot.\n---\n",
            "skills/admin-evidence-pilot/references/guide.md": b"Pilot reference.\n",
            "rules/admin-evidence-pilot.md": b"---\ntrigger: always_on\n---\nTemporary pilot rule.\n",
        }
        self.write_source()

    def write_source(self):
        pilot = self.source / "pilot"
        pilot.mkdir(parents=True, exist_ok=True)
        for relative, data in self.payload.items():
            path = pilot / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (pilot / "manifest.json").write_text(json.dumps({
            "schema_version": 1,
            "files": {name: hashlib.sha256(data).hexdigest() for name, data in self.payload.items()},
        }), encoding="utf-8")

    def run_installer(self, *arguments, pilot=True, fault=None):
        environment = os.environ.copy()
        for name in tuple(environment):
            if name.startswith("GOBAL_INSTALL_TEST_"):
                environment.pop(name)
        if fault:
            environment.update(fault)
        return subprocess.run([
            POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
            "-File", str(INSTALLER), "-SourcePath", str(self.source), "-ProfileRoot", str(self.profile),
            *( ["-Pilot"] if pilot else [] ), *arguments,
        ], capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment,
           timeout=40, check=False)

    def start_paused_installer(self, anchor, *arguments):
        # Instrument only a disposable copy, never the installer used on the real
        # profile. The barrier exposes a deterministic external-edit/kill window.
        installer_copy = self.root / "paused installer.ps1"
        script = INSTALLER.read_text(encoding="utf-8")
        self.assertEqual(script.count(anchor), 1, "Pause anchor must be unique")
        script = script.replace(anchor, anchor + "\n        [Console]::WriteLine('TEST BARRIER'); "
                                "$null = [Console]::ReadLine()", 1)
        installer_copy.write_text(script, encoding="utf-8")
        environment = {name: value for name, value in os.environ.items()
                       if not name.startswith("GOBAL_INSTALL_TEST_")}
        process = subprocess.Popen([
            POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
            "-File", str(installer_copy), "-SourcePath", str(self.source),
            "-ProfileRoot", str(self.profile), "-Pilot", *arguments,
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", env=environment)
        self.addCleanup(self.stop_process, process)
        lines = queue.Queue()

        def read_lines():
            for line in iter(process.stdout.readline, ""):
                lines.put(line)
                if line.strip() == "TEST BARRIER":
                    return
            lines.put("")

        threading.Thread(target=read_lines, daemon=True).start()
        output = []
        deadline = time.monotonic() + 15
        while True:
            try:
                line = lines.get(timeout=max(0.01, deadline - time.monotonic()))
            except queue.Empty:
                process.terminate()
                self.fail("Installer did not reach test barrier within 15 seconds")
            output.append(line)
            if line.strip() == "TEST BARRIER":
                return process, "".join(output)
            if not line:
                self.fail("Installer exited before test barrier: " + "".join(output)
                          + process.stderr.read())

    @staticmethod
    def stop_process(process):
        if process.poll() is None:
            process.terminate()
        process.communicate(timeout=10)

    def snapshot(self):
        return {path.relative_to(self.profile).as_posix(): path.read_bytes()
                for path in self.profile.rglob("*") if path.is_file()}

    def target(self, relative):
        return self.profile / ".gemini" / "config" / relative

    @property
    def state_dir(self):
        return self.target(".gobal-agent-skills")

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_full_rollout_is_not_released_and_writes_nothing(self):
        result = self.run_installer(pilot=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not released", (result.stdout + result.stderr).lower())
        self.assertEqual(self.snapshot(), {})

    def test_dry_run_validates_payload_and_writes_nothing(self):
        result = self.run_installer("-DryRun")

        self.assert_success(result)
        self.assertIn("DRY RUN", result.stdout)
        self.assertIn("other chats", result.stdout)
        self.assertEqual(self.snapshot(), {})

    def test_documented_default_source_dry_run_works_from_repository_and_unrelated_cwd(self):
        environment = {name: value for name, value in os.environ.items()
                       if not name.startswith("GOBAL_INSTALL_TEST_")}
        invocations = (
            (Path("scripts") / "install-antigravity.ps1", REPO_ROOT),
            (INSTALLER, REPO_ROOT),
            (INSTALLER, self.root),
        )
        for script, working_directory in invocations:
            with self.subTest(script=script, cwd=working_directory):
                result = subprocess.run([
                    POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                    "-File", str(script), "-Pilot", "-DryRun", "-ProfileRoot", str(self.profile),
                ], cwd=working_directory, capture_output=True, text=True, encoding="utf-8",
                    errors="replace", env=environment, timeout=40, check=False)

                self.assert_success(result)
                self.assertIn("DRY RUN", result.stdout)
                self.assertEqual(self.snapshot(), {})

    def test_install_and_uninstall_preserve_unrelated_profile_files(self):
        unrelated = {
            "skills/cv-maker/SKILL.md": b"User CV skill.\r\n",
            "rules/user.md": b"User rule.\n",
            "settings.json": b'{"mcpServers":{"user":{}}}\n',
        }
        for relative, data in unrelated.items():
            path = self.target(relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

        installed = self.run_installer()

        self.assert_success(installed)
        for relative, data in self.payload.items():
            self.assertEqual(self.target(relative).read_bytes(), data)
        ownership = json.loads((self.state_dir / "pilot-ownership.json").read_text(encoding="utf-8"))
        self.assertEqual(set(ownership["files"]), set(self.payload))
        self.assertEqual(list(self.target("rules").glob("admin-evidence-pilot*.md")),
                         [self.target("rules/admin-evidence-pilot.md")])
        self.assert_success(self.run_installer("-Uninstall"))
        for relative in self.payload:
            self.assertFalse(self.target(relative).exists())
        for relative, data in unrelated.items():
            self.assertEqual(self.target(relative).read_bytes(), data)

    def test_unmanaged_collision_refuses_without_force_and_force_backs_up(self):
        relative = "rules/admin-evidence-pilot.md"
        path = self.target(relative)
        path.parent.mkdir(parents=True)
        path.write_bytes(b"User's existing namespaced rule.\n")

        refused = self.run_installer()

        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("unmanaged collision", (refused.stdout + refused.stderr).lower())
        self.assertEqual(path.read_bytes(), b"User's existing namespaced rule.\n")
        self.assert_success(self.run_installer("-Force"))
        backups = list((self.state_dir / "transactions").glob("*/backups/rules/admin-evidence-pilot.md"))
        self.assertTrue(any(backup.read_bytes() == b"User's existing namespaced rule.\n" for backup in backups))

    def test_equal_unmanaged_files_still_require_force_and_acquire_ownership(self):
        for relative, data in self.payload.items():
            path = self.target(relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

        refused = self.run_installer()

        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("unmanaged collision", (refused.stdout + refused.stderr).lower())
        self.assertFalse((self.state_dir / "pilot-ownership.json").exists())
        acquired = self.run_installer("-Force")
        self.assert_success(acquired)
        self.assertNotIn("no-op", acquired.stdout.lower())
        ownership = json.loads((self.state_dir / "pilot-ownership.json").read_text(encoding="utf-8"))
        self.assertEqual(set(ownership["files"]), set(self.payload))
        self.assertEqual(len(list((self.state_dir / "transactions").iterdir())), 1)

    def test_drifted_owned_file_refuses_update_and_uninstall_unless_force(self):
        self.assert_success(self.run_installer())
        relative = "skills/admin-evidence-pilot/SKILL.md"
        self.target(relative).write_bytes(b"User changed pilot.\n")
        for arguments in ((), ("-Uninstall",)):
            with self.subTest(arguments=arguments):
                refused = self.run_installer(*arguments)
                self.assertNotEqual(refused.returncode, 0)
                self.assertIn("owned file drift", (refused.stdout + refused.stderr).lower())
                self.assertEqual(self.target(relative).read_bytes(), b"User changed pilot.\n")
        self.assert_success(self.run_installer("-Uninstall", "-Force"))
        backups = list((self.state_dir / "transactions").glob("*/backups/skills/admin-evidence-pilot/SKILL.md"))
        self.assertTrue(any(backup.read_bytes() == b"User changed pilot.\n" for backup in backups))
        self.assertFalse(self.target(relative).exists())

    def test_caught_midwrite_failure_restores_previous_owned_bytes(self):
        self.assert_success(self.run_installer())
        old_payload = {relative: self.target(relative).read_bytes() for relative in self.payload}
        owner_before = (self.state_dir / "pilot-ownership.json").read_bytes()
        self.payload = {relative: data + b"Updated.\n" for relative, data in self.payload.items()}
        self.write_source()

        failed = self.run_installer(fault={"GOBAL_INSTALL_TEST_FAIL_AFTER": "1"})

        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("Injected failure", failed.stdout + failed.stderr)
        for relative, data in old_payload.items():
            self.assertEqual(self.target(relative).read_bytes(), data)
        self.assertEqual((self.state_dir / "pilot-ownership.json").read_bytes(), owner_before)
        journal = json.loads((self.state_dir / "pilot-journal.json").read_text(encoding="utf-8"))
        self.assertEqual(journal["status"], "rolled_back")

    def test_apply_refuses_stage_corruption_after_durable_journal(self):
        installer, initial = self.start_paused_installer("    Write-Json $journalPath $activeJournal")
        journal_path = self.state_dir / "pilot-journal.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        relative = journal["entries"][0]["path"]
        staged = self.state_dir / "transactions" / journal["id"] / "stage" / relative
        staged.write_bytes(b"External stage corruption\n")

        stdout, stderr = installer.communicate("\n", timeout=15)

        self.assertNotEqual(installer.returncode, 0, initial + stdout + stderr)
        self.assertIn("stage", (stdout + stderr).lower())
        self.assertNotIn("Pilot installed;", stdout)
        for relative in self.payload:
            self.assertFalse(self.target(relative).exists())
        self.assertFalse((self.state_dir / "pilot-ownership.json").exists())
        self.assertEqual(json.loads(journal_path.read_text(encoding="utf-8"))["status"], "rolled_back")

    def test_commit_refuses_corrupt_staged_ownership_and_rolls_back(self):
        installer, initial = self.start_paused_installer("    Write-Json $journalPath $activeJournal")
        journal_path = self.state_dir / "pilot-journal.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        owner_after = self.state_dir / "transactions" / journal["id"] / "ownership.after.json"
        owner_after.write_text(json.dumps({"schema_version": 1, "scope": "pilot", "files": {}}),
                               encoding="utf-8")

        stdout, stderr = installer.communicate("\n", timeout=15)

        self.assertNotEqual(installer.returncode, 0, initial + stdout + stderr)
        self.assertIn("ownership", (stdout + stderr).lower())
        self.assertNotIn("Pilot installed;", stdout)
        for relative in self.payload:
            self.assertFalse(self.target(relative).exists())
        self.assertFalse((self.state_dir / "pilot-ownership.json").exists())
        self.assertEqual(json.loads(journal_path.read_text(encoding="utf-8"))["status"], "rolled_back")

    def test_commit_preserves_external_ownership_drift_and_requires_recovery(self):
        installer, initial = self.start_paused_installer("    Write-Json $journalPath $activeJournal")
        journal_path = self.state_dir / "pilot-journal.json"
        owner_path = self.state_dir / "pilot-ownership.json"
        external_owner = json.dumps({"schema_version": 1, "scope": "pilot", "files": {}}).encode("utf-8")
        owner_path.write_bytes(external_owner)

        stdout, stderr = installer.communicate("\n", timeout=15)

        self.assertNotEqual(installer.returncode, 0, initial + stdout + stderr)
        self.assertIn("ownership", (stdout + stderr).lower())
        self.assertIn("explicit recovery", (stdout + stderr).lower())
        self.assertNotIn("Pilot installed;", stdout)
        self.assertEqual(owner_path.read_bytes(), external_owner)
        self.assertEqual(json.loads(journal_path.read_text(encoding="utf-8"))["status"], "applying")
        before = self.snapshot()
        refused = self.run_installer("-Recover", "-Force")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.snapshot(), before)
        # Resolve the synthetic external drift explicitly; recovery can then
        # restore the journal's original absent ownership and managed files.
        owner_path.unlink()
        self.assert_success(self.run_installer("-Recover"))
        for relative in self.payload:
            self.assertFalse(self.target(relative).exists())

    def test_explicit_recover_restores_interrupted_install(self):
        interrupted = self.run_installer(fault={"GOBAL_INSTALL_TEST_INTERRUPT_AFTER": "1"})
        self.assertEqual(interrupted.returncode, 97, interrupted.stdout + interrupted.stderr)
        pending = self.run_installer()
        self.assertNotEqual(pending.returncode, 0)
        self.assertIn("-Recover", pending.stdout + pending.stderr)

        recovered = self.run_installer("-Recover")

        self.assert_success(recovered)
        for relative in self.payload:
            self.assertFalse(self.target(relative).exists())
        journal = json.loads((self.state_dir / "pilot-journal.json").read_text(encoding="utf-8"))
        self.assertEqual(journal["status"], "rolled_back")
        self.assert_success(self.run_installer())

    def test_source_corruption_or_incomplete_manifest_causes_no_writes(self):
        manifest_path = self.source / "pilot" / "manifest.json"
        original_manifest = manifest_path.read_bytes()
        relative = "rules/admin-evidence-pilot.md"
        original_file = (self.source / "pilot" / relative).read_bytes()
        for failure in ("corrupt_hash", "missing_file", "incomplete_manifest", "extra_file", "bad_schema", "escape"):
            with self.subTest(failure=failure):
                manifest_path.write_bytes(original_manifest)
                (self.source / "pilot" / relative).write_bytes(original_file)
                extra = self.source / "pilot" / "unexpected.md"
                if extra.exists():
                    extra.unlink()
                manifest = json.loads(original_manifest)
                if failure == "corrupt_hash":
                    (self.source / "pilot" / relative).write_bytes(b"Corrupt bytes")
                elif failure == "missing_file":
                    (self.source / "pilot" / relative).unlink()
                elif failure == "incomplete_manifest":
                    manifest["files"].pop(relative)
                elif failure == "extra_file":
                    extra.write_bytes(b"Unlisted source")
                elif failure == "bad_schema":
                    manifest["schema_version"] = True
                else:
                    manifest["files"]["skills/admin-evidence-pilot/../../cv-maker/SKILL.md"] = "0" * 64
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

                refused = self.run_installer()

                self.assertNotEqual(refused.returncode, 0, refused.stdout + refused.stderr)
                self.assertEqual(self.snapshot(), {})

    def test_recovery_refuses_user_drift_and_journal_escape(self):
        self.assertEqual(self.run_installer(fault={"GOBAL_INSTALL_TEST_INTERRUPT_AFTER": "1"}).returncode, 97)
        journal_path = self.state_dir / "pilot-journal.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        changed_target = self.target(journal["entries"][0]["path"])
        changed_target.write_bytes(b"User changed interrupted target.\n")
        before = self.snapshot()

        refused = self.run_installer("-Recover", "-Force")

        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("user drift", (refused.stdout + refused.stderr).lower())
        self.assertEqual(self.snapshot(), before)
        journal["entries"][0]["path"] = "skills/admin-evidence-pilot/../../cv-maker/SKILL.md"
        journal_path.write_text(json.dumps(journal), encoding="utf-8")
        before = self.snapshot()
        refused = self.run_installer("-Recover")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_recovery_restores_prior_ownership_after_interruption_before_commit(self):
        self.assert_success(self.run_installer())
        owner_before = (self.state_dir / "pilot-ownership.json").read_bytes()
        old_payload = self.payload.copy()
        self.payload = {relative: data + b"Update.\n" for relative, data in self.payload.items()}
        self.write_source()
        interrupted = self.run_installer(fault={"GOBAL_INSTALL_TEST_INTERRUPT_BEFORE_COMMIT": "1"})
        self.assertEqual(interrupted.returncode, 97)

        self.assert_success(self.run_installer("-Recover"))

        self.assertEqual((self.state_dir / "pilot-ownership.json").read_bytes(), owner_before)
        for relative, data in old_payload.items():
            self.assertEqual(self.target(relative).read_bytes(), data)

    def test_recovery_refuses_external_edit_after_staging_restore(self):
        self.assert_success(self.run_installer())
        self.payload = {relative: data + b"Updated.\n" for relative, data in self.payload.items()}
        self.write_source()
        self.assertEqual(self.run_installer(fault={"GOBAL_INSTALL_TEST_INTERRUPT_AFTER": "1"}).returncode, 97)
        journal_path = self.state_dir / "pilot-journal.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        changed_target = self.target(journal["entries"][0]["path"])
        recovery, initial = self.start_paused_installer(
            "            [IO.File]::Copy($backup, $restore, $true)", "-Recover")
        changed_target.write_bytes(b"Concurrent external user edit.\n")

        stdout, stderr = recovery.communicate("\n", timeout=15)

        self.assertNotEqual(recovery.returncode, 0, initial + stdout + stderr)
        self.assertIn("drift", (stdout + stderr).lower())
        self.assertEqual(changed_target.read_bytes(), b"Concurrent external user edit.\n")
        self.assertEqual(json.loads(journal_path.read_text(encoding="utf-8"))["status"], "applying")

    def test_external_process_termination_leaves_a_recoverable_journal(self):
        installer, initial = self.start_paused_installer("        Invoke-TestFault $operationCount")
        journal_path = self.state_dir / "pilot-journal.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        self.assertEqual(journal["status"], "applying")
        self.assertEqual(sum(self.target(relative).exists() for relative in self.payload), 1)

        installer.terminate()
        stdout, stderr = installer.communicate(timeout=10)

        self.assertNotEqual(installer.returncode, 0, initial + stdout + stderr)
        self.assert_success(self.run_installer("-Recover"))
        self.assertEqual(json.loads(journal_path.read_text(encoding="utf-8"))["status"], "rolled_back")
        for relative in self.payload:
            self.assertFalse(self.target(relative).exists())

    def test_recovery_refuses_restore_bytes_changed_by_an_external_writer(self):
        self.assert_success(self.run_installer())
        self.payload = {relative: data + b"Updated.\n" for relative, data in self.payload.items()}
        self.write_source()
        self.assertEqual(self.run_installer(fault={"GOBAL_INSTALL_TEST_INTERRUPT_AFTER": "1"}).returncode, 97)
        journal_path = self.state_dir / "pilot-journal.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        relative = journal["entries"][0]["path"]
        target_before = self.target(relative).read_bytes()
        recovery, initial = self.start_paused_installer(
            "            [IO.File]::Copy($backup, $restore, $true)", "-Recover")
        restore_file = self.state_dir / "transactions" / journal["id"] / "restore" / relative
        restore_file.write_bytes(b"Externally changed staged restore.\n")

        stdout, stderr = recovery.communicate("\n", timeout=15)

        self.assertNotEqual(recovery.returncode, 0, initial + stdout + stderr)
        self.assertIn("restore", (stdout + stderr).lower())
        self.assertEqual(self.target(relative).read_bytes(), target_before)
        self.assertEqual(json.loads(journal_path.read_text(encoding="utf-8"))["status"], "applying")

    def test_recovery_refuses_a_restore_directory_junction_without_outside_writes(self):
        self.assert_success(self.run_installer())
        self.payload = {relative: data + b"Updated.\n" for relative, data in self.payload.items()}
        self.write_source()
        self.assertEqual(self.run_installer(fault={"GOBAL_INSTALL_TEST_INTERRUPT_AFTER": "1"}).returncode, 97)
        journal_path = self.state_dir / "pilot-journal.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        outside = self.root / "outside restore"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_bytes(b"Outside restore bytes must survive.")
        junction = self.state_dir / "transactions" / journal["id"] / "restore"
        command = (
            "New-Item -ItemType Junction -Path '" + str(junction).replace("'", "''")
            + "' -Target '" + str(outside).replace("'", "''") + "' | Out-Null"
        )
        encoded = base64.b64encode(command.encode("utf-16-le")).decode("ascii")
        created = subprocess.run([POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
                                 capture_output=True, text=True, timeout=10)
        if created.returncode != 0 or not junction.exists():
            self.skipTest("OS did not permit directory-junction creation: " + created.stderr.strip())
        try:
            refused = self.run_installer("-Recover")

            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("reparse", (refused.stdout + refused.stderr).lower())
            self.assertEqual(list(outside.iterdir()), [sentinel])
            self.assertEqual(sentinel.read_bytes(), b"Outside restore bytes must survive.")
            self.assertEqual(json.loads(journal_path.read_text(encoding="utf-8"))["status"], "applying")
        finally:
            junction.rmdir()

    def test_fault_markers_are_rejected_for_the_environment_user_profile(self):
        for marker in ("GOBAL_INSTALL_TEST_FAIL_AFTER", "GOBAL_INSTALL_TEST_INTERRUPT_AFTER",
                       "GOBAL_INSTALL_TEST_INTERRUPT_BEFORE_COMMIT"):
            with self.subTest(marker=marker):
                refused = self.run_installer(fault={marker: "1", "USERPROFILE": str(self.profile)})

                self.assertNotEqual(refused.returncode, 0)
                # PowerShell wraps Write-Error output to the console width, so compare whitespace-normalized text.
                output = " ".join((refused.stdout + refused.stderr).lower().split())
                self.assertIn("forbidden on the real profile", output)
                self.assertEqual(self.snapshot(), {})

    def test_exclusive_lock_rejects_a_concurrent_installer(self):
        self.state_dir.mkdir(parents=True)
        lock_path = str(self.state_dir / "pilot.lock").replace("'", "''")
        command = (
            f"$pilotHandle = [IO.File]::Open('{lock_path}', [IO.FileMode]::OpenOrCreate, "
            "[IO.FileAccess]::ReadWrite, [IO.FileShare]::None); "
            "[Console]::WriteLine('READY'); Start-Sleep -Seconds 10; $pilotHandle.Dispose()"
        )
        encoded = base64.b64encode(command.encode("utf-16-le")).decode("ascii")
        holder = subprocess.Popen([POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            self.assertEqual(holder.stdout.readline().strip(), "READY")

            refused = self.run_installer()

            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("exclusive lock", (refused.stdout + refused.stderr).lower())
            for relative in self.payload:
                self.assertFalse(self.target(relative).exists())
        finally:
            holder.terminate()
            holder.communicate(timeout=10)

    def test_recovery_dry_run_validates_pending_journal_without_writes(self):
        self.assertEqual(self.run_installer(fault={"GOBAL_INSTALL_TEST_INTERRUPT_AFTER": "1"}).returncode, 97)
        before = self.snapshot()

        result = self.run_installer("-Recover", "-DryRun")

        self.assert_success(result)
        self.assertIn("DRY RUN", result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_source_and_destination_reparse_points_are_rejected(self):
        outside = self.root / "outside profile"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_bytes(b"Outside bytes must survive.")
        junctions = (
            self.source / "pilot" / "skills" / "admin-evidence-pilot" / "linked",
            self.profile / ".gemini",
            self.target("skills"),
            self.state_dir,
        )
        for junction in junctions:
            with self.subTest(junction=junction):
                junction.parent.mkdir(parents=True, exist_ok=True)
                command = (
                    "New-Item -ItemType Junction -Path '" + str(junction).replace("'", "''")
                    + "' -Target '" + str(outside).replace("'", "''") + "' | Out-Null"
                )
                encoded = base64.b64encode(command.encode("utf-16-le")).decode("ascii")
                created = subprocess.run([POWERSHELL, "-NoLogo", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
                                         capture_output=True, text=True, timeout=10)
                if created.returncode != 0 or not junction.exists():
                    self.skipTest("OS did not permit directory-junction creation: " + created.stderr.strip())
                try:
                    refused = self.run_installer()

                    self.assertNotEqual(refused.returncode, 0)
                    self.assertIn("reparse", (refused.stdout + refused.stderr).lower())
                    self.assertEqual(sentinel.read_bytes(), b"Outside bytes must survive.")
                finally:
                    junction.rmdir()

    def test_repeated_install_and_uninstall_are_idempotent(self):
        self.assert_success(self.run_installer())
        before = {relative: self.target(relative).read_bytes() for relative in self.payload}
        state_before = self.snapshot()
        transactions_before = set((self.state_dir / "transactions").iterdir())

        repeated = self.run_installer()

        self.assert_success(repeated)
        self.assertIn("0 managed file operations", repeated.stdout)
        self.assertEqual(self.snapshot(), state_before)
        self.assertEqual(set((self.state_dir / "transactions").iterdir()), transactions_before)
        self.assertIn("no-op", repeated.stdout.lower())
        self.assertIn("Reload", repeated.stdout)
        for relative, data in before.items():
            self.assertEqual(self.target(relative).read_bytes(), data)
        self.assert_success(self.run_installer("-Uninstall"))
        state_before = self.snapshot()
        transactions_before = set((self.state_dir / "transactions").iterdir())
        repeated = self.run_installer("-Uninstall")
        self.assert_success(repeated)
        self.assertIn("0 managed file operations", repeated.stdout)
        self.assertIn("no-op", repeated.stdout.lower())
        self.assertEqual(self.snapshot(), state_before)
        self.assertEqual(set((self.state_dir / "transactions").iterdir()), transactions_before)
        self.assertEqual(json.loads((self.state_dir / "pilot-ownership.json").read_text(encoding="utf-8"))["files"], {})

    def test_install_dry_run_refuses_pending_journal_without_writes(self):
        self.assertEqual(self.run_installer(fault={"GOBAL_INSTALL_TEST_INTERRUPT_AFTER": "1"}).returncode, 97)
        before = self.snapshot()

        refused = self.run_installer("-DryRun")

        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("-Recover", refused.stdout + refused.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_json_and_exact_duplicate_manifest_keys_are_rejected(self):
        path = self.source / "pilot" / "manifest.json"
        original = path.read_text(encoding="utf-8")
        relative = "rules/admin-evidence-pilot.md"
        digest = hashlib.sha256(self.payload[relative]).hexdigest()
        duplicate = original.replace(f'"{relative}": "{digest}"',
                                     f'"{relative}": "{digest}", "{relative}": "{digest}"')
        for text in ("{ invalid JSON", duplicate):
            with self.subTest(text=text[:40]):
                path.write_text(text, encoding="utf-8")

                refused = self.run_installer()

                self.assertNotEqual(refused.returncode, 0, refused.stdout + refused.stderr)
                self.assertEqual(self.snapshot(), {})


if __name__ == "__main__":
    unittest.main()
