#!/usr/bin/env python3
"""Conformance tests for the formal Dayi Health Hall M0-C1 scope/IA freeze."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[6]
MODULE = ROOT / "contracts/modules/health-manager/dayi-health-hall/m0"
CONTRACT_PATH = MODULE / "scope-ia.v1.json"
SCHEMA_PATH = MODULE / "scope-ia.v1.schema.json"

EXPECTED_SOURCES = {
    "scope-pause-decision": "1130fee3c432cfd3abadb2b5a06c1f496c5cd36a265168fb813287d3fbb0ab47",
    "cross-module-requirement-supplement": "fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012",
    "historical-r1-boundary": "5b93845530b702f930c2257d60fec1e33f4925a7410ccd578d5d2fd98667e5ea",
}
EXPECTED_LAYERS = ["platform", "region", "hall"]
EXPECTED_PARENTS = {"platform": None, "region": "platform", "hall": "region"}
EXPECTED_PAGES = [
    "hall-home", "hall-discovery", "hall-detail", "hall-lifecycle-status",
    "member-hall-relationship", "learning-and-club-navigation", "scope-and-safety",
]
EXPECTED_STATES = {
    "draft", "submitted", "under_review", "approved", "onboarding",
    "active", "suspended", "exiting", "exited", "rejected",
}
EXPECTED_TRANSITIONS = {
    ("draft", "submitted", "applicant"),
    ("submitted", "under_review", "platform_reviewer"),
    ("under_review", "approved", "platform_reviewer"),
    ("under_review", "rejected", "platform_reviewer"),
    ("rejected", "draft", "applicant"),
    ("approved", "onboarding", "hall_owner"),
    ("onboarding", "active", "platform_reviewer"),
    ("active", "suspended", "regional_operator"),
    ("suspended", "active", "platform_reviewer"),
    ("active", "exiting", "hall_owner"),
    ("suspended", "exiting", "hall_owner"),
    ("exiting", "exited", "platform_reviewer"),
}
EXPECTED_ROLES = {
    "platform_reviewer", "regional_operator", "hall_owner", "hall_staff", "member", "auditor",
}
EXPECTED_PROTOCOL = ["show_minimum_summary", "navigate_to_authority", "member_confirmed_return"]
EXPECTED_AUTHORITIES = {"learning": "learning-plaza", "club": "club-alliance"}
REQUIRED_AI_FORBIDDEN = {
    "diagnose", "treat", "prescribe", "change_medication", "recommend_doctor",
    "provide_real_consultation", "impersonate_doctor", "promise_outcome",
    "close_professional_risk", "close_emergency_risk",
}
REQUIRED_NO_GO = {
    "business_runtime", "api", "database", "real_identity", "real_health_data",
    "medical_record", "diagnosis", "treatment", "prescription", "medication_change",
    "doctor_recommendation", "real_consultation", "second_opinion", "case_solicitation",
    "multidisciplinary_consultation", "charging", "payment", "test_server_deployment",
    "production", "irreversible_operation",
}
FORBIDDEN_UI_ACTIONS = {
    "online_consultation", "doctor_recommendation", "second_opinion", "prescription",
    "medication_advice", "case_solicitation", "multidisciplinary_consultation",
    "treatment_promise", "real_health_profile", "payment_action",
}
PHONE_PATTERN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
NATIONAL_ID_PATTERN = re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\w)")
JWT_PATTERN = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_semantics(contract: dict[str, Any]) -> str | None:
    sources = contract.get("source_bindings", [])
    source_map = {item.get("source_id"): item.get("sha256") for item in sources}
    if source_map != EXPECTED_SOURCES:
        return "DHHM0_SOURCE_BINDING_DRIFT"

    if contract.get("synthetic_only") is not True or contract.get("executable") is not False:
        return "DHHM0_EXECUTION_PREMATURE"
    flags = contract.get("runtime_flags", {})
    if set(flags) != {
        "real_identity_enabled", "real_health_data_enabled", "medical_capabilities_enabled",
        "payment_enabled", "deployment_enabled", "production_enabled",
    } or any(value is not False for value in flags.values()):
        return "DHHM0_RUNTIME_FLAG_OPEN"

    positioning = contract.get("positioning", {})
    if positioning.get("is_medical_institution") is not False or positioning.get("grants_medical_authority") is not False:
        return "DHHM0_MEDICAL_POSITIONING"
    if "不提供诊断或处方" not in positioning.get("safety_notice", ""):
        return "DHHM0_SAFETY_NOTICE_MISSING"

    layers = contract.get("organization_layers", [])
    layer_ids = [item.get("layer_id") for item in layers]
    if layer_ids != EXPECTED_LAYERS:
        return "DHHM0_ORGANIZATION_ORDER_INVALID"
    if any(item.get("parent_layer_id") != EXPECTED_PARENTS[item["layer_id"]] for item in layers):
        return "DHHM0_ORGANIZATION_PARENT_INVALID"
    if any("provide_medical_service" not in item.get("prohibitions", []) for item in layers[:2]):
        return "DHHM0_ORGANIZATION_MEDICAL_BOUNDARY_MISSING"
    hall = layers[2]
    if "impersonate_medical_institution" not in hall.get("prohibitions", []):
        return "DHHM0_ORGANIZATION_MEDICAL_BOUNDARY_MISSING"

    architecture = contract.get("information_architecture", {})
    pages = architecture.get("pages", [])
    if [page.get("page_id") for page in pages] != EXPECTED_PAGES:
        return "DHHM0_PAGE_SET_INVALID"
    if any(not str(page.get("route", "")).startswith("/services/dayi-health-hall") for page in pages):
        return "DHHM0_ROUTE_AUTHORITY_INVALID"
    member_pages = [page for page in pages if page.get("data_class") == "member_synthetic"]
    if any(not {"unauthenticated", "access_denied", "unavailable_fail_closed"}.issubset(page.get("required_states", [])) for page in member_pages):
        return "DHHM0_MEMBER_PAGE_FAIL_CLOSED_MISSING"
    rules = architecture.get("global_state_rules", {})
    if rules.get("unauthorized_hides_member_summary") is not True or rules.get("error_disables_mutating_actions") is not True:
        return "DHHM0_PAGE_FAIL_CLOSED_RULE_MISSING"
    if rules.get("medical_actions_visible") is not False or rules.get("real_health_fields_visible") is not False:
        return "DHHM0_FORBIDDEN_UI_VISIBLE"
    page_actions = {action for page in pages for action in page.get("allowed_actions", [])}
    if page_actions & FORBIDDEN_UI_ACTIONS:
        return "DHHM0_FORBIDDEN_UI_VISIBLE"

    lifecycle = contract.get("hall_lifecycle", {})
    if set(lifecycle.get("states", [])) != EXPECTED_STATES:
        return "DHHM0_LIFECYCLE_STATE_SET_INVALID"
    transitions = lifecycle.get("transitions", [])
    transition_set = {(item.get("from"), item.get("to"), item.get("actor")) for item in transitions}
    if transition_set != EXPECTED_TRANSITIONS or any(item.get("audit_required") is not True for item in transitions):
        return "DHHM0_LIFECYCLE_TRANSITION_SET_INVALID"
    if any(lifecycle.get(key) is not True for key in [
        "skip_review_forbidden", "self_approval_forbidden",
        "reactivation_requires_platform_review", "exited_requires_new_application",
    ]):
        return "DHHM0_LIFECYCLE_GUARD_MISSING"

    roles = contract.get("role_boundaries", [])
    role_map = {item.get("role_id"): item for item in roles}
    if set(role_map) != EXPECTED_ROLES:
        return "DHHM0_ROLE_SET_INVALID"
    if "confirm_for_member" not in role_map["hall_staff"].get("prohibitions", []):
        return "DHHM0_STAFF_CONFIRMATION_BOUNDARY_MISSING"
    if "mutate_business_state" not in role_map["auditor"].get("prohibitions", []):
        return "DHHM0_AUDITOR_MUTATION_BOUNDARY_MISSING"

    relationship = contract.get("member_relationship", {})
    if relationship.get("member_confirmation_required") is not True:
        return "DHHM0_MEMBER_CONFIRMATION_MISSING"
    if relationship.get("automatic_confirmation") is not False or relationship.get("hall_staff_may_change_consent") is not False:
        return "DHHM0_MEMBER_CONFIRMATION_BYPASS"
    if relationship.get("exited_relationship_auto_reactivation") is not False or relationship.get("source_and_version_required") is not True:
        return "DHHM0_RELATIONSHIP_TRACE_OR_EXIT_INVALID"
    actions = {item.get("action") for item in relationship.get("member_actions", [])}
    if actions != {"confirm_candidate", "request_correction", "request_exit"}:
        return "DHHM0_MEMBER_ACTION_SET_INVALID"

    protocols = contract.get("cross_module_protocols", [])
    protocol_map = {item.get("target_id"): item for item in protocols}
    if set(protocol_map) != set(EXPECTED_AUTHORITIES):
        return "DHHM0_PROTOCOL_TARGET_SET_INVALID"
    for target, authority in EXPECTED_AUTHORITIES.items():
        protocol = protocol_map[target]
        if protocol.get("authority_module") != authority or protocol.get("protocol") != EXPECTED_PROTOCOL:
            return "DHHM0_PROTOCOL_AUTHORITY_OR_ORDER_INVALID"
        if protocol.get("direct_database_write") is not False:
            return "DHHM0_CROSS_MODULE_DIRECT_WRITE"
        if protocol.get("member_confirmation_required") is not True or protocol.get("return_requires_provenance_and_version") is not True:
            return "DHHM0_RETURN_CONFIRMATION_INCOMPLETE"

    services = contract.get("non_medical_service_catalog", [])
    if len(services) != 5 or len({item.get("service_id") for item in services}) != 5:
        return "DHHM0_SERVICE_CATALOG_INVALID"
    if any(item.get("medical_service") is not False or item.get("payment_available") is not False for item in services):
        return "DHHM0_SERVICE_MEDICAL_OR_PAYMENT_ENABLED"

    ai = contract.get("ai_boundary", {})
    if not REQUIRED_AI_FORBIDDEN.issubset(set(ai.get("forbidden", []))):
        return "DHHM0_AI_BOUNDARY_MISSING"
    if ai.get("professional_or_emergency_risk_must_remain_open") is not True:
        return "DHHM0_AI_RISK_CLOSURE_ENABLED"

    authorizations = contract.get("pending_authorizations", [])
    if len(authorizations) != 4 or any("m0_synthetic_contract" not in item.get("does_not_block", []) for item in authorizations):
        return "DHHM0_PENDING_BLOCKS_SYNTHETIC"
    medical = next((item for item in authorizations if item.get("authorization_id") == "medical-reactivation"), {})
    if medical.get("status") != "paused-by-highest-owner":
        return "DHHM0_MEDICAL_PAUSE_DRIFT"

    cases = contract.get("acceptance_cases", [])
    if [item.get("case_id") for item in cases] != [f"M0-A{i:03d}" for i in range(1, 17)]:
        return "DHHM0_ACCEPTANCE_CASE_SET_INVALID"
    if sum(item.get("polarity") == "positive" for item in cases) != 6:
        return "DHHM0_ACCEPTANCE_POLARITY_INVALID"
    if not REQUIRED_NO_GO.issubset(set(contract.get("no_go", []))):
        return "DHHM0_NO_GO_MISSING"

    scrubbed = copy.deepcopy(contract)
    scrubbed["source_bindings"] = []
    serialized = json.dumps(scrubbed, ensure_ascii=False)
    if PHONE_PATTERN.search(serialized) or NATIONAL_ID_PATTERN.search(serialized) or JWT_PATTERN.search(serialized) or "Bearer " in serialized:
        return "DHHM0_SENSITIVE_DATA_PATTERN"
    return None


class DayiHealthHallM0ScopeIATest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load_json(CONTRACT_PATH)
        cls.schema = load_json(SCHEMA_PATH)

    def test_01_schema_instance(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        Draft202012Validator(self.schema).validate(self.contract)

    def test_02_semantic_baseline(self) -> None:
        self.assertIsNone(validate_semantics(copy.deepcopy(self.contract)))

    def test_03_negative_source_hash_drift(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["source_bindings"][0]["sha256"] = "0" * 64
        self.assertEqual("DHHM0_SOURCE_BINDING_DRIFT", validate_semantics(mutated))

    def test_04_negative_executable(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["executable"] = True
        self.assertEqual("DHHM0_EXECUTION_PREMATURE", validate_semantics(mutated))

    def test_05_negative_runtime_flag(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["runtime_flags"]["medical_capabilities_enabled"] = True
        self.assertEqual("DHHM0_RUNTIME_FLAG_OPEN", validate_semantics(mutated))

    def test_06_negative_medical_positioning(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["positioning"]["is_medical_institution"] = True
        self.assertEqual("DHHM0_MEDICAL_POSITIONING", validate_semantics(mutated))

    def test_07_negative_organization_parent(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["organization_layers"][2]["parent_layer_id"] = "platform"
        self.assertEqual("DHHM0_ORGANIZATION_PARENT_INVALID", validate_semantics(mutated))

    def test_08_negative_missing_page(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["information_architecture"]["pages"].pop()
        self.assertEqual("DHHM0_PAGE_SET_INVALID", validate_semantics(mutated))

    def test_09_negative_member_page_not_fail_closed(self) -> None:
        mutated = copy.deepcopy(self.contract)
        page = next(item for item in mutated["information_architecture"]["pages"] if item["page_id"] == "member-hall-relationship")
        page["required_states"].remove("access_denied")
        self.assertEqual("DHHM0_MEMBER_PAGE_FAIL_CLOSED_MISSING", validate_semantics(mutated))

    def test_10_negative_forbidden_ui_visible(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["information_architecture"]["pages"][0]["allowed_actions"].append("doctor_recommendation")
        self.assertEqual("DHHM0_FORBIDDEN_UI_VISIBLE", validate_semantics(mutated))

    def test_11_negative_lifecycle_skip(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["hall_lifecycle"]["transitions"][0] = {"from": "submitted", "to": "active", "actor": "applicant", "audit_required": True}
        self.assertEqual("DHHM0_LIFECYCLE_TRANSITION_SET_INVALID", validate_semantics(mutated))

    def test_12_negative_lifecycle_guard(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["hall_lifecycle"]["self_approval_forbidden"] = False
        self.assertEqual("DHHM0_LIFECYCLE_GUARD_MISSING", validate_semantics(mutated))

    def test_13_negative_staff_confirms_member(self) -> None:
        mutated = copy.deepcopy(self.contract)
        staff = next(item for item in mutated["role_boundaries"] if item["role_id"] == "hall_staff")
        staff["prohibitions"].remove("confirm_for_member")
        self.assertEqual("DHHM0_STAFF_CONFIRMATION_BOUNDARY_MISSING", validate_semantics(mutated))

    def test_14_negative_automatic_confirmation(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["member_relationship"]["automatic_confirmation"] = True
        self.assertEqual("DHHM0_MEMBER_CONFIRMATION_BYPASS", validate_semantics(mutated))

    def test_15_negative_exit_auto_reactivation(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["member_relationship"]["exited_relationship_auto_reactivation"] = True
        self.assertEqual("DHHM0_RELATIONSHIP_TRACE_OR_EXIT_INVALID", validate_semantics(mutated))

    def test_16_negative_cross_module_write(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["cross_module_protocols"][0]["direct_database_write"] = True
        self.assertEqual("DHHM0_CROSS_MODULE_DIRECT_WRITE", validate_semantics(mutated))

    def test_17_negative_unconfirmed_return(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["cross_module_protocols"][1]["member_confirmation_required"] = False
        self.assertEqual("DHHM0_RETURN_CONFIRMATION_INCOMPLETE", validate_semantics(mutated))

    def test_18_negative_medical_service(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["non_medical_service_catalog"][0]["medical_service"] = True
        self.assertEqual("DHHM0_SERVICE_MEDICAL_OR_PAYMENT_ENABLED", validate_semantics(mutated))

    def test_19_negative_ai_diagnosis(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["ai_boundary"]["forbidden"].remove("diagnose")
        self.assertEqual("DHHM0_AI_BOUNDARY_MISSING", validate_semantics(mutated))

    def test_20_negative_pending_blocks_synthetic(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["pending_authorizations"][0]["does_not_block"] = []
        self.assertEqual("DHHM0_PENDING_BLOCKS_SYNTHETIC", validate_semantics(mutated))

    def test_21_negative_no_go_removed(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["no_go"].remove("real_health_data")
        self.assertEqual("DHHM0_NO_GO_MISSING", validate_semantics(mutated))

    def test_22_negative_sensitive_pattern(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["positioning"]["safety_notice"] += " 13800138000"
        self.assertEqual("DHHM0_SENSITIVE_DATA_PATTERN", validate_semantics(mutated))


if __name__ == "__main__":
    unittest.main(verbosity=2)
