import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "contracts/modules/health-manager"
PLAN_PATH = BASE / "mvp90-m1/synthetic-replay-plan.v1.json"
PLAN_SCHEMA_PATH = BASE / "mvp90-m1/synthetic-replay-plan.v1.schema.json"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def split_transition(reference: str):
    machine, state_change, event = reference.split(":")
    source, target = state_change.split("->")
    return machine, source, target, event


class SyntheticReplayPlanContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = load("contracts/modules/health-manager/mvp90-m1/synthetic-replay-plan.v1.json")
        cls.schema = load("contracts/modules/health-manager/mvp90-m1/synthetic-replay-plan.v1.schema.json")
        cls.vertical = load(cls.plan["source_contracts"]["vertical_slice"])
        cls.machines = load(cls.plan["source_contracts"]["state_machines"])
        cls.actions = load(cls.plan["source_contracts"]["security_authorization"])
        cls.scenarios = load(cls.plan["source_contracts"]["scenarios"])
        cls.fixtures = load(cls.plan["source_contracts"]["fixtures"])

    def test_plan_schema_and_exact_scenario_set(self):
        Draft202012Validator(self.schema).validate(self.plan)
        expected = {f"MVP-A{i:03d}" for i in range(1, 16)}
        actual = [item["scenario_id"] for item in self.plan["scenarios"]]
        self.assertEqual(set(actual), expected)
        self.assertEqual(len(actual), len(set(actual)))
        fixture_ids = [item["fixture_id"] for item in self.plan["scenarios"]]
        self.assertEqual(len(fixture_ids), len(set(fixture_ids)))

    def test_scenario_and_fixture_source_closure(self):
        signed_by_id = {item["scenario_id"]: item for item in self.scenarios["scenarios"]}
        fixture_by_id = {item["fixture_id"]: item for item in self.fixtures["fixtures"]}
        for index, item in enumerate(self.plan["scenarios"]):
            self.assertEqual(item["scenario_source_ref"], f"{self.plan['source_contracts']['scenarios']}#/scenarios/{index}")
            self.assertEqual(item["fixture_source_ref"], f"{self.plan['source_contracts']['fixtures']}#/fixtures/{index}")
            signed = signed_by_id[item["scenario_id"]]
            fixture = fixture_by_id[item["fixture_id"]]
            self.assertEqual(signed["fixture_id"], item["fixture_id"])
            self.assertEqual(fixture["scenario_id"], item["scenario_id"])
            self.assertEqual(item["required_step_refs"], signed["required_step_refs"])

    def test_all_events_resolve_to_steps_actions_transitions_and_denials(self):
        steps = {item["step_id"]: item for item in self.vertical["steps"]}
        actions = {item["action_id"] for item in self.actions["actions"]}
        denials = {item["condition"]: item["error_id"] for item in self.actions["server_denial_matrix"]}
        machines = {item["machine_id"]: item for item in self.machines["machines"]}
        covered_steps = set()
        covered_machines = set()
        for scenario in self.plan["scenarios"]:
            for event in scenario["events"]:
                step = steps[event["step_id"]]
                covered_steps.add(event["step_id"])
                self.assertIn(event["action_id"], actions)
                denial = event["denial_expectation"]
                if event["actor_role"] not in step["actor_roles"]:
                    self.assertEqual(denial["condition"], "ai_policy_or_tool_not_allowed")
                if denial["outcome"] == "deny":
                    self.assertEqual(denials[denial["condition"]], denial["error_id"])
                    if event["transition_ref"] is None:
                        self.assertEqual(event["expected_version"]["before"], event["expected_version"]["after"])
                else:
                    self.assertIsNone(denial["condition"])
                    self.assertIsNone(denial["error_id"])
                if event["transition_ref"] is None:
                    continue
                machine_id, source, target, trigger = split_transition(event["transition_ref"])
                covered_machines.add(machine_id)
                if event["transition_ref"] not in step["machine_transition_refs"]:
                    self.assertEqual(denial["outcome"], "deny")
                transition = next(
                    candidate for candidate in machines[machine_id]["transitions"]
                    if candidate["from"] == source and candidate["to"] == target and candidate["event"] == trigger
                )
                self.assertIn(event["actor_role"], transition["required_actor_roles"])
                self.assertEqual(event["expected_from"], source)
                self.assertEqual(event["expected_to"], target)
        self.assertEqual(covered_steps, {f"M1-S{i:02d}" for i in range(1, 11)})
        self.assertEqual(covered_machines, {item["machine_id"] for item in self.machines["machines"]})

    def test_a001_covers_all_ten_steps_in_order(self):
        a001 = self.plan["scenarios"][0]
        observed = []
        for event in a001["events"]:
            if event["step_id"] not in observed:
                observed.append(event["step_id"])
        self.assertEqual(observed, [f"M1-S{i:02d}" for i in range(1, 11)])

    def test_fail_closed_schema_mutations_are_rejected(self):
        mutations = []
        missing_scenario = copy.deepcopy(self.plan)
        missing_scenario["scenarios"].pop()
        mutations.append(missing_scenario)
        promoted = copy.deepcopy(self.plan)
        promoted["executable"] = True
        mutations.append(promoted)
        real_data = copy.deepcopy(self.plan)
        real_data["synthetic_only"] = False
        mutations.append(real_data)
        unknown_action = copy.deepcopy(self.plan)
        unknown_action["scenarios"][0]["events"][0]["action_id"] = "ai.activate_plan"
        mutations.append(unknown_action)
        unknown_step = copy.deepcopy(self.plan)
        unknown_step["scenarios"][0]["events"][0]["step_id"] = "M1-S99"
        mutations.append(unknown_step)
        validator = Draft202012Validator(self.schema)
        for mutated in mutations:
            self.assertTrue(list(validator.iter_errors(mutated)))


if __name__ == "__main__":
    unittest.main()
