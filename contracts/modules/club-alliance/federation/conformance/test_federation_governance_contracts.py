#!/usr/bin/env python3
"""CA-UF M0 governance contract conformance tests."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    path = ROOT / name
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), f"BOM forbidden: {path}"
    return json.loads(raw.decode("utf-8"))


class FederationGovernanceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load("federation-governance.v1.json")
        cls.schema = load("federation-governance.v1.schema.json")
        cls.fixtures = load("fixtures/cases.v1.json")

    def test_01_schema_is_valid_and_contract_conforms(self):
        Draft202012Validator.check_schema(self.schema)
        Draft202012Validator(self.schema).validate(self.contract)

    def test_02_relationship_semantics_and_authorization_boundary(self):
        self.assertEqual("club_relationship", self.contract["entity_kind"])
        self.assertEqual("club-federation", self.contract["relationship_kind"])
        self.assertFalse(self.contract["implementation_authorized"])

    def test_03_code_namespaces_are_unique_and_non_reusable(self):
        identity = self.contract["identity"]
        prefixes = [item["prefix"] for item in identity["namespaces"]]
        self.assertEqual({"CA-CLB", "CA-UF", "CA-MBR", "CA-GRP", "CA-APP", "CA-RES"}, set(prefixes))
        self.assertEqual(len(prefixes), len(set(prefixes)))
        self.assertEqual("never", identity["public_code_policy"]["reuse"])
        for item in identity["namespaces"]:
            re.compile(item["pattern"])

    def test_04_code_is_server_allocated_after_authoritative_event(self):
        policy = self.contract["identity"]["public_code_policy"]
        self.assertEqual("server-only-after-authoritative-event", policy["allocation"])
        self.assertFalse(policy["mutable_attributes_embedded"])
        self.assertEqual("forbidden", self.contract["approval"]["official_code_before_approval"])

    def test_05_four_approval_dimensions_and_maker_checker(self):
        approval = self.contract["approval"]
        dimensions = {item["dimension_id"] for item in approval["dimensions"]}
        self.assertEqual({"organization-eligibility", "member-club-consent", "alliance-governance-review", "risk-and-compliance"}, dimensions)
        self.assertTrue(approval["maker_checker"]["required"])
        self.assertEqual("forbidden", approval["maker_checker"]["same_actor_final_review"])

    def test_06_policy_thresholds_are_versioned_keys_and_fail_closed(self):
        approval = self.contract["approval"]
        self.assertEqual("fail-closed", approval["missing_variable_behavior"])
        self.assertTrue(all(value.startswith("club_federation.") for value in approval["variable_keys"].values()))
        self.assertTrue(all(not isinstance(value, (int, float)) for value in approval["variable_keys"].values()))

    def test_07_representation_comes_from_club_mandate(self):
        rep = self.contract["representation"]
        self.assertEqual("member-club-mandate", rep["source_of_authority"])
        self.assertEqual("forbidden", rep["direct_personal_membership_in_federation"])
        ordinary = next(role for role in rep["roles"] if role["role"] == "ordinary-member")
        self.assertFalse(ordinary["may_vote"])

    def test_08_mandate_term_revocation_and_conflicts_fail_closed(self):
        rules = self.contract["representation"]["rules"]
        self.assertEqual("deny", rules["expired_or_revoked_mandate"])
        self.assertTrue(rules["member_club_may_revoke"])
        self.assertEqual("recuse", rules["conflicted_actor_decision"])
        self.assertEqual("forbidden", rules["auditor_reviews_own_action"])

    def test_09_charter_is_versioned_immutable_and_required(self):
        charter = self.contract["charter"]
        self.assertTrue(charter["versioned"])
        self.assertTrue(charter["effective_version_immutable"])
        self.assertGreaterEqual(len(charter["required_sections"]), 10)
        self.assertEqual("forbidden", charter["activation_without_effective_charter"])
        self.assertEqual("fail-closed", charter["missing_variable_behavior"])

    def test_10_communication_spaces_have_distinct_role_boundaries(self):
        spaces = {item["space_type"]: item for item in self.contract["communication"]["spaces"]}
        self.assertEqual({"official-announcement", "governance-deliberation", "member-collaboration", "public-information"}, set(spaces))
        self.assertNotIn("ordinary-member", spaces["official-announcement"]["publish_roles"])
        self.assertIn("ordinary-member", spaces["member-collaboration"]["publish_roles"])

    def test_11_group_code_dm_consent_and_privacy_are_required(self):
        communication = self.contract["communication"]
        self.assertTrue(communication["group_unique_code_required"])
        self.assertEqual("disabled", communication["direct_message"]["default"])
        self.assertEqual("mutual-explicit-consent", communication["direct_message"]["enablement"])
        self.assertEqual("forbidden-by-default", communication["privacy"]["cross_club_phone_visibility"])

    def test_12_moderation_has_reason_evidence_audit_and_appeal(self):
        moderation = self.contract["communication"]["moderation"]
        for field in ("reason_required", "evidence_reference_required", "immutable_audit_event_required", "appeal_required", "appeal_reviewer_independent", "report_entry_required"):
            self.assertTrue(moderation[field])

    def test_13_commercial_capabilities_are_forbidden(self):
        self.assertTrue(all(value == "forbidden" for value in self.contract["commercial"].values()))
        self.assertIn("unauthorized-fundraising-or-financial-solicitation", self.contract["communication"]["prohibited_content_classes"])

    def test_14_fixture_ids_are_unique_and_cover_all_domains(self):
        cases = self.fixtures["cases"]
        ids = [case["case_id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(self.fixtures["synthetic_only"])
        self.assertTrue({"approval", "identity", "representation", "charter", "communication", "commercial", "moderation"}.issubset({case["area"] for case in cases}))

    def test_15_fixtures_cover_positive_and_fail_closed_paths(self):
        expected = {case["expected"] for case in self.fixtures["cases"]}
        self.assertIn("approve-and-allocate-ca-uf-code", expected)
        self.assertIn("fail-closed", expected)
        self.assertIn("reject-and-require-new-version", expected)
        self.assertIn("reject-sanction", expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
