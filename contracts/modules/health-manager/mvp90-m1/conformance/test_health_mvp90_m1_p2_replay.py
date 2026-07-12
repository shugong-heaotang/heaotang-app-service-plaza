import ast
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from .synthetic_pdcar_reference import (
    ERR_AUDIT_REQUIRED,
    ERR_ACTION_NOT_AUTHORIZED,
    ERR_IDEMPOTENCY_CONFLICT,
    ERR_AI_RUNTIME_NOT_AUTHORIZED,
    ERR_STATE_CONFLICT,
    ERR_UNKNOWN_TRANSITION,
    ERR_VERSION_CONFLICT,
    SyntheticPdcarReferenceRunner,
)


ROOT = Path(__file__).resolve().parents[5]
PLAN_REL = "contracts/modules/health-manager/mvp90-m1/synthetic-replay-plan.v1.json"
SCHEMA_REL = "contracts/modules/health-manager/mvp90-m1/synthetic-replay-plan.v1.schema.json"
MATRIX_REL = "contracts/modules/health-manager/mvp90-m1/conformance/fixtures/synthetic-replay-negative-cases.v1.json"
MATRIX_SCHEMA_REL = "contracts/modules/health-manager/mvp90-m1/conformance/fixtures/synthetic-replay-negative-cases.v1.schema.json"
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


