#!/usr/bin/env python3
"""CA-SC P0/P1 contract and deterministic synthetic conformance."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
MODULE = ROOT.parent
FIXTURES = ROOT / "fixtures"
SEED = "HEAOTANG-CA-SC-20260712-V1"
SENSITIVE_FIELDS = {"owner_id","user_id","user_name","reviewed_by","internal_code"}
REQUIRED_ERRORS = {
    "CLUB_ID_INVALID","CLUB_NOT_FOUND","CLUB_DETAIL_UNAVAILABLE","INVALID_IDEMPOTENCY_KEY",
    "CLUB_JOIN_MESSAGE_TOO_LONG","IDEMPOTENCY_KEY_REUSED","IDEMPOTENCY_IN_PROGRESS",
    "CLUB_NOT_ACTIVE","CLUB_ALREADY_MEMBER","CLUB_JOIN_UNAVAILABLE",
    "CLUB_FILTER_CATEGORY_INVALID","CLUB_CATEGORY_CROSSOVER_DETECTED","CLUB_APPLICATION_ACCESS_DENIED",
}


def load(path: Path):
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), f"BOM forbidden: {path}"
    assert b"\r\n" not in raw, f"CRLF forbidden: {path}"
    return json.loads(raw.decode("utf-8"))


def generator_module():
    path = FIXTURES / "generate_fixtures.py"
    spec = importlib.util.spec_from_file_location("ca_sc_fixtures", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("fixture generator unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def semantic_error(contract, errors, fixtures):
    selector = contract.get("semantic_selector", {})
    if selector != {"club_type":"standard","category":"general","operator":"and","authority":"server","frontend_filtering":False}:
        return "SC_SELECTOR_INVALID"
    if contract.get("member_side_capabilities") != ["list","detail","join","my-applications"]:
        return "SC_CAPABILITY_SCOPE_INVALID"
    interfaces = contract["interfaces"]
    if any(interfaces[name].get("authentication") != "required" or interfaces[name].get("auth_mode") != "shared_session" for name in ("list", "detail", "join", "my_applications")):
        return "SC_ACCESS_CONTRACT_INVALID"
    exposed = set(interfaces["list"]["allowed_item_fields"]) | set(interfaces["detail"]["allowed_fields"])
    if exposed & SENSITIVE_FIELDS or not SENSITIVE_FIELDS.issubset(set(contract["forbidden_response_fields"])):
        return "SC_SENSITIVE_FIELD_EXPOSED"
    if interfaces["list"]["required_query"] != {"type":"standard","category":"general"} or interfaces["list"]["pagination"]["authority"] != "server-after-filter":
        return "SC_LIST_AUTHORITY_INVALID"
    if interfaces["list"]["allowed_item_fields"] != ["id","name","intro","city","type","category","status"]:
        return "SC_DTO_FIELD_INVALID"
    if interfaces["detail"]["required_predicate"] != "type=standard AND category=general AND status=active" or interfaces["detail"]["failure_mode"] != "not-found-resource-hiding":
        return "SC_DETAIL_GUARD_INVALID"
    if interfaces["detail"].get("path") != "/api/v1/clubs/self-created/:id" or interfaces["detail"].get("generic_detail_compatibility") != "/api/v1/clubs/:id remains type-agnostic":
        return "SC_DETAIL_ROUTE_COMPATIBILITY_INVALID"
    if interfaces["detail"].get("route_id_format") != "canonical-positive-safe-integer" or interfaces["detail"].get("invalid_route_behavior") != "zero-request-CLUB_ID_INVALID":
        return "SC_ROUTE_ID_CANONICALIZATION_INVALID"
    if interfaces["detail"]["allowed_fields"] != ["id","name","intro","city","type","category","status","member_count","created_at"]:
        return "SC_DTO_FIELD_INVALID"
    idem = interfaces["join"]["idempotency"]
    if (idem["first_status"], idem["same_payload_replay_status"], idem["different_payload_status"], idem["concurrency_result"]) != (201,200,409,"at-most-one-pending"):
        return "SC_IDEMPOTENCY_INVALID"
    if interfaces["my_applications"]["identity_source"] != "authenticated-session-only" or interfaces["my_applications"]["ignored_identity_query"] != ["user_id"]:
        return "SC_IDENTITY_ISOLATION_INVALID"
    if not {"payment","withdraw","refund","subscription","join-review","member-management"}.issubset(set(contract["forbidden_capabilities"])):
        return "SC_FORBIDDEN_SCOPE_MISSING"
    error_ids = [item["error_id"] for item in errors["errors"]]
    if len(error_ids) != len(set(error_ids)) or not REQUIRED_ERRORS.issubset(set(error_ids)):
        return "SC_ERROR_CATALOG_INVALID"
    status_by_error = {item["error_id"]: item["http_status"] for item in errors["errors"]}
    if status_by_error.get("CLUB_DETAIL_UNAVAILABLE") != 500 or status_by_error.get("CLUB_JOIN_UNAVAILABLE") != 500 or status_by_error.get("CLUB_NOT_FOUND") != 404:
        return "SC_ERROR_CATALOG_INVALID"
    if fixtures.get("seed") != SEED or fixtures.get("synthetic_only") is not True or fixtures.get("environment") != "non-production":
        return "SC_FIXTURE_NOT_SYNTHETIC"
    clubs = fixtures["clubs"]
    selected = [item for item in clubs if item["type"] == "standard" and item["category"] == "general" and item["status"] == "active"]
    if len(selected) != 5:
        return "SC_MIXED_DATA_CROSSOVER"
    if any(item in selected for item in clubs if item["category"] in {"charity","health","trade"} or item["type"] in {"family","direct"} or item["status"] != "active"):
        return "SC_MIXED_DATA_CROSSOVER"
    scenarios = fixtures["scenarios"]
    if len(scenarios) != 14 or len({item["case_id"] for item in scenarios}) != 14:
        return "SC_SCENARIO_SET_INVALID"
    text = json.dumps(fixtures, ensure_ascii=False)
    patterns = [r"(?<!\d)1[3-9]\d{9}(?!\d)", r"(?<!\d)\d{17}[0-9Xx](?!\w)", r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", r"(?i)Bearer\s+"]
    if any(re.search(pattern, text) for pattern in patterns):
        return "SC_FIXTURE_SENSITIVE_PATTERN"
    return None


class SelfCreatedClubContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load(MODULE / "self-created-club.v1.json")
        cls.errors = load(MODULE / "error-catalog.v1.json")
        cls.fixtures = load(FIXTURES / "cases.v1.json")

    def test_01_schema_instances(self):
        for name in ("self-created-club.v1","error-catalog.v1"):
            Draft202012Validator(load(MODULE / f"{name}.schema.json")).validate(load(MODULE / f"{name}.json"))

    def test_02_semantic_baseline(self):
        self.assertIsNone(semantic_error(copy.deepcopy(self.contract), copy.deepcopy(self.errors), copy.deepcopy(self.fixtures)))

    def test_03_generator_replay(self):
        module = generator_module()
        self.assertEqual(module.build_bundle(), module.build_bundle())
        self.assertEqual(module.build_bundle(), self.fixtures)

    def test_04_selector_rejects_type_only(self):
        changed = copy.deepcopy(self.contract)
        changed["semantic_selector"]["category"] = ""
        self.assertEqual("SC_SELECTOR_INVALID", semantic_error(changed, self.errors, self.fixtures))

    def test_05_detail_guard_fail_closed(self):
        changed = copy.deepcopy(self.contract)
        changed["interfaces"]["detail"]["required_predicate"] = "type=standard"
        self.assertEqual("SC_DETAIL_GUARD_INVALID", semantic_error(changed, self.errors, self.fixtures))

    def test_06_idempotency_contract(self):
        changed = copy.deepcopy(self.contract)
        changed["interfaces"]["join"]["idempotency"]["different_payload_status"] = 200
        self.assertEqual("SC_IDEMPOTENCY_INVALID", semantic_error(changed, self.errors, self.fixtures))

    def test_07_cross_user_identity(self):
        changed = copy.deepcopy(self.contract)
        changed["interfaces"]["my_applications"]["identity_source"] = "query"
        self.assertEqual("SC_IDENTITY_ISOLATION_INVALID", semantic_error(changed, self.errors, self.fixtures))

    def test_08_sensitive_dto_field(self):
        changed = copy.deepcopy(self.contract)
        changed["interfaces"]["detail"]["allowed_fields"].append("owner_id")
        self.assertEqual("SC_SENSITIVE_FIELD_EXPOSED", semantic_error(changed, self.errors, self.fixtures))

    def test_09_error_catalog_unique(self):
        changed = copy.deepcopy(self.errors)
        changed["errors"].append(copy.deepcopy(changed["errors"][0]))
        self.assertEqual("SC_ERROR_CATALOG_INVALID", semantic_error(self.contract, changed, self.fixtures))

    def test_10_mixed_data_zero_crossover(self):
        changed = copy.deepcopy(self.fixtures)
        changed["clubs"][5].update({"category":"general"})
        self.assertEqual("SC_MIXED_DATA_CROSSOVER", semantic_error(self.contract, self.errors, changed))

    def test_11_synthetic_sensitive_pattern(self):
        changed = copy.deepcopy(self.fixtures)
        changed["actors"]["candidate_a"] = "13800138000"
        self.assertEqual("SC_FIXTURE_SENSITIVE_PATTERN", semantic_error(self.contract, self.errors, changed))

    def test_12_forbidden_business_scope(self):
        changed = copy.deepcopy(self.contract)
        changed["forbidden_capabilities"].remove("payment")
        self.assertEqual("SC_FORBIDDEN_SCOPE_MISSING", semantic_error(changed, self.errors, self.fixtures))

    def test_13_description_is_not_authoritative_field(self):
        changed = copy.deepcopy(self.contract)
        changed["interfaces"]["detail"]["allowed_fields"][2] = "description"
        self.assertEqual("SC_DTO_FIELD_INVALID", semantic_error(changed, self.errors, self.fixtures))

    def test_14_access_requires_shared_session(self):
        changed = copy.deepcopy(self.contract)
        changed["interfaces"]["list"]["authentication"] = "anonymous"
        self.assertEqual("SC_ACCESS_CONTRACT_INVALID", semantic_error(changed, self.errors, self.fixtures))

    def test_15_internal_errors_are_not_resource_boundaries(self):
        changed = copy.deepcopy(self.errors)
        next(item for item in changed["errors"] if item["error_id"] == "CLUB_JOIN_UNAVAILABLE")["http_status"] = 409
        self.assertEqual("SC_ERROR_CATALOG_INVALID", semantic_error(self.contract, changed, self.fixtures))

    def test_16_generic_detail_cannot_be_narrowed_by_sc(self):
        changed = copy.deepcopy(self.contract)
        changed["interfaces"]["detail"]["path"] = "/api/v1/clubs/:id"
        self.assertEqual("SC_DETAIL_ROUTE_COMPATIBILITY_INVALID", semantic_error(changed, self.errors, self.fixtures))

    def test_17_route_id_must_be_canonical_before_request(self):
        changed = copy.deepcopy(self.contract)
        changed["interfaces"]["detail"]["route_id_format"] = "coerce-number"
        self.assertEqual("SC_ROUTE_ID_CANONICALIZATION_INVALID", semantic_error(changed, self.errors, self.fixtures))


if __name__ == "__main__":
    unittest.main(verbosity=2)
