#!/usr/bin/env python3
"""Validate the foundation capability graph and evidence paths."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ALLOWED_STATUS = {"draft", "implemented", "verified", "deployed", "deprecated"}
READY_STATUS = {"verified", "deployed"}
ID_PATTERN = re.compile(r"^foundation\.[a-z0-9]+(?:[.-][a-z0-9]+)*$")


def schema_errors(schema_path: Path, instance: object, label: str) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return [
        f"{label}:{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda item: list(item.path))
    ]


def validate(registry_path: Path, project_root: Path, module_paths: list[Path] | None = None) -> list[str]:
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    errors = schema_errors(registry_path.with_name("foundation-capabilities.v1.schema.json"), data, "registry")
    if data.get("contract_version") != "foundation-capabilities.v1":
        errors.append("contract_version must be foundation-capabilities.v1")
    capabilities = data.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        return errors + ["capabilities must be a non-empty array"]
    by_id: dict[str, dict] = {}
    gate_ids: set[str] = set()
    for capability in capabilities:
        capability_id = capability.get("capability_id", "")
        if not ID_PATTERN.fullmatch(capability_id):
            errors.append(f"invalid capability_id: {capability_id!r}")
        if capability_id in by_id:
            errors.append(f"duplicate capability_id: {capability_id}")
        by_id[capability_id] = capability
        if capability.get("status") not in ALLOWED_STATUS:
            errors.append(f"{capability_id}: invalid status")
        if not re.fullmatch(r"v[1-9][0-9]*", str(capability.get("version", ""))):
            errors.append(f"{capability_id}: invalid version")
        for gate in capability.get("gates", []):
            gate_id = gate.get("gate_id", "")
            if gate_id in gate_ids:
                errors.append(f"duplicate gate_id: {gate_id}")
            gate_ids.add(gate_id)
            for evidence in gate.get("evidence", []):
                if not (project_root / evidence).exists():
                    errors.append(f"{capability_id}: missing evidence {evidence}")
    for capability_id, capability in by_id.items():
        for dependency in capability.get("depends_on", []):
            if dependency not in by_id:
                errors.append(f"{capability_id}: unknown dependency {dependency}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, path: list[str]) -> None:
        if node in visiting:
            errors.append("dependency cycle: " + " -> ".join(path + [node]))
            return
        if node in visited or node not in by_id:
            return
        visiting.add(node)
        for dependency in by_id[node].get("depends_on", []):
            visit(dependency, path + [node])
        visiting.remove(node)
        visited.add(node)

    for capability_id in by_id:
        visit(capability_id, [])
    module_schema = registry_path.with_name("module-dependencies.v1.schema.json")
    for module_path in module_paths or []:
        module = json.loads(module_path.read_text(encoding="utf-8"))
        errors.extend(schema_errors(module_schema, module, str(module_path)))
        seen_requirements: set[str] = set()
        for requirement in module.get("requires", []):
            capability_id = requirement.get("capability_id", "")
            if capability_id in seen_requirements:
                errors.append(f"{module_path}: duplicate requirement {capability_id}")
            seen_requirements.add(capability_id)
            capability = by_id.get(capability_id)
            if capability is None:
                errors.append(f"{module_path}: unknown capability {capability_id}")
                continue
            if capability.get("status") not in READY_STATUS:
                errors.append(f"{module_path}: capability {capability_id} is not ready")
            available = int(str(capability.get("version", "v0"))[1:])
            required = int(str(requirement.get("minimum_version", "v0"))[1:])
            if available < required:
                errors.append(f"{module_path}: {capability_id} requires v{required}, only v{available} is available")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--module", action="append", type=Path, default=[])
    args = parser.parse_args()
    errors = validate(args.registry, args.project_root.resolve(), args.module)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Foundation dependency registry is valid and all evidence paths exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
