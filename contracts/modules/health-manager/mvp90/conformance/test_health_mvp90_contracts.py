#!/usr/bin/env python3
"""Health Manager MVP-90 M0 contract and synthetic fixture conformance."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "contracts/modules/health-manager/mvp90"
FIXTURES = MODULE / "conformance/fixtures"
SEED = "HEAOTANG-HM-MVP90-M0-20260712-V1"
EXPECTED_OBJECT_IDS = {
    "MemberServiceRelationship", "ConsentGrant", "HealthProfileItem", "AssessmentSession",
    "HealthGoal", "HealthPlan", "HealthPlanVersion", "HealthTask", "TaskFeedback", "CheckRecord",
    "RiskEvent", "HumanHandoff", "CommunicationRecord", "ServiceRecord", "TemplateVersion", "AuditEvent",
}
EXPECTED_MACHINE_IDS = {
    "health-management-entry", "health-plan-version", "health-task",
    "risk-event", "human-handoff", "consent-grant",
}
EXPECTED_ROLE_IDS = {"member", "ai", "health_manager", "professional", "doctor_group", "platform"}
EXPECTED_SCENARIO_IDS = [f"MVP-A{i:03d}" for i in range(1, 16)]
PHONE_PATTERN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
NATIONAL_ID_PATTERN = re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\w)")
JWT_PATTERN = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load_generator_module():
    path = FIXTURES / "generate_synthetic_fixtures.py"
    spec = importlib.util.spec_from_file_location("health_m0_fixture_generator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("fixture generator cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_bundle() -> dict[str, Any]:
    return {
        "object_model": load_json(MODULE / "object-model.v1.json"),
        "state_machines": load_json(MODULE / "state-machines.v1.json"),
        "role_actions": load_json(MODULE / "role-actions.v1.json"),
        "scenarios": load_json(MODULE / "synthetic-scenarios.v1.json"),
        "fixtures": load_json(FIXTURES / "mvp90-synthetic-fixtures.v1.json"),
    }


def schema_pairs() -> list[tuple[Path, Path]]:
    return [
        (MODULE / "object-model.v1.json", MODULE / "object-model.v1.schema.json"),
        (MODULE / "state-machines.v1.json", MODULE / "state-machines.v1.schema.json"),
        (MODULE / "role-actions.v1.json", MODULE / "role-actions.v1.schema.json"),
        (MODULE / "synthetic-scenarios.v1.json", MODULE / "synthetic-scenarios.v1.schema.json"),
        (FIXTURES / "mvp90-synthetic-fixtures.v1.json", FIXTURES / "synthetic-fixtures.v1.schema.json"),
    ]


def validate_semantics(bundle: dict[str, Any]) -> str | None:
    objects = bundle["object_model"].get("objects", [])
    object_ids = [item.get("object_id") for item in objects]
    if len(objects) != 16 or len(set(object_ids)) != 16 or set(object_ids) != EXPECTED_OBJECT_IDS:
        return "HMM0_OBJECT_SET_INVALID"
    if any(not item.get("owner") or not item.get("version") or not item.get("forbidden_fields") for item in objects):
        return "HMM0_OBJECT_GOVERNANCE_MISSING"

    pending = bundle["object_model"].get("pending_decisions", [])
    pending_ids = [item.get("decision_id") for item in pending]
    if len(pending) != 27 or len(set(pending_ids)) != 27:
        return "HMM0_PENDING_DECISION_SET_INVALID"
    if any(item.get("status") != "pending-with-owner" or item.get("executable") is not False or not item.get("owner") for item in pending):
        return "HMM0_PENDING_DECISION_EXECUTABLE"

    machines = bundle["state_machines"].get("machines", [])
    machine_ids = [machine.get("machine_id") for machine in machines]
    if len(machines) != 6 or len(set(machine_ids)) != 6 or set(machine_ids) != EXPECTED_MACHINE_IDS:
        return "HMM0_STATE_MACHINE_SET_INVALID"
    for machine in machines:
        states = set(machine.get("states", []))
        if machine.get("initial_state") not in states:
            return "HMM0_INITIAL_STATE_UNKNOWN"
        seen: set[tuple[str, str, str]] = set()
        allowed_pairs: set[tuple[str, str]] = set()
        for transition in machine.get("transitions", []):
            if transition.get("from") not in states or transition.get("to") not in states:
                return "HMM0_TRANSITION_STATE_UNKNOWN"
            key = (transition["from"], transition["to"], transition["event"])
            if key in seen:
                return "HMM0_TRANSITION_DUPLICATE"
            seen.add(key)
            allowed_pairs.add((transition["from"], transition["to"]))
        for forbidden in machine.get("forbidden_transitions", []):
            if forbidden.get("from") not in states or forbidden.get("to") not in states:
                return "HMM0_TRANSITION_STATE_UNKNOWN"
            if (forbidden["from"], forbidden["to"]) in allowed_pairs:
                return "HMM0_FORBIDDEN_TRANSITION_ALLOWED"

    roles = bundle["role_actions"].get("roles", [])
    role_ids = [role.get("role_id") for role in roles]
    if len(roles) != 6 or len(set(role_ids)) != 6 or set(role_ids) != EXPECTED_ROLE_IDS:
        return "HMM0_ROLE_SET_INVALID"
    scope = bundle["role_actions"].get("scope_naming", {})
    if scope.get("status") != "pending-with-owner" or scope.get("executable") is not False or scope.get("scope_name") is not None:
        return "HMM0_FINAL_SCOPE_PREMATURE"
    for role in roles:
        allowed = set(role.get("allowed_actions", []))
        forbidden = set(role.get("forbidden_actions", []))
        if allowed.intersection(forbidden):
            return "HMM0_ROLE_ACTION_CONFLICT"
        auth = role.get("server_authorization", {})
        if auth.get("required") is not True or auth.get("missing_behavior") != "fail-closed":
            return "HMM0_AUTHORIZATION_FAIL_OPEN"
    ai = next(role for role in roles if role["role_id"] == "ai")
    if not {"DIAGNOSE", "PRESCRIBE", "CHANGE_MEDICATION", "CLOSE_PROFESSIONAL_RISK", "CLOSE_EMERGENCY_RISK"}.issubset(set(ai["forbidden_actions"])):
        return "HMM0_AI_BOUNDARY_MISSING"

    scenarios = bundle["scenarios"].get("scenarios", [])
    scenario_ids = [item.get("scenario_id") for item in scenarios]
    if scenario_ids != EXPECTED_SCENARIO_IDS or len({item.get("fixture_id") for item in scenarios}) != 15:
        return "HMM0_SCENARIO_SET_INVALID"
    for scenario in scenarios:
        if any(ref not in EXPECTED_OBJECT_IDS for ref in scenario.get("contract_refs", [])):
            return "HMM0_SCENARIO_OBJECT_REF_UNKNOWN"

    fixture_items = bundle["fixtures"].get("fixtures", [])
    if [item.get("scenario_id") for item in fixture_items] != EXPECTED_SCENARIO_IDS:
        return "HMM0_FIXTURE_SET_INVALID"
    if bundle["fixtures"].get("generator", {}).get("seed") != SEED:
        return "HMM0_FIXTURE_SEED_INVALID"
    member_refs: set[str] = set()
    object_refs: set[str] = set()
    for scenario, fixture in zip(scenarios, fixture_items, strict=True):
        if fixture.get("fixture_id") != scenario.get("fixture_id"):
            return "HMM0_FIXTURE_SCENARIO_MISMATCH"
        if fixture.get("synthetic") is not True or fixture.get("environment") != "non-production" or fixture.get("seed") != SEED:
            return "HMM0_FIXTURE_NOT_SYNTHETIC"
        if fixture.get("expected_outcomes") != scenario.get("expected_outcomes") or fixture.get("forbidden_outcomes") != scenario.get("forbidden_outcomes"):
            return "HMM0_FIXTURE_EXPECTATION_DRIFT"
        inputs = fixture.get("inputs", {})
        if inputs.get("synthetic_member_ref") in member_refs or inputs.get("synthetic_object_ref") in object_refs:
            return "HMM0_FIXTURE_REFERENCE_DUPLICATE"
        member_refs.add(inputs.get("synthetic_member_ref"))
        object_refs.add(inputs.get("synthetic_object_ref"))
        without_hash = {key: value for key, value in fixture.items() if key != "canonical_sha256"}
        actual_hash = hashlib.sha256(canonical_bytes(without_hash)).hexdigest()
        if fixture.get("canonical_sha256") != actual_hash:
            return "HMM0_FIXTURE_HASH_MISMATCH"
    fixture_text = json.dumps(bundle["fixtures"], ensure_ascii=False)
    if PHONE_PATTERN.search(fixture_text) or NATIONAL_ID_PATTERN.search(fixture_text) or JWT_PATTERN.search(fixture_text) or "Bearer " in fixture_text:
        return "HMM0_FIXTURE_SENSITIVE_PATTERN"
    return None


class HealthMvp90ContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = load_bundle()

    def test_01_schema_instances(self) -> None:
        for instance_path, schema_path in schema_pairs():
            with self.subTest(instance=instance_path.name):
                Draft202012Validator(load_json(schema_path)).validate(load_json(instance_path))

    def test_02_semantic_baseline(self) -> None:
        self.assertIsNone(validate_semantics(copy.deepcopy(self.bundle)))

    def test_03_deterministic_replay_and_sha(self) -> None:
        generator = load_generator_module()
        replay_one = generator.build_bundle()
        replay_two = generator.build_bundle()
        self.assertEqual(replay_one, replay_two)
        self.assertEqual(replay_one, self.bundle["fixtures"])
        self.assertEqual(hashlib.sha256(canonical_bytes(replay_one)).hexdigest(), hashlib.sha256(canonical_bytes(replay_two)).hexdigest())

    def test_04_negative_object_set(self) -> None:
        mutated = copy.deepcopy(self.bundle)
        mutated["object_model"]["objects"].pop()
        self.assertEqual("HMM0_OBJECT_SET_INVALID", validate_semantics(mutated))

    def test_05_negative_pending_execution(self) -> None:
        mutated = copy.deepcopy(self.bundle)
        mutated["object_model"]["pending_decisions"][0]["executable"] = True
        self.assertEqual("HMM0_PENDING_DECISION_EXECUTABLE", validate_semantics(mutated))

    def test_06_negative_unknown_transition(self) -> None:
        mutated = copy.deepcopy(self.bundle)
        mutated["state_machines"]["machines"][0]["transitions"][0]["to"] = "unknown_state"
        self.assertEqual("HMM0_TRANSITION_STATE_UNKNOWN", validate_semantics(mutated))

    def test_07_negative_forbidden_transition_allowed(self) -> None:
        mutated = copy.deepcopy(self.bundle)
        machine = next(item for item in mutated["state_machines"]["machines"] if item["machine_id"] == "health-management-entry")
        machine["transitions"].append({"from":"emergency_guidance","to":"continue_allowed","event":"FAIL_OPEN","required_actor_roles":["ai"]})
        self.assertEqual("HMM0_FORBIDDEN_TRANSITION_ALLOWED", validate_semantics(mutated))

    def test_08_negative_role_conflict(self) -> None:
        mutated = copy.deepcopy(self.bundle)
        ai = next(item for item in mutated["role_actions"]["roles"] if item["role_id"] == "ai")
        ai["allowed_actions"].append("DIAGNOSE")
        self.assertEqual("HMM0_ROLE_ACTION_CONFLICT", validate_semantics(mutated))

    def test_09_negative_scope_premature(self) -> None:
        mutated = copy.deepcopy(self.bundle)
        mutated["role_actions"]["scope_naming"].update({"status":"accepted","executable":True,"scope_name":"health:all"})
        self.assertEqual("HMM0_FINAL_SCOPE_PREMATURE", validate_semantics(mutated))

    def test_10_negative_fixture_marker(self) -> None:
        mutated = copy.deepcopy(self.bundle)
        mutated["fixtures"]["fixtures"][0]["synthetic"] = False
        self.assertEqual("HMM0_FIXTURE_NOT_SYNTHETIC", validate_semantics(mutated))

    def test_11_negative_fixture_sensitive_pattern(self) -> None:
        mutated = copy.deepcopy(self.bundle)
        fixture = mutated["fixtures"]["fixtures"][0]
        fixture["inputs"]["display_marker"] = "合成验收数据 13800138000"
        without_hash = {key: value for key, value in fixture.items() if key != "canonical_sha256"}
        fixture["canonical_sha256"] = hashlib.sha256(canonical_bytes(without_hash)).hexdigest()
        self.assertEqual("HMM0_FIXTURE_SENSITIVE_PATTERN", validate_semantics(mutated))

    def test_12_fixture_file_hash_stable(self) -> None:
        first = hashlib.sha256((FIXTURES / "mvp90-synthetic-fixtures.v1.json").read_bytes()).hexdigest()
        second = hashlib.sha256((FIXTURES / "mvp90-synthetic-fixtures.v1.json").read_bytes()).hexdigest()
        self.assertEqual(first, second)
        print(f"FIXTURE_FILE_SHA256={first}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
