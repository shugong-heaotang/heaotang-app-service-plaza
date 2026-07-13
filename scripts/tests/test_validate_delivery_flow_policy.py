import copy
import importlib.util
import json
import tempfile
import unittest
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

    def run_validation(self, policy=None, registry=None):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "policy.json"
            r = Path(tmp) / "registry.json"
            p.write_text(json.dumps(policy or self.policy), encoding="utf-8")
            r.write_text(json.dumps(registry or self.registry), encoding="utf-8")
            return FLOW.validate(p, self.schema, r)

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


if __name__ == "__main__":
    unittest.main()
