"""Fail CI when a Service Plaza v1 contract change is not backward compatible."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True, order=True)
class Finding:
    rule: str
    path: str
    message: str


def load_json(path: Path, git_ref: str | None = None) -> Any:
    try:
        if git_ref:
            result = subprocess.run(
                ["git", "show", f"{git_ref}:{path.as_posix()}"],
                check=True,
                capture_output=True,
            )
            return json.loads(result.stdout.decode("utf-8"))
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        raise ValueError(f"cannot read {path}: {error}") from error


def pointer(path: Iterable[str]) -> str:
    parts = [part.replace("~", "~0").replace("/", "~1") for part in path]
    return "/" + "/".join(parts) if parts else "/"


def add(findings: list[Finding], rule: str, path: Iterable[str], message: str) -> None:
    findings.append(Finding(rule, pointer(path), message))


def detect_kind(old: Any, new: Any) -> str:
    if isinstance(old, dict) and isinstance(new, dict):
        if "$schema" in old or "$schema" in new or "$defs" in old or "$defs" in new:
            return "json-schema"
        versions = {old.get("contract_version"), new.get("contract_version")}
        if any(isinstance(version, str) and version.startswith("service-plaza.action.") for version in versions):
            return "action-baseline"
        if any(isinstance(version, str) and version.startswith("service-plaza.") for version in versions):
            return "service-manifest"
    raise ValueError("cannot detect contract kind; pass --kind explicitly")


def compare_contract_version(old: dict[str, Any], new: dict[str, Any], findings: list[Finding]) -> None:
    if old.get("contract_version") != new.get("contract_version"):
        add(
            findings,
            "CONTRACT_VERSION_CHANGED",
            ["contract_version"],
            f"{old.get('contract_version')!r} -> {new.get('contract_version')!r}; compare changes within one contract version only",
        )


def compare_action_baseline(old: dict[str, Any], new: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    compare_contract_version(old, new, findings)
    if old.get("page_id") != new.get("page_id"):
        add(findings, "PAGE_ID_CHANGED", ["page_id"], f"{old.get('page_id')!r} -> {new.get('page_id')!r}")

    old_actions = old.get("actions")
    new_actions = new.get("actions")
    if not isinstance(old_actions, list) or not isinstance(new_actions, list):
        add(findings, "INVALID_ACTION_LIST", ["actions"], "both baselines must contain an actions array")
        return findings

    old_ids = [item.get("action_id") if isinstance(item, dict) else None for item in old_actions]
    new_ids = [item.get("action_id") if isinstance(item, dict) else None for item in new_actions]
    if len(old_ids) != len(new_ids) or old.get("expected_action_count") != new.get("expected_action_count"):
        add(
            findings,
            "ACTION_SET_CHANGED",
            ["actions"],
            f"locked action count changed from {len(old_ids)} to {len(new_ids)}",
        )

    removed = [action_id for action_id in old_ids if action_id not in new_ids]
    for action_id in removed:
        add(findings, "ACTION_REMOVED", ["actions", str(old_ids.index(action_id))], f"action_id {action_id!r} was removed")

    shared_old = [action_id for action_id in old_ids if action_id in new_ids]
    shared_new = [action_id for action_id in new_ids if action_id in old_ids]
    if shared_old != shared_new:
        add(findings, "ACTION_REORDERED", ["actions"], f"existing action order changed: {shared_old!r} -> {shared_new!r}")

    old_by_id = {item.get("action_id"): item for item in old_actions if isinstance(item, dict) and item.get("action_id")}
    new_by_id = {item.get("action_id"): item for item in new_actions if isinstance(item, dict) and item.get("action_id")}
    old_slots = {item.get("sort_order"): item.get("action_id") for item in old_actions if isinstance(item, dict)}
    new_slots = {item.get("sort_order"): item.get("action_id") for item in new_actions if isinstance(item, dict)}
    for slot, old_id in old_slots.items():
        new_id = new_slots.get(slot)
        if new_id is not None and new_id != old_id:
            add(findings, "ACTION_ID_REUSED", ["actions"], f"sort_order {slot!r} was reassigned from {old_id!r} to {new_id!r}")

    boundary_fields = (
        "region",
        "sort_order",
        "action_type",
        "target",
        "service_id",
        "return_target",
        "telemetry_event",
    )
    for action_id in sorted(old_by_id.keys() & new_by_id.keys()):
        before = old_by_id[action_id]
        after = new_by_id[action_id]
        index = new_ids.index(action_id)
        for field in boundary_fields:
            if before.get(field) != after.get(field):
                add(
                    findings,
                    "ACTION_BOUNDARY_CHANGED",
                    ["actions", str(index), field],
                    f"action {action_id!r}: {before.get(field)!r} -> {after.get(field)!r}",
                )
        compare_access(before.get("access"), after.get("access"), findings, ["actions", str(index), "access"], action_id)
        if before.get("lifecycle_status") == "active" and after.get("lifecycle_status") != "active":
            add(
                findings,
                "ACTIVE_ACTION_DISABLED",
                ["actions", str(index), "lifecycle_status"],
                f"action {action_id!r} changed from active to {after.get('lifecycle_status')!r}",
            )
    return findings


def compare_access(
    old: Any,
    new: Any,
    findings: list[Finding],
    path: list[str],
    identity: str,
) -> None:
    if not isinstance(old, dict) or not isinstance(new, dict):
        if old != new:
            add(findings, "AUTH_BOUNDARY_CHANGED", path, f"{identity!r}: access definition changed")
        return
    if old.get("auth_mode") != new.get("auth_mode"):
        add(
            findings,
            "AUTH_BOUNDARY_CHANGED",
            [*path, "auth_mode"],
            f"{identity!r}: {old.get('auth_mode')!r} -> {new.get('auth_mode')!r}",
        )
    old_scopes = set(old.get("required_scopes") or [])
    new_scopes = set(new.get("required_scopes") or [])
    if old_scopes != new_scopes:
        add(
            findings,
            "SCOPE_BOUNDARY_CHANGED",
            [*path, "required_scopes"],
            f"{identity!r}: {sorted(old_scopes)!r} -> {sorted(new_scopes)!r}",
        )


def value_at(document: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = document
    for part in path:
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def compare_service_manifest(old: dict[str, Any], new: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    compare_contract_version(old, new, findings)
    identity = str(old.get("service_id"))
    required_paths = (
        ("service_id",),
        ("display_name",),
        ("summary",),
        ("category",),
        ("sort_order",),
        ("lifecycle_status",),
        ("entry",),
        ("entry", "type"),
        ("entry", "target"),
        ("entry", "return_target"),
        ("access",),
        ("access", "auth_mode"),
        ("access", "required_scopes"),
        ("provider",),
        ("provider", "provider_id"),
        ("provider", "display_name"),
        ("capabilities",),
        ("privacy_level",),
        ("business_api_version",),
    )
    for path in required_paths:
        if value_at(old, path) is not None and value_at(new, path) is None:
            add(findings, "MANIFEST_FIELD_REMOVED", path, f"required manifest field {'.'.join(path)!r} was removed")
    boundary_paths = (
        ("service_id",),
        ("category",),
        ("entry", "type"),
        ("entry", "target"),
        ("entry", "return_target"),
        ("provider", "provider_id"),
        ("privacy_level",),
        ("business_api_version",),
    )
    for path in boundary_paths:
        before = value_at(old, path)
        after = value_at(new, path)
        if before != after:
            add(findings, "SERVICE_BOUNDARY_CHANGED", path, f"service {identity!r}: {before!r} -> {after!r}")
    compare_access(old.get("access"), new.get("access"), findings, ["access"], identity)

    old_capabilities = set(old.get("capabilities") or [])
    new_capabilities = set(new.get("capabilities") or [])
    removed_capabilities = sorted(old_capabilities - new_capabilities)
    if removed_capabilities:
        add(
            findings,
            "CAPABILITY_REMOVED",
            ["capabilities"],
            f"service {identity!r} removed {removed_capabilities!r}",
        )
    if old.get("lifecycle_status") == "active" and new.get("lifecycle_status") != "active":
        add(
            findings,
            "ACTIVE_SERVICE_DISABLED",
            ["lifecycle_status"],
            f"service {identity!r} changed from active to {new.get('lifecycle_status')!r}",
        )
    return findings


def normalized_types(schema: dict[str, Any]) -> set[str] | None:
    value = schema.get("type")
    if isinstance(value, str):
        return {value}
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return set(value)
    return None


def compare_schema_node(old: Any, new: Any, path: list[str], findings: list[Finding]) -> None:
    if not isinstance(old, dict) or not isinstance(new, dict):
        if old != new:
            add(findings, "SCHEMA_NODE_REPLACED", path, "schema node was replaced with a different shape")
        return

    old_types = normalized_types(old)
    new_types = normalized_types(new)
    if old_types is not None and new_types is not None and not old_types.issubset(new_types):
        add(findings, "TYPE_NARROWED", [*path, "type"], f"accepted types narrowed from {sorted(old_types)!r} to {sorted(new_types)!r}")
    if "$ref" in old and old.get("$ref") != new.get("$ref"):
        add(findings, "REFERENCE_CHANGED", [*path, "$ref"], f"{old.get('$ref')!r} -> {new.get('$ref')!r}")
    if "const" in old and "const" in new and old.get("const") != new.get("const"):
        add(findings, "CONST_CHANGED", [*path, "const"], f"{old.get('const')!r} -> {new.get('const')!r}")
    if "const" not in old and "const" in new:
        add(findings, "CONST_ADDED", [*path, "const"], f"new const {new.get('const')!r} narrows accepted values")

    old_enum = old.get("enum")
    new_enum = new.get("enum")
    encode = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True)
    if isinstance(old_enum, list) and isinstance(new_enum, list) and not set(map(encode, old_enum)).issubset(set(map(encode, new_enum))):
        add(findings, "ENUM_NARROWED", [*path, "enum"], f"accepted enum values changed from {old_enum!r} to {new_enum!r}")
    if old_enum is None and isinstance(new_enum, list):
        add(findings, "ENUM_ADDED", [*path, "enum"], "a new enum restricts previously accepted values")

    lower_bounds = ("minimum", "exclusiveMinimum", "minLength", "minItems", "minProperties")
    upper_bounds = ("maximum", "exclusiveMaximum", "maxLength", "maxItems", "maxProperties")
    for keyword in lower_bounds:
        if keyword in new and (keyword not in old or new[keyword] > old[keyword]):
            add(findings, "LOWER_BOUND_TIGHTENED", [*path, keyword], f"{old.get(keyword)!r} -> {new[keyword]!r}")
    for keyword in upper_bounds:
        if keyword in new and (keyword not in old or new[keyword] < old[keyword]):
            add(findings, "UPPER_BOUND_TIGHTENED", [*path, keyword], f"{old.get(keyword)!r} -> {new[keyword]!r}")
    if new.get("pattern") != old.get("pattern") and "pattern" in new:
        add(findings, "PATTERN_ADDED_OR_CHANGED", [*path, "pattern"], f"{old.get('pattern')!r} -> {new.get('pattern')!r}")
    if new.get("format") != old.get("format") and "format" in new:
        add(findings, "FORMAT_ADDED_OR_CHANGED", [*path, "format"], f"{old.get('format')!r} -> {new.get('format')!r}")
    if new.get("multipleOf") != old.get("multipleOf") and "multipleOf" in new:
        add(findings, "MULTIPLE_OF_ADDED_OR_CHANGED", [*path, "multipleOf"], f"{old.get('multipleOf')!r} -> {new.get('multipleOf')!r}")
    if old.get("additionalProperties", True) is not False and new.get("additionalProperties") is False:
        add(findings, "ADDITIONAL_PROPERTIES_FORBIDDEN", [*path, "additionalProperties"], "previously accepted properties are now forbidden")
    if not isinstance(old.get("additionalProperties"), dict) and isinstance(new.get("additionalProperties"), dict):
        add(findings, "ADDITIONAL_PROPERTIES_CONSTRAINED", [*path, "additionalProperties"], "additional properties now have a validation schema")
    if isinstance(old.get("additionalProperties"), dict) and isinstance(new.get("additionalProperties"), dict):
        compare_schema_node(old["additionalProperties"], new["additionalProperties"], [*path, "additionalProperties"], findings)
    if old.get("uniqueItems") is not True and new.get("uniqueItems") is True:
        add(findings, "UNIQUE_ITEMS_REQUIRED", [*path, "uniqueItems"], "duplicate array items are no longer accepted")

    old_required = set(old.get("required") or [])
    new_required = set(new.get("required") or [])
    for field in sorted(new_required - old_required):
        add(findings, "REQUIRED_FIELD_ADDED", [*path, "required"], f"field {field!r} became required")

    old_properties = old.get("properties") if isinstance(old.get("properties"), dict) else {}
    new_properties = new.get("properties") if isinstance(new.get("properties"), dict) else {}
    for field in sorted(old_properties.keys() - new_properties.keys()):
        add(findings, "PROPERTY_REMOVED", [*path, "properties", field], f"property {field!r} was removed")
    for field in sorted(old_properties.keys() & new_properties.keys()):
        compare_schema_node(old_properties[field], new_properties[field], [*path, "properties", field], findings)

    old_defs = old.get("$defs") if isinstance(old.get("$defs"), dict) else {}
    new_defs = new.get("$defs") if isinstance(new.get("$defs"), dict) else {}
    for name in sorted(old_defs.keys() - new_defs.keys()):
        add(findings, "DEFINITION_REMOVED", [*path, "$defs", name], f"definition {name!r} was removed")
    for name in sorted(old_defs.keys() & new_defs.keys()):
        compare_schema_node(old_defs[name], new_defs[name], [*path, "$defs", name], findings)

    if not isinstance(old.get("items"), dict) and isinstance(new.get("items"), dict):
        add(findings, "ARRAY_ITEMS_CONSTRAINED", [*path, "items"], "array items now have a validation schema")
    if isinstance(old.get("items"), dict) and isinstance(new.get("items"), dict):
        compare_schema_node(old["items"], new["items"], [*path, "items"], findings)
    if old.get("items") is not False and new.get("items") is False:
        add(findings, "ARRAY_ITEMS_FORBIDDEN", [*path, "items"], "additional array items are now forbidden")
    old_prefix = old.get("prefixItems") if isinstance(old.get("prefixItems"), list) else []
    new_prefix = new.get("prefixItems") if isinstance(new.get("prefixItems"), list) else []
    if len(new_prefix) < len(old_prefix):
        add(findings, "PREFIX_ITEM_REMOVED", [*path, "prefixItems"], f"tuple length changed from {len(old_prefix)} to {len(new_prefix)}")
    for index in range(min(len(old_prefix), len(new_prefix))):
        compare_schema_node(old_prefix[index], new_prefix[index], [*path, "prefixItems", str(index)], findings)
    for keyword in ("allOf", "anyOf", "oneOf", "not", "contains", "dependentRequired", "propertyNames"):
        if keyword in new and encode(old.get(keyword)) != encode(new.get(keyword)):
            add(findings, "SCHEMA_COMPOSITION_CHANGED", [*path, keyword], f"{keyword} was added or changed; compatibility requires explicit review")


def compare_json_schema(old: dict[str, Any], new: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if old.get("$id") != new.get("$id"):
        add(findings, "SCHEMA_ID_CHANGED", ["$id"], f"{old.get('$id')!r} -> {new.get('$id')!r}")
    compare_schema_node(old, new, [], findings)
    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", type=Path, help="last released JSON contract")
    parser.add_argument("new", type=Path, help="candidate JSON contract")
    parser.add_argument(
        "--kind",
        choices=("auto", "action-baseline", "service-manifest", "json-schema"),
        default="auto",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--old-git-ref", help="load OLD from this Git revision instead of the worktree")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        old = load_json(args.old, args.old_git_ref)
        new = load_json(args.new)
        kind = detect_kind(old, new) if args.kind == "auto" else args.kind
        if not isinstance(old, dict) or not isinstance(new, dict):
            raise ValueError("contract roots must be JSON objects")
        comparators = {
            "action-baseline": compare_action_baseline,
            "service-manifest": compare_service_manifest,
            "json-schema": compare_json_schema,
        }
        findings = sorted(set(comparators[kind](old, new)))
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps({"compatible": not findings, "kind": kind, "findings": [finding.__dict__ for finding in findings]}, ensure_ascii=False, indent=2))
    elif findings:
        print(f"BREAKING: {len(findings)} incompatible {kind} change(s):", file=sys.stderr)
        for finding in findings:
            print(f"- [{finding.rule}] {finding.path}: {finding.message}", file=sys.stderr)
    else:
        print(f"Compatible {kind} change: no backward-incompatible differences found.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
