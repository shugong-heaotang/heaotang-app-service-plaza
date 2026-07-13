#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

REQUIRED_FLOW_FIELDS = {
    "flow_class", "business_stream_id", "module_id", "priority", "risk_level",
    "updated_at", "target_date", "next_checkpoint", "status_expires_at",
    "developer_role", "reviewer_role", "approver_role", "blocks",
    "does_not_block", "auto_continue", "stop_conditions",
}
REQUIRED_BUSINESS_FIELDS = {
    "customer_segment", "customer_problem", "value_event", "success_metric",
    "metric_target", "measurement_window", "end_to_end_owner_role",
    "commercial_hypothesis", "kill_condition", "journey_scope",
}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate(policy_path: Path, schema_path: Path, registry_path: Path, now: datetime | None = None) -> list[str]:
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    errors = [e.message for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(policy)]
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("validation clock must be timezone-aware")
    work_items = registry["work_items"]
    cutover_id = policy.get("migration", {}).get("legacy_cutover_work_id")
    cutover_indexes = [n for n, item in enumerate(work_items) if item.get("work_id") == cutover_id]
    if len(cutover_indexes) != 1:
        errors.append("DELIVERY_LEGACY_CUTOVER_NOT_UNIQUE")
        cutover_index = -1
    else:
        cutover_index = cutover_indexes[0]
        legacy_ids = "\n".join(item["work_id"] for item in work_items[:cutover_index + 1]) + "\n"
        actual_hash = hashlib.sha256(legacy_ids.encode("utf-8")).hexdigest()
        if actual_hash != policy["migration"]["legacy_work_ids_sha256"]:
            errors.append("DELIVERY_LEGACY_BOUNDARY_CHANGED")
        legacy_states = "\n".join(
            f"{item['work_id']}\t{item['status']}" for item in work_items[:cutover_index + 1]
        ) + "\n"
        actual_state_hash = hashlib.sha256(legacy_states.encode("utf-8")).hexdigest()
        if actual_state_hash != policy["migration"]["legacy_work_states_sha256"]:
            errors.append("DELIVERY_LEGACY_STATE_CHANGED_WITHOUT_MIGRATION")
        for item in work_items[cutover_index + 1:]:
            if item.get("flow_policy_version") != policy.get("contract_version"):
                errors.append(f"{item['work_id']}: DELIVERY_NEW_ITEM_POLICY_REQUIRED")

    governed = [i for i in work_items if i.get("flow_policy_version") == policy.get("contract_version")]
    for item in governed:
        missing = sorted(REQUIRED_FLOW_FIELDS - item.keys())
        if missing:
            errors.append(f"{item['work_id']}: missing flow fields: {', '.join(missing)}")
            continue
        if item.get("status") in {"active", "handoff-ready"}:
            expiry = parse_time(item["status_expires_at"])
            if expiry <= parse_time(item["updated_at"]):
                errors.append(f"{item['work_id']}: status expiry must be after updated_at")
            if expiry <= now:
                errors.append(f"{item['work_id']}: DELIVERY_STATUS_EXPIRED")
        if item.get("developer_role") == item.get("reviewer_role"):
            errors.append(f"{item['work_id']}: developer and independent reviewer must be separated")
        if item.get("risk_level") in {"high", "critical"}:
            roles = {item.get("developer_role"), item.get("reviewer_role"), item.get("approver_role")}
            if len(roles) != 3:
                errors.append(f"{item['work_id']}: high-risk roles must be separated")
        if item.get("flow_class") == "business-stream" and item.get("status") in {"active", "handoff-ready"}:
            missing_business = sorted(REQUIRED_BUSINESS_FIELDS - item.keys())
            if missing_business:
                errors.append(f"{item['work_id']}: missing business value fields: {', '.join(missing_business)}")
        if item.get("status") == "handoff-ready":
            if not item.get("next_owner_role") or not item.get("handoff_requested_at"):
                errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_OWNER_OR_REQUEST_MISSING")
            else:
                requested = parse_time(item["handoff_requested_at"])
                response = item.get("handoff_first_response_at")
                if response and parse_time(response) < requested:
                    errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_RESPONSE_BEFORE_REQUEST")
                if not response and now > requested + timedelta(hours=policy["handoff"]["first_response_sla_hours"]):
                    errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_RESPONSE_SLA_EXCEEDED")
                if response and parse_time(response) > requested + timedelta(hours=policy["handoff"]["first_response_sla_hours"]):
                    errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_RESPONSE_SLA_EXCEEDED")
                decision = item.get("handoff_decided_at")
                if bool(decision) != bool(item.get("handoff_decision")):
                    errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_DECISION_INCOMPLETE")
                if decision and parse_time(decision) < requested:
                    errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_DECISION_BEFORE_REQUEST")
                if not decision and now > requested + timedelta(hours=policy["handoff"]["decision_sla_hours"]):
                    errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_DECISION_SLA_EXCEEDED")
                if decision and parse_time(decision) > requested + timedelta(hours=policy["handoff"]["decision_sla_hours"]):
                    errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_DECISION_SLA_EXCEEDED")
        if item.get("status") == "integrated":
            if item.get("flow_class") == "business-stream":
                missing_business = sorted(REQUIRED_BUSINESS_FIELDS - item.keys())
                if missing_business:
                    errors.append(f"{item['work_id']}: missing business value fields: {', '.join(missing_business)}")
                if not item.get("metric_evidence") or not item.get("value_event_evidence"):
                    errors.append(f"{item['work_id']}: DELIVERY_COMPLETION_VALUE_EVIDENCE_REQUIRED")
            acceptance = item.get("independent_acceptance")
            if not acceptance or acceptance.get("verdict") not in policy["completion"]["accepted_independent_verdicts"]:
                errors.append(f"{item['work_id']}: DELIVERY_INDEPENDENT_ACCEPTANCE_REQUIRED")
            elif acceptance.get("reviewer_role") == item.get("developer_role"):
                errors.append(f"{item['work_id']}: DELIVERY_INDEPENDENT_ACCEPTANCE_ROLE_CONFLICT")
            if not item.get("integration_commit"):
                errors.append(f"{item['work_id']}: DELIVERY_INTEGRATION_COMMIT_REQUIRED")

    in_flight_stream_items = [
        i for i in governed
        if i.get("status") in {"active", "handoff-ready"} and i.get("flow_class") == "business-stream"
    ]
    stream_counts = Counter(i["business_stream_id"] for i in in_flight_stream_items)
    if any(v > 1 for v in stream_counts.values()):
        errors.append("DELIVERY_DUPLICATE_ACTIVE_BUSINESS_STREAM")
    active_streams = {i["business_stream_id"]: i for i in in_flight_stream_items}
    module_counts = Counter(i["module_id"] for i in active_streams.values())
    if len(active_streams) > policy["wip"]["max_active_business_streams"]:
        errors.append("DELIVERY_WIP_GLOBAL_EXCEEDED")
    if any(v > policy["wip"]["max_active_business_streams_per_module"] for v in module_counts.values()):
        errors.append("DELIVERY_WIP_MODULE_EXCEEDED")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("policy", type=Path)
    parser.add_argument("schema", type=Path)
    parser.add_argument("registry", type=Path)
    args = parser.parse_args()
    errors = validate(args.policy, args.schema, args.registry)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Delivery flow policy is valid; governed WIP, expiry and role separation gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
