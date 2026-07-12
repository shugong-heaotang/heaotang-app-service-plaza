"""Deterministic, in-memory reference runner for HM-MVP90-M1 P2.

This module is development evidence, not a production health service.  It accepts
already loaded versioned contracts and synthetic events.  It deliberately has no
file, network, database, clock, random, browser, or model integration.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional


SYNTHETIC_ONLY = True
EXECUTABLE = False

ERR_SYNTHETIC_BOUNDARY = "HM_P2_SYNTHETIC_BOUNDARY_REQUIRED"
ERR_EXECUTABLE_PROMOTION = "HM_P2_EXECUTABLE_PROMOTION_FORBIDDEN"
ERR_UNKNOWN_SCENARIO = "HM_P2_UNKNOWN_SCENARIO"
ERR_UNKNOWN_TRANSITION = "HM_P2_UNKNOWN_TRANSITION"
ERR_ACTOR_NOT_AUTHORIZED = "HM_P2_ACTOR_NOT_AUTHORIZED"
ERR_ACTION_NOT_AUTHORIZED = "HM_P2_ACTION_NOT_AUTHORIZED"
ERR_RESOURCE_NOT_AUTHORIZED = "HM_P2_RESOURCE_NOT_AUTHORIZED"
ERR_STATE_CONFLICT = "HM_RESOURCE_STATE_CONFLICT"
ERR_VERSION_CONFLICT = "HM_VERSION_CONFLICT"
ERR_IDEMPOTENCY_CONFLICT = "HM_IDEMPOTENCY_CONFLICT"
ERR_AUDIT_REQUIRED = "HM_AUDIT_WRITE_REQUIRED"
ERR_AI_RUNTIME_NOT_AUTHORIZED = "HM_AI_RUNTIME_NOT_AUTHORIZED"


SUBJECT_BY_ACTOR = {
    "member": "adult_member_self",
    "ai": "ai_runtime",
    "health_manager": "health_manager",
    "professional": "qualified_professional",
}


def canonical_json(value: Any) -> str:
    """Return the stable JSON form used by P2 synthetic trace hashing."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _transition_parts(reference: str):
    try:
        machine_id, state_change, trigger = reference.split(":")
        source, target = state_change.split("->")
    except ValueError as exc:
        raise ValueError(ERR_UNKNOWN_TRANSITION) from exc
    return machine_id, source, target, trigger


