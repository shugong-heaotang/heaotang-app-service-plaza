import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from validate_governance_exams import validate


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class GovernanceExamValidationTests(unittest.TestCase):
    def test_passed_attempt_is_bound_to_current_bank_reading_list_and_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            foundation = root / "contracts/foundation"
            attempts = foundation / "governance-exams"
            attempts.mkdir(parents=True)
            source = root / "RULE.md"
            source.write_text("rule", encoding="utf-8")
            reading = foundation / "governance-reading-list.v1.json"
            reading.write_text(json.dumps({"core": ["RULE.md"], "module_overlays": {}}), encoding="utf-8")
            questions = []
            for index in range(1, 13):
                questions.append({
                    "question_id": f"GQ-{index:03d}",
                    "scenario": "This is a sufficiently long governance scenario.",
                    "options": [
                        {"option_id": "A", "text": "correct"},
                        {"option_id": "B", "text": "wrong"},
                        {"option_id": "C", "text": "wrong"},
                    ],
                    "correct_option": "A",
                    "source_path": "RULE.md",
                    "explanation": "Apply the rule.",
                })
            bank = foundation / "governance-exam-bank.v1.json"
            bank.write_text(json.dumps({
                "contract_version": "governance-exam-bank.v1",
                "question_count_per_attempt": 8,
                "passing_score": 100,
                "questions": questions,
            }), encoding="utf-8")
            checklist = foundation / "checklist.json"
            checklist.write_text(json.dumps({"record_id": "IR-20260710-TEST", "status": "completed"}), encoding="utf-8")
            responses = [{
                "question_id": f"GQ-{index:03d}",
                "selected_option": "A",
                "correct": True,
                "source_path": "RULE.md",
            } for index in range(1, 9)]
            attempt = {
                "contract_version": "governance-exam.v1",
                "attempt_id": "EX-20260710-TEST-1",
                "record_id": "IR-20260710-TEST",
                "actor": "test agent",
                "attempt_number": 1,
                "status": "passed",
                "generated_at": "2026-07-10T00:00:00Z",
                "completed_at": "2026-07-10T00:01:00Z",
                "question_count": 8,
                "passing_score": 100,
                "score": 100,
                "bank_sha256": sha(bank),
                "reading_list_sha256": sha(reading),
                "checklist_path": "contracts/foundation/checklist.json",
                "checklist_sha256": sha(checklist),
                "responses": responses,
                "remediation_sources": [],
            }
            (attempts / "attempt.json").write_text(json.dumps(attempt), encoding="utf-8")
            base = Path(__file__).resolve().parents[2] / "contracts/foundation"
            errors = validate(base / "governance-exam.v1.schema.json", base / "governance-exam-bank.v1.schema.json", bank, attempts, root)
            self.assertEqual(errors, [])
            checklist.write_text(json.dumps({"record_id": "IR-20260710-TEST", "status": "completed", "changed": True}), encoding="utf-8")
            errors = validate(base / "governance-exam.v1.schema.json", base / "governance-exam-bank.v1.schema.json", bank, attempts, root)
            self.assertTrue(any("checklist changed" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
