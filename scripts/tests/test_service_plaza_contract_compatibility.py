import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "check_service_plaza_contract_compatibility.py"
FIXTURES = ROOT / "contracts" / "service-plaza" / "compatibility-fixtures"


class CompatibilityGateTests(unittest.TestCase):
    def run_gate(self, old: str, new: str, kind: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), str(FIXTURES / old), str(FIXTURES / new), "--kind", kind, "--format", "json"],
            check=False,
            capture_output=True,
            encoding="utf-8",
        )

    def assert_compatible(self, old: str, new: str, kind: str) -> None:
        result = self.run_gate(old, new, kind)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertTrue(json.loads(result.stdout)["compatible"])

    def assert_breaking(self, old: str, new: str, kind: str, rules: set[str]) -> None:
        result = self.run_gate(old, new, kind)
        self.assertEqual(result.returncode, 1, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["compatible"])
        actual_rules = {finding["rule"] for finding in payload["findings"]}
        self.assertTrue(rules.issubset(actual_rules), (rules, actual_rules))

    def test_action_display_only_change_is_compatible(self) -> None:
        self.assert_compatible("action-old.json", "action-compatible.json", "action-baseline")

    def test_action_reorder_id_reuse_target_and_auth_changes_are_blocked(self) -> None:
        self.assert_breaking(
            "action-old.json",
            "action-breaking.json",
            "action-baseline",
            {"ACTION_REORDERED", "ACTION_ID_REUSED", "ACTION_BOUNDARY_CHANGED", "AUTH_BOUNDARY_CHANGED"},
        )

    def test_manifest_display_and_capability_addition_are_compatible(self) -> None:
        self.assert_compatible("manifest-old.json", "manifest-compatible.json", "service-manifest")

    def test_manifest_navigation_auth_and_privacy_changes_are_blocked(self) -> None:
        self.assert_breaking(
            "manifest-old.json",
            "manifest-breaking.json",
            "service-manifest",
            {"SERVICE_BOUNDARY_CHANGED", "AUTH_BOUNDARY_CHANGED", "SCOPE_BOUNDARY_CHANGED", "CAPABILITY_REMOVED"},
        )

    def test_schema_optional_field_is_compatible(self) -> None:
        self.assert_compatible("schema-old.json", "schema-compatible.json", "json-schema")

    def test_schema_required_and_constraint_tightening_are_blocked(self) -> None:
        self.assert_breaking(
            "schema-old.json",
            "schema-breaking.json",
            "json-schema",
            {"REQUIRED_FIELD_ADDED", "ENUM_NARROWED", "LOWER_BOUND_TIGHTENED", "PATTERN_ADDED_OR_CHANGED"},
        )

    def test_old_git_ref_reads_the_released_blob_not_the_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            contract = repository / "action.json"
            contract.write_text((FIXTURES / "action-old.json").read_text(encoding="utf-8"), encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
            subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=repository, check=True)
            subprocess.run(["git", "config", "user.email", "gate-test@example.invalid"], cwd=repository, check=True)
            subprocess.run(["git", "config", "user.name", "Compatibility Gate Test"], cwd=repository, check=True)
            subprocess.run(["git", "add", "action.json"], cwd=repository, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repository, check=True)
            contract.write_text((FIXTURES / "action-breaking.json").read_text(encoding="utf-8"), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-X", "utf8", str(SCRIPT), "action.json", "action.json", "--old-git-ref", "HEAD", "--kind", "action-baseline"],
                cwd=repository,
                check=False,
                capture_output=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 1, result.stderr or result.stdout)
            self.assertIn("ACTION_REORDERED", result.stderr)


if __name__ == "__main__":
    unittest.main()
