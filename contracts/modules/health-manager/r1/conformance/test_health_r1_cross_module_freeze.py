#!/usr/bin/env python3
"""Conformance tests for the Health Manager R1-C1 cross-module freeze."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "contracts/modules/health-manager/r1"
CONTRACT_PATH = MODULE / "cross-module-freeze.v1.json"
SCHEMA_PATH = MODULE / "cross-module-freeze.v1.schema.json"

EXPECTED_SOURCE_SHA256 = "fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012"
EXPECTED_ENTRY_IDS = {
    "health_record", "health_plan", "professional_help", "complex_case_coordination",
    "health_learning", "health_clubs", "dayi_health_center_services",
}
EXPECTED_AUTHORITY_IDS = {
    "health-manager", "learning-plaza", "club-alliance",
    "doctor-group-platform-directory", "regulated-medical-institution",
}
EXPECTED_PROTOCOL_ACTIONS = ["show_minimum_summary", "navigate_to_authority", "member_confirmed_return"]
EXPECTED_SIGNOFF_IDS = {"privacy-legal", "medical-quality", "platform-security", "operations"}
EXPECTED_SCENARIO_IDS = [f"R1-A{i:03d}" for i in range(1, 13)]
REQUIRED_AI_FORBIDDEN = {
    "diagnose", "prescribe", "change_medication", "impersonate_doctor", "promise_cure",
    "close_professional_risk", "close_emergency_risk", "recommend_unverified_practitioner",
    "change_medical_priority_for_payment",
}
REQUIRED_NO_GO = {
    "business_code", "api", "database", "real_identity", "real_health_data",
    "internet_medical_service", "diagnosis", "prescription", "medication_change",
    "charging", "payment", "test_server_deployment", "production", "irreversible_operation",
}
PHONE_PATTERN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
NATIONAL_ID_PATTERN = re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\w)")
JWT_PATTERN = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_semantics(contract: dict[str, Any]) -> str | None:
    if contract.get("source", {}).get("sha256") != EXPECTED_SOURCE_SHA256:
        return "HMR1_SOURCE_HASH_DRIFT"
    if contract.get("synthetic_only") is not True or contract.get("executable") is not False:
        return "HMR1_EXECUTION_PREMATURE"

    architecture = contract.get("information_architecture", {})
    entry_ids = [item.get("entry_id") for item in architecture.get("entrypoints", [])]
    if len(entry_ids) != 7 or len(set(entry_ids)) != 7 or set(entry_ids) != EXPECTED_ENTRY_IDS:
        return "HMR1_ENTRYPOINT_SET_INVALID"
    journeys = architecture.get("journeys", [])
    if [item.get("journey_id") for item in journeys] != ["vertical_health_service", "horizontal_health_participation"]:
        return "HMR1_JOURNEY_ORDER_INVALID"

    boundaries = contract.get("authority_boundaries", [])
    boundary_ids = [item.get("authority_id") for item in boundaries]
    if len(boundary_ids) != 5 or len(set(boundary_ids)) != 5 or set(boundary_ids) != EXPECTED_AUTHORITY_IDS:
        return "HMR1_AUTHORITY_SET_INVALID"
    learning = next((item for item in boundaries if item.get("authority_id") == "learning-plaza"), {})
    clubs = next((item for item in boundaries if item.get("authority_id") == "club-alliance"), {})
    health = next((item for item in boundaries if item.get("authority_id") == "health-manager"), {})
    if "learning_progress" not in learning.get("owns", []) or "club_membership" not in clubs.get("owns", []):
        return "HMR1_AUTHORITY_OWNERSHIP_DRIFT"
    if "learning_progress" in health.get("owns", []) or "club_membership" in health.get("owns", []):
        return "HMR1_CROSS_MODULE_OWNERSHIP_CAPTURE"

    protocol = contract.get("cross_module_protocol", {})
    steps = protocol.get("steps", [])
    if [step.get("step") for step in steps] != [1, 2, 3] or [step.get("action") for step in steps] != EXPECTED_PROTOCOL_ACTIONS:
        return "HMR1_PROTOCOL_ORDER_INVALID"
    if "no_shared_database_write" not in steps[1].get("requirements", []):
        return "HMR1_DIRECT_WRITE_NOT_BLOCKED"
    return_requirements = set(steps[2].get("requirements", []))
    if not {"explicit_member_confirmation", "provenance", "source_version", "responsible_actor", "target_review_before_recording"}.issubset(return_requirements):
        return "HMR1_RETURN_CONFIRMATION_INCOMPLETE"
    required_prohibitions = {
        "cross_module_direct_database_write", "automatic_learning_completion_to_health_record",
        "automatic_club_activity_to_health_record", "health_manager_membership_mutation",
        "club_full_health_profile_read", "unconfirmed_return",
    }
    if not required_prohibitions.issubset(set(protocol.get("prohibited", []))):
        return "HMR1_PROTOCOL_PROHIBITION_MISSING"

    if not REQUIRED_AI_FORBIDDEN.issubset(set(contract.get("ai_boundary", {}).get("forbidden", []))):
        return "HMR1_AI_BOUNDARY_MISSING"

    signoffs = contract.get("pending_signoffs", [])
    signoff_ids = [item.get("signoff_id") for item in signoffs]
    if len(signoff_ids) != 4 or set(signoff_ids) != EXPECTED_SIGNOFF_IDS:
        return "HMR1_SIGNOFF_SET_INVALID"
    if any(item.get("status") != "pending-with-owner" or item.get("executable") is not False or not item.get("owner") for item in signoffs):
        return "HMR1_SIGNOFF_PREMATURE"

    scenario_ids = [item.get("scenario_id") for item in contract.get("acceptance_scenarios", [])]
    if scenario_ids != EXPECTED_SCENARIO_IDS:
        return "HMR1_SCENARIO_SET_INVALID"
    if not REQUIRED_NO_GO.issubset(set(contract.get("no_go", []))):
        return "HMR1_NO_GO_MISSING"

    serialized = json.dumps(contract, ensure_ascii=False)
    if PHONE_PATTERN.search(serialized) or NATIONAL_ID_PATTERN.search(serialized) or JWT_PATTERN.search(serialized) or "Bearer " in serialized:
        return "HMR1_SENSITIVE_DATA_PATTERN"
    return None


class HealthR1CrossModuleFreezeTest(unittest.TestCase):
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
        self.assertEqual("HMR1_SOURCE_HASH_DRIFT", validate_semantics(mutated))

    def test_04_negative_missing_entrypoint(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["information_architecture"]["entrypoints"].pop()
        self.assertEqual("HMR1_ENTRYPOINT_SET_INVALID", validate_semantics(mutated))

    def test_05_negative_authority_capture(self) -> None:
        mutated = copy.deepcopy(self.contract)
        health = next(item for item in mutated["authority_boundaries"] if item["authority_id"] == "health-manager")
        health["owns"].append("learning_progress")
        self.assertEqual("HMR1_CROSS_MODULE_OWNERSHIP_CAPTURE", validate_semantics(mutated))

    def test_06_negative_protocol_direct_write(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["cross_module_protocol"]["steps"][1]["requirements"].remove("no_shared_database_write")
        self.assertEqual("HMR1_DIRECT_WRITE_NOT_BLOCKED", validate_semantics(mutated))

    def test_07_negative_unconfirmed_return(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["cross_module_protocol"]["steps"][2]["requirements"].remove("explicit_member_confirmation")
        self.assertEqual("HMR1_RETURN_CONFIRMATION_INCOMPLETE", validate_semantics(mutated))

    def test_08_negative_automatic_writeback(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["cross_module_protocol"]["prohibited"].remove("automatic_learning_completion_to_health_record")
        self.assertEqual("HMR1_PROTOCOL_PROHIBITION_MISSING", validate_semantics(mutated))

    def test_09_negative_ai_diagnosis(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["ai_boundary"]["forbidden"].remove("diagnose")
        self.assertEqual("HMR1_AI_BOUNDARY_MISSING", validate_semantics(mutated))

    def test_10_negative_premature_signoff(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["pending_signoffs"][0].update({"status": "accepted", "executable": True})
        self.assertEqual("HMR1_SIGNOFF_PREMATURE", validate_semantics(mutated))

    def test_11_negative_contract_executable(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["executable"] = True
        self.assertEqual("HMR1_EXECUTION_PREMATURE", validate_semantics(mutated))

    def test_12_negative_no_go_removed(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["no_go"].remove("real_health_data")
        self.assertEqual("HMR1_NO_GO_MISSING", validate_semantics(mutated))

    def test_13_negative_sensitive_pattern(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["does_not_block"].append("synthetic marker 13800138000")
        self.assertEqual("HMR1_SENSITIVE_DATA_PATTERN", validate_semantics(mutated))


if __name__ == "__main__":
    unittest.main(verbosity=2)
