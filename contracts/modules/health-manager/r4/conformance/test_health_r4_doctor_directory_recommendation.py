#!/usr/bin/env python3
"""Conformance tests for the synthetic-only Health Manager R4-C1 contract."""

from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "contracts/modules/health-manager/r4"
CONTRACT_PATH = MODULE / "doctor-directory-recommendation.v1.json"
SCHEMA_PATH = MODULE / "doctor-directory-recommendation.v1.schema.json"
SOURCE_SHA256 = "fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012"
DIRECTORY_FIELDS = {
    "doctor_reference", "identity_verification_status", "qualification_reference",
    "practice_license_reference", "practice_institution_reference", "practice_scope",
    "clinical_departments", "specialty_evidence_references", "training_governance_status",
    "service_modes", "service_availability_status", "quality_governance_status",
    "complaint_or_exit_status", "verification_timestamp",
}
PIPELINE = [
    "legal_qualification_and_practice_gate",
    "specialty_disease_and_scope_match",
    "online_or_offline_safety_triage",
    "quality_governance",
    "training_and_professional_governance",
    "availability_region_and_service_mode",
    "member_explicit_preferences",
]
NON_BYPASSABLE = set(PIPELINE[:4])
COMMERCIAL_INFLUENCES = {
    "payment", "bidding", "commission", "advertising_spend",
    "institution_commercial_relationship", "result_fee",
}
EXPLANATION_FIELDS = {
    "candidate_reference", "matched_need_tags", "qualification_evidence_references",
    "practice_evidence_references", "quality_basis", "service_mode_basis", "uncertainties",
    "human_review_status", "generated_at", "policy_version",
}
AI_FORBIDDEN = {
    "diagnose", "prescribe", "change_medication", "impersonate_doctor", "promise_outcome",
    "create_credential", "create_specialty_tag_without_authority", "override_hard_gate",
    "change_ranking_for_payment", "close_professional_risk", "close_emergency_risk", "approve_reentry",
}
NO_GO = {
    "business_code", "shared_runtime", "api", "database", "real_doctor_data", "real_identity",
    "real_member", "real_health_data", "internet_medical_service", "diagnosis", "prescription",
    "medication_change", "doctor_impersonation", "outcome_promise", "public_doctor_ranking",
    "paid_medical_ranking", "charging", "payment", "test_server_deployment", "production",
    "irreversible_operation",
}
PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
NATIONAL_ID = re.compile(r"(?<![0-9a-fA-F])\d{17}[0-9Xx](?![0-9a-fA-F])")
JWT = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_semantics(contract: dict[str, Any]) -> str | None:
    if contract.get("source", {}).get("sha256") != SOURCE_SHA256:
        return "HMR4_SOURCE_HASH_DRIFT"
    if contract.get("synthetic_only") is not True or contract.get("executable") is not False:
        return "HMR4_EXECUTION_PREMATURE"

    directory = contract.get("directory_entry", {})
    if not DIRECTORY_FIELDS.issubset(set(directory.get("minimum_fields", []))):
        return "HMR4_DIRECTORY_FIELDS_INCOMPLETE"
    if directory.get("authority_id") != "doctor-group-governance-directory":
        return "HMR4_DIRECTORY_AUTHORITY_INVALID"
    if set(directory.get("health_manager_permissions", [])) != {
        "read_verified_directory_summary", "build_explainable_candidate_set", "request_human_review"
    }:
        return "HMR4_DIRECTORY_AUTHORITY_CAPTURE"

    gates = contract.get("hard_eligibility_gates", {})
    qualification = gates.get("qualification", {})
    if gates.get("all_required") is not True or gates.get("default_decision") != "reject":
        return "HMR4_HARD_GATE_NOT_FAIL_CLOSED"
    if any(qualification.get(key) is not True for key in (
        "identity_verified", "qualification_verified", "practice_license_verified",
        "verification_authority_required", "verification_timestamp_required",
    )):
        return "HMR4_CREDENTIAL_GATE_MISSING"
    if qualification.get("accepted_statuses") != ["active"]:
        return "HMR4_CREDENTIAL_STATUS_INVALID"
    if not {"missing", "unverified", "expired", "revoked", "suspended", "conflicting_source"}.issubset(
        set(qualification.get("fail_closed_conditions", []))
    ):
        return "HMR4_CREDENTIAL_FAILURE_NOT_COVERED"

    practice = gates.get("practice_relation", {})
    if any(practice.get(key) is not True for key in (
        "institution_verified", "practice_scope_match_required", "clinical_department_match_required",
        "service_mode_authorized_required",
    )):
        return "HMR4_PRACTICE_GATE_MISSING"
    service = gates.get("service_and_quality", {})
    if service.get("complaint_hold_excludes_candidate") is not True or service.get("exit_or_suspension_excludes_candidate") is not True:
        return "HMR4_QUALITY_EXIT_GATE_MISSING"

    pipeline = contract.get("recommendation_pipeline", {})
    if pipeline.get("ordered_stages") != PIPELINE:
        return "HMR4_PIPELINE_ORDER_INVALID"
    if not NON_BYPASSABLE.issubset(set(pipeline.get("non_bypassable_stages", []))):
        return "HMR4_SAFETY_STAGE_BYPASS"
    if pipeline.get("online_unsuitable_action") != "route_to_human_and_offline_medical_institution":
        return "HMR4_ONLINE_SAFETY_TRIAGE_INVALID"
    if not {"legal_qualification", "practice_scope", "safety_triage", "quality_hold"}.issubset(
        set(pipeline.get("member_preferences_cannot_override", []))
    ):
        return "HMR4_PREFERENCE_OVERRIDE"

    training = contract.get("training_governance", {})
    if training.get("training_replaces_legal_qualification") is not False or training.get("training_replaces_practice_scope") is not False:
        return "HMR4_TRAINING_SUBSTITUTES_LEGAL_GATE"
    if training.get("ai_may_create_training_status") is not False:
        return "HMR4_AI_CREATES_TRAINING_STATUS"

    commercial = contract.get("commercial_neutrality", {})
    if commercial.get("medical_safety_order_immutable") is not True or commercial.get("professional_match_order_immutable") is not True:
        return "HMR4_COMMERCIAL_ORDER_OVERRIDE"
    if commercial.get("commercial_inputs_allowed_in_medical_ranking") != []:
        return "HMR4_PAID_RANKING_ALLOWED"
    if not COMMERCIAL_INFLUENCES.issubset(set(commercial.get("prohibited_influences", []))):
        return "HMR4_COMMERCIAL_GUARD_MISSING"
    if commercial.get("public_ranking_authorized") is not False or commercial.get("charging_or_payment_authorized") is not False:
        return "HMR4_COMMERCIAL_AUTHORIZATION_PREMATURE"

    explanation = contract.get("recommendation_explanation", {})
    if explanation.get("required") is not True or not EXPLANATION_FIELDS.issubset(set(explanation.get("required_fields", []))):
        return "HMR4_EXPLANATION_INCOMPLETE"
    if explanation.get("evidence_references_required") is not True or explanation.get("uncertainty_required") is not True:
        return "HMR4_EXPLANATION_TRACEABILITY_MISSING"

    review = contract.get("human_review_and_exit", {})
    if review.get("human_reviewer_identity_required") is not True or review.get("review_reason_and_version_required") is not True:
        return "HMR4_HUMAN_REVIEW_BYPASS"
    if review.get("ai_may_close_professional_risk") is not False or review.get("ai_may_close_emergency_risk") is not False:
        return "HMR4_AI_RISK_CLOSURE"
    if not {"remove_from_candidate_pool", "stop_new_recommendations", "preserve_audit_history"}.issubset(
        set(review.get("exit_actions", []))
    ) or review.get("reentry_requires_fresh_verification_and_human_approval") is not True:
        return "HMR4_EXIT_GUARD_MISSING"
    if not AI_FORBIDDEN.issubset(set(contract.get("ai_boundary", {}).get("forbidden", []))):
        return "HMR4_AI_BOUNDARY_MISSING"

    signoffs = contract.get("pending_signoffs", [])
    if len(signoffs) != 4 or any(item.get("status") != "pending-with-owner" or item.get("executable") is not False for item in signoffs):
        return "HMR4_SIGNOFF_PREMATURE"
    if not NO_GO.issubset(set(contract.get("no_go", []))):
        return "HMR4_NO_GO_MISSING"

    serialized = json.dumps(contract, ensure_ascii=False)
    if PHONE.search(serialized) or NATIONAL_ID.search(serialized) or JWT.search(serialized) or "Bearer " in serialized:
        return "HMR4_SENSITIVE_DATA_PATTERN"
    return None


