import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "validate_agent_collaboration", ROOT / "scripts" / "validate_agent_collaboration.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)
SCHEMA = ROOT / "contracts" / "foundation" / "agent-collaboration.v1.schema.json"


class BaseCommitExistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo_a, self.commit_a = self._new_repo("repo-a")
        self.repo_b, self.commit_b = self._new_repo("repo-b")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _git(self, repo: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout.strip()

    def _new_repo(self, name: str) -> tuple[Path, str]:
        repo = self.root / name
        repo.mkdir()
        self._git(repo, "init")
        self._git(repo, "config", "user.email", "validator@example.invalid")
        self._git(repo, "config", "user.name", "Validator Test")
        (repo / "seed.txt").write_text(name + "\n", encoding="utf-8")
        self._git(repo, "add", "seed.txt")
        self._git(repo, "commit", "-m", "seed")
        return repo, self._git(repo, "rev-parse", "HEAD")

    def _item(self, work_id: str, status: str, repository_root: Path, base_commit: str) -> dict:
        return {
            "work_id": work_id,
            "title": work_id,
            "owner": "test owner",
            "owner_role": "module owner",
            "status": status,
            "repository_root": repository_root.as_posix(),
            "workspace_path": (self.root / ("workspace-" + work_id.lower())).as_posix(),
            "branch": "codex/" + work_id.lower(),
            "base_commit": base_commit,
            "allowed_paths": ["modules/" + work_id.lower()],
            "started_with_clean_worktree": True,
            "preexisting_changes_acknowledged": False,
            "migration_note": None,
            "handoff_record": None,
        }

    def _validate(self, items: list[dict]) -> list[str]:
        registry = self.root / "registry.json"
        registry.write_text(
            json.dumps(
                {
                    "contract_version": "agent-collaboration.v1",
                    "integration_owner_role": "platform owner",
                    "workspace_policy": "isolated-branch-and-worktree",
                    "protected_paths": ["contracts/foundation"],
                    "work_items": items,
                }
            ),
            encoding="utf-8",
        )
        return VALIDATOR.validate(SCHEMA, registry)

    def test_active_commit_is_checked_in_its_own_cross_repository_root(self) -> None:
        item = self._item("AIW-20260713-CROSS-REPO", "active", self.repo_b, self.commit_b)
        self.assertEqual([], self._validate([item]))

    def test_active_commit_from_another_repository_is_rejected(self) -> None:
        item = self._item("AIW-20260713-WRONG-REPO", "active", self.repo_b, self.commit_a)
        errors = self._validate([item])
        self.assertTrue(any("does not exist as a commit" in error for error in errors), errors)

    def test_handoff_ready_missing_commit_is_rejected(self) -> None:
        item = self._item("AIW-20260713-HANDOFF", "handoff-ready", self.repo_a, "0" * 40)
        errors = self._validate([item])
        self.assertTrue(any("does not exist as a commit" in error for error in errors), errors)

    def test_planned_and_cancelled_legacy_rows_do_not_require_local_objects(self) -> None:
        planned = self._item("AIW-20260713-PLANNED", "planned", self.root / "gone-a", "1" * 40)
        cancelled = self._item("AIW-20260713-CANCELLED", "cancelled", self.root / "gone-b", "2" * 40)
        self.assertEqual([], self._validate([planned, cancelled]))

    def test_active_missing_repository_root_is_rejected(self) -> None:
        item = self._item("AIW-20260713-MISSING-ROOT", "active", self.root / "gone", "3" * 40)
        errors = self._validate([item])
        self.assertTrue(any("repository_root does not exist" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
