#!/usr/bin/env python3
"""Conformance tests for the synthetic-only Health Manager R3-C1 contract."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "contracts/modules/health-manager/r3"
CONTRACT_PATH = MODULE / "learning-club-entry.v1.json"
SCHEMA_PATH = MODULE / "learning-club-entry.v1.schema.json"
SOURCE_SHA256 = "fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012"
AUTHORITY_ORDER = ["learning-plaza", "club-alliance"]
SUMMARY_FIELDS = {
    "learning-plaza": {"currently_learning", "recently_completed", "recommended_learning", "resource_reference"},
    "club-alliance": {"visible_club_card", "member_join_status", "join_mode", "safety_notice"},
}
ROUTES = {"learning-plaza": "/services/learning-plaza", "club-alliance": "/services/club-alliance"}
RETURN_FIELDS = {
    "source_authority", "source_reference", "source_version", "member_confirmation_id",
    "confirmed_at", "responsible_actor_id", "target_review_status",
}
AI_FORBIDDEN = {
    "diagnose", "prescribe", "change_medication", "impersonate_doctor",
    "promise_health_improvement", "auto_confirm_return", "close_professional_risk",
    "close_emergency_risk", "expand_authorization_scope",
}
NO_GO = {
    "business_code", "shared_runtime", "api", "database", "cross_module_direct_write",
    "real_identity", "real_member", "real_health_data", "internet_medical_service",
    "diagnosis", "prescription", "medication_change", "charging", "payment",
    "test_server_deployment", "production", "irreversible_operation",
}
PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
NATIONAL_ID = re.compile(r"(?<![0-9a-fA-F])\d{17}[0-9Xx](?![0-9a-fA-F])")
JWT = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_semantics(contract: dict[str, Any]) -> str | None:
    if contract.get("source", {}).get("sha256") != SOURCE_SHA256:
        return "HMR3_SOURCE_HASH_DRIFT"
    if contract.get("synthetic_only") is not True or contract.get("executable") is not False:
        return "HMR3_EXECUTION_PREMATURE"

    authorities = contract.get("authority_snapshots", [])
    if [item.get("authority_id") for item in authorities] != AUTHORITY_ORDER:
        return "HMR3_AUTHORITY_SET_INVALID"
    for authority in authorities:
        authority_id = authority["authority_id"]
        if set(authority.get("minimum_summary_fields", [])) != SUMMARY_FIELDS[authority_id]:
            return "HMR3_SUMMARY_ALLOWLIST_INVALID"
        if authority.get("canonical_route") != ROUTES[authority_id]:
            return "HMR3_CANONICAL_ROUTE_INVALID"
        if authority.get("health_manager_permissions") != ["read_authorized_minimum_summary", "navigate_to_authority"]:
            return "HMR3_AUTHORITY_CAPTURE"

    access = contract.get("summary_access_policy", {})
    if any(access.get(key) is not True for key in (
        "authorization_required", "data_minimization_required", "source_authority_required", "source_version_required"
    )):
        return "HMR3_SUMMARY_GUARD_MISSING"
    if access.get("member_scope") != "self_only":
        return "HMR3_MEMBER_SCOPE_INVALID"

    navigation = contract.get("navigation_policy", {})
    if navigation.get("authority_retains_write_ownership") is not True:
        return "HMR3_AUTHORITY_CAPTURE"
    if navigation.get("no_shared_database_write") is not True:
        return "HMR3_DIRECT_WRITE_NOT_BLOCKED"
    if not {"route_spoofing", "cross_module_database_write", "health_manager_state_replica_as_authority"}.issubset(set(navigation.get("prohibited", []))):
        return "HMR3_NAVIGATION_GUARD_MISSING"

    returned = contract.get("member_confirmed_return", {})
    if returned.get("explicit_member_confirmation_required") is not True:
        return "HMR3_MEMBER_CONFIRMATION_MISSING"
    if returned.get("target_review_required") is not True or returned.get("target_record_class") != "health_management_record_candidate":
        return "HMR3_TARGET_REVIEW_MISSING"
    if not RETURN_FIELDS.issubset(set(returned.get("required_fields", []))):
        return "HMR3_RETURN_TRACEABILITY_INCOMPLETE"
    if not {"automatic_return", "unconfirmed_return", "direct_health_record_write", "medical_record_promotion"}.issubset(set(returned.get("prohibited", []))):
        return "HMR3_AUTOMATIC_RETURN_NOT_BLOCKED"

    isolation = contract.get("module_isolation", {})
    if isolation.get("shared_database_tables") is not False or isolation.get("health_manager_owns_learning_or_club_state") is not False:
        return "HMR3_MODULE_ISOLATION_BROKEN"
    if isolation.get("club_full_health_profile_default_access") is not False:
        return "HMR3_FULL_HEALTH_PROFILE_EXPOSED"
    if not AI_FORBIDDEN.issubset(set(contract.get("ai_boundary", {}).get("forbidden", []))):
        return "HMR3_AI_BOUNDARY_MISSING"

    signoffs = contract.get("pending_signoffs", [])
    if len(signoffs) != 4 or any(item.get("status") != "pending-with-owner" or item.get("executable") is not False for item in signoffs):
        return "HMR3_SIGNOFF_PREMATURE"
    if not NO_GO.issubset(set(contract.get("no_go", []))):
        return "HMR3_NO_GO_MISSING"

    serialized = json.dumps(contract, ensure_ascii=False)
    if PHONE.search(serialized) or NATIONAL_ID.search(serialized) or JWT.search(serialized) or "Bearer " in serialized:
        return "HMR3_SENSITIVE_DATA_PATTERN"
    return None


class HealthR3LearningClubEntryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load_json(CONTRACT_PATH)
        cls.schema = load_json(SCHEMA_PATH)

    def test_01_schema_instance(self) -> None:
        Draft202012Validator(self.schema).validate(self.contract)

    def test_02_semantic_baseline(self) -> None:
        self.assertIsNone(validate_semantics(copy.deepcopy(self.contract)))

    def test_03_negative_source_hash_drift(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["source"]["sha256"] = "0" * 64
        self.assertEqual("HMR3_SOURCE_HASH_DRIFT", validate_semantics(mutated))

    def test_04_negative_learning_summary_expansion(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["authority_snapshots"][0]["minimum_summary_fields"].append("full_learning_note")
        self.assertEqual("HMR3_SUMMARY_ALLOWLIST_INVALID", validate_semantics(mutated))

    def test_05_negative_club_summary_expansion(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["authority_snapshots"][1]["minimum_summary_fields"].append("full_member_roster")
        self.assertEqual("HMR3_SUMMARY_ALLOWLIST_INVALID", validate_semantics(mutated))

    def test_06_negative_missing_authorization(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["summary_access_policy"]["authorization_required"] = False
        self.assertEqual("HMR3_SUMMARY_GUARD_MISSING", validate_semantics(mutated))

    def test_07_negative_route_spoofing(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["authority_snapshots"][0]["canonical_route"] = "/services/health-manager/learning"
        self.assertEqual("HMR3_CANONICAL_ROUTE_INVALID", validate_semantics(mutated))

    def test_08_negative_direct_database_write(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["navigation_policy"]["no_shared_database_write"] = False
        self.assertEqual("HMR3_DIRECT_WRITE_NOT_BLOCKED", validate_semantics(mutated))

    def test_09_negative_authority_capture(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["navigation_policy"]["authority_retains_write_ownership"] = False
        self.assertEqual("HMR3_AUTHORITY_CAPTURE", validate_semantics(mutated))

    def test_10_negative_automatic_return(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["member_confirmed_return"]["prohibited"].remove("automatic_return")
        self.assertEqual("HMR3_AUTOMATIC_RETURN_NOT_BLOCKED", validate_semantics(mutated))

    def test_11_negative_unconfirmed_return(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["member_confirmed_return"]["explicit_member_confirmation_required"] = False
        self.assertEqual("HMR3_MEMBER_CONFIRMATION_MISSING", validate_semantics(mutated))

    def test_12_negative_missing_return_version(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["member_confirmed_return"]["required_fields"].remove("source_version")
        self.assertEqual("HMR3_RETURN_TRACEABILITY_INCOMPLETE", validate_semantics(mutated))

    def test_13_negative_club_full_profile_access(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["module_isolation"]["club_full_health_profile_default_access"] = True
        self.assertEqual("HMR3_FULL_HEALTH_PROFILE_EXPOSED", validate_semantics(mutated))

    def test_14_negative_ai_diagnosis(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["ai_boundary"]["forbidden"].remove("diagnose")
        self.assertEqual("HMR3_AI_BOUNDARY_MISSING", validate_semantics(mutated))

    def test_15_negative_premature_signoff(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["pending_signoffs"][0].update({"status": "accepted", "executable": True})
        self.assertEqual("HMR3_SIGNOFF_PREMATURE", validate_semantics(mutated))

    def test_16_negative_real_data_authorization(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["no_go"].remove("real_health_data")
        self.assertEqual("HMR3_NO_GO_MISSING", validate_semantics(mutated))

    def test_17_negative_sensitive_pattern(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["does_not_block"].append("synthetic marker 13800138000")
        self.assertEqual("HMR3_SENSITIVE_DATA_PATTERN", validate_semantics(mutated))


if __name__ == "__main__":
    unittest.main(verbosity=2)
