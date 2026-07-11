#!/usr/bin/env python3
"""Generate deterministic, obviously synthetic MVP-90 fixtures."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MODULE = HERE.parents[1]
SCENARIOS_PATH = MODULE / "synthetic-scenarios.v1.json"
OUTPUT_PATH = HERE / "mvp90-synthetic-fixtures.v1.json"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def token(seed: str, scenario_id: str, purpose: str) -> str:
    return hashlib.sha256(f"{seed}|{scenario_id}|{purpose}".encode("utf-8")).hexdigest()[:16]


def trigger_code(scenario_id: str) -> str:
    return "SYNTHETIC_" + scenario_id.replace("MVP-", "").replace("-", "_")


def scenario_payload(scenario_id: str) -> dict[str, Any]:
    payloads: dict[str, dict[str, Any]] = {
        "MVP-A001": {"consent_state": "confirmed", "screening_state": "clear", "goal_marker": "synthetic-daily-routine", "task_feedback": "completed"},
        "MVP-A002": {"critical_answer_state": "unknown-or-refused", "default_answer_allowed": False},
        "MVP-A003": {"reviewed_rule_result": "synthetic-urgent", "normal_plan_allowed": False},
        "MVP-A004": {"task_state": "in-progress", "feedback_type": "discomfort", "continue_encouragement_allowed": False},
        "MVP-A005": {"execution_barrier_state": "repeated-synthetic", "red_flag_present": False, "penalty_allowed": False},
        "MVP-A006": {"request_classes": ["diagnosis", "medication-change", "outcome-guarantee"], "professional_answer_allowed": False},
        "MVP-A007": {"failure_modes": ["timeout", "unavailable", "unparsable"], "confirmed_plan_available": True},
        "MVP-A008": {"withdrawn_purposes": ["ai-processing", "sharing"], "new_processing_allowed": False},
        "MVP-A009": {"service_relationship": "absent", "requester_role_state": "mismatched", "resource_disclosure_allowed": False},
        "MVP-A010": {"capacity_policy_state": "limit-reached", "new_assignment_allowed": False, "existing_risk_visibility": True},
        "MVP-A011": {"template_states": ["expired", "unreviewed"], "reviewer_separation": "same-person-negative", "new_plan_allowed": False},
        "MVP-A012": {"replay_variants": ["same-payload", "conflicting-payload"], "duplicate_object_allowed": False},
        "MVP-A013": {"message_states": ["send-failed", "unread", "channel-unavailable"], "resolved_allowed": False},
        "MVP-A014": {"correction_source": "synthetic-extraction-error", "history_preservation_required": True, "impact_review_state": "pending"},
        "MVP-A015": {"service_state": "exit-requested", "ordinary_task_continuation": False, "open_risk_preserved": True},
    }
    return payloads[scenario_id]


def build_bundle() -> dict[str, Any]:
    scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    generator = scenarios["generator"]
    seed = generator["seed"]
    fixtures = []
    for scenario in scenarios["scenarios"]:
        scenario_id = scenario["scenario_id"]
        fixture = {
            "scenario_id": scenario_id,
            "fixture_id": scenario["fixture_id"],
            "synthetic": True,
            "environment": "non-production",
            "generator_version": "heaotang-deterministic-fixture-v1",
            "seed": seed,
            "destruction_policy": generator["destruction_policy"],
            "inputs": {
                "synthetic_member_ref": f"SYN-MEMBER-{token(seed, scenario_id, 'member')}",
                "synthetic_object_ref": f"SYN-OBJECT-{token(seed, scenario_id, 'object')}",
                "synthetic_correlation_id": f"SYN-CORR-{token(seed, scenario_id, 'correlation')}",
                "trigger_code": trigger_code(scenario_id),
                "display_marker": "合成验收数据",
            },
            "scenario_payload": scenario_payload(scenario_id),
            "expected_outcomes": scenario["expected_outcomes"],
            "forbidden_outcomes": scenario["forbidden_outcomes"],
        }
        fixture["canonical_sha256"] = hashlib.sha256(canonical_bytes(fixture)).hexdigest()
        fixtures.append(fixture)
    return {
        "contract_version": "health-manager.mvp90.synthetic-fixtures.v1",
        "generator": {
            "generator_id": generator["generator_id"],
            "version": generator["version"],
            "algorithm": generator["algorithm"],
            "seed": seed,
        },
        "fixtures": fixtures,
    }


def main() -> int:
    content = json.dumps(build_bundle(), ensure_ascii=False, indent=2) + "\n"
    OUTPUT_PATH.write_text(content, encoding="utf-8", newline="\n")
    print(f"generated {OUTPUT_PATH} with 15 deterministic synthetic fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
