#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


def normalize(value: str) -> str:
    return str(PurePosixPath(value.replace("\\", "/"))).rstrip("/") or "."


def overlaps(left: str, right: str) -> bool:
    left, right = normalize(left), normalize(right)
    if "." in (left, right):
        return True
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def validate(schema_path: Path, registry_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(data)]
    owner_role = data.get("integration_owner_role")
    protected = data.get("protected_paths", [])
    active = [item for item in data.get("work_items", []) if item.get("status") in {"active", "handoff-ready"}]
    identities: dict[str, set[str]] = {"work_id": set(), "workspace_path": set(), "branch": set()}
    for item in data.get("work_items", []):
        for field in identities:
            value = normalize(item.get(field, ""))
            if value in identities[field]:
                errors.append(f"duplicate {field}: {value}")
            identities[field].add(value)
        if not item.get("started_with_clean_worktree"):
            if not item.get("preexisting_changes_acknowledged") or not item.get("migration_note"):
                errors.append(f"{item.get('work_id')}: dirty start requires explicit acknowledgement and migration_note")
        if any(overlaps(scope, guard) for scope in item.get("allowed_paths", []) for guard in protected):
            if item.get("owner_role") != owner_role:
                errors.append(f"{item.get('work_id')}: protected paths require role {owner_role}")
    for index, left in enumerate(active):
        for right in active[index + 1:]:
            if normalize(left["repository_root"]) != normalize(right["repository_root"]):
                continue
            if normalize(left["workspace_path"]) == normalize(right["workspace_path"]):
                errors.append(f"active work items share workspace: {left['work_id']} and {right['work_id']}")
            if any(overlaps(a, b) for a in left["allowed_paths"] for b in right["allowed_paths"]):
                errors.append(f"active work item scopes overlap: {left['work_id']} and {right['work_id']}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("registry", type=Path)
    args = parser.parse_args()
    errors = validate(args.schema, args.registry)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Agent collaboration registry is valid; active workspaces and scopes do not conflict.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
