from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "Test-IntegrationPushFreshness.ps1"
POLICY = ROOT / "contracts" / "foundation" / "integration-push-policy.v1.json"
SCHEMA = ROOT / "contracts" / "foundation" / "integration-push-policy.v1.schema.json"
VALIDATOR = ROOT / "scripts" / "validate_integration_push_policy.py"
AUTHORITY_BRANCH = "codex/service-plaza-phase1-integration"
POWERSHELL = shutil.which("powershell") or shutil.which("powershell.exe")


def git(*args: str, cwd: Path | None = None) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


class IntegrationPushFreshnessTests(unittest.TestCase):
    def setUp(self) -> None:
        if POWERSHELL is None:
            self.skipTest("Windows PowerShell is required")
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.repo = self.root / "candidate"
        git("init", "--bare", str(self.remote))
        git("init", str(self.repo))
        git("config", "user.name", "Freshness Test", cwd=self.repo)
        git("config", "user.email", "freshness@example.invalid", cwd=self.repo)
        git("config", "core.autocrlf", "false", cwd=self.repo)
        git("checkout", "-b", "codex/test-candidate", cwd=self.repo)
        (self.repo / "state.txt").write_text("base\n", encoding="utf-8")
        git("add", "state.txt", cwd=self.repo)
        git("commit", "-m", "base", cwd=self.repo)
        self.base = git("rev-parse", "HEAD", cwd=self.repo)
        git("remote", "add", "origin", str(self.remote), cwd=self.repo)
        git("push", "origin", f"HEAD:refs/heads/{AUTHORITY_BRANCH}", cwd=self.repo)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def commit_candidate(self, value: str = "candidate") -> str:
        (self.repo / "state.txt").write_text(f"{value}\n", encoding="utf-8")
        git("add", "state.txt", cwd=self.repo)
        git("commit", "-m", value, cwd=self.repo)
        return git("rev-parse", "HEAD", cwd=self.repo)

    def move_remote(self, value: str = "remote-moved") -> str:
        updater = self.root / f"updater-{value}"
        git("clone", "--branch", AUTHORITY_BRANCH, str(self.remote), str(updater))
        git("config", "user.name", "Remote Test", cwd=updater)
        git("config", "user.email", "remote@example.invalid", cwd=updater)
        (updater / "remote.txt").write_text(f"{value}\n", encoding="utf-8")
        git("add", "remote.txt", cwd=updater)
        git("commit", "-m", value, cwd=updater)
        git("push", "origin", f"HEAD:refs/heads/{AUTHORITY_BRANCH}", cwd=updater)
        return git("rev-parse", "HEAD", cwd=updater)

    def run_gate(self, expected: str, execute: bool = False) -> tuple[int, dict]:
        command = [
            POWERSHELL,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(SCRIPT),
            "-ProjectRoot",
            str(self.repo),
            "-ExpectedRemoteHead",
            expected,
            "-PolicyPath",
            str(POLICY),
        ]
        if execute:
            command.append("-ExecutePush")
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        lines = [line for line in completed.stdout.splitlines() if line.strip().startswith("{")]
        self.assertTrue(lines, completed.stdout + completed.stderr)
        return completed.returncode, json.loads(lines[-1])

    def test_policy_contract_validates(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(VALIDATOR), str(SCHEMA), str(POLICY)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_fresh_candidate_is_ready(self) -> None:
        candidate = self.commit_candidate()
        code, result = self.run_gate(self.base)
        self.assertEqual(0, code)
        self.assertEqual("ready", result["status"])
        self.assertEqual(candidate, result["details"]["candidate_head"])
        self.assertEqual(0, result["details"]["behind"])
        self.assertEqual(1, result["details"]["ahead"])

    def test_lease_protected_push_updates_remote(self) -> None:
        candidate = self.commit_candidate()
        code, result = self.run_gate(self.base, execute=True)
        self.assertEqual(0, code)
        self.assertEqual("pushed", result["status"])
        actual = git("ls-remote", "origin", f"refs/heads/{AUTHORITY_BRANCH}", cwd=self.repo).split()[0]
        self.assertEqual(candidate, actual)

    def test_stale_expected_remote_is_rejected(self) -> None:
        self.commit_candidate()
        self.move_remote()
        code, result = self.run_gate(self.base)
        self.assertNotEqual(0, code)
        self.assertEqual("INTEGRATION_REMOTE_HEAD_CHANGED", result["error_id"])

    def test_diverged_candidate_is_rejected(self) -> None:
        self.commit_candidate()
        remote_head = self.move_remote()
        code, result = self.run_gate(remote_head)
        self.assertNotEqual(0, code)
        self.assertEqual("INTEGRATION_REMOTE_NOT_ANCESTOR", result["error_id"])

    def test_behind_candidate_is_rejected(self) -> None:
        remote_head = self.move_remote()
        code, result = self.run_gate(remote_head)
        self.assertNotEqual(0, code)
        self.assertEqual("INTEGRATION_CANDIDATE_BEHIND", result["error_id"])

    def test_dirty_worktree_is_rejected(self) -> None:
        self.commit_candidate()
        (self.repo / "untracked.txt").write_text("dirty\n", encoding="utf-8")
        code, result = self.run_gate(self.base)
        self.assertNotEqual(0, code)
        self.assertEqual("INTEGRATION_WORKTREE_DIRTY", result["error_id"])

    def test_non_codex_branch_is_rejected(self) -> None:
        self.commit_candidate()
        git("branch", "-m", "main", cwd=self.repo)
        code, result = self.run_gate(self.base)
        self.assertNotEqual(0, code)
        self.assertEqual("INTEGRATION_CANDIDATE_BRANCH_INVALID", result["error_id"])


if __name__ == "__main__":
    unittest.main()
