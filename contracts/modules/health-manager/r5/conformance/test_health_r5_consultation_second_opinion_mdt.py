#!/usr/bin/env python3
"""Conformance tests for the synthetic-only Health Manager R5-C1 contract."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "contracts/modules/health-manager/r5"
CONTRACT_PATH = MODULE / "consultation-second-opinion-mdt.v1.json"
SCHEMA_PATH = MODULE / "consultation-second-opinion-mdt.v1.schema.json"
SOURCE_SHA256 = "fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012"
REFERRAL_FIELDS = {
    "request_reference", "request_type", "applicant_reference", "applicant_authority_role",
    "authorization_reference", "authorization_status", "primary_request", "source_record_references",
    "source_provenance", "source_versions", "missing_information", "responsible_coordinator",
    "submitted_at", "package_version",
}
EXPERT_FIELDS = {
    "expert_reference", "qualification_evidence_references", "practice_institution_reference",
    "practice_scope", "service_mode", "required_materials", "conflict_disclosure",
    "availability_status", "accepted_at",
}
AUDIT_EVENTS = {
    "request_submitted", "authorization_verified", "summary_generated", "human_intake_reviewed",
    "triage_decided", "expert_invited", "conflict_reviewed", "expert_accepted_or_declined",
    "responsible_physician_or_mdt_assigned", "opinion_recorded", "follow_up_arranged",
    "service_relationship_changed",
}
AUDIT_FIELDS = {
    "event_reference", "event_type", "actor_reference", "actor_role", "occurred_at",
    "source_reference", "source_version", "policy_version", "correlation_reference",
}
AI_FORBIDDEN = {
    "diagnose", "prescribe", "change_medication", "impersonate_doctor", "promise_outcome",
    "close_professional_risk", "close_emergency_risk", "approve_intake",
    "publish_identity_or_full_record", "invite_unverified_expert", "create_qualification_or_specialty",
    "hide_conflict_of_interest", "assign_responsible_physician", "form_medical_record",
    "merge_or_replace_medical_opinion", "choose_final_medical_conclusion", "authorize_charging_or_payment",
}
NO_GO = {
    "business_code", "shared_runtime", "api", "database", "real_doctor_data", "real_identity",
    "real_member", "real_health_data", "internet_medical_service", "diagnosis", "prescription",
    "medication_change", "doctor_impersonation", "outcome_promise", "public_case_record",
    "open_case_grabbing", "doctor_bidding", "cure_bounty", "outcome_based_payment", "charging",
    "payment", "test_server_deployment", "production", "irreversible_operation",
}
PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
NATIONAL_ID = re.compile(r"(?<![0-9a-fA-F])\d{17}[0-9Xx](?![0-9a-fA-F])")
JWT = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_semantics(contract: dict[str, Any]) -> str | None:
    if contract.get("source", {}).get("sha256") != SOURCE_SHA256:
        return "HMR5_SOURCE_HASH_DRIFT"
    if contract.get("synthetic_only") is not True or contract.get("executable") is not False:
        return "HMR5_EXECUTION_PREMATURE"

    referral = contract.get("referral_package", {})
    if not REFERRAL_FIELDS.issubset(set(referral.get("required_fields", []))):
        return "HMR5_REFERRAL_FIELDS_INCOMPLETE"
    if referral.get("accepted_applicant_authority_roles") != ["member_self", "verified_legal_representative"]:
        return "HMR5_APPLICANT_AUTHORITY_INVALID"
    if referral.get("authorization_required") is not True or referral.get("accepted_authorization_statuses") != ["active"]:
        return "HMR5_AUTHORIZATION_NOT_FAIL_CLOSED"
    if referral.get("source_references_only") is not True or referral.get("ai_output_is_diagnosis") is not False:
        return "HMR5_AI_SUMMARY_BOUNDARY_INVALID"

    triage = contract.get("human_intake_and_triage", {})
    if triage.get("initial_review_required") is not True or triage.get("reviewer_identity_required") is not True:
        return "HMR5_HUMAN_INTAKE_BYPASS"
    if triage.get("emergency_or_professional_risk_action") != "stop_online_flow_and_route_to_offline_medical_institution":
        return "HMR5_EMERGENCY_TRIAGE_INVALID"
    if triage.get("online_unsuitable_action") != "route_to_offline_medical_institution":
        return "HMR5_ONLINE_UNSUITABLE_ROUTE_INVALID"
    if any(triage.get(key) is not False for key in ("ai_may_close_professional_risk", "ai_may_close_emergency_risk", "ai_may_approve_intake")):
        return "HMR5_AI_RISK_OR_INTAKE_CLOSURE"

    solicitation = contract.get("expert_solicitation", {})
    if solicitation.get("mode") != "directed_verified_expert_pool_only":
        return "HMR5_EXPERT_SOLICITATION_MODE_INVALID"
    if solicitation.get("public_case_board_allowed") is not False or solicitation.get("open_claim_or_grab_allowed") is not False:
        return "HMR5_PUBLIC_OR_GRAB_MODE_ALLOWED"
    for key in ("verified_identity_required", "qualification_and_license_required", "practice_scope_match_required", "service_mode_authorized_required", "conflict_of_interest_disclosure_required", "conflict_review_required"):
        if solicitation.get(key) is not True:
            return "HMR5_EXPERT_GATE_MISSING"
    if not EXPERT_FIELDS.issubset(set(solicitation.get("acceptance_fields", []))):
        return "HMR5_EXPERT_ACCEPTANCE_INCOMPLETE"

    care = contract.get("responsible_care_governance", {})
    for key in ("responsible_physician_or_mdt_required", "responsible_physician_verified", "mdt_member_identity_and_role_required", "mdt_member_scope_match_required", "verified_medical_institution_required"):
        if care.get(key) is not True:
            return "HMR5_RESPONSIBLE_CARE_GATE_MISSING"
    if care.get("formal_diagnosis_or_treatment_owner") != "qualified_medical_institution":
        return "HMR5_MEDICAL_INSTITUTION_AUTHORITY_INVALID"
    if care.get("health_manager_may_form_medical_record") is not False or care.get("health_venue_may_form_medical_record") is not False:
        return "HMR5_NON_MEDICAL_RECORD_OWNER"

    opinion = contract.get("second_opinion_governance", {})
    for key in ("independent_reviewer_required", "independent_qualification_and_scope_required", "original_opinion_immutable", "second_opinion_preserved_as_separate_version", "disagreement_preserved", "responsible_human_review_required"):
        if opinion.get(key) is not True:
            return "HMR5_SECOND_OPINION_INTEGRITY_MISSING"
    if opinion.get("ai_may_merge_or_replace_opinions") is not False or opinion.get("ai_may_choose_final_medical_conclusion") is not False:
        return "HMR5_AI_OPINION_OVERRIDE"

    audit = contract.get("audit_trail", {})
    if not AUDIT_EVENTS.issubset(set(audit.get("required_events", []))) or not AUDIT_FIELDS.issubset(set(audit.get("required_fields_per_event", []))):
        return "HMR5_AUDIT_TRAIL_INCOMPLETE"
    if audit.get("original_opinion_and_source_immutable") is not True or audit.get("corrections_append_new_version") is not True:
        return "HMR5_AUDIT_IMMUTABILITY_MISSING"
    if audit.get("real_amount_authorized") is not False or audit.get("charging_or_payment_authorized") is not False:
        return "HMR5_FEE_AUTHORIZATION_PREMATURE"

    prohibited = contract.get("prohibited_modes", {})
    if any(value is not False for value in prohibited.values()):
        return "HMR5_PROHIBITED_MODE_ENABLED"
    if not AI_FORBIDDEN.issubset(set(contract.get("ai_boundary", {}).get("forbidden", []))):
        return "HMR5_AI_BOUNDARY_MISSING"
    signoffs = contract.get("pending_signoffs", [])
    if len(signoffs) != 5 or any(item.get("status") != "pending-with-owner" or item.get("executable") is not False for item in signoffs):
        return "HMR5_SIGNOFF_PREMATURE"
    if not NO_GO.issubset(set(contract.get("no_go", []))):
        return "HMR5_NO_GO_MISSING"

    serialized = json.dumps(contract, ensure_ascii=False)
    if PHONE.search(serialized) or NATIONAL_ID.search(serialized) or JWT.search(serialized) or "Bearer " in serialized:
        return "HMR5_SENSITIVE_DATA_PATTERN"
    return None


class HealthR5ConsultationSecondOpinionMdtTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load_json(CONTRACT_PATH)
        cls.schema = load_json(SCHEMA_PATH)

    def test_01_schema_instance(self) -> None:
        Draft202012Validator(self.schema).validate(self.contract)

    def test_02_semantic_baseline(self) -> None:
        self.assertIsNone(validate_semantics(copy.deepcopy(self.contract)))

    def mutate(self, path: list[str], value: Any, expected: str) -> None:
        mutated = copy.deepcopy(self.contract)
        target = mutated
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        self.assertEqual(expected, validate_semantics(mutated))

    def test_03_negative_source_hash_drift(self) -> None:
        self.mutate(["source", "sha256"], "0" * 64, "HMR5_SOURCE_HASH_DRIFT")

    def test_04_negative_referral_field_missing(self) -> None:
        mutated = copy.deepcopy(self.contract); mutated["referral_package"]["required_fields"].remove("authorization_reference")
        self.assertEqual("HMR5_REFERRAL_FIELDS_INCOMPLETE", validate_semantics(mutated))

    def test_05_negative_unverified_applicant_authority(self) -> None:
        self.mutate(["referral_package", "accepted_applicant_authority_roles"], ["member_self", "unverified_helper"], "HMR5_APPLICANT_AUTHORITY_INVALID")

    def test_06_negative_authorization_not_required(self) -> None:
        self.mutate(["referral_package", "authorization_required"], False, "HMR5_AUTHORIZATION_NOT_FAIL_CLOSED")

    def test_07_negative_ai_summary_as_diagnosis(self) -> None:
        self.mutate(["referral_package", "ai_output_is_diagnosis"], True, "HMR5_AI_SUMMARY_BOUNDARY_INVALID")

    def test_08_negative_human_intake_bypass(self) -> None:
        self.mutate(["human_intake_and_triage", "initial_review_required"], False, "HMR5_HUMAN_INTAKE_BYPASS")

    def test_09_negative_emergency_flow_continues_online(self) -> None:
        self.mutate(["human_intake_and_triage", "emergency_or_professional_risk_action"], "continue_online", "HMR5_EMERGENCY_TRIAGE_INVALID")

    def test_10_negative_ai_closes_risk(self) -> None:
        self.mutate(["human_intake_and_triage", "ai_may_close_emergency_risk"], True, "HMR5_AI_RISK_OR_INTAKE_CLOSURE")

    def test_11_negative_public_case_board(self) -> None:
        self.mutate(["expert_solicitation", "public_case_board_allowed"], True, "HMR5_PUBLIC_OR_GRAB_MODE_ALLOWED")

    def test_12_negative_unverified_expert(self) -> None:
        self.mutate(["expert_solicitation", "qualification_and_license_required"], False, "HMR5_EXPERT_GATE_MISSING")

    def test_13_negative_conflict_not_reviewed(self) -> None:
        self.mutate(["expert_solicitation", "conflict_review_required"], False, "HMR5_EXPERT_GATE_MISSING")

    def test_14_negative_no_responsible_physician_or_mdt(self) -> None:
        self.mutate(["responsible_care_governance", "responsible_physician_or_mdt_required"], False, "HMR5_RESPONSIBLE_CARE_GATE_MISSING")

    def test_15_negative_non_medical_institution_owner(self) -> None:
        self.mutate(["responsible_care_governance", "formal_diagnosis_or_treatment_owner"], "health_venue", "HMR5_MEDICAL_INSTITUTION_AUTHORITY_INVALID")

    def test_16_negative_original_opinion_overwritten(self) -> None:
        self.mutate(["second_opinion_governance", "original_opinion_immutable"], False, "HMR5_SECOND_OPINION_INTEGRITY_MISSING")

    def test_17_negative_ai_chooses_final_conclusion(self) -> None:
        self.mutate(["second_opinion_governance", "ai_may_choose_final_medical_conclusion"], True, "HMR5_AI_OPINION_OVERRIDE")

    def test_18_negative_audit_source_version_missing(self) -> None:
        mutated = copy.deepcopy(self.contract); mutated["audit_trail"]["required_fields_per_event"].remove("source_version")
        self.assertEqual("HMR5_AUDIT_TRAIL_INCOMPLETE", validate_semantics(mutated))

    def test_19_negative_real_fee_authorized(self) -> None:
        self.mutate(["audit_trail", "real_amount_authorized"], True, "HMR5_FEE_AUTHORIZATION_PREMATURE")

    def test_20_negative_cure_bounty_enabled(self) -> None:
        self.mutate(["prohibited_modes", "cure_bounty"], True, "HMR5_PROHIBITED_MODE_ENABLED")

    def test_21_negative_premature_signoff(self) -> None:
        mutated = copy.deepcopy(self.contract); mutated["pending_signoffs"][0].update({"status": "accepted", "executable": True})
        self.assertEqual("HMR5_SIGNOFF_PREMATURE", validate_semantics(mutated))

    def test_22_negative_real_data_authorization(self) -> None:
        mutated = copy.deepcopy(self.contract); mutated["no_go"].remove("real_health_data")
        self.assertEqual("HMR5_NO_GO_MISSING", validate_semantics(mutated))

    def test_23_negative_sensitive_pattern(self) -> None:
        mutated = copy.deepcopy(self.contract); mutated["does_not_block"].append("synthetic marker 13800138000")
        self.assertEqual("HMR5_SENSITIVE_DATA_PATTERN", validate_semantics(mutated))


if __name__ == "__main__":
    unittest.main(verbosity=2)
