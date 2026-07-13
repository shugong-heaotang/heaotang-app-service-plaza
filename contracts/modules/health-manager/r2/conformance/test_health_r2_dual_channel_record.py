#!/usr/bin/env python3
"""Conformance tests for the synthetic-only Health Manager R2-C1 contract."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "contracts/modules/health-manager/r2"
CONTRACT_PATH = MODULE / "dual-channel-record.v1.json"
SCHEMA_PATH = MODULE / "dual-channel-record.v1.schema.json"
SOURCE_SHA256 = "fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012"
CHANNELS = ["member_self_service", "dayi_center_assisted"]
MEMBER_ONLY = {"identity_confirmation", "consent_grant", "candidate_final_confirmation"}
PROVENANCE = {
    "source_type", "source_reference", "recorded_by_actor_id", "recorded_by_actor_role",
    "recorded_at", "member_confirmation_status", "source_version",
}
AI_FORBIDDEN = {
    "verify_real_identity", "grant_consent", "final_confirm_candidate", "delete_original_material",
    "diagnose", "prescribe", "change_medication", "impersonate_doctor",
    "close_professional_or_emergency_risk",
}
NO_GO = {
    "business_code", "api", "database", "real_identity", "real_member", "real_health_data",
    "proxy_onboarding", "internet_medical_service", "diagnosis", "prescription",
    "medication_change", "charging", "payment", "test_server_deployment", "production",
    "irreversible_operation",
}
PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
NATIONAL_ID = re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\w)")
JWT = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_semantics(contract: dict[str, Any]) -> str | None:
    if contract.get("source", {}).get("sha256") != SOURCE_SHA256:
        return "HMR2_SOURCE_HASH_DRIFT"
    if contract.get("synthetic_only") is not True or contract.get("executable") is not False:
        return "HMR2_EXECUTION_PREMATURE"

    authority = contract.get("record_authority", {})
    required_invariants = {
        "one_platform_member_one_master_health_record",
        "member_remains_record_subject_and_data_rights_holder",
        "channel_does_not_create_second_identity_or_master_record",
        "assisting_center_never_becomes_record_owner",
    }
    if authority.get("subject") != "member" or authority.get("record_key") != "unified_health_record_id":
        return "HMR2_RECORD_AUTHORITY_INVALID"
    if not required_invariants.issubset(set(authority.get("invariants", []))):
        return "HMR2_UNIFIED_RECORD_INVARIANT_MISSING"

    channels = contract.get("onboarding_channels", [])
    if [item.get("channel_id") for item in channels] != CHANNELS:
        return "HMR2_CHANNEL_SET_INVALID"
    if any(not MEMBER_ONLY.issubset(set(item.get("member_only_actions", []))) for item in channels):
        return "HMR2_MEMBER_ONLY_ACTION_MISSING"
    assisted = channels[1]
    if assisted.get("initiator") != "authorized_center_staff":
        return "HMR2_ASSISTED_INITIATOR_INVALID"
    assisted_prohibited = set(assisted.get("prohibited", []))
    if not {"staff_grants_consent_for_member", "staff_final_confirms_for_member", "automatic_doctor_relationship"}.issubset(assisted_prohibited):
        return "HMR2_ASSISTED_BOUNDARY_MISSING"

    item_policy = contract.get("record_item_policy", {})
    if not PROVENANCE.issubset(set(item_policy.get("required_provenance", []))):
        return "HMR2_PROVENANCE_INCOMPLETE"
    if item_policy.get("candidate_rule") != "unconfirmed_material_remains_candidate_and_cannot_become_member_confirmed":
        return "HMR2_UNCONFIRMED_PROMOTION_ALLOWED"
    if item_policy.get("class_separation_required") is not True or len(item_policy.get("record_classes", [])) != 4:
        return "HMR2_RECORD_CLASS_CONFLATION"

    correction = contract.get("correction_policy", {})
    if correction.get("mode") != "append_only_correction" or correction.get("preserve_original") is not True:
        return "HMR2_CORRECTION_NOT_APPEND_ONLY"
    if not {"delete_original", "rewrite_source", "erase_audit_history"}.issubset(set(correction.get("prohibited", []))):
        return "HMR2_CORRECTION_HISTORY_ERASURE_ALLOWED"

    authorization = contract.get("authorization_policy", {})
    if authorization.get("authority") != "member" or authorization.get("versioned") is not True:
        return "HMR2_AUTHORIZATION_AUTHORITY_INVALID"
    if not {"staff_self_authorization", "implicit_consent", "unversioned_scope_change"}.issubset(set(authorization.get("prohibited", []))):
        return "HMR2_AUTHORIZATION_GUARD_MISSING"

    audit = contract.get("audit_policy", {})
    if audit.get("append_only") is not True:
        return "HMR2_AUDIT_NOT_APPEND_ONLY"
    if not {"actor_id", "actor_role", "occurred_at", "record_version", "source_reference", "authorization_version"}.issubset(set(audit.get("required_fields", []))):
        return "HMR2_AUDIT_FIELD_MISSING"

    relationship = contract.get("doctor_relationship", {})
    if relationship.get("default") != "not_established" or relationship.get("assisted_onboarding_effect") != "no_automatic_relationship":
        return "HMR2_DOCTOR_RELATIONSHIP_AUTO_CREATED"
    if not AI_FORBIDDEN.issubset(set(contract.get("ai_boundary", {}).get("forbidden", []))):
        return "HMR2_AI_BOUNDARY_MISSING"

    signoffs = contract.get("pending_signoffs", [])
    if len(signoffs) != 4 or any(item.get("status") != "pending-with-owner" or item.get("executable") is not False for item in signoffs):
        return "HMR2_SIGNOFF_PREMATURE"
    if not NO_GO.issubset(set(contract.get("no_go", []))):
        return "HMR2_NO_GO_MISSING"
    if any("proxy" in step for channel in channels for step in channel.get("steps", [])):
        return "HMR2_PROXY_ONBOARDING_ENABLED"

    serialized = json.dumps(contract, ensure_ascii=False)
    if PHONE.search(serialized) or NATIONAL_ID.search(serialized) or JWT.search(serialized) or "Bearer " in serialized:
        return "HMR2_SENSITIVE_DATA_PATTERN"
    return None


class HealthR2DualChannelRecordTest(unittest.TestCase):
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
        self.assertEqual("HMR2_SOURCE_HASH_DRIFT", validate_semantics(mutated))

    def test_04_negative_second_master_record(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["record_authority"]["invariants"].remove("one_platform_member_one_master_health_record")
        self.assertEqual("HMR2_UNIFIED_RECORD_INVARIANT_MISSING", validate_semantics(mutated))

    def test_05_negative_staff_consent(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["onboarding_channels"][1]["prohibited"].remove("staff_grants_consent_for_member")
        self.assertEqual("HMR2_ASSISTED_BOUNDARY_MISSING", validate_semantics(mutated))

    def test_06_negative_unconfirmed_promotion(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["record_item_policy"]["candidate_rule"] = "staff_may_promote_candidate"
        self.assertEqual("HMR2_UNCONFIRMED_PROMOTION_ALLOWED", validate_semantics(mutated))

    def test_07_negative_missing_provenance(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["record_item_policy"]["required_provenance"].remove("source_version")
        self.assertEqual("HMR2_PROVENANCE_INCOMPLETE", validate_semantics(mutated))

    def test_08_negative_record_class_conflation(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["record_item_policy"]["class_separation_required"] = False
        self.assertEqual("HMR2_RECORD_CLASS_CONFLATION", validate_semantics(mutated))

    def test_09_negative_original_deletion(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["correction_policy"]["preserve_original"] = False
        self.assertEqual("HMR2_CORRECTION_NOT_APPEND_ONLY", validate_semantics(mutated))

    def test_10_negative_unversioned_authorization(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["authorization_policy"]["versioned"] = False
        self.assertEqual("HMR2_AUTHORIZATION_AUTHORITY_INVALID", validate_semantics(mutated))

    def test_11_negative_missing_audit_actor(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["audit_policy"]["required_fields"].remove("actor_id")
        self.assertEqual("HMR2_AUDIT_FIELD_MISSING", validate_semantics(mutated))

    def test_12_negative_auto_doctor_relationship(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["doctor_relationship"]["assisted_onboarding_effect"] = "established"
        self.assertEqual("HMR2_DOCTOR_RELATIONSHIP_AUTO_CREATED", validate_semantics(mutated))

    def test_13_negative_ai_final_confirmation(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["ai_boundary"]["forbidden"].remove("final_confirm_candidate")
        self.assertEqual("HMR2_AI_BOUNDARY_MISSING", validate_semantics(mutated))

    def test_14_negative_proxy_onboarding(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["onboarding_channels"][0]["steps"].append("proxy_confirms_identity")
        self.assertEqual("HMR2_PROXY_ONBOARDING_ENABLED", validate_semantics(mutated))

    def test_15_negative_real_data_authorization(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["no_go"].remove("real_health_data")
        self.assertEqual("HMR2_NO_GO_MISSING", validate_semantics(mutated))

    def test_16_negative_sensitive_pattern(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["does_not_block"].append("synthetic marker 13800138000")
        self.assertEqual("HMR2_SENSITIVE_DATA_PATTERN", validate_semantics(mutated))


if __name__ == "__main__":
    unittest.main(verbosity=2)
