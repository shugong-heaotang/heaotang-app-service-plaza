import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from validate_implementation_records import record_directories, validate


class ImplementationRecordValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = Path(__file__).resolve().parents[2] / "contracts/foundation/implementation-record.v1.schema.json"

    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def fixture(self, root: Path) -> tuple[Path, Path, dict]:
        record_id = "IR-20260713-CROSS-RECORD-TEST"
        checklist = root / "contracts/modules/test/development-checklists/current.json"
        exam = root / "contracts/modules/test/governance-exams/attempt-1.json"
        records = root / "contracts/modules/test/implementation-records"
        self.write_json(checklist, {"record_id": record_id, "status": "completed"})
        self.write_json(exam, {"record_id": record_id, "status": "passed", "score": 100})
        for relative in ("RULE.md", "REQ.md", "CONTRACT.json", "ADR.md", "EVIDENCE.md"):
            (root / relative).write_text(relative, encoding="utf-8")
        record = {
            "contract_version": "implementation-record.v1",
            "record_id": record_id,
            "title": "cross-record test",
            "date": "2026-07-13",
            "status": "verified",
            "objective": "fail closed when exam evidence contradicts the record",
            "governance_checklist": checklist.relative_to(root).as_posix(),
            "governance_exam": exam.relative_to(root).as_posix(),
            "governance_inputs": ["RULE.md", "ADR.md", "REQ.md"],
            "requirement_sources": ["REQ.md"],
            "capabilities": ["foundation.governance-certification"],
            "contracts": ["CONTRACT.json"],
            "decisions": ["docs/decisions/0017-readme-course-and-random-governance-exam.md"],
            "changed_areas": ["scripts/validate_implementation_records.py"],
            "verification": ["unit test"],
            "evidence": ["EVIDENCE.md"],
            "premises": ["offline synthetic fixture"],
            "implementation_mode": "ai-assisted",
        }
        decision = root / record["decisions"][0]
        decision.parent.mkdir(parents=True, exist_ok=True)
        decision.write_text("decision", encoding="utf-8")
        self.write_json(records / "record.json", record)
        return records, exam, record

    def errors(self, root: Path, records: Path) -> list[str]:
        foundation_records = root / "contracts/foundation/implementation-records"
        foundation_records.mkdir(parents=True, exist_ok=True)
        return validate(self.schema, foundation_records, root, include_module_records=True)

    def test_same_record_passed_100_is_accepted_from_module_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records, _, _ = self.fixture(root)
            self.assertIn(records, record_directories(root / "contracts/foundation/implementation-records", root, True))
            self.assertEqual(self.errors(root, records), [])

    def test_failed_75_exam_cannot_support_verified_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records, exam, _ = self.fixture(root)
            self.write_json(exam, {"record_id": "IR-20260713-CROSS-RECORD-TEST", "status": "failed", "score": 75})
            errors = self.errors(root, records)
            self.assertTrue(any("status=failed" in error and "score=75" in error for error in errors))

    def test_exam_record_id_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records, exam, _ = self.fixture(root)
            self.write_json(exam, {"record_id": "IR-20260713-OTHER-RECORD", "status": "passed", "score": 100})
            errors = self.errors(root, records)
            self.assertTrue(any("actual record_id=IR-20260713-OTHER-RECORD" in error for error in errors))

    def test_missing_exam_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records, exam, record = self.fixture(root)
            exam.unlink()
            record["governance_exam"] = None
            record["decisions"] = []
            self.write_json(records / "record.json", record)
            self.assertTrue(any("missing required governance exam" in error for error in self.errors(root, records)))


if __name__ == "__main__":
    unittest.main()
