import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
PLAN_REL = "contracts/modules/health-manager/mvp90-m1/synthetic-replay-plan.v1.json"
SCHEMA_REL = "contracts/modules/health-manager/mvp90-m1/synthetic-replay-plan.v1.schema.json"
SUBJECT_BY_ACTOR = {
    "member": "adult_member_self",
    "ai": "ai_runtime",
    "health_manager": "health_manager",
    "professional": "qualified_professional",
}


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def split_transition(reference: str):
    machine, state_change, event = reference.split(":")
    source, target = state_change.split("->")
    return machine, source, target, event


def resolve_pointer(reference: str, documents=None):
    path, fragment = reference.split("#", 1)
    document = documents[path] if documents and path in documents else load(path)
    value = document
    if fragment:
        if not fragment.startswith("/"):
            raise AssertionError(f"unsupported JSON pointer: {reference}")
        for token in fragment[1:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def validate_source_closure(plan, documents=None):
    vertical = documents.get(plan["source_contracts"]["vertical_slice"]) if documents else None
    vertical = vertical or load(plan["source_contracts"]["vertical_slice"])
    machine_doc = documents.get(plan["source_contracts"]["state_machines"]) if documents else None
    machine_doc = machine_doc or load(plan["source_contracts"]["state_machines"])
    security = documents.get(plan["source_contracts"]["security_authorization"]) if documents else None
    security = security or load(plan["source_contracts"]["security_authorization"])
    steps = {item["step_id"]: item for item in vertical["steps"]}
    machines = {item["machine_id"]: item for item in machine_doc["machines"]}
    actions = {item["action_id"]: item for item in security["actions"]}
    denials = {item["condition"]: item["error_id"] for item in security["server_denial_matrix"]}
    event_ids, idempotency_keys, payload_refs = [], [], []
    covered_steps, covered_machines = set(), set()

    for scenario in plan["scenarios"]:
        scenario_source = resolve_pointer(scenario["scenario_source_ref"], documents)
        fixture_source = resolve_pointer(scenario["fixture_source_ref"], documents)
        professional_source = resolve_pointer(scenario_source["review_source_ref"], documents)
        if scenario_source["scenario_id"] != scenario["scenario_id"]:
            raise AssertionError("scenario pointer does not resolve to the declared scenario_id")
        if scenario_source["fixture_id"] != scenario["fixture_id"]:
            raise AssertionError("scenario pointer does not resolve to the declared fixture_id")
        if fixture_source["scenario_id"] != scenario["scenario_id"] or fixture_source["fixture_id"] != scenario["fixture_id"]:
            raise AssertionError("fixture pointer does not resolve to the declared pair")
        if scenario["required_step_refs"] != scenario_source["required_step_refs"]:
            raise AssertionError("required steps drift from the signed scenario source")
        if not fixture_source["expected_result"]:
            raise AssertionError("fixture expected_result is missing")
        if scenario_source["safe_outcome"] != professional_source["proposed_safe_outcome"]:
            raise AssertionError("scenario safe outcome drifts from the signed professional source")

        events_by_resource = {}
        for event in scenario["events"]:
            events_by_resource.setdefault(event["resource_ref"], []).append(event)
        for resource_events in events_by_resource.values():
            for previous, current in zip(resource_events, resource_events[1:]):
                if previous["expected_to"] != current["expected_from"]:
                    raise AssertionError("same-resource state sequence is discontinuous")
                if previous["expected_version"]["after"] != current["expected_version"]["before"]:
                    raise AssertionError("same-resource version sequence is discontinuous")

        resource_types = {event["resource_ref"].split(":", 1)[0] for event in scenario["events"]}
        if fixture_source["expected_result"] == "pdcar_loop_recorded":
            if not {"RiskEvent", "HumanHandoff"}.isdisjoint(resource_types):
                raise AssertionError("normal PDCAR fixture cannot emit risk or handoff resources")
            if "无专业触发" not in scenario_source["safe_outcome"]:
                raise AssertionError("normal PDCAR profile is not closed by the signed safe outcome")
            task_events = [event for event in scenario["events"] if event["resource_ref"].startswith("HealthTask:")]
            if not task_events or task_events[-1]["expected_to"] != "recorded":
                raise AssertionError("normal PDCAR task chain does not end in recorded")
        if fixture_source["expected_result"] == "emergency_handoff_open":
            expected = "risk-event:triage_pending->emergency:CLASSIFY_EMERGENCY"
            if [event["transition_ref"] for event in scenario["events"]] != [expected]:
                raise AssertionError("emergency fixture does not use the signed emergency classification profile")
            if "紧急" not in scenario_source["safe_outcome"] or "风险开放" not in scenario_source["safe_outcome"]:
                raise AssertionError("emergency fixture is not closed by the signed safe outcome")

        for event in scenario["events"]:
            event_ids.append(event["event_id"])
            idempotency_keys.append(event["idempotency"]["key"])
            payload_refs.append(event["idempotency"]["payload_ref"])
            step = steps[event["step_id"]]
            covered_steps.add(event["step_id"])
            denial = event["denial_expectation"]
            if denial["outcome"] == "deny":
                if denials.get(denial["condition"]) != denial["error_id"]:
                    raise AssertionError("denial condition and error_id do not resolve to C4-S04")
                if event["transition_ref"] is None and event["expected_version"]["before"] != event["expected_version"]["after"]:
                    raise AssertionError("denied non-transition event changed version")
            elif denial["condition"] is not None or denial["error_id"] is not None:
                raise AssertionError("allowed event contains a denial condition")

            action_id = event["authorization_action_id"]
            resource_type = event["resource_ref"].split(":", 1)[0]
            if action_id is not None:
                action = actions[action_id]
                if action_id == "security.audit_metadata" or "business_write" in action["prohibitions"]:
                    raise AssertionError("audit metadata action cannot represent a business event")
                if resource_type not in action["resources"]:
                    raise AssertionError("authorization action does not cover the event resource")
                subject = SUBJECT_BY_ACTOR.get(event["actor_role"])
                if subject not in action["subjects"]:
                    raise AssertionError("authorization action does not cover the event actor")
                if not action["prerequisites"]:
                    raise AssertionError("authorization action has no source prerequisites")
                if action["effect"] in {"read", "read-metadata"}:
                    if event["expected_from"] != event["expected_to"] or event["expected_version"]["before"] != event["expected_version"]["after"]:
                        raise AssertionError("read-only action was used as a business write")

            transition_ref = event["transition_ref"]
            if transition_ref is None:
                if action_id is None:
                    raise AssertionError("event has neither an authorization action nor a transition")
                continue
            machine_id, source, target, trigger = split_transition(transition_ref)
            covered_machines.add(machine_id)
            transition = next(
                (
                    candidate for candidate in machines[machine_id]["transitions"]
                    if candidate["from"] == source and candidate["to"] == target and candidate["event"] == trigger
                ),
                None,
            )
            if transition is None:
                raise AssertionError("transition does not resolve to the M0 state machine")
            if event["actor_role"] not in transition["required_actor_roles"]:
                raise AssertionError("transition does not authorize the declared actor")
            if event["expected_from"] != source or event["expected_to"] != target:
                raise AssertionError("event state expectation drifts from the transition")
            if transition_ref not in step["machine_transition_refs"] and denial["outcome"] != "deny":
                raise AssertionError("allowed transition is not closed by its P1 step")

    if len(event_ids) != 25:
        raise AssertionError("replay plan must contain exactly 25 events")
    for label, values in (("event_id", event_ids), ("idempotency key", idempotency_keys), ("payload_ref", payload_refs)):
        if len(values) != len(set(values)):
            raise AssertionError(f"duplicate {label}")
    if covered_steps != {f"M1-S{i:02d}" for i in range(1, 11)}:
        raise AssertionError("replay plan does not cover all ten PDCAR steps")
    if covered_machines != set(machines):
        raise AssertionError("replay plan does not cover all six state machines")


class SyntheticReplayPlanContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = load(PLAN_REL)
        cls.schema = load(SCHEMA_REL)

    def test_plan_schema_exact_sets_and_source_closure(self):
        Draft202012Validator(self.schema).validate(self.plan)
        self.assertEqual({item["scenario_id"] for item in self.plan["scenarios"]}, {f"MVP-A{i:03d}" for i in range(1, 16)})
        self.assertEqual(len({item["fixture_id"] for item in self.plan["scenarios"]}), 15)
        validate_source_closure(self.plan)

    def test_a001_covers_all_ten_steps_in_order(self):
        a001 = self.plan["scenarios"][0]
        observed = []
        for event in a001["events"]:
            if event["step_id"] not in observed:
                observed.append(event["step_id"])
        self.assertEqual(observed, [f"M1-S{i:02d}" for i in range(1, 11)])

    def test_schema_rejects_missing_extra_unknown_and_promotion(self):
        mutations = []
        missing_scenario = copy.deepcopy(self.plan)
        missing_scenario["scenarios"].pop()
        mutations.append(missing_scenario)
        extra_event = copy.deepcopy(self.plan)
        extra_event["scenarios"][1]["events"].append(copy.deepcopy(extra_event["scenarios"][1]["events"][0]))
        mutations.append(extra_event)
        promoted = copy.deepcopy(self.plan)
        promoted["executable"] = True
        mutations.append(promoted)
        real_data = copy.deepcopy(self.plan)
        real_data["synthetic_only"] = False
        mutations.append(real_data)
        unknown_action = copy.deepcopy(self.plan)
        unknown_action["scenarios"][0]["events"][0]["authorization_action_id"] = "ai.activate_plan"
        mutations.append(unknown_action)
        unknown_step = copy.deepcopy(self.plan)
        unknown_step["scenarios"][0]["events"][0]["step_id"] = "M1-S99"
        mutations.append(unknown_step)
        validator = Draft202012Validator(self.schema)
        for mutated in mutations:
            self.assertTrue(list(validator.iter_errors(mutated)))

    def test_closure_rejects_duplicate_ids_keys_wrong_pointer_and_action_resource(self):
        mutations = []
        duplicate_event = copy.deepcopy(self.plan)
        duplicate_event["scenarios"][1]["events"][0]["event_id"] = duplicate_event["scenarios"][0]["events"][0]["event_id"]
        mutations.append(duplicate_event)
        duplicate_key = copy.deepcopy(self.plan)
        duplicate_key["scenarios"][1]["events"][0]["idempotency"]["key"] = duplicate_key["scenarios"][0]["events"][0]["idempotency"]["key"]
        mutations.append(duplicate_key)
        wrong_pointer = copy.deepcopy(self.plan)
        wrong_pointer["scenarios"][0]["scenario_source_ref"] = wrong_pointer["scenarios"][1]["scenario_source_ref"]
        mutations.append(wrong_pointer)
        wrong_fixture_pointer = copy.deepcopy(self.plan)
        wrong_fixture_pointer["scenarios"][0]["fixture_source_ref"] = wrong_fixture_pointer["scenarios"][1]["fixture_source_ref"]
        mutations.append(wrong_fixture_pointer)
        wrong_action_resource = copy.deepcopy(self.plan)
        wrong_action_resource["scenarios"][0]["events"][0]["resource_ref"] = "HealthTask:syn-member-001:t1"
        mutations.append(wrong_action_resource)
        audit_as_write = copy.deepcopy(self.plan)
        audit_as_write["scenarios"][0]["events"][10]["authorization_action_id"] = "security.audit_metadata"
        mutations.append(audit_as_write)
        discontinuous_state = copy.deepcopy(self.plan)
        discontinuous_state["scenarios"][0]["events"][6]["expected_from"] = "pending"
        mutations.append(discontinuous_state)
        discontinuous_version = copy.deepcopy(self.plan)
        discontinuous_version["scenarios"][0]["events"][6]["expected_version"]["before"] = 9
        mutations.append(discontinuous_version)
        normal_with_risk = copy.deepcopy(self.plan)
        normal_with_risk["scenarios"][0]["events"][10]["resource_ref"] = "RiskEvent:syn-member-001:r1"
        mutations.append(normal_with_risk)
        wrong_emergency_profile = copy.deepcopy(self.plan)
        wrong_emergency_profile["scenarios"][2]["events"][0]["transition_ref"] = "risk-event:triage_pending->professional:CLASSIFY_PROFESSIONAL"
        wrong_emergency_profile["scenarios"][2]["events"][0]["expected_to"] = "professional"
        mutations.append(wrong_emergency_profile)
        for mutated in mutations:
            with self.assertRaises(AssertionError):
                validate_source_closure(mutated)

    def test_pointer_resolution_rejects_reordered_upstream_arrays(self):
        scenario_path = self.plan["source_contracts"]["scenarios"]
        fixture_path = self.plan["source_contracts"]["fixtures"]
        documents = {
            scenario_path: load(scenario_path),
            fixture_path: load(fixture_path),
        }
        documents[scenario_path]["scenarios"].reverse()
        with self.assertRaises(AssertionError):
            validate_source_closure(self.plan, documents)
        documents = {
            scenario_path: load(scenario_path),
            fixture_path: load(fixture_path),
        }
        documents[fixture_path]["fixtures"].reverse()
        with self.assertRaises(AssertionError):
            validate_source_closure(self.plan, documents)


if __name__ == "__main__":
    unittest.main()