class SyntheticPdcarReferenceRunner:
    """Execute injected synthetic replay events with transactional in-memory state."""

    def __init__(
        self,
        replay_plan: Mapping[str, Any],
        state_machines: Mapping[str, Any],
        security_authorization: Mapping[str, Any],
    ) -> None:
        if replay_plan.get("synthetic_only") is not True:
            raise ValueError(ERR_SYNTHETIC_BOUNDARY)
        if replay_plan.get("executable") is not False:
            raise ValueError(ERR_EXECUTABLE_PROMOTION)
        self._plan = copy.deepcopy(dict(replay_plan))
        self._scenarios = {item["scenario_id"]: item for item in replay_plan["scenarios"]}
        self._first_event_by_resource = {}
        for scenario in replay_plan["scenarios"]:
            for event in scenario["events"]:
                self._first_event_by_resource.setdefault(
                    (scenario["scenario_id"], event["resource_ref"]), event["event_id"]
                )
        self._machines = {item["machine_id"]: item for item in state_machines["machines"]}
        self._actions = {item["action_id"]: item for item in security_authorization["actions"]}
        self._denials = {
            item["condition"]: item["error_id"] for item in security_authorization["server_denial_matrix"]
        }
        self._resources: Dict[str, Dict[str, Any]] = {}
        self._idempotency: Dict[str, Dict[str, Any]] = {}
        self._audit_events = []
        self._trace_events = []

    @property
    def resources(self):
        return copy.deepcopy(self._resources)

    @property
    def audit_events(self):
        return copy.deepcopy(self._audit_events)

    @property
    def trace_events(self):
        return copy.deepcopy(self._trace_events)

    def trace_hash(self) -> str:
        return canonical_sha256(
            {
                "synthetic_only": SYNTHETIC_ONLY,
                "executable": EXECUTABLE,
                "resources": self._resources,
                "audit_events": self._audit_events,
                "trace_events": self._trace_events,
            }
        )

    def seed_resource(self, resource_ref: str, state: str, version: int) -> None:
        if version < 0:
            raise ValueError(ERR_VERSION_CONFLICT)
        self._resources[resource_ref] = {"state": state, "version": version}

    def _result(
        self,
        event: Mapping[str, Any],
        outcome: str,
        committed: bool,
        error_id: Optional[str],
        state: Optional[str] = None,
        version: Optional[int] = None,
        replayed: bool = False,
    ) -> Dict[str, Any]:
        return {
            "scenario_id": event.get("scenario_id"),
            "event_id": event.get("event_id"),
            "outcome": outcome,
            "committed": committed,
            "error_id": error_id,
            "state": state,
            "version": version,
            "replayed": replayed,
            "synthetic_only": SYNTHETIC_ONLY,
            "executable": EXECUTABLE,
        }

    def _find_transition(self, reference: str, actor_role: str):
        try:
            machine_id, source, target, trigger = _transition_parts(reference)
        except ValueError:
            return None, ERR_UNKNOWN_TRANSITION
        machine = self._machines.get(machine_id)
        if machine is None:
            return None, ERR_UNKNOWN_TRANSITION
        for transition in machine["transitions"]:
            if (
                transition["from"] == source
                and transition["to"] == target
                and transition["event"] == trigger
            ):
                if actor_role not in transition["required_actor_roles"]:
                    return None, ERR_AI_RUNTIME_NOT_AUTHORIZED if actor_role == "ai" else ERR_ACTOR_NOT_AUTHORIZED
                return (source, target, trigger), None
        for forbidden in machine.get("forbidden_transitions", []):
            if forbidden["from"] == source and forbidden["to"] == target:
                return None, forbidden["error_id"]
        return None, ERR_UNKNOWN_TRANSITION

    def _validate_action(self, event: Mapping[str, Any]):
        action_id = event.get("authorization_action_id")
        if action_id is None:
            return None
        action = self._actions.get(action_id)
        if action is None:
            return ERR_ACTION_NOT_AUTHORIZED
        if action_id == "security.audit_metadata" or "business_write" in action.get("prohibitions", []):
            return ERR_ACTION_NOT_AUTHORIZED
        resource_type = event["resource_ref"].split(":", 1)[0]
        if resource_type not in action["resources"]:
            return ERR_RESOURCE_NOT_AUTHORIZED
        if SUBJECT_BY_ACTOR.get(event["actor_role"]) not in action["subjects"]:
            return ERR_AI_RUNTIME_NOT_AUTHORIZED if event["actor_role"] == "ai" else ERR_ACTOR_NOT_AUTHORIZED
        if not action["prerequisites"]:
            return ERR_ACTION_NOT_AUTHORIZED
        if action["effect"] in {"read", "read-metadata"} and (
            event["expected_from"] != event["expected_to"]
            or event["expected_version"]["before"] != event["expected_version"]["after"]
        ):
            return ERR_ACTION_NOT_AUTHORIZED
        return None

    def execute_event(
        self,
        scenario_id: str,
        event: Mapping[str, Any],
        *,
        audit_write_succeeds: bool = True,
    ) -> Dict[str, Any]:
        """Execute one event atomically and return a stable machine result."""

        if scenario_id not in self._scenarios:
            synthetic_event = dict(event)
            synthetic_event["scenario_id"] = scenario_id
            return self._result(synthetic_event, "rejected", False, ERR_UNKNOWN_SCENARIO)

        candidate = copy.deepcopy(dict(event))
        candidate["scenario_id"] = scenario_id
        idempotency = candidate["idempotency"]
        key = idempotency["key"]
        payload_basis = copy.deepcopy(candidate)
        payload_basis["idempotency"].pop("key", None)
        payload_basis["idempotency"].pop("expectation", None)
        payload_digest = canonical_sha256(payload_basis)
        previous = self._idempotency.get(key)
        if previous is not None:
            if previous["payload_digest"] != payload_digest:
                current = self._resources.get(candidate["resource_ref"])
                return self._result(
                    candidate,
                    "rejected",
                    False,
                    ERR_IDEMPOTENCY_CONFLICT,
                    current["state"] if current else None,
                    current["version"] if current else None,
                )
            result = copy.deepcopy(previous["result"])
            result["outcome"] = "replayed"
            result["replayed"] = True
            return result

        action_error = self._validate_action(candidate)
        if action_error:
            return self._result(candidate, "rejected", False, action_error)

        transition = None
        if candidate.get("transition_ref") is not None:
            transition, transition_error = self._find_transition(
                candidate["transition_ref"], candidate["actor_role"]
            )
            if transition_error:
                return self._result(candidate, "rejected", False, transition_error)
        elif candidate.get("authorization_action_id") is None:
            return self._result(candidate, "rejected", False, ERR_ACTION_NOT_AUTHORIZED)

        denial = candidate["denial_expectation"]
        if denial["outcome"] == "deny" and self._denials.get(denial["condition"]) != denial["error_id"]:
            return self._result(candidate, "rejected", False, ERR_ACTION_NOT_AUTHORIZED)

        resource_ref = candidate["resource_ref"]
        expected_version = candidate["expected_version"]
        current = self._resources.get(resource_ref)
        if current is None:
            if self._first_event_by_resource.get((scenario_id, resource_ref)) != candidate["event_id"]:
                return self._result(candidate, "rejected", False, ERR_STATE_CONFLICT)
            current = {"state": candidate["expected_from"], "version": expected_version["before"]}
        if current["state"] != candidate["expected_from"]:
            return self._result(candidate, "rejected", False, ERR_STATE_CONFLICT, current["state"], current["version"])
        if current["version"] != expected_version["before"]:
            return self._result(candidate, "rejected", False, ERR_VERSION_CONFLICT, current["state"], current["version"])

        staged_resources = copy.deepcopy(self._resources)
        staged_audit = copy.deepcopy(self._audit_events)
        staged_trace = copy.deepcopy(self._trace_events)
        staged_idempotency = copy.deepcopy(self._idempotency)
        next_state = candidate["expected_to"]
        next_version = expected_version["after"]
        expected_delta = 0 if next_state == current["state"] else 1
        if next_version != current["version"] + expected_delta:
            return self._result(candidate, "rejected", False, ERR_VERSION_CONFLICT, current["state"], current["version"])
        if transition is not None and (transition[0] != current["state"] or transition[1] != next_state):
            return self._result(candidate, "rejected", False, ERR_STATE_CONFLICT, current["state"], current["version"])

        staged_resources[resource_ref] = {"state": next_state, "version": next_version}
        audit_record = {
            "scenario_id": scenario_id,
            "event_id": candidate["event_id"],
            "resource_ref": resource_ref,
            "actor_role": candidate["actor_role"],
            "decision": denial["outcome"],
            "error_id": denial["error_id"],
        }
        trace_record = {
            "scenario_id": scenario_id,
            "event_id": candidate["event_id"],
            "resource_ref": resource_ref,
            "from": current["state"],
            "to": next_state,
            "version_before": current["version"],
            "version_after": next_version,
            "decision": denial["outcome"],
            "error_id": denial["error_id"],
        }
        staged_audit.append(audit_record)
        staged_trace.append(trace_record)

        if candidate["audit_expectation"]["required"] and not audit_write_succeeds:
            return self._result(candidate, "rejected", False, ERR_AUDIT_REQUIRED, current["state"], current["version"])

        outcome = "denied" if denial["outcome"] == "deny" else "applied"
        result = self._result(
            candidate,
            outcome,
            True,
            denial["error_id"],
            next_state,
            next_version,
        )
        staged_idempotency[key] = {"payload_digest": payload_digest, "result": copy.deepcopy(result)}
        self._resources = staged_resources
        self._audit_events = staged_audit
        self._trace_events = staged_trace
        self._idempotency = staged_idempotency
        return result

    def replay_scenario(
        self,
        scenario_id: str,
        *,
        audit_fail_event_ids: Optional[Iterable[str]] = None,
    ) -> Dict[str, Any]:
        scenario = self._scenarios.get(scenario_id)
        if scenario is None:
            return {
                "scenario_id": scenario_id,
                "outcome": "rejected",
                "error_id": ERR_UNKNOWN_SCENARIO,
                "results": [],
                "trace_hash": self.trace_hash(),
                "synthetic_only": SYNTHETIC_ONLY,
                "executable": EXECUTABLE,
            }
        failures = set(audit_fail_event_ids or [])
        results = []
        for event in scenario["events"]:
            result = self.execute_event(
                scenario_id,
                event,
                audit_write_succeeds=event["event_id"] not in failures,
            )
            results.append(result)
            if result["outcome"] == "rejected":
                break
        return {
            "scenario_id": scenario_id,
            "outcome": results[-1]["outcome"] if results else "rejected",
            "error_id": results[-1]["error_id"] if results else ERR_UNKNOWN_SCENARIO,
            "results": results,
            "trace_hash": self.trace_hash(),
            "synthetic_only": SYNTHETIC_ONLY,
            "executable": EXECUTABLE,
        }
