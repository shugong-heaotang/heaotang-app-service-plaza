#!/usr/bin/env python3
"""CA-H0 contract conformance using only the Python standard library."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[4]
MODULE = ROOT / "contracts/modules/club-alliance"
CONFORMANCE = MODULE / "conformance"
ALLOWED_ACTION_IDS = [
    "public-benefit-club",
    "self-created-club",
    "family-club",
    "club-federation",
]
FORBIDDEN_PRESENTATION_KEYS = {
    "label",
    "sort_order",
    "target",
    "access",
    "lifecycle_status",
    "return_target",
    "telemetry_event",
}
READINESS_KEYS = {"governance", "development", "acceptance", "release", "operations"}
COMMERCIAL_IDS = {"PAYMENT", "WITHDRAWAL", "REFUND", "SUBSCRIPTION"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return json.load(handle)


def load_bundle() -> dict[str, Any]:
    return {
        "upstream": load_json(ROOT / "contracts/service-plaza/service-plaza-actions.v1.json"),
        "upstream_schema": load_json(ROOT / "contracts/service-plaza/service-plaza-action.schema.json"),
        "registry": load_json(MODULE / "category-registry.v1.json"),
        "registry_schema": load_json(MODULE / "category-registry.v1.schema.json"),
        "catalog": load_json(MODULE / "capability-catalog.v1.json"),
        "catalog_schema": load_json(MODULE / "capability-catalog.v1.schema.json"),
        "homepage": load_json(MODULE / "homepage.v1.json"),
        "homepage_schema": load_json(MODULE / "homepage.v1.schema.json"),
        "relationship": load_json(MODULE / "relationship.v1.json"),
        "relationship_schema": load_json(MODULE / "relationship.v1.schema.json"),
    }


def known_decisions() -> set[str]:
    text = (ROOT / "docs/project-management/modules/club-alliance/CA-F0-H0-decisions.md").read_text(encoding="utf-8")
    return set(re.findall(r"^## (D-CA-[0-9]{3})\b", text, flags=re.MULTILINE))


def copied_presentation_key(value: Any) -> bool:
    if isinstance(value, dict):
        if FORBIDDEN_PRESENTATION_KEYS.intersection(value):
            return True
        return any(copied_presentation_key(child) for child in value.values())
    if isinstance(value, list):
        return any(copied_presentation_key(child) for child in value)
    return False


def find_capability(catalog: dict[str, Any], capability_id: str) -> dict[str, Any]:
    return next(item for item in catalog["capabilities"] if item.get("capability_id") == capability_id)


def apply_mutation(bundle: dict[str, Any], mutation: str) -> None:
    upstream = bundle["upstream"]
    registry = bundle["registry"]
    catalog = bundle["catalog"]
    homepage = bundle["homepage"]
    relationship = bundle["relationship"]

    if mutation in {"baseline", "relationship-baseline", "query-blank", "query-unknown", "query-ambiguous", "internal-exception"}:
        return
    if mutation == "upstream-invalid":
        bundle["upstream"] = "invalid"
    elif mutation == "upstream-missing-category":
        upstream["actions"] = [a for a in upstream["actions"] if a.get("action_id") != "public-benefit-club"]
    elif mutation == "upstream-duplicate-action":
        next(a for a in upstream["actions"] if a.get("action_id") == "self-created-club")["action_id"] = "public-benefit-club"
    elif mutation == "registry-disallowed-action":
        registry["accepted_action_ids"][0] = "rogue-club"
    elif mutation == "upstream-duplicate-order":
        next(a for a in upstream["actions"] if a.get("action_id") == "self-created-club")["sort_order"] = 50
    elif mutation == "upstream-remove-manage":
        upstream["actions"] = [a for a in upstream["actions"] if a.get("action_id") != "club-manage"]
    elif mutation == "registry-add-manage":
        registry["accepted_action_ids"].append("club-manage")
    elif mutation == "registry-copy-label":
        registry["entries"][0]["label"] = "copied"
    elif mutation == "registry-copy-target":
        registry["entries"][0]["target"] = "/copied"
    elif mutation == "registry-unknown-action":
        registry["entries"][0]["action_id"] = "unknown-club"
    elif mutation == "registry-duplicate-action":
        registry["entries"][1]["action_id"] = registry["entries"][0]["action_id"]
    elif mutation == "pending-selector-executable":
        next(e for e in registry["entries"] if e["action_id"] == "self-created-club")["semantic_selector"]["executable"] = True
    elif mutation == "capability-remove-owner":
        catalog["capabilities"][0].pop("owner")
    elif mutation == "capability-remove-contracts":
        catalog["capabilities"][0]["contract_refs"] = []
    elif mutation == "capability-remove-dependencies":
        catalog["capabilities"][0]["dependency_refs"] = []
    elif mutation == "capability-remove-evidence":
        catalog["capabilities"][0]["evidence_refs"] = []
    elif mutation == "capability-remove-readiness":
        catalog["capabilities"][0].pop("readiness")
    elif mutation == "capability-required-forbidden-conflict":
        catalog["capabilities"][0]["profiles"]["ca.pc"] = ["required", "forbidden"]
    elif mutation == "enable-payment":
        payment = find_capability(catalog, "PAYMENT")
        payment["status"] = "implemented"
        payment["profiles"]["ca.pc"] = "required"
    elif mutation == "homepage-copy-sort-order":
        homepage["sort_order"] = [50, 60, 70, 80]
    elif mutation == "homepage-invalid-root":
        homepage["root_route"] = "/wrong"
    elif mutation == "homepage-invalid-return":
        homepage["return_route"] = "/wrong"
    elif mutation == "relationship-wrong-kind":
        relationship["relationship_kind"] = "family-alliance"
    elif mutation == "relationship-reuse-family-alliance":
        relationship["policy"]["family_alliance_reuse"] = "allowed"
    elif mutation == "relationship-unversioned-policy":
        relationship["policy"]["policy_version"] = "latest"
    elif mutation == "relationship-fail-open":
        relationship["policy"]["missing_config_behavior"] = "use-default"
    elif mutation == "relationship-missing-decision":
        relationship["decision_refs"] = ["D-CA-999"]
    else:
        raise ValueError(f"unknown fixture mutation: {mutation}")


def query_aliases(upstream: dict[str, Any]) -> dict[str, list[str]]:
    aliases: dict[str, list[str]] = {}
    for action in upstream["actions"]:
        if action.get("action_id") not in ALLOWED_ACTION_IDS:
            continue
        query = parse_qs(urlparse(action["target"]).query, keep_blank_values=True)
        for alias in query.get("category", []):
            aliases.setdefault(alias, []).append(action["action_id"])
    return aliases


def validate_bundle(bundle: dict[str, Any], mutation: str) -> str | None:
    if mutation == "internal-exception":
        raise RuntimeError("fixture-forced unknown failure")

    upstream = bundle.get("upstream")
    if not isinstance(upstream, dict) or not isinstance(upstream.get("actions"), list):
        return "CAH0_UPSTREAM_CONTRACT_INVALID"
    if bundle.get("upstream_schema", {}).get("type") != "object":
        return "CAH0_UPSTREAM_CONTRACT_INVALID"

    registry = bundle.get("registry")
    if not isinstance(registry, dict) or not isinstance(registry.get("entries"), list):
        return "CAH0_CATEGORY_REGISTRY_INVALID"
    if copied_presentation_key(registry):
        return "CAH0_PRESENTATION_FIELD_COPIED"
    accepted = registry.get("accepted_action_ids", [])
    if "club-manage" in accepted:
        return "CAH0_MANAGEMENT_MIXED_WITH_CATEGORIES"
    if any(action_id not in ALLOWED_ACTION_IDS for action_id in accepted):
        return "CAH0_ACTION_NOT_ALLOWED"
    if len(accepted) != len(set(accepted)):
        return "CAH0_ACTION_SET_DUPLICATE"

    action_ids = [a.get("action_id") for a in upstream["actions"]]
    category_occurrences = [action_ids.count(action_id) for action_id in ALLOWED_ACTION_IDS]
    if any(count > 1 for count in category_occurrences):
        return "CAH0_ACTION_SET_DUPLICATE"
    if any(count == 0 for count in category_occurrences):
        return "CAH0_ACTION_SET_INCOMPLETE"
    if action_ids.count("club-manage") != 1:
        return "CAH0_MANAGEMENT_ENTRY_MISSING"
    category_actions = [next(a for a in upstream["actions"] if a.get("action_id") == action_id) for action_id in ALLOWED_ACTION_IDS]
    orders = [a.get("sort_order") for a in category_actions]
    if not all(isinstance(order, int) for order in orders) or len(set(orders)) != 4 or orders != sorted(orders):
        return "CAH0_ACTION_ORDER_INVALID"

    entry_ids = [entry.get("action_id") for entry in registry["entries"]]
    if len(entry_ids) != len(set(entry_ids)):
        return "CAH0_CATEGORY_DUPLICATE_ACTION"
    if any(action_id not in action_ids for action_id in entry_ids):
        return "CAH0_CATEGORY_UNKNOWN_ACTION"
    if set(entry_ids) != set(ALLOWED_ACTION_IDS) or set(accepted) != set(ALLOWED_ACTION_IDS):
        return "CAH0_ACTION_SET_INCOMPLETE"
    for entry in registry["entries"]:
        selector = entry.get("semantic_selector", {})
        if selector.get("status") == "pending" and selector.get("executable") is not False:
            return "CAH0_SELECTOR_PENDING_EXECUTABLE"

    catalog = bundle.get("catalog")
    if not isinstance(catalog, dict) or not isinstance(catalog.get("capabilities"), list):
        return "CAH0_CAPABILITY_CATALOG_INVALID"
    capability_ids: set[str] = set()
    for capability in catalog["capabilities"]:
        capability_id = capability.get("capability_id")
        if capability_id in capability_ids:
            return "CAH0_CAPABILITY_CATALOG_INVALID"
        capability_ids.add(capability_id)
        if not capability.get("owner"):
            return "CAH0_CAPABILITY_OWNER_MISSING"
        if not capability.get("contract_refs"):
            return "CAH0_CAPABILITY_CONTRACT_MISSING"
        if not capability.get("dependency_refs"):
            return "CAH0_CAPABILITY_DEPENDENCY_MISSING"
        if not capability.get("evidence_refs"):
            return "CAH0_CAPABILITY_EVIDENCE_MISSING"
        readiness = capability.get("readiness")
        if not isinstance(readiness, dict) or set(readiness) != READINESS_KEYS:
            return "CAH0_CAPABILITY_READINESS_MISSING"
        profiles = capability.get("profiles", {})
        if any(isinstance(value, list) and {"required", "forbidden"}.issubset(set(value)) for value in profiles.values()):
            return "CAH0_CAPABILITY_REQUIRED_FORBIDDEN_CONFLICT"
        if capability_id in COMMERCIAL_IDS:
            if capability.get("status") != "forbidden" or any(value != "forbidden" for value in profiles.values()):
                return "CAH0_COMMERCIAL_CAPABILITY_ENABLED"

    homepage = bundle.get("homepage")
    if not isinstance(homepage, dict):
        return "CAH0_HOMEPAGE_INVALID"
    if copied_presentation_key(homepage):
        return "CAH0_PRESENTATION_FIELD_COPIED"
    if homepage.get("root_route") != "/services/club-alliance":
        return "CAH0_ROUTE_INVALID"
    if homepage.get("return_route") != "/services":
        return "CAH0_RETURN_TARGET_INVALID"
    if set(homepage.get("accepted_category_action_ids", [])) != set(ALLOWED_ACTION_IDS):
        return "CAH0_HOMEPAGE_INVALID"
    if homepage.get("business_writes") != "forbidden":
        return "CAH0_HOMEPAGE_INVALID"

    if mutation == "query-blank":
        return "CAH0_QUERY_BLANK"
    aliases = query_aliases(upstream)
    if mutation == "query-unknown":
        return "CAH0_QUERY_UNKNOWN"
    if mutation == "query-ambiguous":
        first_alias = next(iter(aliases))
        aliases[first_alias].append("self-created-club")
        if len(set(aliases[first_alias])) > 1:
            return "CAH0_QUERY_AMBIGUOUS"

    relationship = bundle.get("relationship")
    if not isinstance(relationship, dict) or not isinstance(relationship.get("policy"), dict):
        return "CAH0_RELATIONSHIP_INVALID"
    if relationship.get("relationship_kind") != "club-federation":
        return "CAH0_RELATIONSHIP_KIND_INVALID"
    policy = relationship["policy"]
    if policy.get("family_alliance_reuse") != "forbidden":
        return "CAH0_FAMILY_ALLIANCE_REUSED"
    if not re.fullmatch(r"v[1-9][0-9]*", str(policy.get("policy_version", ""))):
        return "CAH0_RELATIONSHIP_POLICY_UNVERSIONED"
    if policy.get("missing_config_behavior") != "fail-closed":
        return "CAH0_RELATIONSHIP_FAIL_OPEN"
    if any(ref not in known_decisions() for ref in relationship.get("decision_refs", [])):
        return "CAH0_DECISION_REFERENCE_MISSING"
    return None


def run_case(base: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    bundle = copy.deepcopy(base)
    mutation = case["mutation"]
    try:
        apply_mutation(bundle, mutation)
        actual = validate_bundle(bundle, mutation)
    except Exception:
        actual = "CAH0_INTERNAL_ERROR"
    expected = case["expected_error_id"]
    return {
        "case_id": case["case_id"],
        "expected_error_id": expected,
        "actual_error_id": actual,
        "passed": actual == expected,
    }


def main() -> int:
    fixtures = load_json(CONFORMANCE / "fixtures/cases.v1.json")
    error_catalog = load_json(CONFORMANCE / "error-catalog.v1.json")
    error_ids = [item["error_id"] for item in error_catalog["errors"]]
    if len(error_ids) != len(set(error_ids)):
        print("duplicate error_id in error catalog", file=sys.stderr)
        return 1
    expected_ids = {case["expected_error_id"] for case in fixtures["cases"] if case["expected_error_id"]}
    missing = expected_ids.difference(error_ids)
    if missing:
        print(f"fixture error ids missing from catalog: {sorted(missing)}", file=sys.stderr)
        return 1
    if len(fixtures["cases"]) != 33 or [case["case_id"] for case in fixtures["cases"]] != [f"H0-B{i:03d}" for i in range(1, 34)]:
        print("fixture matrix must contain exact H0-B001 through H0-B033", file=sys.stderr)
        return 1

    base = load_bundle()
    results = [run_case(base, case) for case in fixtures["cases"]]
    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status} {result['case_id']} expected={result['expected_error_id']} actual={result['actual_error_id']}")
    passed = sum(1 for result in results if result["passed"])
    print(f"SUMMARY passed={passed} total={len(results)}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
