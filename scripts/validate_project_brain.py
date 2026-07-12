from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SNAPSHOT_KEYS = {"contract_version", "generated_at", "source_commit", "overall_verdict", "source_freshness", "modules", "work_summary", "active_work", "pending_decisions", "risks", "acceptance_queue", "recent_integrations", "audit_summary"}
AUDIT_KEYS = {"contract_version", "generated_at", "source_commit", "verdict", "errors", "warnings", "unknowns", "rule_summary"}
FINDING_KEYS = {"rule_id", "severity", "subject_type", "subject_id", "source_path", "message"}
FORBIDDEN = ("password", "authorization", "api_key", "private_key", "workspace_path", "repository_root")


def validate(snapshot: dict, audit: dict) -> list[str]:
    errors: list[str] = []
    if set(snapshot) != SNAPSHOT_KEYS:
        errors.append("snapshot top-level contract mismatch")
    if set(audit) != AUDIT_KEYS:
        errors.append("audit top-level contract mismatch")
    if snapshot.get("contract_version") != "project-brain.snapshot.v1":
        errors.append("snapshot version mismatch")
    if audit.get("contract_version") != "project-brain.audit.v1":
        errors.append("audit version mismatch")
    findings = sum((audit.get(name, []) for name in ("errors", "warnings", "unknowns")), [])
    for item in findings:
        if not isinstance(item, dict) or set(item) != FINDING_KEYS:
            errors.append("audit finding contract mismatch")
    if audit.get("errors") and (audit.get("verdict") != "no-go" or snapshot.get("overall_verdict") != "no-go"):
        errors.append("errors must fail closed")
    encoded = json.dumps({"snapshot": snapshot, "audit": audit}, ensure_ascii=False).casefold()
    for name in FORBIDDEN:
        if f'"{name.casefold()}"' in encoded:
            errors.append(f"forbidden output field: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--audit", required=True, type=Path)
    args = parser.parse_args()
    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        audit = json.loads(args.audit.read_text(encoding="utf-8"))
        errors = validate(snapshot, audit)
    except (OSError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 2
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
