#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def validate(schema_path: Path, records_dir: Path, project_root: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    records = sorted(records_dir.glob("*.json"))
    if not records:
        return ["no implementation records found"]
    seen: set[str] = set()
    path_fields = ("governance_inputs", "requirement_sources", "contracts", "decisions", "evidence")
    for record_path in records:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{record_path}:{location}: {error.message}")
        record_id = record.get("record_id", "")
        if record_id in seen:
            errors.append(f"duplicate record_id: {record_id}")
        seen.add(record_id)
        checklist = record.get("governance_checklist", "")
        checklist_path = project_root / checklist
        if not checklist or not checklist_path.exists():
            errors.append(f"{record_id}: missing governance checklist {checklist}")
        else:
            checklist_data = json.loads(checklist_path.read_text(encoding="utf-8"))
            if checklist_data.get("record_id") != record_id:
                errors.append(f"{record_id}: checklist belongs to {checklist_data.get('record_id')}")
            if checklist_data.get("status") != "completed":
                errors.append(f"{record_id}: checklist is not completed")
        exam = record.get("governance_exam")
        requires_exam = "docs/decisions/0017-readme-course-and-random-governance-exam.md" in record.get("decisions", [])
        if requires_exam:
            exam_path = project_root / (exam or "")
            if not exam or not exam_path.exists():
                errors.append(f"{record_id}: missing required governance exam {exam}")
            else:
                exam_data = json.loads(exam_path.read_text(encoding="utf-8"))
                if exam_data.get("record_id") != record_id or exam_data.get("status") != "passed" or exam_data.get("score") != 100:
                    errors.append(f"{record_id}: governance exam must be passed with score 100 for the same record_id")
        for field in path_fields:
            for value in record.get(field, []):
                if not (project_root / value).exists():
                    errors.append(f"{record_id}: missing {field} path {value}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("records", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.schema, args.records, args.project_root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("AI implementation records are schema-valid and all referenced evidence paths exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
