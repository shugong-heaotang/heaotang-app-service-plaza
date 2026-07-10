#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def validate(schema_path: Path, directory: Path, project_root: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    records: set[str] = set()
    reading_list = json.loads((project_root / "contracts/foundation/governance-reading-list.v1.json").read_text(encoding="utf-8"))
    files = sorted(directory.glob("*.json"))
    if not files:
        return ["no completed development checklists found"]
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        for error in validator.iter_errors(data):
            errors.append(f"{path}:{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}")
        record_id = data.get("record_id", "")
        if record_id in records:
            errors.append(f"duplicate checklist record_id: {record_id}")
        records.add(record_id)
        if data.get("status") != "completed" or not data.get("completed_at"):
            errors.append(f"{path}: checklist is not completed")
        if data.get("attestation") != "I read and applied every checked governance input to this implementation.":
            errors.append(f"{path}: exact attestation is required")
        expected = list(reading_list.get("core", []))
        module_id = data.get("module_id")
        if module_id:
            expected.extend(reading_list.get("module_overlays", {}).get(module_id, []))
        expected = list(dict.fromkeys(expected))
        actual = [item.get("path") for item in data.get("items", [])]
        if len(actual) != len(set(actual)):
            errors.append(f"{path}: duplicate governance input path")
        if set(actual) != set(expected):
            missing = sorted(set(expected) - set(actual))
            extra = sorted(set(actual) - set(expected))
            errors.append(f"{path}: checklist does not match reading list; missing={missing}, extra={extra}")
        for item in data.get("items", []):
            source = project_root / item.get("path", "")
            if not item.get("checked") or not item.get("checked_at"):
                errors.append(f"{path}: unchecked governance input {item.get('path')}")
                continue
            if not source.exists():
                errors.append(f"{path}: missing governance input {item.get('path')}")
                continue
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            if digest != item.get("sha256"):
                errors.append(f"{path}: stale acknowledgement for {item.get('path')}; file changed and must be reread")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.schema, args.directory, args.project_root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("AI development flight checklists are complete and match current governance file hashes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