class HealthR4DoctorDirectoryRecommendationTest(unittest.TestCase):
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
        self.assertEqual("HMR4_SOURCE_HASH_DRIFT", validate_semantics(mutated))

    def test_04_negative_directory_field_removed(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["directory_entry"]["minimum_fields"].remove("practice_license_reference")
        self.assertEqual("HMR4_DIRECTORY_FIELDS_INCOMPLETE", validate_semantics(mutated))

    def test_05_negative_unverified_credential_allowed(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["hard_eligibility_gates"]["qualification"]["qualification_verified"] = False
        self.assertEqual("HMR4_CREDENTIAL_GATE_MISSING", validate_semantics(mutated))

    def test_06_negative_expired_or_revoked_not_rejected(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["hard_eligibility_gates"]["qualification"]["fail_closed_conditions"].remove("revoked")
        self.assertEqual("HMR4_CREDENTIAL_FAILURE_NOT_COVERED", validate_semantics(mutated))

    def test_07_negative_practice_scope_mismatch_allowed(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["hard_eligibility_gates"]["practice_relation"]["practice_scope_match_required"] = False
        self.assertEqual("HMR4_PRACTICE_GATE_MISSING", validate_semantics(mutated))

    def test_08_negative_online_unsuitable_not_routed_offline(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["recommendation_pipeline"]["online_unsuitable_action"] = "continue_online_match"
        self.assertEqual("HMR4_ONLINE_SAFETY_TRIAGE_INVALID", validate_semantics(mutated))

    def test_09_negative_pipeline_order_changed(self) -> None:
        mutated = copy.deepcopy(self.contract)
        stages = mutated["recommendation_pipeline"]["ordered_stages"]
        stages[0], stages[-1] = stages[-1], stages[0]
        self.assertEqual("HMR4_PIPELINE_ORDER_INVALID", validate_semantics(mutated))

    def test_10_negative_training_replaces_license(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["training_governance"]["training_replaces_legal_qualification"] = True
        self.assertEqual("HMR4_TRAINING_SUBSTITUTES_LEGAL_GATE", validate_semantics(mutated))

    def test_11_negative_paid_priority(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["commercial_neutrality"]["commercial_inputs_allowed_in_medical_ranking"] = ["payment"]
        self.assertEqual("HMR4_PAID_RANKING_ALLOWED", validate_semantics(mutated))

    def test_12_negative_ai_created_specialty(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["ai_boundary"]["forbidden"].remove("create_specialty_tag_without_authority")
        self.assertEqual("HMR4_AI_BOUNDARY_MISSING", validate_semantics(mutated))

    def test_13_negative_explanation_without_evidence(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["recommendation_explanation"]["required_fields"].remove("qualification_evidence_references")
        self.assertEqual("HMR4_EXPLANATION_INCOMPLETE", validate_semantics(mutated))

    def test_14_negative_human_review_bypass(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["human_review_and_exit"]["human_reviewer_identity_required"] = False
        self.assertEqual("HMR4_HUMAN_REVIEW_BYPASS", validate_semantics(mutated))

    def test_15_negative_exit_still_recommended(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["human_review_and_exit"]["exit_actions"].remove("stop_new_recommendations")
        self.assertEqual("HMR4_EXIT_GUARD_MISSING", validate_semantics(mutated))

    def test_16_negative_ai_closes_emergency_risk(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["human_review_and_exit"]["ai_may_close_emergency_risk"] = True
        self.assertEqual("HMR4_AI_RISK_CLOSURE", validate_semantics(mutated))

    def test_17_negative_premature_signoff(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["pending_signoffs"][0].update({"status": "accepted", "executable": True})
        self.assertEqual("HMR4_SIGNOFF_PREMATURE", validate_semantics(mutated))

    def test_18_negative_real_data_authorization(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["no_go"].remove("real_doctor_data")
        self.assertEqual("HMR4_NO_GO_MISSING", validate_semantics(mutated))

    def test_19_negative_sensitive_pattern(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["does_not_block"].append("synthetic marker 13800138000")
        self.assertEqual("HMR4_SENSITIVE_DATA_PATTERN", validate_semantics(mutated))


if __name__ == "__main__":
    unittest.main(verbosity=2)
