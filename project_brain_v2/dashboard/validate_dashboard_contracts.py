from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts/project-brain/v2/dashboard"
PACKAGE = ROOT / "project_brain_v2/dashboard"
SCHEMAS = (
    "dashboard-policy.v1.schema.json",
    "server-session-claims.v1.schema.json",
    "dashboard-overview.v1.schema.json",
)
FORBIDDEN_IMPORTS = {"aiohttp", "fastapi", "flask", "http.server", "os", "requests", "shutil", "socket", "subprocess", "urllib"}
FORBIDDEN_CALLS = {"mkdir", "open", "remove", "rename", "rmdir", "touch", "unlink", "write_bytes", "write_text"}


def validate() -> None:
    schemas: dict[str, dict] = {}
    for name in SCHEMAS:
        schema = json.loads((CONTRACTS / name).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        schemas[name] = schema
    policy = json.loads((CONTRACTS / "dashboard-policy.disabled.v1.json").read_text(encoding="utf-8"))
    Draft202012Validator(schemas["dashboard-policy.v1.schema.json"]).validate(policy)
    required_false = (
        "enabled", "production_enabled", "network_route_enabled", "real_sources_enabled",
        "export_enabled", "source_writes_enabled", "external_auth_enabled",
    )
    if policy.get("environment") != "production" or any(policy.get(key) is not False for key in required_false):
        raise ValueError("shipped dashboard policy must be production-shaped and fully disabled")
    for path in sorted(PACKAGE.glob("*.py")):
        if path.name == "validate_dashboard_contracts.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = {alias.name for alias in node.names}
            elif isinstance(node, ast.ImportFrom):
                names = {node.module or ""}
            else:
                names = set()
            if any(name in FORBIDDEN_IMPORTS or any(name.startswith(item + ".") for item in FORBIDDEN_IMPORTS) for name in names):
                raise ValueError(f"forbidden network/process/write-capable import in {path.name}: {sorted(names)}")
            if isinstance(node, ast.Call):
                name = node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id if isinstance(node.func, ast.Name) else ""
                if name in FORBIDDEN_CALLS:
                    if path.name == "reader.py" and name == "open" and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == "rb":
                        continue
                    raise ValueError(f"forbidden filesystem mutation call in {path.name}: {name}")
    print("Project Brain v2 M3 dashboard contracts are valid, default-off, offline and read-only.")


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
