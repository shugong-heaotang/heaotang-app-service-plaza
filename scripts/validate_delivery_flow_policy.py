#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
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
LEGACY_SNAPSHOT_COMMIT = "33f5e45499fbadaac71f07bbe6de5d72579e39c9"
LEGACY_SNAPSHOT_PATH = "contracts/foundation/agent-collaboration.v1.json"
LEGACY_TRANSITION_SHA256 = "5dfa87a441a04eb8a24e3a4de883648780b6eaeddf2c870d831fa6ed29620939"
LEGACY_POST_STATES_SHA256 = "7f1991952dea49dff84e6378dbdc4edd22f4bf72334e0a8c08a36474fb984ec6"


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def evidence_exists(repo_root: Path, value: str) -> bool:
    try:
        candidate = (repo_root / value).resolve()
        candidate.relative_to(repo_root)
    except (ValueError, TypeError):
        return False
    return candidate.is_file()


def evidence_hash_matches(repo_root: Path, value: str, expected: str) -> bool:
    if not evidence_exists(repo_root, value):
        return False
    candidate = (repo_root / value).resolve()
    return hashlib.sha256(candidate.read_bytes()).hexdigest() == expected


def git_commit_exists(repo_root: Path, value: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "cat-file", "-e", f"{value}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def git_is_ancestor(repo_root: Path, ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "merge-base", "--is-ancestor", ancestor, descendant],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def git_json_at_commit(repo_root: Path, commit: str, path: str) -> dict | None:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "show", f"{commit}:{path}"],
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def git_bytes_at_commit(repo_root: Path, commit: str, path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "show", f"{commit}:{path}"],
        capture_output=True,
    )
    return result.stdout if result.returncode == 0 else None


