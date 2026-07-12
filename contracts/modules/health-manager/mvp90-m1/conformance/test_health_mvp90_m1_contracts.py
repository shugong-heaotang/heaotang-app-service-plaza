import copy
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[5]
M0 = ROOT / "contracts/modules/health-manager/mvp90"
M1 = ROOT / "contracts/modules/health-manager/mvp90-m1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(instance, schema):
    return list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance))


def resolve_ref(ref: str):
    path_text, pointer = ref.split("#", 1)
    value = load(ROOT / path_text)
    for token in pointer.lstrip("/").split("/") if pointer else []:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def assert_boundary_consistency(contract, signed_decision):
    signed_by_id = {item["action_id"]: item for item in signed_decision["actions"]}
    for boundary in contract["boundaries"]:
        source = resolve_ref(contract["source_decision"] + boundary["source_pointer"])
        assert source["action_id"] == boundary["action_id"]
        assert source == signed_by_id[boundary["action_id"]]
        assert source["ai"]["proposed_decision"] == boundary["ai"]
        assert source["health_manager"]["proposed_decision"] == boundary["health_manager"]
        assert source["doctor"]["proposed_decision"] == boundary["professional"]
        assert source["fail_closed_result"] == boundary["fail_closed"]
        assert source["transfer_escalation_responsibility"] == boundary["transfer_owner"]


def assert_scenario_consistency(contract):
    for scenario in contract["scenarios"]:
        review = resolve_ref(scenario["review_source_ref"])
        m0 = resolve_ref(scenario["m0_source_ref"])
        assert review["scenario_id"] == scenario["scenario_id"]
        assert m0["scenario_id"] == scenario["scenario_id"]
        assert review["decision_status"] == scenario["professional_status"] == "Accepted"
        assert review["title_zh"] == scenario["title_zh"]
        assert review["proposed_safe_outcome"] == scenario["safe_outcome"]
        assert review["proposed_forbidden_outcome"] == scenario["forbidden_outcome"]
        assert review["stop_or_transfer_condition"] == scenario["stop_or_transfer"]


def assert_fixture_consistency(fixtures):
    records = fixtures["fixtures"]
    assert len(records) == 15
    expected_numbers = range(1, 16)
    expected_fixture_ids = {f"HMM1-F{i:03d}" for i in expected_numbers}
    expected_scenario_ids = {f"MVP-A{i:03d}" for i in expected_numbers}
    expected_members = {f"syn-member-{i:03d}" for i in expected_numbers}
    expected_requests = {f"syn-request-{i:03d}" for i in expected_numbers}
    assert {x["fixture_id"] for x in records} == expected_fixture_ids
    assert {x["scenario_id"] for x in records} == expected_scenario_ids
    assert {x["member_ref"] for x in records} == expected_members
    assert {x["request_ref"] for x in records} == expected_requests
    assert all(len({x[field] for x in records}) == 15 for field in ("fixture_id", "scenario_id", "member_ref", "request_ref"))


