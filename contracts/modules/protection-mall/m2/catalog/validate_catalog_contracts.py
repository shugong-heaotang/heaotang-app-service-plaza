import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).parent

EXPECTED_ERRORS = [
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
]

EXPECTED_CASES = {
    "four-kinds": "accept",
    "missing-seller": "MALL_CATALOG_RESPONSIBILITY_MISSING",
    "kind-product-type-mismatch": "MALL_CATALOG_INVALID_ARGUMENT",
    "cross-seller-denied": "MALL_CATALOG_FORBIDDEN",
    "untrusted-scope-source": "MALL_CATALOG_UNTRUSTED_SCOPE",
    "missing-plan-scope": "MALL_CATALOG_FORBIDDEN",
    "club-assurance-denied": "MALL_BENEFIT_FORBIDDEN",
    "protection-assurance-snapshot-deferred": "accept_snapshot_only",
    "snapshot-mutation-denied": "MALL_CATALOG_SNAPSHOT_IMMUTABLE",
    "snapshot-detached": "detached_copy",
    "compose-budget-ok": "accept",
    "compose-budget-exceeded": "MALL_CATALOG_BUDGET_EXCEEDED",
    "mixed-currency-denied": "MALL_CATALOG_CURRENCY_MISMATCH",
    "arithmetic-overflow": "MALL_CATALOG_ARITHMETIC_OVERFLOW",
    "duplicate-plan-item": "MALL_CATALOG_DUPLICATE_PLAN_ITEM",
    "replacement-not-found": "MALL_CATALOG_REPLACEMENT_NOT_FOUND",
    "owner-bound-replace": "MALL_CATALOG_FORBIDDEN",
    "delegated-replace-preserves-owner": "accept_preserve_owner",
    "parallel-read-write": "race_free",
}

EXPECTED_RULES = {
    "four-kinds": "catalog_kinds",
    "missing-seller": "responsibility",
    "kind-product-type-mismatch": "kind_product_type",
    "cross-seller-denied": "ownership",
    "untrusted-scope-source": "authorization",
    "missing-plan-scope": "authorization",
    "club-assurance-denied": "assurance",
    "protection-assurance-snapshot-deferred": "assurance",
    "snapshot-mutation-denied": "snapshot",
    "snapshot-detached": "snapshot_copy",
    "compose-budget-ok": "budget",
    "compose-budget-exceeded": "budget",
    "mixed-currency-denied": "currency",
    "arithmetic-overflow": "arithmetic",
    "duplicate-plan-item": "composition",
    "replacement-not-found": "replacement",
    "owner-bound-replace": "plan_owner",
    "delegated-replace-preserves-owner": "plan_owner",
    "parallel-read-write": "concurrency",
}

EXPECTED_INPUTS = {
    "four-kinds": ["product", "service", "course", "activity"],
    "missing-seller": {"seller_id": ""},
    "kind-product-type-mismatch": {"kind": "product", "product_type": "service"},
    "cross-seller-denied": {"actor": "seller-b", "seller": "seller-a", "scopes": ["catalog:write"]},
    "untrusted-scope-source": {"source": "client_claim", "scopes": ["catalog:plan"]},
    "missing-plan-scope": {"source": "server_authorization_registry", "scopes": ["catalog:read"]},
    "club-assurance-denied": {"mall_type": "club_mall", "benefit": "assurance"},
    "protection-assurance-snapshot-deferred": {"mall_type": "protection_mall", "benefit": "assurance"},
    "snapshot-mutation-denied": {"existing": True, "changed": True},
    "snapshot-detached": {"mutate_returned_copy": True},
    "compose-budget-ok": {"budget_minor": 6000, "total_minor": 6000},
    "compose-budget-exceeded": {"budget_minor": 5999, "total_minor": 6000},
    "mixed-currency-denied": ["CNY", "USD"],
    "arithmetic-overflow": {"amount_minor": 9223372036854775807, "quantity": 2},
    "duplicate-plan-item": ["product-a", "product-a"],
    "replacement-not-found": {"old_entry_id": "missing"},
    "owner-bound-replace": {"owner": "member-a", "actor": "member-b"},
    "delegated-replace-preserves-owner": {
        "owner": "member-a", "actor": "platform-operator", "scopes": ["catalog:plan", "catalog:plan:any"]
    },
    "parallel-read-write": {"readers": 16, "writers": 16},
}