def canonical_row_sha256(row: dict) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_legacy_receipt(policy: dict, repo_root: Path, registry: dict) -> tuple[list[str], dict | None]:
    if policy.get("contract_version") != "delivery-flow-policy.v2":
        return [], None
    errors: list[str] = []
    migration = policy.get("migration", {})
    receipt_rel = migration.get("receipt_path", "")
    schema_rel = migration.get("receipt_schema_path", "")
    try:
        receipt_path = (repo_root / receipt_rel).resolve()
        schema_path = (repo_root / schema_rel).resolve()
        receipt_path.relative_to(repo_root)
        schema_path.relative_to(repo_root)
    except (ValueError, TypeError):
        return ["DELIVERY_LEGACY_RECEIPT_PATH_INVALID"], None
    if not receipt_path.is_file() or not schema_path.is_file():
        return ["DELIVERY_LEGACY_RECEIPT_OR_SCHEMA_MISSING"], None
    receipt_bytes = receipt_path.read_bytes()
    if hashlib.sha256(receipt_bytes).hexdigest() != migration.get("receipt_sha256"):
        errors.append("DELIVERY_LEGACY_RECEIPT_HASH_MISMATCH")
    try:
        receipt = json.loads(receipt_bytes.decode("utf-8"))
        receipt_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return errors + ["DELIVERY_LEGACY_RECEIPT_JSON_INVALID"], None
    errors.extend(
        f"DELIVERY_LEGACY_RECEIPT_SCHEMA: {error.message}"
        for error in Draft202012Validator(receipt_schema, format_checker=FormatChecker()).iter_errors(receipt)
    )
    task = receipt.get("task_order", {})
    if not evidence_hash_matches(repo_root, task.get("path", ""), task.get("sha256", "")):
        errors.append("DELIVERY_LEGACY_RECEIPT_TASK_ORDER_INVALID")
    source = receipt.get("source_registry", {})
    source_bytes = git_bytes_at_commit(repo_root, source.get("commit", ""), source.get("path", ""))
    if source_bytes is None or hashlib.sha256(source_bytes).hexdigest() != source.get("sha256"):
        errors.append("DELIVERY_LEGACY_RECEIPT_SOURCE_REGISTRY_INVALID")
        return errors, receipt
    try:
        source_registry = json.loads(source_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return errors + ["DELIVERY_LEGACY_RECEIPT_SOURCE_REGISTRY_INVALID"], receipt
    transitions = receipt.get("transitions", [])
    canonical = "".join(
        f"{entry.get('work_id')}\t{entry.get('from_status')}\t{entry.get('to_status')}\n"
        for entry in transitions
    )
    if hashlib.sha256(canonical.encode("utf-8")).hexdigest() != LEGACY_TRANSITION_SHA256:
        errors.append("DELIVERY_LEGACY_TRANSITION_HASH_INVALID")
    source_items = source_registry.get("work_items", [])
    current_items = registry.get("work_items", [])
    if [entry.get("legacy_index") for entry in transitions] != sorted(entry.get("legacy_index") for entry in transitions):
        errors.append("DELIVERY_LEGACY_TRANSITION_ORDER_INVALID")
    transition_by_index = {entry.get("legacy_index"): entry for entry in transitions}
    state_modes: set[str] = set()
    for index, entry in transition_by_index.items():
        if not isinstance(index, int) or index >= len(source_items) or index >= len(current_items):
            errors.append("DELIVERY_LEGACY_TRANSITION_INDEX_INVALID")
            continue
        before = source_items[index]
        current = current_items[index]
        if before.get("work_id") != entry.get("work_id") or before.get("status") != entry.get("from_status"):
            errors.append("DELIVERY_LEGACY_TRANSITION_BEFORE_MISMATCH")
        if canonical_row_sha256(before) != entry.get("source_row_sha256"):
            errors.append("DELIVERY_LEGACY_TRANSITION_SOURCE_ROW_HASH_INVALID")
        before_state = f"{entry.get('work_id')}\t{entry.get('from_status')}\n".encode("utf-8")
        after_state = f"{entry.get('work_id')}\t{entry.get('to_status')}\n".encode("utf-8")
        if hashlib.sha256(before_state).hexdigest() != entry.get("before_state_sha256"):
            errors.append("DELIVERY_LEGACY_TRANSITION_BEFORE_STATE_HASH_INVALID")
        if hashlib.sha256(after_state).hexdigest() != entry.get("after_state_sha256"):
            errors.append("DELIVERY_LEGACY_TRANSITION_AFTER_STATE_HASH_INVALID")
        if current.get("status") == entry.get("from_status"):
            state_modes.add("before")
        elif current.get("status") == entry.get("to_status"):
            state_modes.add("after")
        else:
            state_modes.add("invalid")
    if state_modes not in ({"before"}, {"after"}):
        errors.append("DELIVERY_LEGACY_PARTIAL_TRANSITION")
    effective = []
    for index, row in enumerate(source_items[:115]):
        transition = transition_by_index.get(index)
        status = transition.get("to_status") if transition else row.get("status")
        effective.append(f"{row.get('work_id')}\t{status}\n")
    if hashlib.sha256("".join(effective).encode("utf-8")).hexdigest() != LEGACY_POST_STATES_SHA256:
        errors.append("DELIVERY_LEGACY_POST_STATES_HASH_INVALID")
    for entry in receipt.get("checklist_compatibility", []):
        path = repo_root / entry.get("path", "")
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry.get("sha256"):
            errors.append(f"{entry.get('path')}: DELIVERY_CHECKLIST_PROVENANCE_HASH_INVALID")
            continue
        try:
            checklist = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            errors.append(f"{entry.get('path')}: DELIVERY_CHECKLIST_PROVENANCE_JSON_INVALID")
            continue
        if checklist.get("record_id") != entry.get("record_id") or checklist.get("status") != "completed":
            errors.append(f"{entry.get('path')}: DELIVERY_CHECKLIST_PROVENANCE_ID_INVALID")
        if entry.get("scope") == "legacy-core-only-module" and checklist.get("module_id") is not None:
            errors.append(f"{entry.get('path')}: DELIVERY_CHECKLIST_PROVENANCE_SCOPE_INVALID")
        authority_bytes = git_bytes_at_commit(repo_root, entry.get("authority_commit", ""), entry.get("path", ""))
        if authority_bytes is None or hashlib.sha256(authority_bytes).hexdigest() != entry.get("sha256"):
            errors.append(f"{entry.get('path')}: DELIVERY_CHECKLIST_PROVENANCE_AUTHORITY_INVALID")
        task_path = entry.get("task_order_path")
        if task_path and git_bytes_at_commit(repo_root, entry.get("authority_commit", ""), task_path) is None:
            errors.append(f"{entry.get('path')}: DELIVERY_CHECKLIST_PROVENANCE_TASK_ORDER_INVALID")
    return errors, receipt


def metric_target_met(metric: dict) -> bool:
    actual = metric["actual_value"]
    target = metric["target_value"]
    return {
        "gte": actual >= target,
        "lte": actual <= target,
        "eq": actual == target,
    }[metric["comparison"]]


def validate(
    policy_path: Path,
    schema_path: Path,
    registry_path: Path,
    now: datetime | None = None,
    repo_root: Path | None = None,
) -> list[str]:
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    repo_root = (repo_root or registry_path.resolve().parents[2]).resolve()
    errors = [e.message for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(policy)]
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("validation clock must be timezone-aware")
    work_items = registry["work_items"]
    receipt_errors, receipt = validate_legacy_receipt(policy, repo_root, registry)
    errors.extend(receipt_errors)
    cutover_id = policy.get("migration", {}).get("legacy_cutover_work_id")
    snapshot = git_json_at_commit(repo_root, LEGACY_SNAPSHOT_COMMIT, LEGACY_SNAPSHOT_PATH)
    if snapshot is None:
        errors.append("DELIVERY_LEGACY_EXTERNAL_SNAPSHOT_UNAVAILABLE")
    else:
        snapshot_items = snapshot.get("work_items", [])
        snapshot_cutovers = [n for n, item in enumerate(snapshot_items) if item.get("work_id") == cutover_id]
        if len(snapshot_cutovers) != 1:
            errors.append("DELIVERY_LEGACY_EXTERNAL_CUTOVER_NOT_UNIQUE")
        else:
            snapshot_prefix = [
                (item.get("work_id"), item.get("status"))
                for item in snapshot_items[:snapshot_cutovers[0] + 1]
            ]
            current_prefix = [
                (item.get("work_id"), item.get("status"))
                for item in work_items[:len(snapshot_prefix)]
            ]
            allowed_prefixes = [snapshot_prefix]
            if receipt:
                projected = list(snapshot_prefix)
                for entry in receipt.get("transitions", []):
                    index = entry.get("legacy_index")
                    if isinstance(index, int) and index < len(projected):
                        projected[index] = (entry.get("work_id"), entry.get("to_status"))
                allowed_prefixes.append(projected)
            if current_prefix not in allowed_prefixes:
                errors.append("DELIVERY_LEGACY_EXTERNAL_SNAPSHOT_MISMATCH")
    if (
        policy.get("migration", {}).get("legacy_snapshot_commit") != LEGACY_SNAPSHOT_COMMIT
        or policy.get("migration", {}).get("legacy_snapshot_path") != LEGACY_SNAPSHOT_PATH
    ):
        errors.append("DELIVERY_LEGACY_EXTERNAL_ANCHOR_CHANGED")
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
        allowed_state_hashes = {policy["migration"]["legacy_work_states_sha256"]}
        if receipt:
            allowed_state_hashes.add(receipt.get("post_effective_states_sha256"))
        if actual_state_hash not in allowed_state_hashes:
            errors.append("DELIVERY_LEGACY_STATE_CHANGED_WITHOUT_MIGRATION")
        compatible_versions = set(policy.get("compatible_item_policy_versions", [policy.get("contract_version")]))
        for item in work_items[cutover_index + 1:]:
            if item.get("flow_policy_version") not in compatible_versions:
                errors.append(f"{item['work_id']}: DELIVERY_NEW_ITEM_POLICY_REQUIRED")

    compatible_versions = set(policy.get("compatible_item_policy_versions", [policy.get("contract_version")]))
    governed = [i for i in work_items if i.get("flow_policy_version") in compatible_versions]
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
                    deadline = requested + timedelta(hours=policy["handoff"]["decision_sla_hours"])
                    escalated_at = item.get("escalated_at")
                    if (
                        not escalated_at
                        or item.get("escalated_to_role") != policy["handoff"]["escalation_owner_role"]
                        or parse_time(escalated_at) < deadline
                        or parse_time(escalated_at) > now
                    ):
                        errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_ESCALATION_EVIDENCE_REQUIRED")
                if decision and parse_time(decision) > requested + timedelta(hours=policy["handoff"]["decision_sla_hours"]):
                    errors.append(f"{item['work_id']}: DELIVERY_HANDOFF_DECISION_SLA_EXCEEDED")
        if item.get("status") == "integrated":
            if item.get("flow_class") == "business-stream":
                missing_business = sorted(REQUIRED_BUSINESS_FIELDS - item.keys())
                if missing_business:
                    errors.append(f"{item['work_id']}: missing business value fields: {', '.join(missing_business)}")
                metrics = item.get("metric_evidence", [])
                value_evidence = item.get("value_event_evidence", [])
                if not metrics or not value_evidence:
                    errors.append(f"{item['work_id']}: DELIVERY_COMPLETION_VALUE_EVIDENCE_REQUIRED")
                else:
                    for metric in metrics:
                        required_metric_fields = set(policy["completion"]["required_metric_evidence_fields"])
                        if required_metric_fields - metric.keys():
                            errors.append(f"{item['work_id']}: DELIVERY_METRIC_EVIDENCE_INCOMPLETE")
                            continue
                        if not evidence_hash_matches(repo_root, metric["evidence_path"], metric["evidence_sha256"]):
                            errors.append(f"{item['work_id']}: DELIVERY_METRIC_EVIDENCE_PATH_INVALID")
                        if not metric_target_met(metric):
                            errors.append(f"{item['work_id']}: DELIVERY_METRIC_TARGET_NOT_MET")
                    if any(not evidence_hash_matches(repo_root, evidence.get("path", ""), evidence.get("sha256", "")) for evidence in value_evidence):
                        errors.append(f"{item['work_id']}: DELIVERY_VALUE_EVIDENCE_PATH_INVALID")
            acceptance = item.get("independent_acceptance")
            if not acceptance or acceptance.get("verdict") not in policy["completion"]["accepted_independent_verdicts"]:
                errors.append(f"{item['work_id']}: DELIVERY_INDEPENDENT_ACCEPTANCE_REQUIRED")
            elif acceptance.get("reviewer_role") == item.get("developer_role"):
                errors.append(f"{item['work_id']}: DELIVERY_INDEPENDENT_ACCEPTANCE_ROLE_CONFLICT")
            elif acceptance.get("reviewer_role") != item.get("reviewer_role"):
                errors.append(f"{item['work_id']}: DELIVERY_INDEPENDENT_REVIEWER_NOT_REGISTERED")
            elif not evidence_hash_matches(repo_root, acceptance.get("evidence_path", ""), acceptance.get("evidence_sha256", "")):
                errors.append(f"{item['work_id']}: DELIVERY_ACCEPTANCE_EVIDENCE_PATH_INVALID")
            exact_commit = acceptance.get("exact_commit") if acceptance else None
            integration_commit = item.get("integration_commit")
            if exact_commit and not git_commit_exists(repo_root, exact_commit):
                errors.append(f"{item['work_id']}: DELIVERY_ACCEPTANCE_COMMIT_INVALID")
            if not integration_commit:
                errors.append(f"{item['work_id']}: DELIVERY_INTEGRATION_COMMIT_REQUIRED")
            elif not git_commit_exists(repo_root, integration_commit):
                errors.append(f"{item['work_id']}: DELIVERY_INTEGRATION_COMMIT_INVALID")
            elif exact_commit and git_commit_exists(repo_root, exact_commit) and not git_is_ancestor(repo_root, exact_commit, integration_commit):
                errors.append(f"{item['work_id']}: DELIVERY_ACCEPTED_COMMIT_NOT_IN_INTEGRATION")

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
