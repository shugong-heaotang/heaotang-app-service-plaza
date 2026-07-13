import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from scripts.build_project_brain import atomic_write_json, build_snapshot, safe_repo_path
from scripts.validate_project_brain import validate


class ProjectBrainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "contracts/foundation").mkdir(parents=True)
        (self.root / "contracts/project-brain").mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, rel, value):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def fixture(self, work=None):
        self.write("contracts/foundation/agent-collaboration.v1.json", {"work_items": work or []})
        ids = {"modules": "module_id", "knowledge-sources": "knowledge_id", "decisions": "decision_id", "risks": "risk_id"}
        for name in ids:
            self.write(f"contracts/project-brain/{name}.v1.json", {"contract_version": f"project-brain.{name}.v1", "items": []})
            self.write(f"contracts/project-brain/{name}.v1.schema.json", {"type": "object", "required": ["items"], "properties": {"items": {"type": "array"}}})

    def build(self, work=None):
        self.fixture(work)
        return build_snapshot(self.root, datetime(2026, 7, 12, tzinfo=timezone.utc))

    def test_path_escape_and_absolute_path_are_rejected(self):
        for value in ("../outside", str(self.root.resolve())):
            with self.assertRaises(ValueError):
                safe_repo_path(self.root, value)

    def test_overlap_and_shared_workspace_fail_closed(self):
        snapshot, audit = self.build([
            {"work_id": "A", "status": "active", "workspace_path": "x", "allowed_paths": ["app"]},
            {"work_id": "B", "status": "active", "workspace_path": "x", "allowed_paths": ["app/x"]},
        ])
        rules = {item["rule_id"] for item in audit["errors"]}
        self.assertEqual("no-go", snapshot["overall_verdict"])
        self.assertIn("PB-SCOPE-CONFLICT", rules)
        self.assertIn("PB-WORKSPACE-CONFLICT", rules)

    def test_integrated_without_handoff_is_not_go(self):
        snapshot, audit = self.build([{"work_id": "A", "status": "integrated", "allowed_paths": ["x"], "workspace_path": "x"}])
        self.assertEqual("no-go", snapshot["overall_verdict"])
        self.assertIn("PB-INTEGRATED-EVIDENCE", {x["rule_id"] for x in audit["errors"]})

    def test_high_risk_requires_three_distinct_roles(self):
        _, audit = self.build([{"work_id": "A", "status": "active", "risk_level": "high", "workspace_path": "x", "allowed_paths": ["x"], "developer": "same", "reviewer": "same", "approver": "owner"}])
        self.assertIn("PB-ROLE-SEPARATION", {x["rule_id"] for x in audit["errors"]})

    def test_output_whitelist_excludes_secrets_and_local_paths(self):
        snapshot, audit = self.build([{"work_id": "A", "title": "ok", "status": "active", "workspace_path": "C:/secret", "repository_root": "C:/repo", "allowed_paths": ["x"], "password": "never-copy", "token": "never-copy"}])
        encoded = json.dumps({"snapshot": snapshot, "audit": audit})
        self.assertNotIn("never-copy", encoded)
        self.assertNotIn("C:/secret", encoded)
        self.assertEqual([], validate(snapshot, audit))

    def test_missing_catalog_is_error_not_old_go(self):
        self.fixture([])
        (self.root / "contracts/project-brain/risks.v1.json").unlink()
        snapshot, audit = build_snapshot(self.root, datetime(2026, 7, 12, tzinfo=timezone.utc))
        self.assertEqual("no-go", snapshot["overall_verdict"])
        self.assertTrue(audit["errors"])

    def test_duplicate_authority_and_stale_review_are_reported(self):
        self.fixture([])
        source = self.root / "README.md"
        source.write_text("authority", encoding="utf-8")
        items = [
            {"knowledge_id": "KB-A", "title": "A", "category": "governance", "source_path": "README.md", "owner_role": "owner", "scope": "all", "supersedes": [], "status": "authoritative", "last_reviewed_at": "2026-01-01T00:00:00Z", "next_review_at": "2026-01-02T00:00:00Z"},
            {"knowledge_id": "KB-B", "title": "B", "category": "governance", "source_path": "README.md", "owner_role": "owner", "scope": "all", "supersedes": [], "status": "authoritative", "last_reviewed_at": "2026-01-01T00:00:00Z", "next_review_at": "2026-01-02T00:00:00Z"},
        ]
        self.write("contracts/project-brain/knowledge-sources.v1.json", {"items": items})
        _, audit = build_snapshot(self.root, datetime(2026, 7, 12, tzinfo=timezone.utc))
        rules = {x["rule_id"] for x in audit["errors"] + audit["warnings"]}
        self.assertIn("PB-DUPLICATE-AUTHORITY", rules)
        self.assertIn("PB-STALE-SOURCE", rules)

    def test_sc_t0_integrated_status_is_not_rewritten_as_go(self):
        snapshot, _ = self.build([{"work_id": "AIW-SC-T0", "title": "No-Go remediation evidence", "status": "integrated", "workspace_path": "x", "allowed_paths": ["x"], "handoff_record": "no-go.md"}])
        item = snapshot["recent_integrations"][0]
        self.assertEqual("integrated", item["status"])
        self.assertNotIn("verdict", item)

    def test_authoritative_inputs_are_not_modified(self):
        self.fixture([])
        before = {p: p.read_bytes() for p in self.root.rglob("*.json")}
        build_snapshot(self.root, datetime(2026, 7, 12, tzinfo=timezone.utc))
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*.json")})

    def test_atomic_write_leaves_no_partial_target_on_replace_failure(self):
        target = self.root / "out.json"
        target.write_text('{"old": true}\n', encoding="utf-8")
        with patch("scripts.build_project_brain.os.replace", side_effect=OSError("boom")):
            with self.assertRaises(OSError):
                atomic_write_json(target, {"new": True})
        self.assertEqual('{"old": true}\n', target.read_text(encoding="utf-8"))
        self.assertEqual([], list(self.root.glob("out.json.*.tmp")))


if __name__ == "__main__":
    unittest.main()
