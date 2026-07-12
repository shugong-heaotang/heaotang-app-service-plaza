import copy
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
    def test_retry_generator_orders_presentation_before_interactive_confirmation(self):
        script_path = Path(__file__).resolve().parents[1] / "New-AgentGovernanceExam.ps1"
        script = script_path.read_text(encoding="utf-8-sig")
        self.assertNotIn("RemediationConfirmationsCsv", script)
        presented = script.index('Write-Output $sourceText')
        confirmed = script.index('$confirmation = Read-Host')
        recorded = script.index('$confirmedAt = [DateTime]::UtcNow')
        self.assertLess(presented, confirmed)
        self.assertLess(confirmed, recorded)
        self.assertIn('presentation_nonce = $presentationNonce', script)
        self.assertIn('confirmation_method = "interactive-path-nonce-after-full-output"', script)

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

    def test_retry_requires_explicit_failed_attempt_and_current_remediation_rereads(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            foundation = root / "contracts/foundation"
            attempts = foundation / "governance-exams"
            attempts.mkdir(parents=True)
            source = root / "RULE.md"
            source.write_text("rule", encoding="utf-8")
            reading = foundation / "governance-reading-list.v1.json"
            reading.write_text(json.dumps({"core": ["RULE.md"], "module_overlays": {}}), encoding="utf-8")
            questions = [{
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
            } for index in range(1, 13)]
            bank = foundation / "governance-exam-bank.v1.json"
            bank.write_text(json.dumps({
                "contract_version": "governance-exam-bank.v1",
                "question_count_per_attempt": 8,
                "passing_score": 100,
                "questions": questions,
            }), encoding="utf-8")
            checklist = foundation / "checklist.json"
            checklist.write_text(json.dumps({"record_id": "IR-20260712-RETRY", "status": "completed"}), encoding="utf-8")

            def responses(wrong_first: bool) -> list[dict]:
                return [{
                    "question_id": f"GQ-{index:03d}",
                    "selected_option": "B" if wrong_first and index == 1 else "A",
                    "correct": False if wrong_first and index == 1 else True,
                    "source_path": "RULE.md",
                } for index in range(1, 9)]

            common = {
                "contract_version": "governance-exam.v1",
                "record_id": "IR-20260712-RETRY",
                "actor": "test agent",
                "question_count": 8,
                "passing_score": 100,
                "bank_sha256": sha(bank),
                "reading_list_sha256": sha(reading),
                "checklist_path": "contracts/foundation/checklist.json",
                "checklist_sha256": sha(checklist),
            }
            first = {
                **common,
                "attempt_id": "EX-20260712-RETRY-1",
                "attempt_number": 1,
                "status": "failed",
                "generated_at": "2026-07-12T00:00:00Z",
                "completed_at": "2026-07-12T00:01:00Z",
                "score": 87,
                "responses": responses(True),
                "remediation_sources": ["RULE.md"],
            }
            first_path = attempts / "attempt-1.json"
            first_path.write_text(json.dumps(first), encoding="utf-8")
            retry = {
                **common,
                "attempt_id": "EX-20260712-RETRY-2",
                "attempt_number": 2,
                "status": "passed",
                "generated_at": "2026-07-12T00:03:00Z",
                "completed_at": "2026-07-12T00:04:00Z",
                "score": 100,
                "responses": responses(False),
                "remediation_sources": [],
                "previous_attempt_path": "contracts/foundation/governance-exams/attempt-1.json",
                "previous_attempt_sha256": sha(first_path),
                "remediation_rereads": [{
                    "source_path": "RULE.md",
                    "presented_at": "2026-07-12T00:01:30Z",
                    "presentation_sha256": sha(source),
                    "presentation_nonce": "1" * 32,
                    "confirmed_at": "2026-07-12T00:02:00Z",
                    "source_sha256": sha(source),
                    "confirmed_by": "test agent",
                    "confirmation_method": "interactive-path-nonce-after-full-output",
                }],
            }
            retry_path = attempts / "attempt-2.json"
            schema_root = Path(__file__).resolve().parents[2] / "contracts/foundation"

            def errors_for(candidate: dict) -> list[str]:
                retry_path.write_text(json.dumps(candidate), encoding="utf-8")
                return validate(
                    schema_root / "governance-exam.v1.schema.json",
                    schema_root / "governance-exam-bank.v1.schema.json",
                    bank,
                    attempts,
                    root,
                )

            self.assertEqual(errors_for(retry), [])
            mutations: list[tuple[str, dict]] = []
            missing_previous = copy.deepcopy(retry)
            missing_previous.pop("previous_attempt_path")
            mutations.append(("previous_attempt_path", missing_previous))
            wrong_hash = copy.deepcopy(retry)
            wrong_hash["previous_attempt_sha256"] = "0" * 64
            mutations.append(("hash mismatch", wrong_hash))
            escaped = copy.deepcopy(retry)
            escaped["previous_attempt_path"] = "../attempt-1.json"
            mutations.append(("inside the repository", escaped))
            missing_reread = copy.deepcopy(retry)
            missing_reread["remediation_rereads"] = []
            mutations.append(("remediation_rereads", missing_reread))
            duplicate_reread = copy.deepcopy(retry)
            duplicate_reread["remediation_rereads"].append(copy.deepcopy(duplicate_reread["remediation_rereads"][0]))
            mutations.append(("duplicate source_path", duplicate_reread))
            stale_source = copy.deepcopy(retry)
            stale_source["remediation_rereads"][0]["source_sha256"] = "0" * 64
            mutations.append(("source hash mismatch", stale_source))
            stale_presentation = copy.deepcopy(retry)
            stale_presentation["remediation_rereads"][0]["presentation_sha256"] = "0" * 64
            mutations.append(("source hash mismatch", stale_presentation))
            wrong_actor = copy.deepcopy(retry)
            wrong_actor["remediation_rereads"][0]["confirmed_by"] = "another agent"
            mutations.append(("confirmation actor mismatch", wrong_actor))
            missing_confirmation = copy.deepcopy(retry)
            missing_confirmation["remediation_rereads"][0].pop("confirmation_method")
            mutations.append(("confirmation_method", missing_confirmation))
            confirmation_before_presentation = copy.deepcopy(retry)
            confirmation_before_presentation["remediation_rereads"][0]["confirmed_at"] = "2026-07-12T00:01:00Z"
            mutations.append(("occur in order", confirmation_before_presentation))
            too_early = copy.deepcopy(retry)
            too_early["remediation_rereads"][0]["presented_at"] = "2026-07-11T23:59:00Z"
            mutations.append(("occur in order", too_early))
            too_late = copy.deepcopy(retry)
            too_late["remediation_rereads"][0]["confirmed_at"] = "2026-07-12T00:05:00Z"
            mutations.append(("occur in order", too_late))
            nonconsecutive = copy.deepcopy(retry)
            nonconsecutive["attempt_number"] = 3
            nonconsecutive["attempt_id"] = "EX-20260712-RETRY-3"
            mutations.append(("immediately preceding", nonconsecutive))
            for expected, candidate in mutations:
                with self.subTest(expected=expected):
                    self.assertTrue(any(expected in error for error in errors_for(candidate)))


if __name__ == "__main__":
    unittest.main()
