import copy
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("flow", ROOT / "scripts" / "validate_delivery_flow_policy.py")
FLOW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FLOW)


class DeliveryFlowPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads((ROOT / "contracts/foundation/delivery-flow-policy.v1.json").read_text(encoding="utf-8"))
        self.schema = ROOT / "contracts/foundation/delivery-flow-policy.v1.schema.json"
        self.registry = json.loads((ROOT / "contracts/foundation/agent-collaboration.v1.json").read_text(encoding="utf-8"))

    def run_validation(self, policy=None, registry=None, now=None):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "policy.json"
            r = Path(tmp) / "registry.json"
            p.write_text(json.dumps(policy or self.policy), encoding="utf-8")
            r.write_text(json.dumps(registry or self.registry), encoding="utf-8")
            return FLOW.validate(
                p, self.schema, r,
                now=now or datetime(2026, 7, 13, 6, 0, tzinfo=timezone.utc),
            )

    def governed_template(self):
        return next(i for i in self.registry["work_items"] if i.get("flow_policy_version"))

    def business_template(self):
        return next(i for i in self.registry["work_items"] if i.get("flow_class") == "business-stream")

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


if __name__ == "__main__":
    unittest.main()
