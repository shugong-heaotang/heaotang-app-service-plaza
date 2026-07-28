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


def git_blob_at_commit(repo_root: Path, commit: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", f"{commit}:{path}"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def safe_repo_file(repo_root: Path, relative: str) -> Path | None:
    try:
        candidate = (repo_root / relative).resolve()
        candidate.relative_to(repo_root.resolve())
    except (ValueError, TypeError, OSError):
        return None
    return candidate


def canonical_row_sha256(row: dict) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_live_registry_extension(
    precondition_registry: dict,
    live_registry: dict,
    receipt: dict,
) -> list[str]:
    errors: list[str] = []
    historical_items = precondition_registry.get("work_items", [])
    live_items = live_registry.get("work_items", [])
    if len(live_items) < len(historical_items):
        errors.append("DELIVERY_LEGACY_CURRENT_REGISTRY_HISTORY_INVALID")
        return errors
    if any(
        live_items[index].get("work_id") != historical.get("work_id")
        for index, historical in enumerate(historical_items)
    ):
        errors.append("DELIVERY_LEGACY_CURRENT_REGISTRY_HISTORY_INVALID")
    live_ids = [item.get("work_id") for item in live_items]
    if any(not isinstance(work_id, str) or not work_id for work_id in live_ids) or len(live_ids) != len(set(live_ids)):
        errors.append("DELIVERY_LEGACY_CURRENT_REGISTRY_HISTORY_INVALID")

    transitions = {
        entry.get("registry_index"): entry
        for entry in receipt.get("transitions", [])
        if isinstance(entry.get("registry_index"), int)
    }
    for audit_entry in receipt.get("audit_scope", []):
        index = audit_entry.get("registry_index")
        work_id = audit_entry.get("work_id")
        if (
            not isinstance(index, int)
            or index < 0
            or index >= len(historical_items)
            or index >= len(live_items)
            or historical_items[index].get("work_id") != work_id
            or live_items[index].get("work_id") != work_id
        ):
            errors.append("DELIVERY_LEGACY_AUDIT_ROW_DRIFT")
            continue
        transition = transitions.get(index)
        expected_hash = (
            transition.get("current_row_sha256")
            if transition is not None
            else canonical_row_sha256(historical_items[index])
        )
        if canonical_row_sha256(historical_items[index]) != expected_hash or canonical_row_sha256(live_items[index]) != expected_hash:
            errors.append("DELIVERY_LEGACY_AUDIT_ROW_DRIFT")
    return errors


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


def validate_v2_receipt(
    registration: dict,
    repo_root: Path,
    registry: dict,
    registry_bytes: bytes,
) -> tuple[list[str], dict | None, str | None]:
    errors: list[str] = []
    receipt_path = safe_repo_file(repo_root, registration.get("receipt_path", ""))
    schema_path = safe_repo_file(repo_root, registration.get("schema_path", ""))
    if receipt_path is None or schema_path is None:
        return ["DELIVERY_LEGACY_RECEIPT_PATH_INVALID"], None, None
    if not receipt_path.is_file() or not schema_path.is_file():
        return ["DELIVERY_LEGACY_RECEIPT_OR_SCHEMA_MISSING"], None, None
    receipt_bytes = receipt_path.read_bytes()
    if hashlib.sha256(receipt_bytes).hexdigest() != registration.get("receipt_sha256"):
        errors.append("DELIVERY_LEGACY_RECEIPT_HASH_MISMATCH")
    try:
        receipt = json.loads(receipt_bytes.decode("utf-8"))
        receipt_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return errors + ["DELIVERY_LEGACY_RECEIPT_JSON_INVALID"], None, None
    errors.extend(
        f"DELIVERY_LEGACY_RECEIPT_SCHEMA: {error.message}"
        for error in Draft202012Validator(receipt_schema, format_checker=FormatChecker()).iter_errors(receipt)
    )
    if receipt.get("receipt_id") != registration.get("receipt_id") or receipt.get("contract_version") != registration.get("contract_version"):
        errors.append("DELIVERY_LEGACY_RECEIPT_REGISTRATION_MISMATCH")
    if (
        receipt.get("state") != "authorized-not-applied"
        or receipt.get("execution_enabled") is not False
        or receipt.get("applied") is not False
        or receipt.get("post_registry_sha256") is not None
        or receipt.get("review") is not None
        or receipt.get("integration") is not None
    ):
        errors.append("DELIVERY_LEGACY_RECEIPT_FALSE_AUTHORIZATION")

    task = receipt.get("task_order", {})
    if not evidence_hash_matches(repo_root, task.get("path", ""), task.get("sha256", "")):
        errors.append("DELIVERY_LEGACY_RECEIPT_TASK_ORDER_INVALID")
    source = receipt.get("source_registry", {})
    source_bytes = git_bytes_at_commit(repo_root, source.get("commit", ""), source.get("path", ""))
    if source_bytes is None or hashlib.sha256(source_bytes).hexdigest() != source.get("sha256"):
        errors.append("DELIVERY_LEGACY_RECEIPT_SOURCE_REGISTRY_INVALID")
        return errors, receipt, None
    current = receipt.get("current_registry_precondition", {})
    current_bytes = git_bytes_at_commit(repo_root, current.get("commit", ""), current.get("path", ""))
    if current_bytes is None or hashlib.sha256(current_bytes).hexdigest() != current.get("sha256"):
        errors.append("DELIVERY_LEGACY_CURRENT_REGISTRY_PRECONDITION_INVALID")
        return errors, receipt, None
    try:
        source_registry = json.loads(source_bytes.decode("utf-8"))
        precondition_registry = json.loads(current_bytes.decode("utf-8"))
        live_registry_from_bytes = json.loads(registry_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return errors + ["DELIVERY_LEGACY_RECEIPT_SOURCE_REGISTRY_INVALID"], receipt, None
    if live_registry_from_bytes != registry:
        errors.append("DELIVERY_LEGACY_CURRENT_REGISTRY_BYTES_INVALID")
        return errors, receipt, None

    transitions = receipt.get("transitions", [])
    indices = [entry.get("registry_index") for entry in transitions]
    if any(not isinstance(index, int) for index in indices):
        errors.append("DELIVERY_LEGACY_TRANSITION_INDEX_INVALID")
        return errors, receipt, None
    if indices != sorted(indices) or len(indices) != len(set(indices)):
        errors.append("DELIVERY_LEGACY_TRANSITION_ORDER_INVALID")
    canonical = "".join(
        f"{entry.get('registry_index')}\t{entry.get('work_id')}\t{entry.get('from_status')}\t{entry.get('to_status')}\n"
        for entry in transitions
    )
    if hashlib.sha256(canonical.encode("utf-8")).hexdigest() != receipt.get("transition_sha256"):
        errors.append("DELIVERY_LEGACY_TRANSITION_HASH_INVALID")
    source_items = source_registry.get("work_items", [])
    current_items = registry.get("work_items", [])
    modes: set[str] = set()
    transition_by_index: dict[int, dict] = {}
    for entry in transitions:
        index = entry.get("registry_index")
        if not isinstance(index, int) or index < 0 or index >= len(source_items) or index >= len(current_items):
            errors.append("DELIVERY_LEGACY_TRANSITION_INDEX_INVALID")
            continue
        transition_by_index[index] = entry
        before = source_items[index]
        current_row = current_items[index]
        if before.get("work_id") != entry.get("work_id") or before.get("status") != entry.get("from_status"):
            errors.append("DELIVERY_LEGACY_TRANSITION_BEFORE_MISMATCH")
        if canonical_row_sha256(before) != entry.get("source_row_sha256"):
            errors.append("DELIVERY_LEGACY_TRANSITION_SOURCE_ROW_HASH_INVALID")
        if canonical_row_sha256(current_row) != entry.get("current_row_sha256"):
            errors.append("DELIVERY_LEGACY_TRANSITION_CURRENT_ROW_HASH_INVALID")
        before_state = f"{entry.get('work_id')}\t{entry.get('from_status')}\n".encode("utf-8")
        after_state = f"{entry.get('work_id')}\t{entry.get('to_status')}\n".encode("utf-8")
        if hashlib.sha256(before_state).hexdigest() != entry.get("before_state_sha256"):
            errors.append("DELIVERY_LEGACY_TRANSITION_BEFORE_STATE_HASH_INVALID")
        if hashlib.sha256(after_state).hexdigest() != entry.get("after_state_sha256"):
            errors.append("DELIVERY_LEGACY_TRANSITION_AFTER_STATE_HASH_INVALID")
        if current_row.get("work_id") != entry.get("work_id"):
            modes.add("invalid")
        elif current_row.get("status") == entry.get("from_status"):
            modes.add("before")
        elif current_row.get("status") == entry.get("to_status"):
            modes.add("after")
        else:
            modes.add("invalid")
    mode = next(iter(modes)) if len(modes) == 1 else None
    if mode is None or mode not in set(registration.get("allowed_state_modes", [])):
        errors.append("DELIVERY_LEGACY_PARTIAL_TRANSITION")

    omitted = receipt.get("omitted_rows", [])
    omitted_indices = [entry.get("registry_index") for entry in omitted]
    audit = receipt.get("audit_scope", [])
    audit_pairs = [(entry.get("registry_index"), entry.get("work_id")) for entry in audit]
    covered_pairs = [(entry.get("registry_index"), entry.get("work_id")) for entry in transitions + omitted]
    if len(audit_pairs) != len(set(audit_pairs)) or sorted(audit_pairs) != sorted(covered_pairs):
        errors.append("DELIVERY_LEGACY_AUDIT_SCOPE_INVALID")
    if set(indices) & set(omitted_indices) or len(omitted_indices) != len(set(omitted_indices)):
        errors.append("DELIVERY_LEGACY_OMITTED_ROW_INVALID")
    for entry in omitted:
        index = entry.get("registry_index")
        if not isinstance(index, int) or index >= len(source_items) or source_items[index].get("work_id") != entry.get("work_id"):
            errors.append("DELIVERY_LEGACY_OMITTED_ROW_INVALID")
    errors.extend(validate_live_registry_extension(precondition_registry, registry, receipt))

    declared_groups = receipt.get("atomic_groups", [])
    group_members = {group.get("group_id"): group.get("members", []) for group in declared_groups}
    for group_id, members in group_members.items():
        actual = [entry.get("registry_index") for entry in transitions if entry.get("atomic_group") == group_id]
        if actual != members or len(members) < 2:
            errors.append("DELIVERY_LEGACY_ATOMIC_GROUP_INVALID")
    for entry in transitions:
        if entry.get("atomic_group") and entry.get("atomic_group") not in group_members:
            errors.append("DELIVERY_LEGACY_ATOMIC_GROUP_INVALID")

    effective = []
    for index, row in enumerate(source_items):
        transition = transition_by_index.get(index)
        status = transition.get("to_status") if transition else row.get("status")
        effective.append(f"{index}\t{row.get('work_id')}\t{status}\n")
    if hashlib.sha256("".join(effective).encode("utf-8")).hexdigest() != receipt.get("post_effective_states_sha256"):
        errors.append("DELIVERY_LEGACY_POST_STATES_HASH_INVALID")

    for evidence in receipt.get("evidence_files", []):
        evidence_bytes = git_bytes_at_commit(repo_root, evidence.get("authority_commit", ""), evidence.get("path", ""))
        if evidence_bytes is None or hashlib.sha256(evidence_bytes).hexdigest() != evidence.get("sha256"):
            errors.append("DELIVERY_LEGACY_EVIDENCE_COMMIT_BYTES_INVALID")
    evidence_keys = {
        (entry.get("authority_commit"), entry.get("path"))
        for entry in receipt.get("evidence_files", [])
    }
    repositories = receipt.get("repositories", {})
    for entry in transitions:
        basis = entry.get("projection_basis", {})
        source_row = source_items[entry["registry_index"]] if isinstance(entry.get("registry_index"), int) and entry["registry_index"] < len(source_items) else {}
        if entry.get("to_status") == "integrated":
            accepted_commit = basis.get("accepted_evidence_commit")
            subject_commit = basis.get("acceptance_subject_commit")
            accepted_path = basis.get("acceptance_evidence_path")
            reviewer_role = basis.get("reviewer_role")
            reviewed_at = basis.get("reviewed_at")
            acceptance_index = basis.get("acceptance_registry_index")
            acceptance_row = (
                current_items[acceptance_index]
                if isinstance(acceptance_index, int) and 0 <= acceptance_index < len(current_items)
                else {}
            )
            independent = acceptance_row.get("independent_acceptance", {})
            try:
                reviewed_time = parse_time(reviewed_at)
            except (AttributeError, TypeError, ValueError):
                reviewed_time = None
            if (
                basis.get("accepted_verdict") != "go"
                or not reviewer_role
                or reviewer_role == acceptance_row.get("developer_role")
                or reviewed_time is None
                or reviewed_time.tzinfo is None
                or (accepted_commit, accepted_path) not in evidence_keys
                or acceptance_row.get("work_id") != basis.get("acceptance_work_id")
                or acceptance_row.get("status") != "integrated"
                or independent.get("exact_commit") != subject_commit
                or independent.get("verdict") != basis.get("accepted_verdict")
                or independent.get("reviewer_role") != reviewer_role
                or independent.get("reviewed_at") != reviewed_at
                or independent.get("evidence_path") != accepted_path
                or not any(
                    evidence.get("path") == accepted_path
                    and evidence.get("authority_commit") == accepted_commit
                    and evidence.get("sha256") == independent.get("evidence_sha256")
                    for evidence in receipt.get("evidence_files", [])
                )
            ):
                errors.append("DELIVERY_LEGACY_INDEPENDENT_ACCEPTANCE_INVALID")
            integration_commit = basis.get("app_integration_commit")
            final_commit = basis.get("final_evidence_commit")
            if (
                not git_commit_exists(repo_root, accepted_commit or "")
                or not git_commit_exists(repo_root, subject_commit or "")
                or not git_commit_exists(repo_root, integration_commit or "")
                or not git_commit_exists(repo_root, final_commit or "")
                or not git_is_ancestor(repo_root, subject_commit or "", accepted_commit or "")
                or not git_is_ancestor(repo_root, accepted_commit or "", final_commit or "")
                or not git_is_ancestor(repo_root, integration_commit or "", final_commit or "")
            ):
                errors.append("DELIVERY_LEGACY_ACCEPTANCE_INTEGRATION_CHAIN_INVALID")
        replacement_index = basis.get("replacement_registry_index")
        if replacement_index is not None:
            if (
                not isinstance(replacement_index, int)
                or replacement_index >= len(current_items)
                or current_items[replacement_index].get("work_id") != basis.get("replacement_work_id")
                or current_items[replacement_index].get("status") != "integrated"
                or current_items[replacement_index].get("integration_commit") != basis.get("replacement_app_integration_commit")
            ):
                errors.append("DELIVERY_LEGACY_REPLACEMENT_EVIDENCE_INVALID")
        source_commit = basis.get("implementation_commit") or basis.get("legacy_implementation_commit")
        authority_commit = basis.get("backend_authority_commit")
        for blob in entry.get("blob_equivalence", []):
            repository = repositories.get(blob.get("repository_id"))
            repository_root = Path(repository).resolve() if repository else None
            if repository_root is None or not (repository_root / ".git").exists():
                errors.append("DELIVERY_LEGACY_BLOB_REPOSITORY_INVALID")
                continue
            source_blob = git_blob_at_commit(repository_root, source_commit or "", blob.get("path", ""))
            authority_blob = git_blob_at_commit(repository_root, authority_commit or "", blob.get("path", ""))
            if (
                source_blob is None
                or authority_blob is None
                or source_blob != blob.get("source_blob")
                or authority_blob != blob.get("authority_blob")
                or source_blob != authority_blob
            ):
                errors.append("DELIVERY_LEGACY_BLOB_EQUIVALENCE_INVALID")
    return errors, receipt, mode


ACTIVITY_ONLY_WORK_ID = "AIW-20260728-ACTIVITY-ONLY-LIFECYCLE-MIGRATION-R1"
ACTIVITY_ONLY_EXPIRED_ROWS = {
    109: "AIW-20260713-ACTIVITY-V3-M0",
    111: "AIW-20260713-PROTECTION-MALL-M2-CATALOG-SOLUTION",
    117: "AIW-20260712-NOVA-PHASE5-M1-RUNTIME",
    123: "AIW-20260714-PLATFORM-REGISTRY-DISPATCH-R1",
    130: "AIW-20260715-PLATFORM-REGISTRY-R12K-SOCIAL-OVERLAY-UNBLOCK",
    131: "AIW-20260715-PLATFORM-REGISTRY-R12L-PARALLEL-ACTIVATION",
    134: "AIW-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-V2-INDEPENDENT-ACCEPTANCE-R1",
    137: "AIW-20260715-PLATFORM-REGISTRY-R12M-LEGACY-GENERALIZATION-ACTIVATION",
    138: "AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-APPLICATION-R4",
    139: "AIW-20260715-PLATFORM-REGISTRY-R12N-R2-APPLICATION-ACTIVATION",
    140: "AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-REGISTRY-TRANSACTION-R12O",
}
ACTIVITY_ONLY_ALLOWED_PATHS = [
    "contracts/foundation/agent-collaboration.v1.json",
    "contracts/foundation/delivery-flow-policy.v4.json",
    "contracts/foundation/delivery-flow-policy.v4.schema.json",
    "contracts/foundation/legacy-lifecycle-migration.v3.schema.json",
    "contracts/foundation/legacy-lifecycle-migrations/LLM-20260728-ACTIVITY-ONLY-R1.json",
    "contracts/foundation/legacy-lifecycle-application.v2.schema.json",
    "contracts/foundation/legacy-lifecycle-applications/LLA-20260728-ACTIVITY-ONLY-R1.json",
    "scripts/validate_delivery_flow_policy.py",
    "scripts/tests/test_validate_delivery_flow_policy.py",
    "scripts/Test-ServicePlazaContracts.ps1",
    "docs/decisions/0022-activity-only-legacy-lifecycle-migration.md",
    "docs/project-management/notices/2026-07-28-platform-activity-only-lifecycle-migration-r1-task-order.md",
    "contracts/foundation/development-checklists/2026-07-28-platform-activity-only-lifecycle-migration-r1.json",
    "contracts/foundation/governance-exams/2026-07-28-platform-activity-only-lifecycle-migration-r1-attempt-1.json",
    "contracts/foundation/implementation-records/2026-07-28-platform-activity-only-lifecycle-migration-r1.json",
    "docs/project-management/service-plaza/platform-activity-only-lifecycle-migration-r1-handoff.md",
]


def canonical_row_sha256(row: dict) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_activity_only_v3_receipt(registration: dict, repo_root: Path, registry: dict) -> tuple[list[str], dict | None, str | None]:
    errors: list[str] = []
    receipt_path = registration.get("receipt_path", "")
    schema_path = registration.get("schema_path", "")
    if not evidence_hash_matches(repo_root, receipt_path, registration.get("receipt_sha256", "")):
        return ["DELIVERY_ACTIVITY_ONLY_RECEIPT_HASH_INVALID"], None, None
    try:
        receipt = json.loads((repo_root / receipt_path).read_text(encoding="utf-8"))
        schema = json.loads((repo_root / schema_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["DELIVERY_ACTIVITY_ONLY_RECEIPT_UNREADABLE"], None, None
    errors.extend(e.message for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(receipt))
    if receipt.get("source_registry", {}).get("commit") != "d428747a072ab8a21bc07667d3b65be4906fb6c2":
        errors.append("DELIVERY_ACTIVITY_ONLY_SOURCE_COMMIT_INVALID")
    source = git_json_at_commit(repo_root, "d428747a072ab8a21bc07667d3b65be4906fb6c2", LEGACY_SNAPSHOT_PATH)
    if source is None:
        errors.append("DELIVERY_ACTIVITY_ONLY_SOURCE_UNAVAILABLE")
    elif hashlib.sha256(
        subprocess.run(
            ["git", "-C", str(repo_root), "show", "d428747a072ab8a21bc07667d3b65be4906fb6c2:contracts/foundation/agent-collaboration.v1.json"],
            check=True, capture_output=True,
        ).stdout
    ).hexdigest() != receipt.get("source_registry", {}).get("sha256"):
        errors.append("DELIVERY_ACTIVITY_ONLY_SOURCE_HASH_INVALID")
    expected = receipt.get("activation_registry_precondition", {}).get("sha256")
    current = hashlib.sha256((repo_root / LEGACY_SNAPSHOT_PATH).read_bytes()).hexdigest()
    if expected != current:
        errors.append("DELIVERY_ACTIVITY_ONLY_ACTIVATION_CAS_INVALID")
    transition = receipt.get("transitions", [])
    if transition != [{"registry_index": 109, "work_id": ACTIVITY_ONLY_EXPIRED_ROWS[109], "from_status": "active", "to_status": "handoff-ready"}]:
        errors.append("DELIVERY_ACTIVITY_ONLY_TRANSITION_NOT_UNIQUE")
    for protected in receipt.get("protected_rows", []):
        index = protected.get("registry_index")
        if index not in {111, 112, 113, 114} or index >= len(registry["work_items"]):
            errors.append("DELIVERY_ACTIVITY_ONLY_MALL_SCOPE_INVALID")
            continue
        actual = canonical_row_sha256(registry["work_items"][index])
        if actual != protected.get("activation_row_sha256") or protected.get("activation_row_sha256") != protected.get("candidate_row_sha256"):
            errors.append(f"DELIVERY_ACTIVITY_ONLY_MALL_ROW_DRIFT:{index}")
    return errors, receipt, "activation-base"


def validate_activity_only_application(policy: dict, repo_root: Path, registry: dict) -> list[str]:
    errors: list[str] = []
    applications = policy.get("applications", [])
    if len(applications) != 1:
        return ["DELIVERY_ACTIVITY_ONLY_APPLICATION_REGISTRATION_INVALID"]
    registration = applications[0]
    path = registration.get("application_path", "")
    schema_path = registration.get("schema_path", "")
    if not evidence_hash_matches(repo_root, path, registration.get("application_sha256", "")):
        return ["DELIVERY_ACTIVITY_ONLY_APPLICATION_HASH_INVALID"]
    try:
        application = json.loads((repo_root / path).read_text(encoding="utf-8"))
        schema = json.loads((repo_root / schema_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["DELIVERY_ACTIVITY_ONLY_APPLICATION_UNREADABLE"]
    errors.extend(e.message for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(application))
    dispositions = application.get("expired_dispositions", [])
    actual_set = {(d.get("registry_index"), d.get("work_id")) for d in dispositions}
    expected_set = set(ACTIVITY_ONLY_EXPIRED_ROWS.items())
    if actual_set != expected_set or len(dispositions) != len(expected_set):
        errors.append("DELIVERY_ACTIVITY_ONLY_EXPIRED_SET_INVALID")
    source = git_json_at_commit(repo_root, "d428747a072ab8a21bc07667d3b65be4906fb6c2", LEGACY_SNAPSHOT_PATH)
    for disposition in dispositions:
        index = disposition.get("registry_index")
        if source is None or not isinstance(index, int) or index >= len(registry["work_items"]):
            errors.append("DELIVERY_ACTIVITY_ONLY_DISPOSITION_INDEX_INVALID")
            continue
        before = source["work_items"][index]
        after = registry["work_items"][index]
        if canonical_row_sha256(before) != disposition.get("before_row_sha256") or canonical_row_sha256(after) != disposition.get("after_row_sha256"):
            errors.append(f"DELIVERY_ACTIVITY_ONLY_DISPOSITION_HASH_INVALID:{index}")
        changed = {key for key in before.keys() | after.keys() if before.get(key) != after.get(key)}
        if changed != set(disposition.get("allowed_changed_fields", [])):
            errors.append(f"DELIVERY_ACTIVITY_ONLY_DISPOSITION_FIELDS_INVALID:{index}")
    targets = [item for item in registry["work_items"] if item.get("work_id") == ACTIVITY_ONLY_WORK_ID]
    if len(targets) != 1 or targets[0].get("allowed_paths") != ACTIVITY_ONLY_ALLOWED_PATHS:
        errors.append("DELIVERY_ACTIVITY_ONLY_WORK_ITEM_OR_PATHS_INVALID")
    if any(item.get("work_id") == "AIW-20260728-MEMBER-NOVA-TUTOR-IDENTITY-PROJECTION-R1" for item in registry["work_items"]):
        errors.append("DELIVERY_ACTIVITY_ONLY_P0_01_PREMATURE")
    if not application.get("r12o_guard", {}).get("activation_requires_separate_authorization"):
        errors.append("DELIVERY_ACTIVITY_ONLY_R12O_GUARD_MISSING")
    return errors


def validate_registered_receipts(
    policy: dict,
    repo_root: Path,
    registry: dict,
    registry_bytes: bytes,
) -> tuple[list[str], list[tuple[dict, dict, str | None]]]:
    if policy.get("contract_version") not in {"delivery-flow-policy.v3", "delivery-flow-policy.v4"}:
        old_errors, old_receipt = validate_legacy_receipt(policy, repo_root, registry)
        return old_errors, [({}, old_receipt, None)] if old_receipt else []
    errors: list[str] = []
    validated: list[tuple[dict, dict, str | None]] = []
    registrations = policy.get("migration", {}).get("receipts", [])
    identities = [(entry.get("receipt_id"), entry.get("receipt_path")) for entry in registrations]
    if len(identities) != len(set(identities)):
        errors.append("DELIVERY_LEGACY_RECEIPT_REGISTRATION_DUPLICATE")
    claimed_rows: set[int] = set()
    for registration in registrations:
        version = registration.get("contract_version")
        if version == "legacy-lifecycle-migration.v1":
            compatibility_policy = {
                "contract_version": "delivery-flow-policy.v2",
                "migration": {
                    "receipt_path": registration.get("receipt_path"),
                    "receipt_schema_path": registration.get("schema_path"),
                    "receipt_sha256": registration.get("receipt_sha256"),
                },
            }
            item_errors, receipt = validate_legacy_receipt(compatibility_policy, repo_root, registry)
            mode = None
        elif version == "legacy-lifecycle-migration.v2":
            item_errors, receipt, mode = validate_v2_receipt(registration, repo_root, registry, registry_bytes)
        elif version == "legacy-lifecycle-migration.v3":
            item_errors, receipt, mode = validate_activity_only_v3_receipt(registration, repo_root, registry)
        else:
            item_errors, receipt, mode = ["DELIVERY_LEGACY_RECEIPT_VERSION_UNSUPPORTED"], None, None
        errors.extend(item_errors)
        if receipt is None:
            continue
        if receipt.get("receipt_id") != registration.get("receipt_id"):
            errors.append("DELIVERY_LEGACY_RECEIPT_REGISTRATION_MISMATCH")
        row_key = "legacy_index" if version == "legacy-lifecycle-migration.v1" else "registry_index"
        claimed_entries = receipt.get("transitions", [])
        if version == "legacy-lifecycle-migration.v2":
            claimed_entries = receipt.get("audit_scope", [])
        rows = {entry.get(row_key) for entry in claimed_entries}
        if version != "legacy-lifecycle-migration.v3" and claimed_rows & rows:
            errors.append("DELIVERY_LEGACY_RECEIPT_ROW_OVERLAP")
        if version != "legacy-lifecycle-migration.v3":
            claimed_rows.update(rows)
        validated.append((registration, receipt, mode))
    return errors, validated


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
    receipt_errors, validated_receipts = validate_registered_receipts(
        policy, repo_root, registry, registry_path.read_bytes()
    )
    errors.extend(receipt_errors)
    if policy.get("contract_version") == "delivery-flow-policy.v4":
        errors.extend(validate_activity_only_application(policy, repo_root, registry))
        immutable_artifacts = {
            "contracts/foundation/delivery-flow-policy.v3.json": "1880c069f7fa2e7a3933ca3d749c37adf00d53377bef430e908fbb90abc39841",
            "contracts/foundation/legacy-lifecycle-migration.v1.schema.json": "f35ece671353c53e7314c9eadc1f0b0f6262ceba1e3e292e78b73022a038cde5",
            "contracts/foundation/legacy-lifecycle-migration.v2.schema.json": "ab63b7d55ab652a1e51d34a17363946be9c991c3719dcf1b4d5875e47495ef8a",
            "contracts/foundation/legacy-lifecycle-migrations/LLM-20260715-ACTIVITY-MALL-M2-R1.json": "5e85735d7c70a942efca1b8a8c6d9aecee4805a40282ae8cfbac27beab3207b1",
            "contracts/foundation/legacy-lifecycle-migrations/LLM-20260715-TECHNICAL-SOCIAL-BATCH-R2.json": "13b5096c9af214b9f5c010b0ece65802cdbcef7fb19602c76aa8c6e0c9873cf6",
        }
        for path, expected_hash in immutable_artifacts.items():
            if not evidence_hash_matches(repo_root, path, expected_hash):
                errors.append(f"DELIVERY_IMMUTABLE_LEGACY_ARTIFACT_CHANGED:{path}")
    activity_migrated_integrated_ids: set[str] = set()
    if policy.get("contract_version") == "delivery-flow-policy.v4":
        application_path = policy.get("applications", [{}])[0].get("application_path", "")
        if evidence_exists(repo_root, application_path):
            application = json.loads((repo_root / application_path).read_text(encoding="utf-8"))
            activity_migrated_integrated_ids = {
                entry.get("work_id")
                for entry in application.get("expired_dispositions", [])
                if entry.get("action") == "integrate"
            }
    receipt = next(
        (
            candidate
            for registration, candidate, _mode in validated_receipts
            if registration.get("contract_version") == "legacy-lifecycle-migration.v1"
            or candidate.get("contract_version") == "legacy-lifecycle-migration.v1"
        ),
        None,
    )
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
        if item.get("status") == "integrated" and item.get("work_id") not in activity_migrated_integrated_ids:
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