def load(relative_path: str):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def main() -> int:
    contract = load("catalog.v1.json")
    schema = load("catalog.v1.schema.json")
    fixtures = load("fixtures/cases.v1.json")
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(contract)]
    fixture_ids = [case["id"] for case in fixtures.get("cases", [])]
    fixture_by_id = {case["id"]: case for case in fixtures.get("cases", [])}
    if fixtures.get("contract_version") != "protection-mall.catalog-cases.v1":
        errors.append("fixture contract_version mismatch")
    if len(fixture_ids) != len(set(fixture_ids)):
        errors.append("fixtures must contain unique case ids")
    if contract.get("membership_plan", {}).get("required_scope") != "catalog:plan":
        errors.append("membership plan scope must match Go catalog:plan authorization")
    if contract.get("catalog_entry", {}).get("contract_version") != "mall.catalog.v1":
        errors.append("catalog entry contract_version must match Go CatalogContractVersion")
    if contract.get("error_codes") != EXPECTED_ERRORS:
        errors.append("stable error code set does not match backend catalog_m2.go")
    expected_mapping = {"product": "physical", "service": "service", "course": "service", "activity": "service"}
    if contract.get("responsibility", {}).get("kind_product_type") != expected_mapping:
        errors.append("kind to product_type mapping mismatch")
    assurance = contract.get("responsibility", {}).get("assurance_policy", {})
    if assurance.get("club_mall") != "forbidden" or assurance.get("protection_mall") != "snapshot_allowed_grant_deferred_until_order_completed_and_after_sale_closed":
        errors.append("assurance policy mismatch")
    if contract.get("membership_plan", {}).get("delegated_scope") != "catalog:plan:any" or contract.get("membership_plan", {}).get("delegated_policy") != "preserve_owner":
        errors.append("delegated replacement policy mismatch")
    expected_snapshots = {
        "price": ["snapshot_id", "version", "currency", "amount_minor"],
        "benefit": ["snapshot_id", "version", "grants"],
        "mutation_policy": "immutable_after_first_save",
        "copy_policy": "detached_copy",
    }
    if contract.get("snapshots") != expected_snapshots:
        errors.append("snapshot immutability and copy contract mismatch")
    expected_repository = {
        "implementation": "in_memory_only",
        "concurrency": "safe_for_overlapping_parallel_read_write",
        "external_io": False,
    }
    if contract.get("repository") != expected_repository:
        errors.append("repository boundary mismatch")
    expected_no_go = [
        "database", "route", "network", "payment", "refund", "reconciliation", "real_data", "deployment", "production"
    ]
    if contract.get("no_go") != expected_no_go:
        errors.append("No-Go boundary mismatch")
    for case_id, expected in EXPECTED_CASES.items():
        case = fixture_by_id.get(case_id)
        if case is None:
            errors.append(f"missing semantic fixture: {case_id}")
            continue
        if set(case) != {"id", "rule", "input", "expected"}:
            errors.append(f"{case_id} must contain exactly id, rule, input and expected")
        if case.get("expected") != expected:
            errors.append(f"{case_id} expected must be {expected}")
        if case.get("rule") != EXPECTED_RULES[case_id]:
            errors.append(f"{case_id} rule must be {EXPECTED_RULES[case_id]}")
        if case.get("input") != EXPECTED_INPUTS[case_id]:
            errors.append(f"{case_id} input mismatch")
    unexpected_cases = sorted(set(fixture_ids) - set(EXPECTED_CASES))
    if unexpected_cases:
        errors.append(f"unexpected fixtures without exact validator mapping: {unexpected_cases}")
    declared_errors = set(EXPECTED_ERRORS)
    fixture_errors = {
        case.get("expected")
        for case in fixtures.get("cases", [])
        if isinstance(case.get("expected"), str) and case["expected"].startswith("MALL_")
    }
    missing_declared = sorted(fixture_errors - declared_errors)
    if missing_declared:
        errors.append(f"fixture errors absent from contract: {missing_declared}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Protection Mall M2 catalog contracts valid: 1 contract, {len(fixture_ids)} exact synthetic cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
