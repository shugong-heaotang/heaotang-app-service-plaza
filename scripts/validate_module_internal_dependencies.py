#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def resolve_path(project_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else project_root / path


def validate(schema_path: Path, files: list[Path], project_root: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path)):
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}:{location}: {error.message}")
        dependencies = data.get("dependencies", [])
        by_id: dict[str, dict] = {}
        for dependency in dependencies:
            dependency_id = dependency.get("dependency_id", "")
            if dependency_id in by_id:
                errors.append(f"{path}: duplicate dependency_id {dependency_id}")
            by_id[dependency_id] = dependency
            status = dependency.get("status")
            if status in {"standardized", "implemented", "verified"} and not dependency.get("contracts"):
                errors.append(f"{path}:{dependency_id}: standardized dependency requires a contract")
            if status == "verified" and not dependency.get("evidence"):
                errors.append(f"{path}:{dependency_id}: verified dependency requires evidence")
            for field in ("contracts", "evidence"):
                for value in dependency.get(field, []):
                    if not resolve_path(project_root, value).exists():
                        errors.append(f"{path}:{dependency_id}: missing {field} path {value}")
        for dependency_id, dependency in by_id.items():
            for parent in dependency.get("depends_on", []):
                if parent not in by_id:
                    errors.append(f"{path}:{dependency_id}: unknown internal dependency {parent}")
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str, chain: list[str]) -> None:
            if node in visiting:
                errors.append(f"{path}: dependency cycle {' -> '.join(chain + [node])}")
                return
            if node in visited or node not in by_id:
                return
            visiting.add(node)
            for parent in by_id[node].get("depends_on", []):
                visit(parent, chain + [node])
            visiting.remove(node)
            visited.add(node)

        for dependency_id in by_id:
            visit(dependency_id, [])
        required = [item for item in dependencies if item.get("required_for_slice")]
        development_ready = all(item.get("status") in {"standardized", "implemented", "verified"} for item in required)
        acceptance_ready = all(item.get("status") == "verified" for item in required)
        if data.get("development_readiness") == "go" and not development_ready:
            errors.append(f"{path}: development_readiness go requires every required dependency to be standardized")
        if data.get("acceptance_readiness") == "go" and not acceptance_ready:
            errors.append(f"{path}: acceptance_readiness go requires every required dependency to be verified")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.schema, args.files, args.project_root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Module internal dependency graphs are valid: {len(args.files)} modules.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