class HealthMvp90M1ContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vertical = load(M1 / "vertical-slice.v1.json")
        cls.vertical_schema = load(M1 / "vertical-slice.v1.schema.json")
        cls.boundaries = load(M1 / "professional-boundaries.v1.json")
        cls.boundaries_schema = load(M1 / "professional-boundaries.v1.schema.json")
        cls.scenarios = load(M1 / "synthetic-pdcar-scenarios.v1.json")
        cls.scenarios_schema = load(M1 / "synthetic-pdcar-scenarios.v1.schema.json")
        cls.security = load(M1 / "security-authorization.v1.json")
        cls.security_schema = load(M1 / "security-authorization.v1.schema.json")
        cls.fixtures = load(M1 / "conformance/fixtures/synthetic-pdcar-fixtures.v1.json")
        cls.fixtures_schema = load(M1 / "conformance/fixtures/synthetic-pdcar-fixtures.v1.schema.json")
        cls.objects = load(M0 / "object-model.v1.json")
        cls.states = load(M0 / "state-machines.v1.json")
        cls.roles = load(M0 / "role-actions.v1.json")
        cls.m0_scenarios = load(M0 / "synthetic-scenarios.v1.json")
        cls.c4 = load(M1 / "readiness/c4-h01-action-boundary-decision.v1.json")
        cls.template = load(M1 / "readiness/m1-lifestyle-template-signoff.v1.json")
        cls.professional_scenarios = load(M1 / "readiness/m1-professional-scenario-review.v1.json")

    def test_all_contracts_validate(self):
        for instance, schema in (
            (self.vertical, self.vertical_schema),
            (self.boundaries, self.boundaries_schema),
            (self.scenarios, self.scenarios_schema),
            (self.security, self.security_schema),
            (self.fixtures, self.fixtures_schema),
        ):
            self.assertEqual([], validate(instance, schema))

    def test_exact_sets_and_non_executable_scope(self):
        self.assertFalse(self.vertical["executable"])
        self.assertFalse(self.boundaries["executable"])
        self.assertFalse(self.scenarios["executable"])
        self.assertFalse(self.security["decision"]["executable"])
        self.assertEqual({f"M1-S{i:02d}" for i in range(1, 11)}, {x["step_id"] for x in self.vertical["steps"]})
        self.assertEqual(list(range(1, 11)), [x["sequence"] for x in self.vertical["steps"]])
        self.assertEqual({x["action_id"] for x in self.c4["actions"]}, {x["action_id"] for x in self.boundaries["boundaries"]})
        expected_scenarios = {f"MVP-A{i:03d}" for i in range(1, 16)}
        self.assertEqual(expected_scenarios, {x["scenario_id"] for x in self.scenarios["scenarios"]})
        self.assertEqual(expected_scenarios, {x["scenario_id"] for x in self.fixtures["fixtures"]})

    def test_vertical_references_m0_objects_states_roles_and_security_denials(self):
        object_ids = {x["object_id"] for x in self.objects["objects"]}
        role_ids = {x["role_id"] for x in self.roles["roles"]}
        denial_ids = {x["condition"] for x in self.security["server_denial_matrix"]}
        boundary_ids = {x["action_id"] for x in self.boundaries["boundaries"]}
        transitions = set()
        for machine in self.states["machines"]:
            for transition in machine["transitions"]:
                transitions.add(f"{machine['machine_id']}:{transition['from']}->{transition['to']}:{transition['event']}")
        for step in self.vertical["steps"]:
            self.assertLessEqual(set(step["object_refs"]), object_ids)
            self.assertLessEqual(set(step["actor_roles"]), role_ids)
            self.assertLessEqual(set(step["machine_transition_refs"]), transitions)
            self.assertLessEqual(set(step["fail_closed_conditions"]), denial_ids)
            self.assertLessEqual(set(step["professional_boundary_refs"]), boundary_ids)

    def test_professional_boundaries_are_faithful_to_signed_decision(self):
        assert_boundary_consistency(self.boundaries, self.c4)
        self.assertEqual("Accepted", self.c4["decision_status"])
        self.assertEqual("Accepted", self.template["decision_status"])
        self.assertFalse(self.template["executable"])

    def test_scenarios_align_with_m0_and_professional_review(self):
        assert_scenario_consistency(self.scenarios)
        m0 = {x["scenario_id"]: x for x in self.m0_scenarios["scenarios"]}
        professional = {x["scenario_id"]: x for x in self.professional_scenarios["scenarios"]}
        denial_ids = {x["condition"] for x in self.security["server_denial_matrix"]}
        step_ids = {x["step_id"] for x in self.vertical["steps"]}
        for scenario in self.scenarios["scenarios"]:
            scenario_id = scenario["scenario_id"]
            self.assertIn(scenario_id, m0)
            self.assertEqual("Accepted", professional[scenario_id]["decision_status"])
            self.assertEqual(professional[scenario_id]["title_zh"], scenario["title_zh"])
            self.assertLessEqual(set(scenario["security_denials"]), denial_ids)
            self.assertLessEqual(set(scenario["required_step_refs"]), step_ids)
        self.assertEqual("Accepted", self.professional_scenarios["overall_status"])

    def test_fixed_seed_fixtures_are_synthetic_and_complete(self):
        self.assertTrue(self.fixtures["synthetic_only"])
        self.assertEqual(self.scenarios["seed"], self.fixtures["seed"])
        assert_fixture_consistency(self.fixtures)
        scenario_fixture = {x["scenario_id"]: x["fixture_id"] for x in self.scenarios["scenarios"]}
        for fixture in self.fixtures["fixtures"]:
            self.assertEqual(scenario_fixture[fixture["scenario_id"]], fixture["fixture_id"])
            self.assertRegex(fixture["member_ref"], r"^syn-member-\d{3}$")
            self.assertRegex(fixture["request_ref"], r"^syn-request-\d{3}$")
            serialized = json.dumps(fixture, ensure_ascii=False)
            self.assertIsNone(re.search(r"\b1[3-9]\d{9}\b|\b\d{17}[0-9Xx]\b|@", serialized))

    def test_pending_privacy_and_production_gates_remain_closed(self):
        dependencies = {x["decision_id"]: x for x in self.security["external_dependencies"]}
        self.assertEqual("Accepted", dependencies["C4-H01"]["status"])
        self.assertEqual("Accepted", dependencies["M1-LIFESTYLE-TEMPLATE"]["status"])
        self.assertEqual("Pending with owner", dependencies["C4-L02-L04"]["status"])
        self.assertIn("C4-L02-L04", self.vertical["pending_gates"])
        self.assertIn("C4-H06-global", self.vertical["pending_gates"])

    def test_schema_negative_mutations_reject_missing_ids_and_scope_escape(self):
        mutations = []
        vertical = copy.deepcopy(self.vertical)
        vertical["steps"].pop()
        mutations.append((vertical, self.vertical_schema))
        boundaries = copy.deepcopy(self.boundaries)
        boundaries["boundaries"].pop()
        mutations.append((boundaries, self.boundaries_schema))
        scenarios = copy.deepcopy(self.scenarios)
        scenarios["scenarios"].pop()
        mutations.append((scenarios, self.scenarios_schema))
        scope_escape = copy.deepcopy(self.scenarios)
        scope_escape["synthetic_only"] = False
        mutations.append((scope_escape, self.scenarios_schema))
        executable = copy.deepcopy(self.vertical)
        executable["executable"] = True
        mutations.append((executable, self.vertical_schema))
        for instance, schema in mutations:
            self.assertTrue(validate(instance, schema))

    def test_boundary_semantic_drift_and_bad_pointer_are_rejected(self):
        for field in ("fail_closed", "transfer_owner"):
            mutation = copy.deepcopy(self.boundaries)
            mutation["boundaries"][0][field] += " 漂移"
            with self.assertRaises(AssertionError):
                assert_boundary_consistency(mutation, self.c4)
        mutation = copy.deepcopy(self.boundaries)
        mutation["boundaries"][0]["source_pointer"] = "#/actions/1"
        with self.assertRaises(AssertionError):
            assert_boundary_consistency(mutation, self.c4)

    def test_scenario_semantic_drift_and_bad_pointers_are_rejected(self):
        for field in ("safe_outcome", "forbidden_outcome", "stop_or_transfer"):
            mutation = copy.deepcopy(self.scenarios)
            mutation["scenarios"][0][field] += " 漂移"
            with self.assertRaises(AssertionError):
                assert_scenario_consistency(mutation)
        for field in ("review_source_ref", "m0_source_ref"):
            mutation = copy.deepcopy(self.scenarios)
            mutation["scenarios"][0][field] = mutation["scenarios"][1][field]
            with self.assertRaises(AssertionError):
                assert_scenario_consistency(mutation)

    def test_fixture_duplicate_and_reference_mutations_are_rejected(self):
        duplicate = copy.deepcopy(self.fixtures)
        duplicate["fixtures"][-1] = copy.deepcopy(duplicate["fixtures"][0])
        self.assertTrue(validate(duplicate, self.fixtures_schema))
        with self.assertRaises(AssertionError):
            assert_fixture_consistency(duplicate)
        duplicate_member = copy.deepcopy(self.fixtures)
        duplicate_member["fixtures"][-1]["member_ref"] = duplicate_member["fixtures"][0]["member_ref"]
        with self.assertRaises(AssertionError):
            assert_fixture_consistency(duplicate_member)


if __name__ == "__main__":
    unittest.main()
