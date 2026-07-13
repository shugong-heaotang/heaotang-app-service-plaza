import copy
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError


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
        cls.negative_schema = load("fixtures/m2/negative-cases.v1.schema.json")
        cls.tools = {item["tool_id"]: item for item in cls.contract["tools"]}
        cls.positive_by_id = {case["case_id"]: case for case in cls.positive["cases"]}
        cls.error_by_id = {item["error_id"]: item for item in cls.errors["errors"]}
        cls.error_ids = set(cls.error_by_id)

    def test_contracts_and_schemas_are_valid(self):
        for schema in (
            self.contract_schema,
            self.callback_schema,
            self.errors_schema,
            self.negative_schema,
        ):
            Draft202012Validator.check_schema(schema)
        Draft202012Validator(self.contract_schema).validate(self.contract)
        Draft202012Validator(self.callback_schema).validate(self.callback)
        Draft202012Validator(self.errors_schema).validate(self.errors)
        Draft202012Validator(self.negative_schema).validate(self.negative)

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
        self.assertEqual(
            set(self.contract["canonical_dependency"]["forbidden_routes"]),
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

    def test_member_search_output_is_strict_and_request_conditioned(self):
        search = self.tools["member_search"]
        item_schema = search["output_schema"]["properties"]["items"]["items"]
        self.assertFalse(item_schema["additionalProperties"])
        allowed = set(
            search["input_schema"]["properties"]["requested_field_ids"]["items"]["enum"]
        )
        forbidden = {"phone", "email", "government_id", "raw_health_text", "private_notes"}
        self.assertTrue(forbidden.isdisjoint(allowed))
        self.assertTrue(forbidden.issubset(set(search["redacted_fields"])))
        case = self.positive_by_id["NPM2-P001"]
        requested = set(case["input"]["requested_field_ids"])
        always = {"candidate_ref", "visibility_policy_version"}
        for item in case["output"]["items"]:
            self.assertTrue(set(item).issubset(requested | always))
        for field in forbidden:
            invalid = copy.deepcopy(case["output"])
            invalid["items"][0][field] = "synthetic-forbidden-placeholder"
            with self.assertRaises(ValidationError):
                Draft202012Validator(search["output_schema"]).validate(invalid)

    def test_draft_preview_manifest_and_status_summary_are_strict(self):
        draft = self.tools["connection_draft"]
        status = self.tools["connection_status"]
        self.assertFalse(
            draft["output_schema"]["properties"]["preview"]["additionalProperties"]
        )
        manifest_enum = set(
            draft["output_schema"]["properties"]["disclosure_manifest"]["items"]["enum"]
        )
        self.assertNotIn("phone", manifest_enum)
        self.assertNotIn("private_notes", manifest_enum)
        draft_case = self.positive_by_id["NPM2-P002"]
        self.assertEqual(
            draft_case["output"]["preview"]["field_ids"],
            draft_case["output"]["disclosure_manifest"],
        )
        self.assertTrue(
            set(draft_case["output"]["disclosure_manifest"]).issubset(
                set(draft_case["input"]["disclosure_field_ids"])
            )
        )
        summary_schema = status["output_schema"]["properties"]["result_summary"]
        strict_object = summary_schema["oneOf"][1]
        self.assertFalse(strict_object["additionalProperties"])
        self.assertEqual(set(strict_object["properties"]), {"result_code", "note_present"})

    def test_send_requires_bound_confirmation_and_idempotency(self):
        draft = self.tools["connection_draft"]
        send = self.tools["connection_send"]
        self.assertEqual(draft["classification"], "draft")
        self.assertIn("draft creation produces no external message", draft["resource_policy"])
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
        self.assertIn(
            "actor is sender recipient or explicitly authorized operator",
            status["resource_policy"],
        )
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

    def test_error_catalog_is_complete_referenced_and_target_compatible(self):
        self.assertEqual(len(self.errors["errors"]), 26)
        self.assertEqual(len(self.error_ids), 26)
        referenced = set(self.callback["error_ids"])
        for tool in self.tools.values():
            referenced.update(tool["error_ids"])
        for case in self.negative["cases"]:
            error_id = case["expected"].get("error_id")
            if not error_id:
                continue
            referenced.add(error_id)
            applies_to = set(self.error_by_id[error_id]["applies_to"])
            expected_target = (
                "member_search" if case["target"] == "contract" else case["target"]
            )
            self.assertIn(expected_target, applies_to, case["case_id"])
        self.assertTrue(referenced.issubset(self.error_ids))

    def test_positive_fixtures_validate_against_embedded_schemas(self):
        self.assertTrue(self.positive["synthetic_only"])
        self.assertEqual(
            set(self.positive_by_id),
            {f"NPM2-P{index:03d}" for index in range(1, 6)},
        )
        for case in self.positive["cases"]:
            if case["target"] == "connection_result_callback":
                Draft202012Validator(self.callback["event_schema"]).validate(case["input"])
                continue
            tool = self.tools[case["target"]]
            Draft202012Validator(tool["input_schema"]).validate(case["input"])
            Draft202012Validator(tool["output_schema"]).validate(case["output"])

    def test_all_negative_fixtures_execute_and_return_exact_result(self):
        cases = {case["case_id"]: case for case in self.negative["cases"]}
        self.assertEqual(set(cases), {f"NPM2-N{index:03d}" for index in range(1, 28)})
        for case in cases.values():
            self.assertEqual(self._evaluate_negative_case(case), case["expected"], case["case_id"])

    def test_unknown_target_unknown_rule_and_wrong_error_are_rejected(self):
        unknown_target = copy.deepcopy(self.negative)
        unknown_target["cases"][0]["target"] = "unknown_tool"
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.negative_schema).validate(unknown_target)

        unknown_rule = copy.deepcopy(self.negative["cases"][0])
        unknown_rule["rule_id"] = "unknown_rule"
        with self.assertRaises(AssertionError):
            self._evaluate_negative_case(unknown_rule)

        wrong_error = copy.deepcopy(self.negative["cases"][0])
        wrong_error["expected"]["error_id"] = "NOVA_TOOL_FORBIDDEN"
        self.assertNotEqual(self._evaluate_negative_case(wrong_error), wrong_error["expected"])

        wrong_target = copy.deepcopy(self.negative["cases"][0])
        wrong_target["target"] = "connection_send"
        with self.assertRaises(AssertionError):
            self._evaluate_negative_case(wrong_target)

    def test_authority_mutations_are_rejected(self):
        forged = copy.deepcopy(self.contract)
        forged["security"]["request_may_supply_actor_or_tenant"] = True
        with self.assertRaises(AssertionError):
            self._assert_authority_invariants(forged, self.callback)

        legacy = copy.deepcopy(self.contract)
        legacy["tools"][0]["transport"]["provider_operation"] = (
            "POST /api/v1/network/introductions"
        )
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

    def test_fixtures_contain_no_real_identity_or_secret_patterns(self):
        text = json.dumps([self.positive, self.negative], ensure_ascii=False)
        self.assertIsNone(re.search(r"1[3-9]\d{9}", text))
        self.assertIsNone(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text))
        self.assertNotRegex(text.lower(), r"bearer\s+[a-z0-9._-]+")
        self.assertNotIn("-----BEGIN " + "PRIVATE KEY-----", text)

    def _evaluate_negative_case(self, case):
        rules = {
            "request_actor_forbidden": ("member_search", "NOVA_TOOL_CONTEXT_MISSING"),
            "request_tenant_mismatch": ("member_search", "NOVA_TOOL_TENANT_MISMATCH"),
            "candidate_tenant_mismatch": ("member_search", "NOVA_TOOL_TENANT_MISMATCH"),
            "requested_field_forbidden": ("member_search", "NOVA_MEMBER_FIELD_FORBIDDEN"),
            "target_opted_out": ("connection_draft", "NOVA_CONNECTION_TARGET_UNAVAILABLE"),
            "confirmation_target_mismatch": ("connection_send", "NOVA_CONFIRMATION_BINDING_MISMATCH"),
            "draft_version_stale": ("connection_send", "NOVA_CONNECTION_DRAFT_STALE"),
            "confirmation_missing": ("connection_send", "NOVA_CONFIRMATION_REQUIRED"),
            "confirmation_expired": ("connection_send", "NOVA_CONFIRMATION_EXPIRED"),
            "idempotency_missing": ("connection_send", "NOVA_IDEMPOTENCY_KEY_REQUIRED"),
            "idempotency_payload_conflict": ("connection_send", "NOVA_IDEMPOTENCY_PAYLOAD_CONFLICT"),
            "resource_actor_forbidden": ("connection_status", "NOVA_TOOL_RESOURCE_FORBIDDEN"),
            "callback_principal_forbidden": ("connection_result_callback", "NOVA_CALLBACK_UNAUTHORIZED"),
            "callback_tenant_mismatch": ("connection_result_callback", "NOVA_CALLBACK_TENANT_MISMATCH"),
            "callback_payload_conflict": ("connection_result_callback", "NOVA_CALLBACK_EVENT_CONFLICT"),
            "callback_transition_invalid": ("connection_result_callback", "NOVA_CONNECTION_STATE_CONFLICT"),
            "legacy_route_mapping": ("contract", "NOVA_TOOL_FORBIDDEN"),
            "output_phone_forbidden": ("member_search", "NOVA_MEMBER_FIELD_FORBIDDEN"),
            "callback_safe_replay": ("connection_result_callback", None),
            "output_email_forbidden": ("member_search", "NOVA_MEMBER_FIELD_FORBIDDEN"),
            "output_government_id_forbidden": ("member_search", "NOVA_MEMBER_FIELD_FORBIDDEN"),
            "status_private_notes_forbidden": ("connection_status", "NOVA_MEMBER_FIELD_FORBIDDEN"),
            "status_raw_health_forbidden": ("connection_status", "NOVA_MEMBER_FIELD_FORBIDDEN"),
            "draft_manifest_field_forbidden": ("connection_draft", "NOVA_MEMBER_FIELD_FORBIDDEN"),
            "draft_preview_field_forbidden": ("connection_draft", "NOVA_MEMBER_FIELD_FORBIDDEN"),
            "output_unrequested_field": ("member_search", "NOVA_MEMBER_FIELD_FORBIDDEN"),
            "draft_unrequested_field": ("connection_draft", "NOVA_MEMBER_FIELD_FORBIDDEN"),
        }
        self.assertIn(case["rule_id"], rules)
        expected_target, error_id = rules[case["rule_id"]]
        self.assertEqual(case["target"], expected_target)
        mutated = self._mutated_base(case)
        self._assert_rule_condition(case["rule_id"], mutated)
        if error_id is None:
            return {"result": "safe_replay"}
        return {"result": "reject", "error_id": error_id}

    def _mutated_base(self, case):
        if case["base_case_ref"] == "contract":
            base = copy.deepcopy(self.contract)
        else:
            self.assertIn(case["base_case_ref"], self.positive_by_id)
            base = copy.deepcopy(self.positive_by_id[case["base_case_ref"]])
            self.assertEqual(base["target"], case["target"])
        path = case["mutation"]["path"].split(".")
        cursor = base
        index = 0
        while index < len(path) - 1:
            part = path[index]
            if part == "tools" and isinstance(cursor, dict) and isinstance(cursor.get(part), list):
                index += 1
                tool_id = path[index]
                cursor = next(tool for tool in cursor["tools"] if tool["tool_id"] == tool_id)
            elif isinstance(cursor, list):
                cursor = cursor[int(part)]
            else:
                cursor = cursor[part]
            index += 1
        leaf = path[-1]
        if case["mutation"]["operation"] == "set":
            if isinstance(cursor, list):
                cursor[int(leaf)] = case["mutation"]["value"]
            else:
                cursor[leaf] = case["mutation"]["value"]
        else:
            self.assertIn(leaf, cursor)
            del cursor[leaf]
        return base

    def _assert_rule_condition(self, rule, value):
        context = value.get("trusted_context", {})
        input_value = value.get("input", {})
        output = value.get("output", {})
        if rule == "request_actor_forbidden":
            self.assertIn("actor_ref", input_value)
        elif rule == "request_tenant_mismatch":
            self.assertNotEqual(input_value["tenant_ref"], context["tenant_ref"])
        elif rule == "candidate_tenant_mismatch":
            self.assertNotEqual(context["candidate_tenant_ref"], context["tenant_ref"])
        elif rule == "requested_field_forbidden":
            self.assertIn("phone", input_value["requested_field_ids"])
        elif rule == "target_opted_out":
            self.assertFalse(context["target_introduction_allowed"])
        elif rule == "confirmation_target_mismatch":
            self.assertNotEqual(context["confirmed_target_ref"], context["draft_target_ref"])
        elif rule == "draft_version_stale":
            self.assertNotEqual(context["current_draft_version"], input_value["draft_version"])
        elif rule == "confirmation_missing":
            self.assertNotIn("confirmation_ticket", input_value)
        elif rule == "confirmation_expired":
            self.assertFalse(context["confirmation_valid"])
        elif rule == "idempotency_missing":
            self.assertNotIn("idempotency_key_ref", context)
        elif rule == "idempotency_payload_conflict":
            self.assertNotEqual(context["previous_payload_hash"], context["current_payload_hash"])
        elif rule == "resource_actor_forbidden":
            self.assertFalse(context["actor_is_participant_or_operator"])
        elif rule == "callback_principal_forbidden":
            self.assertNotEqual(context["server_principal_role"], "people_connection_outbox")
        elif rule == "callback_tenant_mismatch":
            self.assertNotEqual(context["callback_tenant_ref"], context["tenant_ref"])
        elif rule == "callback_payload_conflict":
            self.assertNotEqual(context["previous_payload_hash"], input_value["payload_hash"])
        elif rule == "callback_transition_invalid":
            self.assertEqual(context["current_status"], "canceled")
            self.assertEqual(input_value["event_type"], "request_accepted")
        elif rule == "legacy_route_mapping":
            tool = next(item for item in value["tools"] if item["tool_id"] == "member_search")
            self.assertFalse(tool["transport"]["provider_operation"].startswith("people."))
        elif rule in {
            "output_phone_forbidden",
            "output_email_forbidden",
            "output_government_id_forbidden",
        }:
            with self.assertRaises(ValidationError):
                Draft202012Validator(self.tools["member_search"]["output_schema"]).validate(output)
        elif rule in {"status_private_notes_forbidden", "status_raw_health_forbidden"}:
            with self.assertRaises(ValidationError):
                Draft202012Validator(self.tools["connection_status"]["output_schema"]).validate(output)
        elif rule in {"draft_manifest_field_forbidden", "draft_preview_field_forbidden"}:
            with self.assertRaises(ValidationError):
                Draft202012Validator(self.tools["connection_draft"]["output_schema"]).validate(output)
        elif rule == "output_unrequested_field":
            allowed = set(input_value["requested_field_ids"]) | {
                "candidate_ref",
                "visibility_policy_version",
            }
            self.assertFalse(set(output["items"][0]).issubset(allowed))
        elif rule == "draft_unrequested_field":
            self.assertFalse(
                set(output["disclosure_manifest"]).issubset(
                    set(input_value["disclosure_field_ids"])
                )
            )
        elif rule == "callback_safe_replay":
            self.assertEqual(context["previous_payload_hash"], input_value["payload_hash"])
        else:
            self.fail(f"unhandled rule: {rule}")

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
