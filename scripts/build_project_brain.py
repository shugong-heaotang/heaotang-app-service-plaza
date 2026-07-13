from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ACTIVE = {"active", "planned", "handoff-ready"}
CATALOGS = ("modules", "knowledge-sources", "decisions", "risks")
WORK_FIELDS = ("work_id", "title", "owner_role", "status", "branch", "handoff_record")
FORBIDDEN_PARTS = {".env", ".git", "logs", "secrets", "credentials"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_repo_path(root: Path, value: str) -> Path:
    if not value or Path(value).is_absolute() or ".." in Path(value).parts:
        raise ValueError(f"unsafe repository path: {value}")
    if any(part.lower() in FORBIDDEN_PARTS for part in Path(value).parts):
        raise ValueError(f"forbidden repository path: {value}")
    resolved_root = root.resolve()
    candidate = (resolved_root / value).resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValueError(f"path escapes repository: {value}")
    return candidate


def finding(rule: str, severity: str, kind: str, identity: str, source: str, message: str) -> dict[str, str]:
    return {"rule_id": rule, "severity": severity, "subject_type": kind,
            "subject_id": identity or "unknown", "source_path": source, "message": message}


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def overlaps(left: list[str], right: list[str]) -> bool:
    for raw_a in left:
        a = raw_a.rstrip("/")
        for raw_b in right:
            b = raw_b.rstrip("/")
            if a == "." or b == "." or a == b or a.startswith(b + "/") or b.startswith(a + "/"):
                return True
    return False


def public_work(item: dict[str, Any]) -> dict[str, Any]:
    return {key: item[key] for key in WORK_FIELDS if key in item}


def validate_catalog(root: Path, name: str, now: datetime) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    rel = f"contracts/project-brain/{name}.v1.json"
    schema_rel = f"contracts/project-brain/{name}.v1.schema.json"
    output: list[dict[str, str]] = []
    try:
        path, schema_path = safe_repo_path(root, rel), safe_repo_path(root, schema_rel)
        data, schema = read_json(path), read_json(schema_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [], [finding("PB-SOURCE", "error", "catalog", name, rel, str(exc))]
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    for error in errors:
        output.append(finding("PB-SCHEMA", "error", "catalog", name, rel, error.message))
    items = data.get("items", []) if isinstance(data, dict) else []
    seen_ids: set[str] = set()
    id_key = {"modules": "module_id", "knowledge-sources": "knowledge_id", "decisions": "decision_id", "risks": "risk_id"}[name]
    authority_sources: set[str] = set()
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        identity = str(item.get(id_key, ""))
        if identity in seen_ids:
            output.append(finding("PB-DUPLICATE-ID", "error", name, identity, rel, "duplicate catalog identity"))
        seen_ids.add(identity)
        source = str(item.get("source_path", ""))
        try:
            if not safe_repo_path(root, source).exists():
                raise FileNotFoundError(source)
        except (OSError, ValueError) as exc:
            output.append(finding("PB-AUTHORITY-PATH", "error", name, identity, rel, str(exc)))
        if name == "knowledge-sources" and item.get("status") == "authoritative":
            normalized = source.casefold()
            if normalized in authority_sources:
                output.append(finding("PB-DUPLICATE-AUTHORITY", "error", name, identity, rel, "authority source is duplicated"))
            authority_sources.add(normalized)
            due = parse_time(item.get("next_review_at"))
            if due is None or due < now:
                output.append(finding("PB-STALE-SOURCE", "warning", name, identity, rel, "review date is missing, invalid, or expired"))
        if name == "modules" and parse_time(item.get("source_updated_at")) is None:
            output.append(finding("PB-MODULE-FRESHNESS", "error", name, identity, rel, "module source_updated_at is invalid"))
    return items if isinstance(items, list) else [], output


def audit_work(items: list[dict[str, Any]], now: datetime) -> list[dict[str, str]]:
    source = "contracts/foundation/agent-collaboration.v1.json"
    out: list[dict[str, str]] = []
    ids: set[str] = set()
    active = [item for item in items if item.get("status") in ACTIVE]
    for item in items:
        identity = str(item.get("work_id", ""))
        if not identity or identity in ids:
            out.append(finding("PB-WORK-ID", "error", "work-item", identity, source, "work_id is missing or duplicated"))
        ids.add(identity)
        if item.get("status") == "active" and not item.get("next_checkpoint"):
            out.append(finding("PB-WORK-NEXT", "warning", "work-item", identity, source, "active work lacks an explicit next checkpoint"))
        expiry = item.get("status_expires_at")
        if expiry and (parse_time(expiry) is None or parse_time(expiry) < now):
            out.append(finding("PB-WORK-STALE", "error", "work-item", identity, source, "status expiry is invalid or elapsed"))
        if item.get("status") == "integrated" and not item.get("handoff_record"):
            out.append(finding("PB-INTEGRATED-EVIDENCE", "error", "work-item", identity, source, "integrated work lacks a Handoff reference"))
        risk = str(item.get("risk_level", "")).lower()
        if risk in {"high", "critical"}:
            roles = [item.get(k) for k in ("developer", "reviewer", "approver")]
            if any(not role for role in roles) or len(set(roles)) != 3:
                out.append(finding("PB-ROLE-SEPARATION", "error", "work-item", identity, source, "high-risk work lacks three distinct roles"))
    for pos, left in enumerate(active):
        for right in active[pos + 1:]:
            pair = f"{left.get('work_id')}|{right.get('work_id')}"
            if left.get("workspace_path") == right.get("workspace_path"):
                out.append(finding("PB-WORKSPACE-CONFLICT", "error", "work-pair", pair, source, "active work shares a workspace"))
            if overlaps(left.get("allowed_paths", []), right.get("allowed_paths", [])):
                out.append(finding("PB-SCOPE-CONFLICT", "error", "work-pair", pair, source, "active allowed paths overlap"))
    return out


def source_commit(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def build_snapshot(root: Path, now: datetime | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root.resolve()
    now = now or datetime.now(timezone.utc)
    registry_rel = "contracts/foundation/agent-collaboration.v1.json"
    registry = read_json(safe_repo_path(root, registry_rel))
    items = registry.get("work_items", [])
    if not isinstance(items, list):
        raise ValueError("work_items must be an array")
    findings = audit_work(items, now)
    catalogs: dict[str, list[dict[str, Any]]] = {}
    for name in CATALOGS:
        catalogs[name], extra = validate_catalog(root, name, now)
        findings.extend(extra)
    counts = Counter(str(item.get("status", "unknown")) for item in items)
    severities = Counter(item["severity"] for item in findings)
    verdict = "no-go" if severities["error"] else "partial-go" if severities["warning"] or severities["unknown"] else "go"
    stamp = now.isoformat().replace("+00:00", "Z")
    commit = source_commit(root)
    snapshot = {
        "contract_version": "project-brain.snapshot.v1", "generated_at": stamp, "source_commit": commit,
        "overall_verdict": verdict, "source_freshness": "current" if commit != "unknown" else "unknown",
        "modules": catalogs["modules"], "work_summary": dict(sorted(counts.items())),
        "active_work": [public_work(item) for item in items if item.get("status") in ACTIVE],
        "pending_decisions": [x for x in catalogs["decisions"] if x.get("status") == "pending"],
        "risks": catalogs["risks"],
        "acceptance_queue": [public_work(item) for item in items if item.get("status") == "handoff-ready"],
        "recent_integrations": [public_work(item) for item in items if item.get("status") == "integrated"][-10:],
        "audit_summary": dict(sorted(severities.items())),
    }
    audit = {
        "contract_version": "project-brain.audit.v1", "generated_at": stamp, "source_commit": commit,
        "verdict": verdict,
        "errors": [x for x in findings if x["severity"] == "error"],
        "warnings": [x for x in findings if x["severity"] == "warning"],
        "unknowns": [x for x in findings if x["severity"] == "unknown"],
        "rule_summary": dict(sorted(Counter(x["rule_id"] for x in findings).items())),
    }
    return snapshot, audit


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--audit", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        snapshot, audit = build_snapshot(args.project_root)
        atomic_write_json(args.snapshot, snapshot)
        atomic_write_json(args.audit, audit)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Project Brain build failed: {exc}", file=sys.stderr)
        return 2
    return 1 if audit["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
