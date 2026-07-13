#!/usr/bin/env python3
import copy
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parent

EXPECTED_STATE_MODEL = {
    "application_history": {
        "entity": "club-join-application",
        "states": ["pending", "rejected"],
        "counts_as_current_membership": False,
    },
    "membership": {
        "entity": "club-membership",
        "states": ["active", "left", "suspended"],
        "current_states": ["active", "suspended"],
        "history_states": ["left"],
        "optional_states": ["suspended"],
    },
    "club_lifecycle": {
        "entity": "club",
        "states": ["dissolved"],
        "not_a_membership_state": True,
    },
}


def load(name):
    raw = (ROOT / name).read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" not in raw
    return json.loads(raw.decode())


def validate_fixture_state_domains(fixtures):
    for case in fixtures.get("cases", []):
        for club in case.get("clubs", []):
            if "status" in club:
                return "CMH_AMBIGUOUS_STATUS_FIELD"
            if club.get("membership_status") not in {"active", "suspended"}:
                return "CMH_STATE_DOMAIN_LEAK"
            if club.get("club_status") == "dissolved":
                return "CMH_STATE_DOMAIN_LEAK"
        for application in case.get("application_history", []):
            if application.get("status") not in {"pending", "rejected"}:
                return "CMH_STATE_DOMAIN_LEAK"
            if "membership_status" in application or "club_status" in application:
                return "CMH_STATE_DOMAIN_LEAK"
        for history in case.get("membership_history", []):
            if history.get("membership_status") != "left":
                return "CMH_STATE_DOMAIN_LEAK"
            if history.get("club_status") not in {"active", "dissolved"}:
                return "CMH_STATE_DOMAIN_LEAK"
    return None


