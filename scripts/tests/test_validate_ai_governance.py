import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from validate_agent_collaboration import validate as validate_collaboration
from validate_development_checklists import validate as validate_checklists


class AIGovernanceValidationTests(unittest.TestCase):
    def test_checklist_rejects_stale_hash_and_omitted_reading_item(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "RULE.md"
            source.write_text("v1", encoding="utf-8")
            reading = root / "contracts/foundation"
            reading.mkdir(parents=True)
            reading_list = reading / "governance-reading-list.v1.json"
            reading_list.write_text(json.dumps({"core": ["RULE.md"], "module_overlays": {}}), encoding="utf-8")
            schema = Path(__file__).resolve().parents[2] / "contracts/foundation/development-checklist.v1.schema.json"
            checklists = reading / "development-checklists"
            checklists.mkdir()
            checklist = {
                "contract_version": "development-checklist.v1",
                "checklist_id": "FC-20260710-TEST",
                "record_id": "IR-20260710-TEST",
                "task": "test",
                "actor": "test agent",
                "module_id": None,
                "status": "completed",
                "created_at": "2026-07-10T00:00:00Z",
                "completed_at": "2026-07-10T00:01:00Z",
                "items": [{
                    "path": "RULE.md",
                    "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                    "checked": True,
                    "checked_at": "2026-07-10T00:01:00Z",
                }],
                "attestation": "I read and applied every checked governance input to this implementation.",
            }
            target = checklists / "test.json"
            target.write_text(json.dumps(checklist), encoding="utf-8")
            self.assertEqual(validate_checklists(schema, checklists, root, require_current=True), [])
            source.write_text("v2", encoding="utf-8")
            self.assertTrue(any("stale acknowledgement" in error for error in validate_checklists(schema, checklists, root, require_current=True)))
            source.write_text("v1", encoding="utf-8")
            reading_list.write_text(
                json.dumps({"core": ["RULE.md", "MISSING.md"], "module_overlays": {}}), encoding="utf-8"
            )
            self.assertTrue(any("does not match reading list" in error for error in validate_checklists(schema, checklists, root, require_current=True)))

    def test_collaboration_rejects_shared_workspace_and_overlapping_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            schema = Path(__file__).resolve().parents[2] / "contracts/foundation/agent-collaboration.v1.schema.json"
            item = {
                "work_id": "AIW-20260710-ONE",
                "title": "one",
                "owner": "agent one",
                "owner_role": "板块负责人",
                "status": "active",
                "repository_root": "C:/repo",
                "workspace_path": "C:/repo-one",
                "branch": "codex/one",
                "base_commit": "a" * 40,
                "allowed_paths": ["modules/life"],
                "started_with_clean_worktree": True,
                "preexisting_changes_acknowledged": False,
                "handoff_record": None,
            }
            other = copy.deepcopy(item)
            other.update(work_id="AIW-20260710-TWO", owner="agent two", branch="codex/two")
            registry = {
                "contract_version": "agent-collaboration.v1",
                "integration_owner_role": "平台集成负责人",
                "workspace_policy": "isolated-branch-and-worktree",
                "protected_paths": ["contracts/foundation"],
                "work_items": [item, other],
            }
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(registry), encoding="utf-8")
            errors = validate_collaboration(schema, path)
            self.assertTrue(any("share workspace" in error for error in errors))
            self.assertTrue(any("scopes overlap" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
