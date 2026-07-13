from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[4]
MODULE = ROOT / "contracts" / "modules" / "learning-plaza"
ARCHITECTURE = MODULE / "m0-r2" / "learning-plaza-architecture.v3.json"
SCHEMA = MODULE / "m0-r2" / "learning-plaza-architecture.v3.schema.json"
FIXTURES = MODULE / "m0-r2" / "fixtures" / "cases.v3.json"
FOUNDATION = ROOT / "contracts" / "foundation" / "foundation-capabilities.v1.json"
PLATFORM_DEPS = MODULE / "platform-dependencies.v1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def decide(case: dict, contract: dict) -> str:
    operation = case["operation"]
    if operation == "placement":
        component = case["component"]
        if component in contract["internal_apps"]:
            return "internal"
        if component in contract["connected_capabilities"]:
            return "connected"
        if component in contract["external_projects"]:
            return "external"
        return "deny"
    if operation == "club-role":
        return "deny" if case["claims_content_ownership"] else "allow"
    if operation == "review":
        policy = contract["review_policy"]
        if not case["audit_complete"]:
            return "deny"
        if case["ai_enabled"] and not case["ai_passed"]:
            return "deny"
        if case["human_enabled"] and not case["human_passed"]:
            return "deny"
        if not case["ai_enabled"] and not case["human_enabled"]:
            if policy.get("both_disabled_policy") != "authorized-publisher-with-mandatory-audit":
                return "deny"
            return "allow" if case["authorized_publisher"] else "deny"
        return "allow"
    if operation == "nova":
        policy = contract["nova_learning_assistant"]
        if case["action"] in policy["prohibited_actions"]:
            return "deny"
        return "allow" if len(case["citations"]) >= policy["minimum_citations"] else "deny"
    if operation == "catalog":
        ownership = contract["ownership"]
        expected_owner = ownership["knowledge_catalog_owner"] if case["product_kind"] == "knowledge" else ownership["non_knowledge_catalog_owner"]
        return "allow" if case["catalog_owner"] == expected_owner else "deny"
    if operation == "event":
        key = case["idempotency_key"]
        return "allow" if case["source"] == "learning-plaza" and key and key not in case["seen_keys"] else "deny"
    if operation == "port":
        port = next((item for item in contract["ports"] if item["port_id"] == case["port_id"]), None)
        if not port or port["failure_policy"] != "fail-closed":
            return "deny"
        return "allow" if port["readiness"] == "verified" else "deny"
    if operation == "port-readiness":
        port = next((item for item in contract["ports"] if item["port_id"] == case["port_id"]), None)
        return port["readiness"] if port else "missing"
    if operation == "course-loop":
        return "allow" if case["steps"] == contract["first_course_loop"] else "deny"
    return "deny"


def validate_contract(contract: dict) -> list[str]:
    errors = [f"schema: {error.message}" for error in Draft202012Validator(load(SCHEMA)).iter_errors(contract)]
    if contract.get("project_type") != "independent-general-learning-platform":
        errors.append("learning plaza must be an independent general learning platform")
    required_internal = {"course", "reading", "exam-certification", "nova-learning-assistant", "content-review-center"}
    if not required_internal.issubset(contract.get("internal_apps", [])):
        errors.append("internal application registry is incomplete")
    if "nova-ai-engine" not in contract.get("connected_capabilities", []):
        errors.append("Nova AI Engine must remain a connected shared capability")
    if contract.get("ownership", {}).get("club_content_ownership_implicit") is not False:
        errors.append("club organization cannot imply content ownership")
    review = contract.get("review_policy", {})
    if review.get("switch_change_policy") != "versioned-maker-checker":
        errors.append("review switches must use versioned maker-checker")
    required_audit_fields = {"publisher_id", "source_refs", "copyright_basis", "content_version", "published_at", "change_log", "takedown_status", "review_trace"}
    if set(review.get("mandatory_audit_fields", [])) != required_audit_fields:
        errors.append("every publish mode must retain the complete audit record")
    event = contract.get("growth_event", {})
    if event.get("source_of_truth") != "learning-plaza" or "never-write-consumer-database" not in event.get("write_policy", ""):
        errors.append("learning facts must remain owned by learning plaza")
    if any(port.get("failure_policy") != "fail-closed" for port in contract.get("ports", [])):
        errors.append("all provisional ports must fail closed")
    if any(port.get("readiness") != "provisional" for port in contract.get("ports", [])):
        errors.append("M0-R2 ports must remain provisional")
    return errors


def fixture_failures(contract: dict, cases: list[dict]) -> list[str]:
    return [case["id"] for case in cases if decide(case, contract) != case["expect"]]


def validate_mutation_gate(contract: dict, cases: list[dict]) -> list[str]:
    mutations: list[tuple[str, dict]] = []

    external = copy.deepcopy(contract)
    external["external_projects"][1] = "unknown-project"
    mutations.append(("external-project-owner", external))

    catalog = copy.deepcopy(contract)
    catalog["ownership"]["knowledge_catalog_owner"], catalog["ownership"]["non_knowledge_catalog_owner"] = (
        catalog["ownership"]["non_knowledge_catalog_owner"],
        catalog["ownership"]["knowledge_catalog_owner"],
    )
    mutations.append(("catalog-owner-swap", catalog))

    review = copy.deepcopy(contract)
    review["review_policy"]["both_disabled_policy"] = "allow-anyone-no-audit"
    mutations.append(("review-bypass", review))

    readiness = copy.deepcopy(contract)
    for port in readiness["ports"]:
        port["readiness"] = "verified"
    mutations.append(("ports-prematurely-verified", readiness))

    port_id = copy.deepcopy(contract)
    port_id["ports"][0]["port_id"] = "knowledge-base.read.v999"
    mutations.append(("port-id-drift", port_id))

    errors: list[str] = []
    schema = Draft202012Validator(load(SCHEMA))
    for name, mutated in mutations:
        schema_errors = list(schema.iter_errors(mutated))
        invariant_errors = validate_contract(mutated)
        failed_fixtures = fixture_failures(mutated, cases)
        if not schema_errors or not invariant_errors or not failed_fixtures:
            errors.append(
                f"mutation {name} escaped: schema={len(schema_errors)} "
                f"invariants={len(invariant_errors)} fixtures={len(failed_fixtures)}"
            )
    return errors


def validate_platform_dependencies() -> list[str]:
    available = {item["capability_id"]: item for item in load(FOUNDATION)["capabilities"]}
    errors: list[str] = []
    for requirement in load(PLATFORM_DEPS)["requires"]:
        capability = available.get(requirement["capability_id"])
        if not capability or capability["status"] not in {"verified", "deployed"}:
            errors.append(f"platform dependency unavailable: {requirement['capability_id']}")
    return errors


def main() -> int:
    contract = load(ARCHITECTURE)
    cases = load(FIXTURES)["cases"]
    errors = validate_contract(contract) + validate_platform_dependencies() + validate_mutation_gate(contract, cases)
    for case in cases:
        actual = decide(case, contract)
        if actual != case["expect"]:
            errors.append(f"{case['id']}: expected {case['expect']}, got {actual}")
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print("[PASS] independent project architecture invariants")
    print(f"[PASS] platform dependencies={len(load(PLATFORM_DEPS)['requires'])}")
    print(f"[PASS] deterministic fixtures={len(cases)}")
    print("[PASS] critical mutation gates=5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