def semantic(contract, errors, fixtures):
    if contract["layout_order"] != [
        "member-summary",
        "my-clubs",
        "today-tasks",
        "recent-activities",
        "alliance-feed",
        "explore-more",
    ]:
        return "CMH_ORDER_INVALID"
    if contract["sections"]["explore-more"].get("action_ids") != [
        "public-benefit-club",
        "self-created-club",
        "family-club",
        "club-federation",
    ]:
        return "CMH_EXPLORE_INVALID"
    my_clubs = contract["sections"]["my-clubs"]
    if my_clubs["source"] != "GET /api/v1/clubs/my" or my_clubs["privacy"] != "self-only":
        return "CMH_MY_CLUBS_INVALID"
    if "status" in my_clubs.get("fields", []):
        return "CMH_AMBIGUOUS_STATUS_FIELD"
    if not {"club_status", "membership_status"}.issubset(my_clubs.get("fields", [])):
        return "CMH_STATE_FIELDS_INVALID"
    if contract.get("relationship_state_model") != EXPECTED_STATE_MODEL:
        return "CMH_STATE_DOMAINS_INVALID"
    if "membership_states" in contract:
        return "CMH_STATE_DOMAINS_INVALID"
    if (
        contract["degradation"].get("forbid_empty_array_fallback") is not True
        or contract["degradation"].get("forbid_runtime_mock") is not True
    ):
        return "CMH_FALLBACK_INVALID"
    if contract["management"] != {
        "action_id": "club-manage",
        "placement": "secondary",
        "required_scope": "club:manage",
        "hidden_for_ordinary_member": True,
    }:
        return "CMH_MANAGEMENT_INVALID"
    if not {
        "phone",
        "id_card",
        "health_detail",
        "family_private_record",
        "payment_account",
        "raw_token",
    }.issubset(contract["forbidden_response_fields"]):
        return "CMH_PRIVACY_INVALID"
    ids = [item["error_id"] for item in errors["errors"]]
    if len(ids) != len(set(ids)) or len(ids) < 8:
        return "CMH_ERRORS_INVALID"
    if (
        fixtures.get("seed") != "HEAOTANG-CMH-20260712-V1"
        or fixtures.get("synthetic_only") is not True
        or len(fixtures.get("cases", [])) < 10
    ):
        return "CMH_FIXTURES_INVALID"
    fixture_error = validate_fixture_state_domains(fixtures)
    if fixture_error:
        return fixture_error
    if any(
        re.search(pattern, json.dumps(fixtures))
        for pattern in [
            r"(?<!\d)1[3-9]\d{9}(?!\d)",
            r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.",
        ]
    ):
        return "CMH_FIXTURE_SENSITIVE"
    return None


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = load("member-home.v1.json")
        cls.e = load("error-catalog.v1.json")
        cls.f = load("fixtures/cases.v1.json")
        cls.schema = load("member-home.v1.schema.json")

    def test_schema(self):
        Draft202012Validator(self.schema).validate(self.c)
        Draft202012Validator(load("error-catalog.v1.schema.json")).validate(self.e)

    def test_baseline(self):
        self.assertIsNone(semantic(self.c, self.e, self.f))

    def test_order(self):
        changed = copy.deepcopy(self.c)
        changed["layout_order"].reverse()
        self.assertEqual("CMH_ORDER_INVALID", semantic(changed, self.e, self.f))

    def test_explore(self):
        changed = copy.deepcopy(self.c)
        changed["sections"]["explore-more"]["action_ids"].remove("club-federation")
        self.assertEqual("CMH_EXPLORE_INVALID", semantic(changed, self.e, self.f))

    def test_no_runtime_fallback(self):
        changed = copy.deepcopy(self.c)
        changed["degradation"]["forbid_runtime_mock"] = False
        self.assertEqual("CMH_FALLBACK_INVALID", semantic(changed, self.e, self.f))

    def test_privacy(self):
        changed = copy.deepcopy(self.c)
        changed["forbidden_response_fields"].remove("phone")
        self.assertEqual("CMH_PRIVACY_INVALID", semantic(changed, self.e, self.f))

    def test_errors_unique(self):
        changed = copy.deepcopy(self.e)
        changed["errors"].append(changed["errors"][0])
        self.assertEqual("CMH_ERRORS_INVALID", semantic(self.c, changed, self.f))

    def test_state_domains_are_exact(self):
        changed = copy.deepcopy(self.c)
        changed["relationship_state_model"]["membership"]["states"].append("pending")
        self.assertEqual("CMH_STATE_DOMAINS_INVALID", semantic(changed, self.e, self.f))
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.schema).validate(changed)

    def test_old_flat_membership_states_are_rejected(self):
        changed = copy.deepcopy(self.c)
        changed["membership_states"] = [
            "active",
            "pending",
            "rejected",
            "left",
            "suspended",
            "dissolved",
        ]
        self.assertEqual("CMH_STATE_DOMAINS_INVALID", semantic(changed, self.e, self.f))
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.schema).validate(changed)

    def test_ambiguous_status_field_is_rejected(self):
        changed = copy.deepcopy(self.c)
        changed["sections"]["my-clubs"]["fields"].append("status")
        self.assertEqual("CMH_AMBIGUOUS_STATUS_FIELD", semantic(changed, self.e, self.f))

    def test_pending_and_rejected_are_application_history_only(self):
        changed = copy.deepcopy(self.f)
        changed["cases"][0]["clubs"] = [
            {
                "club_id": "c-invalid",
                "club_status": "active",
                "membership_status": "pending",
            }
        ]
        self.assertEqual("CMH_STATE_DOMAIN_LEAK", semantic(self.c, self.e, changed))

    def test_left_is_membership_history_only(self):
        changed = copy.deepcopy(self.f)
        changed["cases"][0]["clubs"] = [
            {
                "club_id": "c-invalid",
                "club_status": "active",
                "membership_status": "left",
            }
        ]
        self.assertEqual("CMH_STATE_DOMAIN_LEAK", semantic(self.c, self.e, changed))

    def test_dissolved_is_club_lifecycle_only(self):
        changed = copy.deepcopy(self.f)
        changed["cases"][0]["clubs"] = [
            {
                "club_id": "c-invalid",
                "club_status": "active",
                "membership_status": "dissolved",
            }
        ]
        self.assertEqual("CMH_STATE_DOMAIN_LEAK", semantic(self.c, self.e, changed))

    def test_suspended_is_optional_membership_state(self):
        suspended = next(
            item for item in self.f["cases"] if item["case_id"] == "suspended-member"
        )
        self.assertEqual("suspended", suspended["clubs"][0]["membership_status"])
        self.assertIn(
            "suspended",
            self.c["relationship_state_model"]["membership"]["optional_states"],
        )

    def test_fixture_identities(self):
        self.assertEqual(
            {
                "new-member",
                "application-history-only",
                "left-membership-history",
                "suspended-member",
                "dissolved-club-history",
                "family-member",
                "multi-club-member",
                "manager",
                "partial-failure",
                "unauthorized",
            },
            {item["case_id"] for item in self.f["cases"]},
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
