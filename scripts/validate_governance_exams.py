#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(schema_path: Path, bank_schema_path: Path, bank_path: Path, attempts_dir: Path, project_root: Path) -> list[str]:
    attempt_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    bank_schema = json.loads(bank_schema_path.read_text(encoding="utf-8"))
    bank = json.loads(bank_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(attempt_schema)
    Draft202012Validator.check_schema(bank_schema)
    errors = [f"bank:{error.message}" for error in Draft202012Validator(bank_schema).iter_errors(bank)]
    questions: dict[str, dict] = {}
    for question in bank.get("questions", []):
        question_id = question.get("question_id", "")
        if question_id in questions:
            errors.append(f"duplicate question_id: {question_id}")
        questions[question_id] = question
        option_ids = [option.get("option_id") for option in question.get("options", [])]
        if set(option_ids) != {"A", "B", "C"} or len(option_ids) != 3:
            errors.append(f"{question_id}: options must be exactly A, B and C")
        if not (project_root / question.get("source_path", "")).exists():
            errors.append(f"{question_id}: missing source_path {question.get('source_path')}")
    files = sorted(attempts_dir.glob("*.json"))
    if not files:
        return errors + ["no governance exam attempts found"]
    validator = Draft202012Validator(attempt_schema)
    seen_ids: set[str] = set()
    attempts_by_record: dict[str, dict[int, dict]] = defaultdict(dict)
    current_bank_hash = digest(bank_path)
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        for error in validator.iter_errors(data):
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}:{location}: {error.message}")
        attempt_id = data.get("attempt_id", "")
        if attempt_id in seen_ids:
            errors.append(f"duplicate attempt_id: {attempt_id}")
        seen_ids.add(attempt_id)
        record_id = data.get("record_id", "")
        number = data.get("attempt_number", 0)
        if number in attempts_by_record[record_id]:
            errors.append(f"{record_id}: duplicate attempt_number {number}")
        attempts_by_record[record_id][number] = data
        if data.get("status") == "pending":
            errors.append(f"{path}: pending exam cannot pass the repository gate")
        if data.get("bank_sha256") != current_bank_hash:
            errors.append(f"{path}: exam bank changed; a new exam is required")
        checklist_path = project_root / data.get("checklist_path", "")
        if not checklist_path.exists():
            errors.append(f"{path}: missing checklist {data.get('checklist_path')}")
        else:
            checklist = json.loads(checklist_path.read_text(encoding="utf-8"))
            if digest(checklist_path) != data.get("checklist_sha256"):
                errors.append(f"{path}: checklist changed; a new exam is required")
            if checklist.get("record_id") != record_id or checklist.get("status") != "completed":
                errors.append(f"{path}: checklist must be completed for the same record_id")
        responses = data.get("responses", [])
        response_ids = [response.get("question_id") for response in responses]
        if len(response_ids) != len(set(response_ids)):
            errors.append(f"{path}: duplicate question in attempt")
        correct_count = 0
        wrong_sources: list[str] = []
        for response in responses:
            question = questions.get(response.get("question_id"))
            if not question:
                errors.append(f"{path}: unknown question {response.get('question_id')}")
                continue
            expected = response.get("selected_option") == question.get("correct_option")
            if response.get("correct") is not expected:
                errors.append(f"{path}: incorrect grading for {response.get('question_id')}")
            if response.get("source_path") != question.get("source_path"):
                errors.append(f"{path}: source mismatch for {response.get('question_id')}")
            if expected:
                correct_count += 1
            else:
                wrong_sources.append(question["source_path"])
        expected_score = (correct_count * 100) // int(data.get("question_count", 8))
        if data.get("score") != expected_score:
            errors.append(f"{path}: score must be {expected_score}")
        expected_status = "passed" if expected_score >= bank.get("passing_score", 100) else "failed"
        if data.get("status") != expected_status:
            errors.append(f"{path}: status must be {expected_status}")
        if set(data.get("remediation_sources", [])) != set(wrong_sources):
            errors.append(f"{path}: remediation_sources must match failed questions")
    for record_id, attempts in attempts_by_record.items():
        for number, attempt in attempts.items():
            if number > 1:
                previous = attempts.get(number - 1)
                if not previous or previous.get("status") != "failed":
                    errors.append(f"{record_id}: attempt {number} must follow attempt {number - 1} with failed status")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("bank_schema", type=Path)
    parser.add_argument("bank", type=Path)
    parser.add_argument("attempts", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.schema, args.bank_schema, args.bank, args.attempts, args.project_root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Governance exam snapshots are correctly graded and linked to immutable completed flight checklists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
