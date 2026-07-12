import copy
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class NovaPeopleToolsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load("nova-people-tools.v1.json")
        cls.contract_schema = load("nova-people-tools.v1.schema.json")
        cls.callback = load("nova-connection-callback.v1.json")
        cls.callback_schema = load("nova-connection-callback.v1.schema.json")
        cls.errors = load("nova-people-tool-errors.v1.json")
        cls.errors_schema = load("nova-people-tool-errors.v1.schema.json")
        cls.positive = load("fixtures/m2/positive-invocations.v1.json")
        cls.negative = load("fixtures/m2/negative-cases.v1.json")
        cls.tools = {item["tool_id"]: item for item in cls.contract["tools"]}
        cls.error_ids = {item["error_id"] for item in cls.errors["errors"]}

    def test_contracts_and_schemas_are_valid(self):
        for schema in (self.contract_schema, self.callback_schema, self.errors_schema):
            Draft202012Validator.check_schema(schema)
        Draft202012Validator(self.contract_schema).validate(self.contract)
        Draft202012Validator(self.callback_schema).validate(self.callback)
        Draft202012Validator(self.errors_schema).validate(self.errors)

    def test_exact_tool_set_and_callback_boundary(self):
        self.assertEqual(
            set(self.tools),
            {"member_search", "connection_draft", "connection_send", "connection_status"},
        )
        self.assertEqual(len(self.tools), len(self.contract["tools"]))
        self.assertNotIn("connection_result_callback", self.tools)
        self.assertFalse(self.callback["transport"]["public_or_model_tool"])
        self.assertEqual(self.callback["classification"], "server_to_server_callback")

    def test_server_identity_tenant_and_legacy_routes_fail_closed(self):
        self.assertEqual(self.contract["security"]["identity_source"], "trusted_server_context")
        self.assertEqual(self.contract["security"]["tenant_source"], "trusted_server_context")
        self.assertFalse(self.contract["security"]["request_may_supply_actor_or_tenant"])
        self.assertEqual(self.contract["canonical_dependency"]["current_status"], "pending")
        self.assertFalse(self.contract["executable"])
        forbidden = set(self.contract["canonical_dependency"]["forbidden_routes"])
        self.assertEqual(
            forbidden,
            {
                "POST /api/v1/network/introductions",
                "PUT /api/v1/network/introductions/{id}",
                "POST /api/v1/network/referral",
            },
        )
        for tool in self.tools.values():
            self.assertTrue(tool["transport"]["provider_operation"].startswith("people."))
            self.assertFalse(tool["transport"]["legacy_endpoint_allowed"])
            self.assertEqual(tool["tenant_source"], "trusted_server_context")
            self.assertFalse(tool["executable"])
            self.assertNotIn("actor", tool["input_schema"].get("properties", {}))
            self.assertNotIn("tenant_id", tool["input_schema"].get("properties", {}))

    def test_member_search_visibility_is_allowlisted(self):
        search = self.tools["member_search"]
        allowed = set(
            search["input_schema"]["properties"]["requested_field_ids"]["items"]["enum"]
        )
        forbidden = {"phone", "email", "government_id", "raw_health_text", "private_notes"}
        self.assertTrue(forbidden.isdisjoint(allowed))
        self.assertTrue(forbidden.issubset(set(search["redacted_fields"])))
        self.assertIn("server filters every result before model exposure", search["resource_policy"])

    def test_draft_has_no_external_effect_and_send_requires_confirmation(self):
        draft = self.tools["connection_draft"]
        send = self.tools["connection_send"]
        self.assertEqual(draft["classification"], "draft")
        self.assertIn("draft creation produces no external message", draft["resource_policy"])
        self.assertIn("disclosure_manifest", draft["output_schema"]["required"])
        self.assertEqual(send["classification"], "external_effect")
        self.assertEqual(
            send["input_schema"]["required"],
            ["draft_id", "draft_version", "confirmation_ticket"],
        )
        self.assertEqual(send["confirmation"]["policy"], "always")
        self.assertTrue(send["confirmation"]["ticket_required"])
        self.assertEqual(
            set(send["confirmation"]["binds"]),
            {
                "actor",
                "tenant",
                "action",
                "target",
                "draft_id",
                "draft_version",
                "disclosure_hash",
                "impact",
                "trace_id",
                "expires_at",
            },
        )
        self.assertTrue(send["idempotency"]["required"])
        self.assertEqual(send["idempotency"]["key_source"], "Idempotency-Key")
        self.assertEqual(send["idempotency"]["same_key_same_payload"], "safe_replay")
        self.assertEqual(send["idempotency"]["same_key_different_payload"], "conflict")

    def test_status_and_callback_responsibilities_are_bounded(self):
        status = self.tools["connection_status"]
        self.assertIn("actor is sender recipient or explicitly authorized operator", status["resource_policy"])
        self.assertEqual(self.callback["transport"]["tenant_source"], "trusted_server_context")
        self.assertFalse(self.callback["transport"]["body_may_override_server_identity_or_tenant"])
        self.assertEqual(
            self.callback["responsibility"]["canonical_state_owner"],
            "People Network module owner",
        )
        self.assertEqual(self.callback["responsibility"]["consumer_effect"], "append_only_task_event")
        self.assertFalse(self.callback["responsibility"]["callback_may_rewrite_canonical_state"])
        self.assertEqual(self.callback["idempotency"]["key"], "event_id")
        self.assertEqual(self.callback["recovery"]["delivery"], "at_least_once")
        self.assertTrue(self.callback["recovery"]["status_reconciliation_required"])

    def test_error_catalog_is_complete_and_referenced(self):
        self.assertEqual(len(self.errors["errors"]), 26)
        self.assertEqual(len(self.error_ids), 26)
        referenced = set(self.callback["error_ids"])
        for tool in self.tools.values():
            referenced.update(tool["error_ids"])
        referenced.update(
            case["expected_error_id"]
            for case in self.negative["cases"]
            if "expected_error_id" in case
        )
        self.assertTrue(referenced.issubset(self.error_ids))

    def test_positive_fixtures_validate_against_embedded_schemas(self):
        self.assertTrue(self.positive["synthetic_only"])
        self.assertEqual(
            {case["case_id"] for case in self.positive["cases"]},
            {f"NPM2-P{index:03d}" for index in range(1, 6)},
        )
        for case in self.positive["cases"]:
            if case["target"] == "connection_result_callback":
                Draft202012Validator(self.callback["event_schema"]).validate(case["input"])
                continue
            tool = self.tools[case["target"]]
            Draft202012Validator(tool["input_schema"]).validate(case["input"])
            Draft202012Validator(tool["output_schema"]).validate(case["output"])

    def test_negative_fixture_matrix_is_exact_and_safe_replay_is_explicit(self):
        self.assertTrue(self.negative["synthetic_only"])
        cases = {case["case_id"]: case for case in self.negative["cases"]}
        self.assertEqual(set(cases), {f"NPM2-N{index:03d}" for index in range(1, 20)})
        self.assertEqual(cases["NPM2-N019"]["expected_outcome"], "safe_replay")
        for case in cases.values():
            if "expected_error_id" in case:
                self.assertIn(case["expected_error_id"], self.error_ids)

    def test_mutations_that_weaken_authority_are_rejected(self):
        forged = copy.deepcopy(self.contract)
        forged["security"]["request_may_supply_actor_or_tenant"] = True
        with self.assertRaises(AssertionError):
            self._assert_authority_invariants(forged, self.callback)

        legacy = copy.deepcopy(self.contract)
        legacy["tools"][0]["transport"]["provider_operation"] = "POST /api/v1/network/introductions"
        with self.assertRaises(AssertionError):
            self._assert_authority_invariants(legacy, self.callback)

        weak_send = copy.deepcopy(self.contract)
        weak_send["tools"][2]["confirmation"]["ticket_required"] = False
        with self.assertRaises(AssertionError):
            self._assert_authority_invariants(weak_send, self.callback)

        public_callback = copy.deepcopy(self.callback)
        public_callback["transport"]["public_or_model_tool"] = True
        with self.assertRaises(AssertionError):
            self._assert_authority_invariants(self.contract, public_callback)

    def test_fixtures_contain_no_identity_or_secret_patterns(self):
        text = json.dumps([self.positive, self.negative], ensure_ascii=False)
        self.assertIsNone(re.search(r"1[3-9]\d{9}", text))
        self.assertIsNone(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text))
        self.assertNotRegex(text.lower(), r"bearer\s+[a-z0-9._-]+")
        self.assertNotIn("government_id", text)

    def _assert_authority_invariants(self, contract, callback):
        self.assertFalse(contract["security"]["request_may_supply_actor_or_tenant"])
        for tool in contract["tools"]:
            self.assertTrue(tool["transport"]["provider_operation"].startswith("people."))
            self.assertFalse(tool["transport"]["legacy_endpoint_allowed"])
        send = next(tool for tool in contract["tools"] if tool["tool_id"] == "connection_send")
        self.assertTrue(send["confirmation"]["ticket_required"])
        self.assertTrue(send["idempotency"]["required"])
        self.assertFalse(callback["transport"]["public_or_model_tool"])


if __name__ == "__main__":
    unittest.main()
