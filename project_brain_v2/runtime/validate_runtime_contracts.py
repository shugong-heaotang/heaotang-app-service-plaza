from __future__ import annotations

import ast
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts/project-brain/v2/runtime"
RUNTIME = ROOT / "project_brain_v2/runtime"
OFF_SWITCHES = ("production_enabled", "production_route_enabled", "production_snapshot_source_enabled",
                "scheduled_production_job_enabled", "boss_dashboard_enabled", "export_enabled",
                "notification_enabled", "network_enabled", "real_sources_enabled", "source_writes_enabled",
                "external_notifications_enabled")
FORBIDDEN_IMPORTS = {"socket", "requests", "urllib", "http", "ftplib", "smtplib", "paramiko"}


def validate() -> None:
    schema = json.loads((CONTRACTS / "runtime-policy.v1.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    policy = json.loads((CONTRACTS / "runtime-policy.disabled.v1.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(policy)
    if policy["enabled"] is not False or any(policy[name] is not False for name in OFF_SWITCHES):
        raise ValueError("shipped runtime policy must be disabled with every production capability off")
    for name in ("run-record.v1.schema.json", "snapshot.v1.schema.json", "alert.v1.schema.json",
                 "schedule-decision.v1.schema.json", "audit-event.v1.schema.json"):
        Draft202012Validator.check_schema(json.loads((CONTRACTS / name).read_text(encoding="utf-8")))
    for path in RUNTIME.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import): imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module: imports.add(node.module.split(".")[0])
        forbidden = imports & FORBIDDEN_IMPORTS
        if forbidden: raise ValueError(f"network-capable import forbidden in M2: {path}: {sorted(forbidden)}")


if __name__ == "__main__":
    validate()
    print("Project Brain v2 M2 runtime contracts passed: default_disabled=true production_capabilities=false network_imports=0 schemas=6")
