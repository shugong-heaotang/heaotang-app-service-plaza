from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
MODULE = ROOT / "contracts" / "modules" / "learning-plaza"
ARCHITECTURE = MODULE / "m0-r2" / "learning-plaza-architecture.v3.json"
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
        if case["ai_enabled"] and not case["ai_passed"]:
            return "deny"
        if case["human_enabled"] and not case["human_passed"]:
            return "deny"
        if not case["ai_enabled"] and not case["human_enabled"]:
            return "allow" if case["authorized_publisher"] and case["audit_complete"] else "deny"
        return "allow"
    if operation == "nova":
        policy = contract["nova_learning_assistant"]
        if case["action"] in policy["prohibited_actions"]:
            return "deny"
        return "allow" if len(case["citations"]) >= policy["minimum_citations"] else "deny"
    if operation == "catalog":
        expected_owner = "learning-plaza" if case["product_kind"] == "knowledge" else "protection-mall"
        return "allow" if case["catalog_owner"] == expected_owner else "deny"
    if operation == "event":
        key = case["idempotency_key"]
        return "allow" if case["source"] == "learning-plaza" and key and key not in case["seen_keys"] else "deny"
    if operation == "port":
        return "allow" if case["readiness"] == "verified" else "deny"
    if operation == "course-loop":
        return "allow" if case["steps"] == contract["first_course_loop"] else "deny"
    return "deny"


def validate_contract(contract: dict) -> list[str]:
    errors: list[str] = []
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
    event = contract.get("growth_event", {})
    if event.get("source_of_truth") != "learning-plaza" or "never-write-consumer-database" not in event.get("write_policy", ""):
        errors.append("learning facts must remain owned by learning plaza")
    if any(port.get("failure_policy") != "fail-closed" for port in contract.get("ports", [])):
        errors.append("all provisional ports must fail closed")
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
    errors = validate_contract(contract) + validate_platform_dependencies()
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
