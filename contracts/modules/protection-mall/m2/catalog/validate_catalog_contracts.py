import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).parent

EXPECTED_ERRORS = {
    "MALL_CATALOG_INVALID_ARGUMENT",
    "MALL_CATALOG_UNTRUSTED_SCOPE",
    "MALL_CATALOG_FORBIDDEN",
    "MALL_CATALOG_RESPONSIBILITY_MISSING",
    "MALL_CATALOG_NOT_FOUND",
    "MALL_CATALOG_SNAPSHOT_IMMUTABLE",
    "MALL_CATALOG_BUDGET_EXCEEDED",
    "MALL_CATALOG_CURRENCY_MISMATCH",
    "MALL_CATALOG_ARITHMETIC_OVERFLOW",
    "MALL_CATALOG_REPLACEMENT_NOT_FOUND",
    "MALL_CATALOG_DUPLICATE_PLAN_ITEM",
    "MALL_BENEFIT_FORBIDDEN",
}

EXPECTED_CASES = {
    "four-kinds": "accept",
    "untrusted-scope": "MALL_CATALOG_UNTRUSTED_SCOPE",
    "kind-product-mapping-mismatch": "MALL_CATALOG_INVALID_ARGUMENT",
    "missing-seller": "MALL_CATALOG_RESPONSIBILITY_MISSING",
    "cross-seller-denied": "MALL_CATALOG_FORBIDDEN",
    "club-assurance-denied": "MALL_BENEFIT_FORBIDDEN",
    "protection-assurance-snapshot": "accept",
    "snapshot-mutation-denied": "MALL_CATALOG_SNAPSHOT_IMMUTABLE",
    "snapshot-detached": "accept",
    "compose-budget-ok": "accept",
    "compose-budget-exceeded": "MALL_CATALOG_BUDGET_EXCEEDED",
    "mixed-currency-denied": "MALL_CATALOG_CURRENCY_MISMATCH",
    "arithmetic-overflow": "MALL_CATALOG_ARITHMETIC_OVERFLOW",
    "duplicate-plan-item": "MALL_CATALOG_DUPLICATE_PLAN_ITEM",
    "replacement-missing": "MALL_CATALOG_REPLACEMENT_NOT_FOUND",
    "owner-denied": "MALL_CATALOG_FORBIDDEN",
    "plan-any-preserves-owner": "accept",
    "parallel-read-write": "race_free",
}

EXPECTED_CASE_RULES = {
    "four-kinds": "catalog_kinds",
    "untrusted-scope": "scope_source",
    "kind-product-mapping-mismatch": "kind_product_type",
    "missing-seller": "responsibility",
    "cross-seller-denied": "ownership",
    "club-assurance-denied": "assurance",
    "protection-assurance-snapshot": "assurance",
    "snapshot-mutation-denied": "snapshot",
    "snapshot-detached": "snapshot",
    "compose-budget-ok": "budget",
    "compose-budget-exceeded": "budget",
    "mixed-currency-denied": "currency",
    "arithmetic-overflow": "arithmetic",
    "duplicate-plan-item": "plan_items",
    "replacement-missing": "replace",
    "owner-denied": "plan_owner",
    "plan-any-preserves-owner": "plan_owner",
    "parallel-read-write": "concurrency",
}


def load(relative_path: str):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def require(errors, actual, expected, label):
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    contract = load("catalog.v1.json")
    schema = load("catalog.v1.schema.json")
    fixtures = load("fixtures/cases.v1.json")
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(contract)]

    require(errors, fixtures.get("contract_version"), "protection-mall.catalog-cases.v1", "fixture contract_version")
    require(errors, contract["catalog_kinds"], ["product", "service", "course", "activity"], "catalog kinds")
    require(errors, contract["responsibility"]["kind_product_type"], {
        "product": "physical", "service": "service", "course": "service", "activity": "service"
    }, "kind/product mapping")
    require(errors, contract["responsibility"]["required_fields"], [
        "mall_type", "product_type", "seller_id", "fulfillment_owner_id", "after_sale_owner_id"
    ], "responsibility fields")
    require(errors, contract["membership_plan"]["required_scope"], "catalog:plan", "membership plan scope")
    require(errors, set(contract["error_codes"]), EXPECTED_ERRORS, "stable error code set")
    require(errors, contract["catalog_entry"]["required_fields"], [
        "contract_version", "id", "kind", "title", "scene_ids", "responsibility", "price_snapshot", "benefit_snapshot"
    ], "catalog entry fields")
    require(errors, contract["snapshots"], {
        "price": ["snapshot_id", "version", "currency", "amount_minor"],
        "benefit": ["snapshot_id", "version", "grants"],
        "mutation_policy": "immutable_after_first_save",
        "copy_policy": "detached_copy",
    }, "snapshot contract")
    require(errors, contract["repository"], {
        "implementation": "in_memory_only",
        "concurrency": "safe_for_parallel_read_write",
        "external_io": False,
    }, "repository boundary")
    require(errors, contract["no_go"], [
        "database", "route", "network", "payment", "refund", "reconciliation", "real_data", "deployment", "production"
    ], "No-Go boundary")

    protection = contract["responsibility"]["assurance_policy"]["protection_mall"]
    club = contract["responsibility"]["assurance_policy"]["club_mall"]
    require(errors, protection, {
        "catalog_snapshot": "permitted", "real_grant_gate": "order_completed && after_sale_closed"
    }, "protection assurance policy")
    require(errors, club, {
        "catalog_snapshot": "forbidden", "error_code": "MALL_BENEFIT_FORBIDDEN"
    }, "club assurance policy")

    cases = fixtures.get("cases", [])
    ids = [case.get("id") for case in cases]
    if len(ids) != len(set(ids)):
        errors.append("fixture case IDs must be unique")
    actual_cases = {case.get("id"): case.get("expected") for case in cases}
    require(errors, actual_cases, EXPECTED_CASES, "named fixture cases and expected outcomes")
    actual_rules = {case.get("id"): case.get("rule") for case in cases}
    require(errors, actual_rules, EXPECTED_CASE_RULES, "named fixture rules")
    for case in cases:
        if set(case) != {"id", "rule", "input", "expected"}:
            errors.append(f"fixture {case.get('id')!r} must contain exactly id, rule, input and expected")

    by_id = {case["id"]: case for case in cases if "id" in case}
    if by_id.get("untrusted-scope", {}).get("input", {}).get("source") != "request_claim":
        errors.append("untrusted-scope must prove an untrusted scope source")
    if by_id.get("kind-product-mapping-mismatch", {}).get("input", {}).get("product_type") != "service":
        errors.append("kind-product-mapping-mismatch must prove product/service mismatch")
    if by_id.get("plan-any-preserves-owner", {}).get("input", {}).get("owner") != "member-a":
        errors.append("plan:any fixture must preserve the original plan owner")
    if by_id.get("protection-assurance-snapshot", {}).get("input", {}).get("grant_gate") != "order_completed && after_sale_closed":
        errors.append("protection assurance fixture must retain the M1 grant gate")
    if by_id.get("parallel-read-write", {}).get("input") != {"readers": 16, "writers": 16}:
        errors.append("concurrency fixture must retain the tested parallel shape")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Protection Mall M2 catalog contracts valid: 1 contract, {len(cases)} exact synthetic cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
