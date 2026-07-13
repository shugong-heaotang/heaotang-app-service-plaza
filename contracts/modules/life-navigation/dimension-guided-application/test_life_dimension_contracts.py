#!/usr/bin/env python3
"""Standard-library conformance for LN-S2 pending Base Contract."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INSTANCE_NAMES = (
    "dimension-registry.v1.json",
    "dimension-directory.v1.json",
    "application-dimension-selector.v1.json",
    "error-catalog.v1.json",
)
SCHEMA_NAMES = tuple(name.replace(".json", ".schema.json") for name in INSTANCE_NAMES)
CASE_ERRORS = {
    "normal-proposed-dimension": "LN_DIMENSION_DECISION_PENDING",
    "blank-dimension": "LN_DIMENSION_REQUIRED",
    "unknown-dimension": "LN_DIMENSION_UNKNOWN",
    "inactive-dimension": "LN_DIMENSION_INACTIVE",
    "incompatible-version": "LN_DIMENSION_VERSION_INCOMPATIBLE",
    "legacy-yun-compatibility-pending": "LN_LEGACY_DIMENSION_DECISION_PENDING",
    "registry-config-missing": "LN_DIMENSION_REGISTRY_MISSING",
    "registry-read-failed": "LN_DIMENSION_REGISTRY_READ_FAILED",
    "duplicate-dimension-id": "LN_DIMENSION_DUPLICATE_ID",
    "duplicate-sort-order": "LN_DIMENSION_DUPLICATE_SORT_ORDER",
    "empty-registry": "LN_DIMENSION_REGISTRY_INVALID",
    "pending-selector-made-executable": "LN_DIMENSION_REGISTRY_INVALID",
}


def load(relative: str) -> object:
    raw = (ROOT / relative).read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM forbidden: {relative}"
    assert b"\r\n" not in raw, f"CRLF forbidden: {relative}"
    return json.loads(raw.decode("utf-8"))


def canonical_sha(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def mutated_error(case: dict[str, object], registry: dict[str, object], selector: dict[str, object]) -> str:
    mutation = case["mutation"]
    if mutation == "registry-missing":
        return "LN_DIMENSION_REGISTRY_MISSING"
    if mutation == "registry-read-failed":
        return "LN_DIMENSION_REGISTRY_READ_FAILED"

    candidate = copy.deepcopy(registry)
    if mutation == "duplicate-first-dimension-id":
        candidate["dimensions"][1]["dimension_id"] = candidate["dimensions"][0]["dimension_id"]
    elif mutation == "duplicate-first-sort-order":
        candidate["dimensions"][1]["sort_order"] = candidate["dimensions"][0]["sort_order"]
    elif mutation == "empty-dimensions":
        candidate["dimensions"] = []
    elif mutation in {"candidate-accepted-inactive", "candidate-accepted-active"}:
        target_id = case["input"]["dimension_id"]
        target = next(item for item in candidate["dimensions"] if item["dimension_id"] == target_id)
        target["decision_status"] = "accepted"
        target["active"] = mutation == "candidate-accepted-active"
    elif mutation == "selector-executable-true":
        changed_selector = copy.deepcopy(selector)
        changed_selector["selector"]["executable"] = True
        assert changed_selector["selector"]["decision_status"] == "pending"
        return "LN_DIMENSION_REGISTRY_INVALID"

    dimensions = candidate["dimensions"]
    if not dimensions:
        return "LN_DIMENSION_REGISTRY_INVALID"
    ids = [item["dimension_id"] for item in dimensions]
    if len(ids) != len(set(ids)):
        return "LN_DIMENSION_DUPLICATE_ID"
    orders = [item["sort_order"] for item in dimensions]
    if len(orders) != len(set(orders)):
        return "LN_DIMENSION_DUPLICATE_SORT_ORDER"

    dimension_id = case["input"]["dimension_id"]
    version = case["input"]["dimension_version"]
    if not dimension_id.strip():
        return "LN_DIMENSION_REQUIRED"
    if dimension_id == "yun":
        return "LN_LEGACY_DIMENSION_DECISION_PENDING"
    item = next((entry for entry in dimensions if entry["dimension_id"] == dimension_id), None)
    if item is None:
        return "LN_DIMENSION_UNKNOWN"
    if item["decision_status"] != "accepted":
        return "LN_DIMENSION_DECISION_PENDING"
    if item["active"] is False:
        return "LN_DIMENSION_INACTIVE"
    if version != item["dimension_version"]:
        return "LN_DIMENSION_VERSION_INCOMPATIBLE"
    if item["executable"] is False:
        return "LN_DIMENSION_REGISTRY_INVALID"
    raise AssertionError("Base Contract must never produce an executable selection")


def main() -> int:
    instances = {name: load(name) for name in INSTANCE_NAMES}
    schemas = {name: load(name) for name in SCHEMA_NAMES}
    fixtures = load("fixtures/cases.v1.json")

    assert all(schema["$schema"] == "https://json-schema.org/draft/2020-12/schema" for schema in schemas.values())
    assert all(value["contract_status"] == "base-contract" for value in instances.values())
    assert all(value[next(key for key in value if key.startswith("authoritative_business_"))] is False for value in instances.values())

    registry = instances["dimension-registry.v1.json"]
    assert registry["registry_frozen"] is False
    assert registry["decision_status"] == "pending"
    assert registry["executable"] is False
    assert all(item["decision_status"] == "pending" for item in registry["dimensions"])
    assert all(item["active"] is False and item["executable"] is False for item in registry["dimensions"])
    assert len({item["dimension_id"] for item in registry["dimensions"]}) == len(registry["dimensions"])
    assert len({item["sort_order"] for item in registry["dimensions"]}) == len(registry["dimensions"])
    assert registry["legacy_dimensions"] == [{"observed_dimension_id": "yun", "decision_status": "pending", "executable": False, "mapping_target": None, "compatibility_action": "not-decided"}]

    directory = instances["dimension-directory.v1.json"]
    assert directory["base_response"]["items"] == []
    assert set(directory["allowed_item_fields"]) == {"dimension_id", "dimension_version", "label", "sort_order"}
    assert set(directory["allowed_item_fields"]).isdisjoint(directory["forbidden_fields"])

    selector = instances["application-dimension-selector.v1.json"]
    assert selector["selector"]["decision_status"] == "pending"
    assert selector["selector"]["registry_frozen"] is False
    assert selector["selector"]["executable"] is False
    assert selector["legacy_yun"] == {"decision_status": "pending", "executable": False, "mapping_target": None}

    error_ids = [item["error_id"] for item in instances["error-catalog.v1.json"]["errors"]]
    assert len(error_ids) == len(set(error_ids))
    assert set(CASE_ERRORS.values()).issubset(error_ids)

    assert fixtures["seed"] == "HEAOTANG-LN-S2-20260712-V1"
    assert fixtures["synthetic_only"] is True and fixtures["non_production"] is True
    cases = fixtures["cases"]
    assert len(cases) == 12 and len({case["case_id"] for case in cases}) == 12
    for case in cases:
        assert case["expected_outcome"] == "fail-closed", case["case_id"]
        assert case["expected_error_id"] == CASE_ERRORS[case["case_kind"]], case["case_id"]
        assert mutated_error(case, registry, selector) == case["expected_error_id"], case["case_id"]

    combined = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in (*INSTANCE_NAMES, *SCHEMA_NAMES, "fixtures/cases.v1.json"))
    forbidden_patterns = {
        "phone": r"(?<!\d)1[3-9]\d{9}(?!\d)",
        "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "bearer": r"(?i)bearer\s+[A-Za-z0-9._-]+",
        "jwt": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    }
    for label, pattern in forbidden_patterns.items():
        assert re.search(pattern, combined) is None, f"sensitive pattern found: {label}"

    hashes = {name: canonical_sha(load(name)) for name in (*INSTANCE_NAMES, *SCHEMA_NAMES, "fixtures/cases.v1.json")}
    print(json.dumps({"status": "pass", "schema_draft": "2020-12", "instances": 4, "schemas": 4, "cases": len(cases), "synthetic_seed": fixtures["seed"], "sensitive_scan": "pass", "canonical_sha256": hashes}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
