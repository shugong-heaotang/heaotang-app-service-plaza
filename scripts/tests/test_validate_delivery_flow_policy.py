import copy
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from unittest import mock
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

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
        self.policy = json.loads((ROOT / "contracts/foundation/delivery-flow-policy.v2.json").read_text(encoding="utf-8"))
        self.schema = ROOT / "contracts/foundation/delivery-flow-policy.v2.schema.json"
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
        post_cutover = copy.deepcopy(self.registry)
        item = next(
            row for row in post_cutover["work_items"]
            if row["work_id"] == "AIW-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-MIGRATION-V2"
        )
        item["flow_policy_version"] = "delivery-flow-policy.v2"
        self.assertEqual([], self.run_validation(registry=post_cutover))
        receipt = json.loads((ROOT / self.policy["migration"]["receipt_path"]).read_text(encoding="utf-8"))
        canonical = "".join(
            f"{entry['work_id']}\t{entry['from_status']}\t{entry['to_status']}\n"
            for entry in receipt["transitions"]
        )
        self.assertEqual(hashlib.sha256(canonical.encode("utf-8")).hexdigest(), FLOW.LEGACY_TRANSITION_SHA256)
        projected = []
        by_index = {entry["legacy_index"]: entry for entry in receipt["transitions"]}
        for index, row in enumerate(self.registry["work_items"][:115]):
            projected.append(f"{row['work_id']}\t{by_index.get(index, {}).get('to_status', row['status'])}\n")
        self.assertEqual(hashlib.sha256("".join(projected).encode("utf-8")).hexdigest(), FLOW.LEGACY_POST_STATES_SHA256)
        schema = json.loads((ROOT / self.policy["migration"]["receipt_schema_path"]).read_text(encoding="utf-8"))
        receipt["transitions"].pop()
        receipt["review"] = {"verdict": "go"}
        messages = [error.message for error in Draft202012Validator(schema).iter_errors(receipt)]
        self.assertTrue(any("too short" in message for message in messages), messages)
        self.assertTrue(any("not of type 'null'" in message for message in messages), messages)

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
        unknown = copy.deepcopy(self.registry)
        unknown["work_items"][-1]["flow_policy_version"] = "delivery-flow-policy.v999"
        self.assertTrue(any("DELIVERY_NEW_ITEM_POLICY_REQUIRED" in e for e in self.run_validation(registry=unknown)))

    def test_rejects_legacy_status_change_without_migration(self):
        registry = copy.deepcopy(self.registry)
        item = next(i for i in registry["work_items"] if i.get("status") == "planned" and not i.get("flow_policy_version"))
        item["status"] = "active"
        errors = self.run_validation(registry=registry)
        self.assertIn("DELIVERY_LEGACY_STATE_CHANGED_WITHOUT_MIGRATION", errors)
        partial = copy.deepcopy(self.registry)
        receipt = json.loads((ROOT / self.policy["migration"]["receipt_path"]).read_text(encoding="utf-8"))
        first = receipt["transitions"][0]
        partial["work_items"][first["legacy_index"]]["status"] = first["to_status"]
        self.assertIn("DELIVERY_LEGACY_PARTIAL_TRANSITION", self.run_validation(registry=partial))

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
        receipt_tamper = copy.deepcopy(self.policy)
        receipt_tamper["migration"]["receipt_sha256"] = "0" * 64
        self.assertIn("DELIVERY_LEGACY_RECEIPT_HASH_MISMATCH", self.run_validation(policy=receipt_tamper))

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
        item = next(
            i for i in registry["work_items"]
            if i.get("flow_policy_version") and i.get("status") in {"active", "handoff-ready"}
        )
        item["updated_at"] = "2026-07-14T23:00:00+00:00"
        item["status_expires_at"] = "2026-07-14T23:30:00+00:00"
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
        projected = copy.deepcopy(self.registry)
        receipt = json.loads((ROOT / self.policy["migration"]["receipt_path"]).read_text(encoding="utf-8"))
        for entry in receipt["transitions"]:
            projected["work_items"][entry["legacy_index"]]["status"] = entry["to_status"]
        projected_errors = self.run_validation(registry=projected)
        self.assertFalse(any("LEGACY" in error for error in projected_errors), projected_errors)
        self.assertTrue(any("HANDOFF_OWNER_OR_REQUEST_MISSING" in error for error in projected_errors), projected_errors)
        self.assertTrue(any("INDEPENDENT_ACCEPTANCE_REQUIRED" in error for error in projected_errors), projected_errors)

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


