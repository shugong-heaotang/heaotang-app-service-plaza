from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_ROOT.parents[2]
FORBIDDEN_CLASSIFICATIONS = {"P1", "H1", "F1", "C1", "S1"}
ROW_LEVEL_KEYS = {
    "rows", "member_id", "name", "phone", "email", "health", "order_id",
    "payment_id", "customer_service_content", "relationship_identity", "precise_address",
}


class ContractError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema_instance(schema: dict[str, Any], instance: Any, label: str) -> None:
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda item: list(item.path))
    if errors:
        detail = "; ".join(f"{'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}" for error in errors)
        raise ContractError("SCHEMA_VALIDATION_FAILED", f"{label}: {detail}")


def recursive_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(key)
            keys.update(recursive_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(recursive_keys(child))
    return keys


def validate_policy(policy: dict[str, Any]) -> None:
    if policy.get("contract_version") != "project-brain-privacy-threshold-policy.v1":
        raise ContractError("POLICY_VERSION_INVALID", "unexpected policy version")
    if policy.get("scope") != "contract_validation_only" or policy.get("production_enabled") is not False:
        raise ContractError("PRODUCTION_ENABLEMENT_FORBIDDEN", "M1 policy may not enable production")
    rules = policy.get("rules", {})
    standard = rules.get("standard_minimum_group_size")
    high = rules.get("high_risk_minimum_group_size")
    if not isinstance(standard, int) or standard < 10:
        raise ContractError("PRIVACY_THRESHOLD_INVALID", "standard threshold must be at least 10")
    if not isinstance(high, int) or high < standard:
        raise ContractError("PRIVACY_THRESHOLD_INVALID", "high-risk threshold must not be lower than standard")
    if rules.get("suppress_below_threshold") is not True or rules.get("drill_down") is not False or rules.get("unauthorized_join") is not False:
        raise ContractError("PRIVACY_POLICY_OPEN", "suppression, no drill-down and no unauthorized join are mandatory")
    if set(policy.get("forbidden_classifications", [])) != FORBIDDEN_CLASSIFICATIONS:
        raise ContractError("FORBIDDEN_CLASSIFICATION_SET_INVALID", "all forbidden classes must be explicit")


def validate_fact(fact: dict[str, Any], policy: dict[str, Any]) -> None:
    if fact.get("classification") in FORBIDDEN_CLASSIFICATIONS:
        raise ContractError("FORBIDDEN_CLASSIFICATION", str(fact.get("classification")))
    if fact.get("classification") not in {"G0", "G1"}:
        raise ContractError("CLASSIFICATION_UNKNOWN", str(fact.get("classification")))
    if fact.get("read_mode") != "read_only" or fact.get("write_capability") != "none":
        raise ContractError("WRITE_CAPABILITY_FORBIDDEN", "every fact must be read-only with no write capability")
    required = {
        "fact_id", "title", "business_definition", "classification", "source_owner", "authority_id",
        "aggregation", "freshness", "quality_rules", "allowed_roles", "permitted_use", "failure",
        "production_eligible", "data_origin",
    }
    missing = sorted(required - set(fact))
    if missing:
        raise ContractError("FACT_REQUIRED_FIELD_MISSING", ",".join(missing))
    if fact.get("production_eligible") is not False:
        raise ContractError("PRODUCTION_ENABLEMENT_FORBIDDEN", fact["fact_id"])
    failure = fact.get("failure", {})
    expected_failure = {"missing": "Unknown", "stale": "Unknown", "quality": "No-Go", "authority_conflict": "No-Go", "unauthorized": "No-Go", "undersized": "No-Go"}
    if failure != expected_failure:
        raise ContractError("FAIL_CLOSED_POLICY_INVALID", fact["fact_id"])
    if not fact.get("quality_rules") or not fact.get("allowed_roles") or not fact.get("permitted_use"):
        raise ContractError("FACT_GOVERNANCE_EMPTY", fact["fact_id"])
    if set(fact.get("aggregation", {}).get("dimensions", [])) & set(policy.get("forbidden_dimensions", [])):
        raise ContractError("FORBIDDEN_DIMENSION", fact["fact_id"])
    if fact["classification"] == "G0":
        if fact.get("privacy_policy_id") is not None or fact.get("data_origin") != "authoritative_governance_artifact":
            raise ContractError("G0_SOURCE_POLICY_INVALID", fact["fact_id"])
    else:
        if fact.get("privacy_policy_id") != policy["policy_id"]:
            raise ContractError("G1_PRIVACY_POLICY_MISSING", fact["fact_id"])
        if fact.get("data_origin") != "synthetic_contract_fixture":
            raise ContractError("G1_REAL_SOURCE_NOT_AUTHORIZED", fact["fact_id"])
        if len(fact.get("aggregation", {}).get("dimensions", [])) > policy["rules"]["maximum_dimensions"]:
            raise ContractError("TOO_MANY_DIMENSIONS", fact["fact_id"])


def validate_source_map(source_map: dict[str, Any], facts: dict[str, dict[str, Any]], strict_evidence: bool = True) -> None:
    sources = source_map.get("sources", [])
    fact_ids = [source.get("fact_id") for source in sources]
    duplicates = sorted({fact_id for fact_id in fact_ids if fact_ids.count(fact_id) > 1})
    if duplicates:
        raise ContractError("MULTIPLE_AUTHORITIES", ",".join(str(item) for item in duplicates))
    seen: set[str] = set()
    for source in sources:
        fact_id = source.get("fact_id")
        seen.add(fact_id)
        if source.get("read_mode") != "read_only" or source.get("write_capability") != "none":
            raise ContractError("WRITE_CAPABILITY_FORBIDDEN", str(fact_id))
        if source.get("classification") in FORBIDDEN_CLASSIFICATIONS:
            raise ContractError("FORBIDDEN_CLASSIFICATION", str(source.get("classification")))
        if source.get("runtime_enabled") is not False:
            if source.get("classification") == "G1":
                raise ContractError("G1_REAL_SOURCE_NOT_AUTHORIZED", str(fact_id))
            raise ContractError("RUNTIME_ENABLEMENT_FORBIDDEN", str(fact_id))
        if source.get("classification") == "G1":
            if source.get("source_status") != "synthetic_only" or not str(source.get("authority_uri", "")).startswith("fixture://"):
                raise ContractError("G1_REAL_SOURCE_NOT_AUTHORIZED", str(fact_id))
        if strict_evidence:
            for evidence in source.get("evidence", []):
                if not (REPOSITORY_ROOT / evidence).exists():
                    raise ContractError("EVIDENCE_PATH_MISSING", evidence)
        if fact_id in facts:
            fact = facts[fact_id]
            for key in ("authority_id", "source_owner", "classification"):
                if source.get(key) != fact.get(key):
                    raise ContractError("SOURCE_MAP_MISMATCH", f"{fact_id}:{key}")
    if strict_evidence and seen != set(facts):
        raise ContractError("SOURCE_MAP_INCOMPLETE", f"expected={sorted(facts)} actual={sorted(seen)}")


def validate_result(result: dict[str, Any], facts: dict[str, dict[str, Any]], sources: dict[str, dict[str, Any]], policy: dict[str, Any]) -> None:
    classification = result.get("classification")
    if classification in FORBIDDEN_CLASSIFICATIONS:
        raise ContractError("FORBIDDEN_CLASSIFICATION", str(classification))
    if recursive_keys(result) & ROW_LEVEL_KEYS:
        raise ContractError("ROW_LEVEL_DATA_FORBIDDEN", ",".join(sorted(recursive_keys(result) & ROW_LEVEL_KEYS)))
    fact_id = result.get("fact_id")
    if fact_id not in facts:
        raise ContractError("FACT_UNKNOWN", str(fact_id))
    fact = facts[fact_id]
    source = sources[fact_id]
    for key in ("classification", "authority_id", "source_owner"):
        if result.get(key) != fact.get(key):
            raise ContractError("RESULT_CONTRACT_MISMATCH", f"{fact_id}:{key}")
    checks = result.get("checks", {})
    if checks.get("authorization") == "fail":
        raise ContractError("AUTHORIZATION_FAILED", fact_id)
    if checks.get("authority_conflict") is True:
        raise ContractError("AUTHORITY_CONFLICT", fact_id)
    if fact["data_origin"] == "synthetic_contract_fixture" and result.get("synthetic") is not True:
        raise ContractError("SYNTHETIC_PROVENANCE_REQUIRED", fact_id)
    if fact["classification"] == "G1":
        sample_size = result.get("sample_size")
        threshold = policy["rules"]["standard_minimum_group_size"]
        if not isinstance(sample_size, int) or sample_size < threshold or checks.get("privacy_threshold") != "pass":
            raise ContractError("PRIVACY_THRESHOLD_FAILED", fact_id)
        value = result.get("value")
        rounding = policy["rules"]["rounding_base"]
        if isinstance(value, (int, float)) and value % rounding != 0:
            raise ContractError("ROUNDING_POLICY_FAILED", fact_id)
        if source.get("source_status") != "synthetic_only" or source.get("runtime_enabled") is not False:
            raise ContractError("G1_REAL_SOURCE_NOT_AUTHORIZED", fact_id)
    status = result.get("status")
    if status in {"Unknown", "No-Go"}:
        if result.get("value") is not None or result.get("decision_usable") is not False:
            raise ContractError("FAIL_CLOSED_VALUE_REQUIRED_NULL", fact_id)
        return
    if status != "Trusted":
        raise ContractError("RESULT_STATUS_INVALID", str(status))
    required_checks = (
        checks.get("source_available") is True,
        checks.get("freshness") == "pass",
        checks.get("quality") == "pass",
        checks.get("authorization") == "pass",
        checks.get("authority_conflict") is False,
    )
    if not all(required_checks):
        raise ContractError("TRUSTED_REQUIRES_ALL_CHECKS", fact_id)
    if result.get("synthetic") is True and result.get("decision_usable") is not False:
        raise ContractError("SYNTHETIC_DECISION_FORBIDDEN", fact_id)
    if result.get("synthetic") is not True and result.get("decision_usable") is not True:
        raise ContractError("TRUSTED_DECISION_FLAG_REQUIRED", fact_id)
    if not result.get("evidence_hash"):
        raise ContractError("TRUSTED_EVIDENCE_REQUIRED", fact_id)


def validate_package() -> dict[str, int]:
    manifest = load_json(PACKAGE_ROOT / "package-manifest.v1.json")
    if manifest.get("runtime_enabled") is not False or manifest.get("production_enabled") is not False:
        raise ContractError("PRODUCTION_ENABLEMENT_FORBIDDEN", "package manifest")
    for relative in manifest["schemas"] + manifest["contracts"] + manifest["positive_fixtures"] + manifest["negative_fixtures"]:
        path = PACKAGE_ROOT / relative
        if not path.is_file():
            raise ContractError("MANIFEST_PATH_MISSING", relative)
        load_json(path)
    schemas = {relative: load_json(PACKAGE_ROOT / relative) for relative in manifest["schemas"]}
    for relative, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            raise ContractError("SCHEMA_INVALID", f"{relative}: {exc}") from exc
    policy = load_json(PACKAGE_ROOT / "privacy-threshold-policy.v1.json")
    validate_schema_instance(schemas["privacy-threshold-policy.v1.schema.json"], policy, "privacy-threshold-policy.v1.json")
    validate_policy(policy)
    catalog = load_json(PACKAGE_ROOT / "fact-catalog.v1.json")
    validate_schema_instance(schemas["fact-catalog.v1.schema.json"], catalog, "fact-catalog.v1.json")
    facts_list = catalog.get("facts", [])
    facts = {fact.get("fact_id"): fact for fact in facts_list}
    if len(facts) != len(facts_list):
        raise ContractError("FACT_ID_DUPLICATE", "fact IDs must be unique")
    authorities: set[str] = set()
    for fact in facts_list:
        validate_fact(fact, policy)
        authority = fact["authority_id"]
        if authority in authorities:
            raise ContractError("AUTHORITY_ID_REUSED", authority)
        authorities.add(authority)
    source_map = load_json(PACKAGE_ROOT / "source-map.v1.json")
    validate_schema_instance(schemas["source-map.v1.schema.json"], source_map, "source-map.v1.json")
    validate_source_map(source_map, facts)
    sources = {source["fact_id"]: source for source in source_map["sources"]}
    for relative in manifest["positive_fixtures"]:
        result = load_json(PACKAGE_ROOT / relative)
        validate_schema_instance(schemas["fact-result.v1.schema.json"], result, relative)
        validate_result(result, facts, sources, policy)
    negative_passed = 0
    for relative in manifest["negative_fixtures"]:
        fixture = load_json(PACKAGE_ROOT / relative)
        expected = fixture["expected_error"]
        try:
            if fixture["fixture_kind"] == "result":
                validate_result(fixture["payload"], facts, sources, policy)
            elif fixture["fixture_kind"] == "source_map":
                validate_source_map(fixture["payload"], facts, strict_evidence=False)
            elif fixture["fixture_kind"] == "fact":
                validate_fact(fixture["payload"], policy)
            else:
                raise ContractError("FIXTURE_KIND_UNKNOWN", fixture["fixture_kind"])
        except ContractError as exc:
            if exc.code != expected:
                raise ContractError("NEGATIVE_ERROR_MISMATCH", f"{relative}: expected {expected}, got {exc.code}") from exc
            negative_passed += 1
        else:
            raise ContractError("NEGATIVE_FIXTURE_ACCEPTED", relative)
    return {"facts": len(facts), "sources": len(sources), "positive": len(manifest["positive_fixtures"]), "negative": negative_passed}


def main() -> int:
    try:
        summary = validate_package()
    except (ContractError, json.JSONDecodeError, OSError, KeyError, TypeError) as exc:
        print(f"Project Brain v2 M1 contract validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "Project Brain v2 M1 contracts passed: "
        f"facts={summary['facts']} sources={summary['sources']} "
        f"positive={summary['positive']} negative_fail_closed={summary['negative']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