def replace_pointer(document, pointer, replacement):
    tokens = [token.replace("~1", "/").replace("~0", "~") for token in pointer.lstrip("/").split("/")]
    target = document
    for token in tokens[:-1]:
        target = target[int(token)] if isinstance(target, list) else target[token]
    final = tokens[-1]
    if isinstance(target, list):
        target[int(final)] = copy.deepcopy(replacement)
    else:
        target[final] = copy.deepcopy(replacement)


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
        cls.matrix = load(MATRIX_REL)
        cls.matrix_schema = load(MATRIX_SCHEMA_REL)

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

    def new_runner(self):
        return SyntheticPdcarReferenceRunner(
            self.plan,
            load(self.plan["source_contracts"]["state_machines"]),
            load(self.plan["source_contracts"]["security_authorization"]),
        )

    def test_runner_replays_a001_contiguously_with_stable_trace_hash(self):
        first = self.new_runner()
        second = self.new_runner()
        first_result = first.replay_scenario("MVP-A001")
        second_result = second.replay_scenario("MVP-A001")
        self.assertEqual(len(first_result["results"]), 11)
        self.assertTrue(all(item["committed"] for item in first_result["results"]))
        self.assertEqual(first_result["trace_hash"], second_result["trace_hash"])
        self.assertEqual(first.resources["HealthTask:syn-member-001:t1"], {"state": "recorded", "version": 4})
        self.assertTrue(first_result["synthetic_only"])
        self.assertFalse(first_result["executable"])
        first_hash = first_result["trace_hash"]
        replayed = first.replay_scenario("MVP-A001")
        self.assertEqual(replayed["trace_hash"], first_hash)
        self.assertTrue(all(item["outcome"] == "replayed" for item in replayed["results"]))

    def test_same_idempotency_key_same_payload_replays_without_duplicate_commit(self):
        runner = self.new_runner()
        event = self.plan["scenarios"][0]["events"][0]
        first = runner.execute_event("MVP-A001", event)
        state_before = runner.resources
        audit_before = runner.audit_events
        trace_before = runner.trace_events
        second = runner.execute_event("MVP-A001", event)
        self.assertEqual(first["state"], second["state"])
        self.assertEqual(second["outcome"], "replayed")
        self.assertTrue(second["replayed"])
        self.assertEqual(runner.resources, state_before)
        self.assertEqual(runner.audit_events, audit_before)
        self.assertEqual(runner.trace_events, trace_before)

    def test_same_idempotency_key_different_payload_conflicts_atomically(self):
        runner = self.new_runner()
        event = self.plan["scenarios"][0]["events"][0]
        runner.execute_event("MVP-A001", event)
        state_before = runner.resources
        audit_before = runner.audit_events
        trace_before = runner.trace_events
        conflicting = copy.deepcopy(event)
        conflicting["idempotency"]["payload_ref"] = "MVP-A001/conflicting-payload"
        result = runner.execute_event("MVP-A001", conflicting)
        self.assertEqual(result["error_id"], ERR_IDEMPOTENCY_CONFLICT)
        self.assertFalse(result["committed"])
        self.assertEqual(runner.resources, state_before)
        self.assertEqual(runner.audit_events, audit_before)
        self.assertEqual(runner.trace_events, trace_before)
        idempotency_before = runner.idempotency_records
        changed_expectation = copy.deepcopy(event)
        changed_expectation["idempotency"]["expectation"] = "return_original_result"
        expectation_result = runner.execute_event("MVP-A001", changed_expectation)
        self.assertEqual(expectation_result["error_id"], ERR_IDEMPOTENCY_CONFLICT)
        self.assertFalse(expectation_result["committed"])
        self.assertEqual(runner.resources, state_before)
        self.assertEqual(runner.audit_events, audit_before)
        self.assertEqual(runner.trace_events, trace_before)
        self.assertEqual(runner.idempotency_records, idempotency_before)
        changed_semantics = copy.deepcopy(event)
        changed_semantics["transition_ref"] = "consent-grant:draft->withdrawn:WITHDRAW_CONSENT"
        changed_semantics["expected_to"] = "withdrawn"
        changed_semantics_result = runner.execute_event("MVP-A001", changed_semantics)
        self.assertEqual(changed_semantics_result["error_id"], ERR_IDEMPOTENCY_CONFLICT)
        self.assertEqual(runner.resources, state_before)

    def test_signed_denials_cannot_be_changed_to_allow_and_fail_atomically(self):
        for scenario_id in ("MVP-A005", "MVP-A008", "MVP-A009", "MVP-A014", "MVP-A015"):
            with self.subTest(scenario_id=scenario_id):
                runner = self.new_runner()
                mutated_plan = copy.deepcopy(self.plan)
                scenario = next(item for item in mutated_plan["scenarios"] if item["scenario_id"] == scenario_id)
                changed = scenario["events"][0]
                changed["denial_expectation"] = {"outcome": "allow", "condition": None, "error_id": None}
                Draft202012Validator(self.schema).validate(mutated_plan)
                resources_before = runner.resources
                audit_before = runner.audit_events
                trace_before = runner.trace_events
                idempotency_before = runner.idempotency_records
                result = runner.execute_event(scenario_id, changed)
                self.assertEqual(result["error_id"], ERR_ACTION_NOT_AUTHORIZED)
                self.assertFalse(result["committed"])
                self.assertEqual(runner.resources, resources_before)
                self.assertEqual(runner.audit_events, audit_before)
                self.assertEqual(runner.trace_events, trace_before)
                self.assertEqual(runner.idempotency_records, idempotency_before)

    def test_authoritative_event_semantics_cannot_drift_on_first_execution(self):
        base = self.plan["scenarios"][0]["events"][0]
        mutations = []
        for field, value in (
            ("actor_role", "ai"),
            ("resource_ref", "AssessmentSession:syn-member-other"),
            ("audit_expectation", {"required": False, "failure_mode": None}),
        ):
            changed = copy.deepcopy(base)
            changed[field] = value
            mutations.append(changed)
        changed = copy.deepcopy(base)
        changed["expected_version"]["after"] = 9
        mutations.append(changed)
        for changed in mutations:
            runner = self.new_runner()
            result = runner.execute_event("MVP-A001", changed)
            self.assertFalse(result["committed"])
            self.assertEqual(runner.resources, {})
            self.assertEqual(runner.audit_events, [])
            self.assertEqual(runner.trace_events, [])
            self.assertEqual(runner.idempotency_records, {})

    def test_version_conflict_leaves_state_audit_and_trace_unchanged(self):
        runner = self.new_runner()
        event = self.plan["scenarios"][0]["events"][0]
        runner.seed_resource(event["resource_ref"], event["expected_from"], 9)
        state_before = runner.resources
        result = runner.execute_event("MVP-A001", event)
        self.assertEqual(result["error_id"], ERR_VERSION_CONFLICT)
        self.assertFalse(result["committed"])
        self.assertEqual(runner.resources, state_before)
        self.assertEqual(runner.audit_events, [])
        self.assertEqual(runner.trace_events, [])

    def test_audit_failure_rolls_back_resource_event_and_idempotency(self):
        runner = self.new_runner()
        event = self.plan["scenarios"][0]["events"][0]
        failed = runner.execute_event("MVP-A001", event, audit_write_succeeds=False)
        self.assertEqual(failed["error_id"], ERR_AUDIT_REQUIRED)
        self.assertFalse(failed["committed"])
        self.assertEqual(runner.resources, {})
        self.assertEqual(runner.audit_events, [])
        self.assertEqual(runner.trace_events, [])
        retried = runner.execute_event("MVP-A001", event)
        self.assertEqual(retried["outcome"], "applied")
        self.assertFalse(retried["replayed"])

        later = self.new_runner()
        failed_scenario = later.replay_scenario("MVP-A001", audit_fail_event_ids={"A001-E07"})
        self.assertEqual(failed_scenario["results"][-1]["error_id"], ERR_AUDIT_REQUIRED)
        self.assertEqual(later.resources["HealthTask:syn-member-001:t1"], {"state": "in_progress", "version": 1})
        self.assertEqual(len(later.audit_events), 6)
        self.assertEqual(len(later.trace_events), 6)
        event_e07 = self.plan["scenarios"][0]["events"][6]
        recovered = later.execute_event("MVP-A001", event_e07)
        self.assertEqual(recovered["outcome"], "applied")
        self.assertEqual(later.resources["HealthTask:syn-member-001:t1"], {"state": "completed", "version": 2})

    def test_ai_plan_activation_and_direct_risk_close_are_rejected(self):
        runner = self.new_runner()
        activate = copy.deepcopy(self.plan["scenarios"][0]["events"][4])
        activate["actor_role"] = "ai"
        activate["authorization_action_id"] = "ai.read_minimum_context_and_draft"
        activation_result = runner.execute_event("MVP-A001", activate)
        self.assertEqual(activation_result["error_id"], ERR_AI_RUNTIME_NOT_AUTHORIZED)
        self.assertFalse(activation_result["committed"])

        professional_conclusion = copy.deepcopy(self.plan["scenarios"][2]["events"][0])
        professional_conclusion["actor_role"] = "ai"
        conclusion_result = runner.execute_event("MVP-A003", professional_conclusion)
        self.assertEqual(conclusion_result["error_id"], ERR_AI_RUNTIME_NOT_AUTHORIZED)
        self.assertFalse(conclusion_result["committed"])

        close_risk = copy.deepcopy(self.plan["scenarios"][2]["events"][0])
        close_risk["actor_role"] = "ai"
        close_risk["transition_ref"] = "risk-event:emergency->human_closed:AI_CLOSE"
        close_risk["expected_from"] = "emergency"
        close_risk["expected_to"] = "human_closed"
        close_result = runner.execute_event("MVP-A003", close_risk)
        self.assertEqual(close_result["error_id"], "HMM0_AI_OR_DIRECT_RISK_CLOSE_FORBIDDEN")
        self.assertFalse(close_result["committed"])
        self.assertEqual(runner.resources, {})

    def test_plan_cannot_be_activated_before_prior_review_sequence(self):
        runner = self.new_runner()
        member_confirm = self.plan["scenarios"][0]["events"][4]
        result = runner.execute_event("MVP-A001", member_confirm)
        self.assertEqual(result["error_id"], ERR_STATE_CONFLICT)
        self.assertFalse(result["committed"])
        self.assertEqual(runner.resources, {})

    def test_unknown_transition_and_forbidden_runtime_imports_fail_closed(self):
        runner = self.new_runner()
        event = copy.deepcopy(self.plan["scenarios"][0]["events"][5])
        event["transition_ref"] = "health-task:pending->completed:SKIP_TASK"
        result = runner.execute_event("MVP-A001", event)
        self.assertEqual(result["error_id"], ERR_UNKNOWN_TRANSITION)
        self.assertFalse(result["committed"])
        source = (Path(__file__).parent / "synthetic_pdcar_reference.py").read_text(encoding="utf-8")
        imported_roots = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".", 1)[0])
        self.assertTrue(imported_roots.isdisjoint({"socket", "requests", "sqlite3", "time", "random", "pathlib", "os"}))
        self.assertNotIn("open(", source)

    def test_c3_matrix_schema_exact_sets_and_failure_closed_constants(self):
        Draft202012Validator(self.matrix_schema).validate(self.matrix)
        self.assertEqual(
            {item["scenario_id"] for item in self.matrix["positive_cases"]},
            {f"MVP-A{i:03d}" for i in range(1, 16)},
        )
        self.assertEqual(
            {item["case_id"] for item in self.matrix["negative_cases"]},
            {f"NEG-A{i:03d}" for i in range(1, 16)},
        )
        self.assertEqual(
            {(item["case_id"], item["scenario_id"]) for item in self.matrix["negative_cases"]},
            {(f"NEG-A{i:03d}", f"MVP-A{i:03d}") for i in range(1, 16)},
        )
        validator = Draft202012Validator(self.matrix_schema)
        mutations = []
        missing = copy.deepcopy(self.matrix)
        missing["negative_cases"].pop()
        mutations.append(missing)
        duplicate = copy.deepcopy(self.matrix)
        duplicate["negative_cases"][14] = copy.deepcopy(duplicate["negative_cases"][0])
        mutations.append(duplicate)
        promoted = copy.deepcopy(self.matrix)
        promoted["executable"] = True
        mutations.append(promoted)
        real_data = copy.deepcopy(self.matrix)
        real_data["synthetic_only"] = False
        mutations.append(real_data)
        for mutated in mutations:
            self.assertTrue(list(validator.iter_errors(mutated)))

    def test_c3_fifteen_positive_results_and_hashes_are_exact_and_deterministic(self):
        for expected in self.matrix["positive_cases"]:
            with self.subTest(scenario_id=expected["scenario_id"]):
                first = self.new_runner().replay_scenario(expected["scenario_id"])
                second = self.new_runner().replay_scenario(expected["scenario_id"])
                self.assertEqual(first["outcome"], expected["expected_outcome"])
                self.assertEqual(first["error_id"], expected["expected_error_id"])
                self.assertEqual(len(first["results"]), expected["expected_result_count"])
                self.assertEqual(first["trace_hash"], expected["expected_trace_hash"])
                self.assertEqual(second["trace_hash"], expected["expected_trace_hash"])
                self.assertTrue(first["synthetic_only"])
                self.assertFalse(first["executable"])

    def test_c3_fifteen_negative_cases_fail_without_any_side_effect(self):
        scenarios = {item["scenario_id"]: item for item in self.plan["scenarios"]}
        for case in self.matrix["negative_cases"]:
            with self.subTest(case_id=case["case_id"]):
                runner = self.new_runner()
                event = copy.deepcopy(
                    next(item for item in scenarios[case["scenario_id"]]["events"] if item["event_id"] == case["event_id"])
                )
                operation = case["operation"]
                kwargs = {}
                if operation["kind"] == "idempotency_replay_patch":
                    first = runner.execute_event(case["scenario_id"], event)
                    self.assertTrue(first["committed"])
                    replace_pointer(event, operation["json_pointer"], operation["replacement"])
                elif operation["kind"] == "event_patch":
                    replace_pointer(event, operation["json_pointer"], operation["replacement"])
                elif operation["kind"] == "seed_version_conflict":
                    runner.seed_resource(event["resource_ref"], operation["seed_state"], operation["seed_version"])
                elif operation["kind"] == "audit_failure":
                    kwargs["audit_write_succeeds"] = False
                else:
                    self.fail(f"unknown negative operation: {operation['kind']}")
                resources_before = runner.resources
                audit_before = runner.audit_events
                trace_before = runner.trace_events
                idempotency_before = runner.idempotency_records
                result = runner.execute_event(case["scenario_id"], event, **kwargs)
                self.assertEqual(result["error_id"], case["expected_error_id"])
                self.assertFalse(result["committed"])
                self.assertTrue(result["synthetic_only"])
                self.assertFalse(result["executable"])
                self.assertEqual(runner.resources, resources_before)
                self.assertEqual(runner.audit_events, audit_before)
                self.assertEqual(runner.trace_events, trace_before)
                self.assertEqual(runner.idempotency_records, idempotency_before)

    def test_c3_runner_has_zero_external_and_real_data_runtime_surface(self):
        source = (Path(__file__).parent / "synthetic_pdcar_reference.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".", 1)[0])
        forbidden_imports = {
            "aiohttp", "datetime", "http", "os", "pathlib", "random", "requests", "socket",
            "sqlite3", "subprocess", "time", "urllib", "webbrowser",
        }
        self.assertTrue(imported_roots.isdisjoint(forbidden_imports))
        for forbidden_text in (
            "open(", "localStorage", "sessionStorage", "fetch(", "http://", "https://",
            "member_phone", "identity_card", "real_health_data",
        ):
            self.assertNotIn(forbidden_text, source)
        self.assertTrue(self.matrix["synthetic_only"])
        self.assertFalse(self.matrix["executable"])


if __name__ == "__main__":
    unittest.main()
