from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
MODULE = ROOT / "contracts" / "modules" / "learning-plaza"
CORE_PATH = MODULE / "m0" / "learning-plaza-core.v1.json"
FIXTURES_PATH = MODULE / "m0" / "fixtures" / "cases.v1.json"
FOUNDATION_PATH = ROOT / "contracts" / "foundation" / "foundation-capabilities.v1.json"
PLATFORM_DEPS_PATH = MODULE / "platform-dependencies.v1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def decide(case: dict, core: dict) -> str:
    operation = case["operation"]
    if operation == "view":
        actor, resource = case["actor"], case["resource"]
        visibility = resource["visibility"]
        if visibility == "public":
            return "allow"
        if not actor.get("authenticated"):
            return "deny"
        if visibility == "login":
            return "allow"
        if visibility == "club_member":
            return "allow" if resource.get("club_id") in actor.get("club_ids", []) else "deny"
        if visibility == "private":
            return "allow" if actor.get("user_id") == resource.get("owner_id") else "deny"
        return "deny"
    if operation == "progress":
        allowed = core["progress_state_machine"]["transitions"].get(case["from"], [])
        return "allow" if case["to"] in allowed else "deny"
    if operation == "nova":
        policy = core["nova_policy"]
        if len(case.get("citations", [])) < policy["minimum_citations"]:
            return "deny"
        return "deny" if case.get("requested_action") in policy["prohibited_actions"] else "allow"
    if operation == "port":
        return "allow" if case["readiness"] == "verified" else "deny"
    if operation == "completion":
        key = case.get("idempotency_key")
        return "allow" if key and key not in case.get("seen_keys", []) else "deny"
    return "deny"


def validate_contract(core: dict) -> list[str]:
    errors: list[str] = []
    if core.get("contract_version") != "learning-plaza.core.v1":
        errors.append("unexpected contract version")
    if core.get("execution") != {"executable": False, "mode": "mock-only", "environment": "non-production"}:
        errors.append("M0 execution must be mock-only and non-production")
    if len(core.get("domains", [])) != 6:
        errors.append("exactly six core domains are required")
    if not {"book", "note"}.issubset(core.get("resource_types", [])):
        errors.append("reading must remain a resource type")
    if set(core.get("visibility", {})) != {"public", "login", "club_member", "private"}:
        errors.append("visibility model is incomplete")
    if core.get("nova_policy", {}).get("minimum_citations", 0) < 1:
        errors.append("Nova must require citations")
    ports = core.get("ports", [])
    if len(ports) != 4 or any(p.get("failure_policy") != "fail-closed" for p in ports):
        errors.append("all cross-module ports must fail closed")
    return errors


def validate_platform_dependencies() -> list[str]:
    foundation = load(FOUNDATION_PATH)
    available = {item["capability_id"]: item for item in foundation["capabilities"]}
    deps = load(PLATFORM_DEPS_PATH)
    errors: list[str] = []
    for requirement in deps["requires"]:
        item = available.get(requirement["capability_id"])
        if not item:
            errors.append(f"missing capability: {requirement['capability_id']}")
        elif item["status"] not in {"verified", "deployed"}:
            errors.append(f"capability not ready: {requirement['capability_id']}")
        elif item["version"] != requirement["minimum_version"]:
            errors.append(f"capability version mismatch: {requirement['capability_id']}")
    return errors


def run_self_test() -> int:
    core = load(CORE_PATH)
    errors = validate_contract(core) + validate_platform_dependencies()
    fixtures = load(FIXTURES_PATH)["cases"]
    for case in fixtures:
        actual = decide(case, core)
        if actual != case["expect"]:
            errors.append(f"{case['id']}: expected {case['expect']}, got {actual}")
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print(f"[PASS] core contract invariants")
    print(f"[PASS] platform dependencies={len(load(PLATFORM_DEPS_PATH)['requires'])}")
    print(f"[PASS] deterministic fixtures={len(fixtures)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    return run_self_test() if args.self_test else run_self_test()


if __name__ == "__main__":
    raise SystemExit(main())
