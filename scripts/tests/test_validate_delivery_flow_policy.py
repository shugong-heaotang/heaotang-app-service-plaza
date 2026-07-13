import copy
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("flow", ROOT / "scripts" / "validate_delivery_flow_policy.py")
FLOW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FLOW)
COLLAB_SPEC = importlib.util.spec_from_file_location(
    "collaboration", ROOT / "scripts" / "validate_agent_collaboration.py"
)
COLLABORATION = importlib.util.module_from_spec(COLLAB_SPEC)
COLLAB_SPEC.loader.exec_module(COLLABORATION)
COLLABORATION_SCHEMA = ROOT / "contracts" / "foundation" / "agent-collaboration.v1.schema.json"


class DeliveryFlowPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads((ROOT / "contracts/foundation/delivery-flow-policy.v1.json").read_text(encoding="utf-8"))
        self.schema = ROOT / "contracts/foundation/delivery-flow-policy.v1.schema.json"
        self.registry = json.loads((ROOT / "contracts/foundation/agent-collaboration.v1.json").read_text(encoding="utf-8"))
        self.repo_commit = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()

    def run_validation(self, policy=None, registry=None, schema=None, now=None):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "policy.json"
            r = Path(tmp) / "registry.json"
            s = Path(tmp) / "schema.json"
            p.write_text(json.dumps(policy or self.policy), encoding="utf-8")
            r.write_text(json.dumps(registry or self.registry), encoding="utf-8")
            s.write_text(json.dumps(schema or json.loads(self.schema.read_text(encoding="utf-8"))), encoding="utf-8")
            return FLOW.validate(
                p, s, r,
                now=now or datetime(2026, 7, 13, 6, 0, tzinfo=timezone.utc),
                repo_root=ROOT,
            )

    def governed_template(self):
        return next(i for i in self.registry["work_items"] if i.get("flow_policy_version"))

    def business_template(self):
        return next(i for i in self.registry["work_items"] if i.get("flow_class") == "business-stream")

    def integrated_business_registry(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("flow_class") == "business-stream")
        readme_hash = hashlib.sha256((ROOT / "README.md").read_bytes()).hexdigest()
        item.update({
            "status": "integrated",
            "metric_evidence": [{
                "metric_name": "synthetic journey pass rate",
                "target_value": 100,
                "actual_value": 100,
                "comparison": "gte",
                "unit": "percent",
                "measured_at": "2026-07-13T06:00:00+00:00",
                "evidence_path": "README.md",
                "evidence_sha256": readme_hash,
            }],
            "value_event_evidence": [{"path": "README.md", "sha256": readme_hash}],
            "independent_acceptance": {
                "exact_commit": self.repo_commit,
                "reviewer_role": item["reviewer_role"],
                "verdict": "go",
                "reviewed_at": "2026-07-13T06:00:00+00:00",
                "evidence_path": "README.md",
                "evidence_sha256": readme_hash,
            },
            "integration_commit": self.repo_commit,
        })
        return registry, item

    def test_current_registry_passes(self):
        self.assertEqual([], self.run_validation())

    def test_rejects_expired_status_contract(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("flow_policy_version"))
        item["status_expires_at"] = item["updated_at"]
        self.assertTrue(any("status expiry" in e for e in self.run_validation(registry=registry)))

    def test_rejects_global_wip_overflow(self):
        registry = copy.deepcopy(self.registry)
        template = next(i for i in registry["work_items"] if i.get("flow_policy_version"))
        for n in range(4):
            item = copy.deepcopy(template)
            item["work_id"] = f"AIW-20260713-TEST-FLOW-{n}"
            item["branch"] = f"codex/test-flow-{n}"
            item["workspace_path"] = f"C:/tmp/test-flow-{n}"
            item["flow_class"] = "business-stream"
            item["business_stream_id"] = f"test-flow-{n}"
            item["module_id"] = f"module-{n}"
            registry["work_items"].append(item)
        self.assertIn("DELIVERY_WIP_GLOBAL_EXCEEDED", self.run_validation(registry=registry))

    def test_rejects_business_stream_without_value_contract(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("flow_policy_version"))
        item["flow_class"] = "business-stream"
        for field in FLOW.REQUIRED_BUSINESS_FIELDS:
            item.pop(field, None)
        errors = self.run_validation(registry=registry)
        self.assertTrue(any("missing business value fields" in error for error in errors))

    def test_rejects_duplicate_active_business_stream(self):
        registry = copy.deepcopy(self.registry)
        template = next(i for i in registry["work_items"] if i.get("flow_class") == "business-stream")
        duplicate = copy.deepcopy(template)
        duplicate["work_id"] = "AIW-20260713-TEST-DUPLICATE-STREAM"
        duplicate["branch"] = "codex/test-duplicate-stream"
        duplicate["workspace_path"] = "C:/tmp/test-duplicate-stream"
        registry["work_items"].append(duplicate)
        self.assertIn("DELIVERY_DUPLICATE_ACTIVE_BUSINESS_STREAM", self.run_validation(registry=registry))

    def test_rejects_new_item_without_policy_fields(self):
        registry = copy.deepcopy(self.registry)
        item = copy.deepcopy(self.governed_template())
        item["work_id"] = "AIW-20260713-TEST-UNGOVERNED"
        for field in FLOW.REQUIRED_FLOW_FIELDS | {"flow_policy_version"}:
            item.pop(field, None)
        registry["work_items"].append(item)
        errors = self.run_validation(registry=registry)
        self.assertTrue(any("DELIVERY_NEW_ITEM_POLICY_REQUIRED" in e for e in errors))

    def test_rejects_legacy_status_change_without_migration(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("status") == "planned" and not i.get("flow_policy_version"))
        item["status"] = "active"
        errors = self.run_validation(registry=registry)
        self.assertIn("DELIVERY_LEGACY_STATE_CHANGED_WITHOUT_MIGRATION", errors)

    def test_rejects_legacy_self_rehashed_policy(self):
        registry = copy.deepcopy(self.registry)
        policy = copy.deepcopy(self.policy)
        item = next(i for i in registry["work_items"] if i.get("status") == "planned" and not i.get("flow_policy_version"))
        item["status"] = "active"
        cutover = policy["migration"]["legacy_cutover_work_id"]
        rows = []
        for legacy in registry["work_items"]:
            rows.append(f"{legacy['work_id']}\t{legacy['status']}")
            if legacy["work_id"] == cutover:
                break
        policy["migration"]["legacy_work_states_sha256"] = hashlib.sha256(
            ("\n".join(rows) + "\n").encode("utf-8")
        ).hexdigest()
        self.assertTrue(self.run_validation(policy=policy, registry=registry))

    def test_rejects_registry_policy_schema_triple_tamper(self):
        registry = copy.deepcopy(self.registry)
        policy = copy.deepcopy(self.policy)
        schema = json.loads(self.schema.read_text(encoding="utf-8"))
        item = next(i for i in registry["work_items"] if i.get("status") == "planned" and not i.get("flow_policy_version"))
        item["status"] = "active"
        cutover = policy["migration"]["legacy_cutover_work_id"]
        rows = []
        for legacy in registry["work_items"]:
            rows.append(f"{legacy['work_id']}\t{legacy['status']}")
            if legacy["work_id"] == cutover:
                break
        tampered_hash = hashlib.sha256(("\n".join(rows) + "\n").encode("utf-8")).hexdigest()
        policy["migration"]["legacy_work_states_sha256"] = tampered_hash
        schema["properties"]["migration"]["properties"]["legacy_work_states_sha256"]["const"] = tampered_hash
        errors = self.run_validation(policy=policy, registry=registry, schema=schema)
        self.assertIn("DELIVERY_LEGACY_EXTERNAL_SNAPSHOT_MISMATCH", errors)

    def test_rejects_status_expired_against_current_clock(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("flow_policy_version"))
        errors = self.run_validation(
            registry=registry,
            now=datetime(2026, 7, 15, 0, 0, tzinfo=timezone.utc),
        )
        self.assertTrue(any("DELIVERY_STATUS_EXPIRED" in e for e in errors))

    def test_rejects_handoff_without_next_owner(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("flow_policy_version"))
        item["status"] = "handoff-ready"
        errors = self.run_validation(registry=registry)
        self.assertTrue(any("DELIVERY_HANDOFF_OWNER_OR_REQUEST_MISSING" in e for e in errors))

    def test_rejects_overdue_handoff_sla(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("flow_policy_version"))
        item.update({
            "status": "handoff-ready",
            "next_owner_role": "independent reviewer",
            "handoff_requested_at": "2026-07-13T00:00:00+00:00",
        })
        errors = self.run_validation(
            registry=registry,
            now=datetime(2026, 7, 14, 1, 0, tzinfo=timezone.utc),
        )
        self.assertTrue(any("DELIVERY_HANDOFF_RESPONSE_SLA_EXCEEDED" in e for e in errors))
        self.assertTrue(any("DELIVERY_HANDOFF_DECISION_SLA_EXCEEDED" in e for e in errors))
        self.assertTrue(any("DELIVERY_HANDOFF_ESCALATION_EVIDENCE_REQUIRED" in e for e in errors))

    def test_rejects_duplicate_stream_across_active_and_handoff(self):
        registry = copy.deepcopy(self.registry)
        template = next(i for i in registry["work_items"] if i.get("flow_class") == "business-stream")
        duplicate = copy.deepcopy(template)
        duplicate.update({
            "work_id": "AIW-20260713-TEST-HANDOFF-DUPLICATE",
            "branch": "codex/test-handoff-duplicate",
            "workspace_path": "C:/tmp/test-handoff-duplicate",
            "status": "handoff-ready",
            "next_owner_role": "independent reviewer",
            "handoff_requested_at": "2026-07-13T05:00:00+00:00",
        })
        registry["work_items"].append(duplicate)
        self.assertIn("DELIVERY_DUPLICATE_ACTIVE_BUSINESS_STREAM", self.run_validation(registry=registry))

    def test_rejects_integrated_business_stream_without_completion_evidence(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("flow_class") == "business-stream")
        item["status"] = "integrated"
        errors = self.run_validation(registry=registry)
        self.assertTrue(any("DELIVERY_COMPLETION_VALUE_EVIDENCE_REQUIRED" in e for e in errors))
        self.assertTrue(any("DELIVERY_INDEPENDENT_ACCEPTANCE_REQUIRED" in e for e in errors))

    def test_rejects_fabricated_integrated_evidence(self):
        registry, item = self.integrated_business_registry()
        item["metric_evidence"][0]["evidence_path"] = "missing/metric-evidence.json"
        item["value_event_evidence"] = [{"path": "missing/value-event.json", "sha256": "0" * 64}]
        item["independent_acceptance"].update({
            "exact_commit": "0" * 40,
            "reviewer_role": "未登记验收角色",
            "evidence_path": "missing/acceptance.md",
        })
        item["integration_commit"] = "f" * 40
        errors = self.run_validation(registry=registry)
        expected = {
            "DELIVERY_METRIC_EVIDENCE_PATH_INVALID",
            "DELIVERY_VALUE_EVIDENCE_PATH_INVALID",
            "DELIVERY_INDEPENDENT_REVIEWER_NOT_REGISTERED",
            "DELIVERY_ACCEPTANCE_COMMIT_INVALID",
            "DELIVERY_INTEGRATION_COMMIT_INVALID",
        }
        self.assertTrue(all(any(code in error for error in errors) for code in expected))

    def test_rejects_metric_below_target(self):
        registry, item = self.integrated_business_registry()
        item["metric_evidence"][0]["actual_value"] = 0
        errors = self.run_validation(registry=registry)
        self.assertTrue(any("DELIVERY_METRIC_TARGET_NOT_MET" in e for e in errors))

    def test_rejects_existing_evidence_with_wrong_hash(self):
        registry, item = self.integrated_business_registry()
        item["metric_evidence"][0]["evidence_sha256"] = "0" * 64
        item["value_event_evidence"][0]["sha256"] = "0" * 64
        item["independent_acceptance"]["evidence_sha256"] = "0" * 64
        errors = self.run_validation(registry=registry)
        expected = {
            "DELIVERY_METRIC_EVIDENCE_PATH_INVALID",
            "DELIVERY_VALUE_EVIDENCE_PATH_INVALID",
            "DELIVERY_ACCEPTANCE_EVIDENCE_PATH_INVALID",
        }
        self.assertTrue(all(any(code in error for error in errors) for code in expected))

    def test_rejects_developer_reviewer_role_conflict(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("flow_policy_version"))
        item["reviewer_role"] = item["developer_role"]
        errors = self.run_validation(registry=registry)
        self.assertTrue(any("developer and independent reviewer" in e for e in errors))

    def test_rejects_per_module_wip_overflow(self):
        registry = copy.deepcopy(self.registry)
        template = next(i for i in registry["work_items"] if i.get("flow_class") == "business-stream")
        duplicate = copy.deepcopy(template)
        duplicate.update({
            "work_id": "AIW-20260713-TEST-MODULE-WIP",
            "branch": "codex/test-module-wip",
            "workspace_path": "C:/tmp/test-module-wip",
            "business_stream_id": "another-stream-same-module",
        })
        registry["work_items"].append(duplicate)
        self.assertIn("DELIVERY_WIP_MODULE_EXCEEDED", self.run_validation(registry=registry))

    def test_rejects_missing_required_flow_field(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("flow_policy_version"))
        item.pop("next_checkpoint")
        errors = self.run_validation(registry=registry)
        self.assertTrue(any("missing flow fields" in e for e in errors))


class AgentCollaborationBaseCommitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo_a, self.commit_a = self.new_repo("repo-a")
        self.repo_b, self.commit_b = self.new_repo("repo-b")

    def tearDown(self):
        self.temp.cleanup()

    def git(self, repo, *args):
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()

    def new_repo(self, name):
        repo = self.root / name
        repo.mkdir()
        self.git(repo, "init")
        self.git(repo, "config", "user.email", "validator@example.invalid")
        self.git(repo, "config", "user.name", "Validator Test")
        (repo / "seed.txt").write_text(name + "\n", encoding="utf-8")
        self.git(repo, "add", "seed.txt")
        self.git(repo, "commit", "-m", "seed")
        return repo, self.git(repo, "rev-parse", "HEAD")

    def item(self, work_id, status, repository_root, base_commit):
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

    def validate(self, items):
        registry = self.root / "registry.json"
        registry.write_text(
            json.dumps({
                "contract_version": "agent-collaboration.v1",
                "integration_owner_role": "platform owner",
                "workspace_policy": "isolated-branch-and-worktree",
                "protected_paths": ["contracts/foundation"],
                "work_items": items,
            }),
            encoding="utf-8",
        )
        return COLLABORATION.validate(COLLABORATION_SCHEMA, registry)

    def test_active_commit_is_checked_in_its_own_cross_repository_root(self):
        item = self.item("AIW-20260713-CROSS-REPO", "active", self.repo_b, self.commit_b)
        self.assertEqual([], self.validate([item]))

    def test_active_commit_from_another_repository_is_rejected(self):
        item = self.item("AIW-20260713-WRONG-REPO", "active", self.repo_b, self.commit_a)
        self.assertTrue(any("does not exist as a commit" in error for error in self.validate([item])))

    def test_handoff_ready_missing_commit_is_rejected(self):
        item = self.item("AIW-20260713-HANDOFF", "handoff-ready", self.repo_a, "0" * 40)
        self.assertTrue(any("does not exist as a commit" in error for error in self.validate([item])))

    def test_planned_and_cancelled_legacy_rows_do_not_require_local_objects(self):
        planned = self.item("AIW-20260713-PLANNED", "planned", self.root / "gone-a", "1" * 40)
        cancelled = self.item("AIW-20260713-CANCELLED", "cancelled", self.root / "gone-b", "2" * 40)
        self.assertEqual([], self.validate([planned, cancelled]))

    def test_active_missing_repository_root_is_rejected(self):
        item = self.item("AIW-20260713-MISSING-ROOT", "active", self.root / "gone", "3" * 40)
        self.assertTrue(any("repository_root does not exist" in error for error in self.validate([item])))


if __name__ == "__main__":
    unittest.main()