class DeliveryFlowPolicyV3ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.policy_path = ROOT / "contracts/foundation/delivery-flow-policy.v3.json"
        self.schema_path = ROOT / "contracts/foundation/delivery-flow-policy.v3.schema.json"
        self.registry_path = ROOT / "contracts/foundation/agent-collaboration.v1.json"
        self.receipt_path = ROOT / "contracts/foundation/legacy-lifecycle-migrations/LLM-20260715-TECHNICAL-SOCIAL-BATCH-R2.json"
        self.receipt_schema_path = ROOT / "contracts/foundation/legacy-lifecycle-migration.v2.schema.json"
        self.policy = json.loads(self.policy_path.read_text(encoding="utf-8"))
        self.registry_bytes = self.registry_path.read_bytes()
        self.registry = json.loads(self.registry_bytes.decode("utf-8"))

    def run_policy(self, policy, registry=None):
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / "policy.json"
            policy_path.write_text(json.dumps(policy, ensure_ascii=False), encoding="utf-8")
            registry_path = self.registry_path
            if registry is not None:
                registry_path = Path(tmp) / "registry.json"
                registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return FLOW.validate(
                policy_path,
                self.schema_path,
                registry_path,
                now=datetime(2026, 7, 15, 12, 50, tzinfo=timezone.utc),
                repo_root=ROOT,
            )

    def run_batch_mutation(self, mutate, registry=None, registry_bytes=None):
        receipt = json.loads(self.receipt_path.read_text(encoding="utf-8"))
        mutate(receipt)
        schema = json.loads(self.receipt_schema_path.read_text(encoding="utf-8"))
        registration = copy.deepcopy(self.policy["migration"]["receipts"][1])
        registration["receipt_path"] = "tmp-receipt.json"
        registration["schema_path"] = "tmp-schema.json"
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            receipt_file = tmp_root / "receipt.json"
            schema_file = tmp_root / "schema.json"
            encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            receipt_file.write_bytes(encoded)
            schema_file.write_text(json.dumps(schema), encoding="utf-8")
            registration["receipt_sha256"] = hashlib.sha256(encoded).hexdigest()
            original = FLOW.safe_repo_file

            def resolve(_root, relative):
                if relative == "tmp-receipt.json":
                    return receipt_file
                if relative == "tmp-schema.json":
                    return schema_file
                return original(_root, relative)

            with mock.patch.object(FLOW, "safe_repo_file", side_effect=resolve):
                live_registry = registry if registry is not None else self.registry
                live_bytes = registry_bytes
                if live_bytes is None:
                    live_bytes = (json.dumps(live_registry, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
                return FLOW.validate_v2_receipt(
                    registration,
                    ROOT,
                    live_registry,
                    live_bytes,
                )[0]

    def test_v3_current_registry_and_both_registered_receipts_pass(self):
        self.assertEqual([], self.run_policy(self.policy))

    def test_v1_policy_and_receipt_bytes_remain_compatible(self):
        v2 = json.loads((ROOT / "contracts/foundation/delivery-flow-policy.v2.json").read_text(encoding="utf-8"))
        activity = ROOT / v2["migration"]["receipt_path"]
        self.assertEqual(v2["migration"]["receipt_sha256"], hashlib.sha256(activity.read_bytes()).hexdigest())
        old = DeliveryFlowPolicyTests()
        old.setUp()
        self.assertEqual([], old.run_validation())

    def test_rejects_duplicate_and_overlapping_receipt_registration(self):
        policy = copy.deepcopy(self.policy)
        policy["migration"]["receipts"].append(copy.deepcopy(policy["migration"]["receipts"][1]))
        errors = self.run_policy(policy)
        self.assertIn("DELIVERY_LEGACY_RECEIPT_REGISTRATION_DUPLICATE", errors)
        self.assertIn("DELIVERY_LEGACY_RECEIPT_ROW_OVERLAP", errors)

    def test_rejects_unregistered_version_and_arbitrary_receipt_substitution(self):
        policy = copy.deepcopy(self.policy)
        policy["migration"]["receipts"][1]["contract_version"] = "legacy-lifecycle-migration.v999"
        self.assertIn("DELIVERY_LEGACY_RECEIPT_VERSION_UNSUPPORTED", self.run_policy(policy))
        substituted = copy.deepcopy(self.policy)
        activity = substituted["migration"]["receipts"][0]
        batch = substituted["migration"]["receipts"][1]
        batch["receipt_path"] = activity["receipt_path"]
        batch["receipt_sha256"] = activity["receipt_sha256"]
        self.assertIn("DELIVERY_LEGACY_RECEIPT_REGISTRATION_MISMATCH", self.run_policy(substituted))

    def test_accepts_live_governance_updates_and_append_only_rows(self):
        registry = copy.deepcopy(self.registry)
        registry["work_items"][136]["status"] = "integrated"
        registry["work_items"][136]["allowed_paths"] = [
            "__released_no_write__/AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-RECEIPT-GENERALIZATION-R3"
        ]
        registry["work_items"][137]["status"] = "handoff-ready"
        registry["work_items"][137]["handoff_record"] = "docs/project-management/service-plaza/r12n-handoff.md"
        registry["work_items"][137]["next_checkpoint"] = "Independent R12-N handoff."
        template = copy.deepcopy(registry["work_items"][132])
        for number in range(3):
            appended = copy.deepcopy(template)
            appended["work_id"] = f"AIW-20260715-R31-APPEND-{number}"
            appended["title"] = f"R3.1 append-only governance row {number}"
            appended["workspace_path"] = f"C:/Users/shugo/Documents/worktrees/r31-append-{number}"
            appended["branch"] = f"codex/r31-append-{number}"
            appended["allowed_paths"] = [f"__r31_append__/{number}"]
            registry["work_items"].append(appended)
        self.assertEqual([], self.run_batch_mutation(lambda _receipt: None, registry=registry))

        globally_valid = copy.deepcopy(registry)
        globally_valid["work_items"][136] = copy.deepcopy(self.registry["work_items"][136])
        globally_valid["work_items"][137] = copy.deepcopy(self.registry["work_items"][137])
        globally_valid["work_items"][136]["migration_note"] += " R3.1 live-governance refresh."
        globally_valid["work_items"][137]["migration_note"] += " R3.1 supervision refresh."
        self.assertEqual([], self.run_policy(self.policy, registry=globally_valid))

    def test_rejects_false_applied_state(self):
        self.assertIn(
            "DELIVERY_LEGACY_RECEIPT_FALSE_AUTHORIZATION",
            self.run_batch_mutation(lambda receipt: receipt.update({"applied": True})),
        )

    def test_rejects_audit_row_field_drift(self):
        for index in (47, 88, 89, 90, 92, 132):
            with self.subTest(index=index):
                registry = copy.deepcopy(self.registry)
                registry["work_items"][index]["migration_note"] = "unauthorized audit row drift"
                self.assertIn(
                    "DELIVERY_LEGACY_AUDIT_ROW_DRIFT",
                    self.run_batch_mutation(lambda _receipt: None, registry=registry),
                )

    def test_rejects_historical_insert_delete_reorder_and_replacement(self):
        cases = {}
        inserted = copy.deepcopy(self.registry)
        inserted["work_items"].insert(10, copy.deepcopy(inserted["work_items"][-1]))
        cases["insert"] = inserted
        deleted = copy.deepcopy(self.registry)
        deleted["work_items"].pop(20)
        cases["delete"] = deleted
        reordered = copy.deepcopy(self.registry)
        reordered["work_items"][20], reordered["work_items"][21] = reordered["work_items"][21], reordered["work_items"][20]
        cases["reorder"] = reordered
        replaced = copy.deepcopy(self.registry)
        replaced["work_items"][20]["work_id"] = "AIW-REPLACED-HISTORICAL-ID"
        cases["replace"] = replaced
        duplicated_append = copy.deepcopy(self.registry)
        duplicated_append["work_items"].append(copy.deepcopy(duplicated_append["work_items"][20]))
        cases["duplicate-append"] = duplicated_append
        for label, registry in cases.items():
            with self.subTest(case=label):
                self.assertIn(
                    "DELIVERY_LEGACY_CURRENT_REGISTRY_HISTORY_INVALID",
                    self.run_batch_mutation(lambda _receipt: None, registry=registry),
                )

    def test_rejects_precondition_commit_path_and_sha_tampering(self):
        mutations = (
            lambda receipt: receipt["current_registry_precondition"].update({"commit": "0" * 40}),
            lambda receipt: receipt["current_registry_precondition"].update({"path": "README.md"}),
            lambda receipt: receipt["current_registry_precondition"].update({"sha256": "0" * 64}),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                self.assertIn(
                    "DELIVERY_LEGACY_CURRENT_REGISTRY_PRECONDITION_INVALID",
                    self.run_batch_mutation(mutate),
                )

    def test_rejects_audit_scope_omission_and_partial_atomic_group(self):
        self.assertIn(
            "DELIVERY_LEGACY_AUDIT_SCOPE_INVALID",
            self.run_batch_mutation(
                lambda receipt: receipt.__setitem__(
                    "audit_scope", [row for row in receipt["audit_scope"] if row["registry_index"] != 92]
                )
            ),
        )

        def drop_atomic_member(receipt):
            receipt["transitions"] = [row for row in receipt["transitions"] if row["registry_index"] != 132]
            canonical = "".join(
                f"{row['registry_index']}\t{row['work_id']}\t{row['from_status']}\t{row['to_status']}\n"
                for row in receipt["transitions"]
            )
            receipt["transition_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        errors = self.run_batch_mutation(drop_atomic_member)
        self.assertIn("DELIVERY_LEGACY_ATOMIC_GROUP_INVALID", errors)
        self.assertIn("DELIVERY_LEGACY_AUDIT_SCOPE_INVALID", errors)

    def test_rejects_commit_path_bytes_and_blob_substitution(self):
        def wrong_commit(receipt):
            target = next(row for row in receipt["evidence_files"] if row["path"].endswith("platform-registry-dispatch-r1-handoff.md"))
            target["authority_commit"] = "610ba65680123758a53badde0fa8dc0cf52e7f20"

        self.assertIn("DELIVERY_LEGACY_EVIDENCE_COMMIT_BYTES_INVALID", self.run_batch_mutation(wrong_commit))

        def wrong_blob(receipt):
            receipt["transitions"][0]["blob_equivalence"][0]["source_blob"] = "0" * 40

        self.assertIn("DELIVERY_LEGACY_BLOB_EQUIVALENCE_INVALID", self.run_batch_mutation(wrong_blob))

    def test_rejects_non_go_role_and_reviewed_at_acceptance(self):
        def non_go(receipt):
            receipt["transitions"][0]["projection_basis"]["accepted_verdict"] = "no-go"

        self.assertIn("DELIVERY_LEGACY_INDEPENDENT_ACCEPTANCE_INVALID", self.run_batch_mutation(non_go))

        def wrong_role(receipt):
            receipt["transitions"][0]["projection_basis"]["reviewer_role"] = "实施负责人"

        self.assertIn("DELIVERY_LEGACY_INDEPENDENT_ACCEPTANCE_INVALID", self.run_batch_mutation(wrong_role))

        def no_reviewed_at(receipt):
            receipt["transitions"][0]["projection_basis"]["reviewed_at"] = None

        self.assertIn("DELIVERY_LEGACY_INDEPENDENT_ACCEPTANCE_INVALID", self.run_batch_mutation(no_reviewed_at))

    def test_rejects_transition_and_projected_state_hash_tampering(self):
        self.assertIn(
            "DELIVERY_LEGACY_TRANSITION_HASH_INVALID",
            self.run_batch_mutation(lambda receipt: receipt.update({"transition_sha256": "0" * 64})),
        )
        self.assertIn(
            "DELIVERY_LEGACY_POST_STATES_HASH_INVALID",
            self.run_batch_mutation(lambda receipt: receipt.update({"post_effective_states_sha256": "0" * 64})),
        )


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

    def test_active_existing_non_git_repository_root_is_rejected(self):
        non_git_root = self.root / "existing-non-git-directory"
        non_git_root.mkdir()
        item = self.item("AIW-20260713-NON-GIT-ROOT", "active", non_git_root, "4" * 40)
        errors = self.validate([item])
        self.assertTrue(
            any(
                "does not exist as a commit" in error and "not a git repository" in error.lower()
                for error in errors
            ),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
