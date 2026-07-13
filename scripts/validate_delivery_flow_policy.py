#!/usr/bin/env python3
import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

REQUIRED_FLOW_FIELDS = {
    "flow_class", "business_stream_id", "module_id", "priority", "risk_level",
    "updated_at", "target_date", "next_checkpoint", "status_expires_at",
    "developer_role", "reviewer_role", "approver_role", "blocks",
    "does_not_block", "auto_continue", "stop_conditions",
}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate(policy_path: Path, schema_path: Path, registry_path: Path) -> list[str]:
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    errors = [e.message for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(policy)]
    governed = [i for i in registry["work_items"] if i.get("flow_policy_version") == policy.get("contract_version")]
    for item in governed:
        missing = sorted(REQUIRED_FLOW_FIELDS - item.keys())
        if missing:
            errors.append(f"{item['work_id']}: missing flow fields: {', '.join(missing)}")
        if item.get("status") in {"active", "handoff-ready"}:
            if parse_time(item["status_expires_at"]) <= parse_time(item["updated_at"]):
                errors.append(f"{item['work_id']}: status expiry must be after updated_at")
        if item.get("risk_level") in {"high", "critical"}:
            roles = {item.get("developer_role"), item.get("reviewer_role"), item.get("approver_role")}
            if len(roles) != 3:
                errors.append(f"{item['work_id']}: high-risk roles must be separated")

    active_streams = {
        i["business_stream_id"]: i for i in governed
        if i.get("status") == "active" and i.get("flow_class") == "business-stream"
    }
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
