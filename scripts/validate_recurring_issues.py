#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def validate(schema_path: Path, registry_path: Path, project_root: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = []
    for error in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda item: list(item.path)):
        errors.append(f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}")
    seen: set[str] = set()
    for issue in data.get("issues", []):
        pattern_id = issue.get("pattern_id", "")
        if pattern_id in seen:
            errors.append(f"duplicate pattern_id: {pattern_id}")
        seen.add(pattern_id)
        if issue.get("occurrence_count") != len(issue.get("occurrences", [])):
            errors.append(f"{pattern_id}: occurrence_count does not match occurrences")
        for occurrence in issue.get("occurrences", []):
            if not (project_root / occurrence.get("evidence", "")).exists():
                errors.append(f"{pattern_id}: missing occurrence evidence {occurrence.get('evidence')}")
        for field in ("prevention_gates", "regression_evidence"):
            for value in issue.get(field, []):
                if not (project_root / value).exists():
                    errors.append(f"{pattern_id}: missing {field} path {value}")
        if issue.get("status") == "verified" and not issue.get("regression_evidence"):
            errors.append(f"{pattern_id}: verified issue requires regression evidence")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.schema, args.registry, args.project_root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Recurring issue registry satisfies the mandatory two-strike root-cause rule.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
