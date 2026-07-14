import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_governance_reading_list import validate  # noqa: E402


SCHEMA = ROOT / "contracts/foundation/governance-reading-list.v1.schema.json"
READING_LIST = ROOT / "contracts/foundation/governance-reading-list.v1.json"
REGISTRY = ROOT / "contracts/foundation/agent-collaboration.v1.json"


class GovernanceReadingListTests(unittest.TestCase):
    def test_current_reading_list_and_activation_gate_pass(self) -> None:
        self.assertEqual(validate(SCHEMA, READING_LIST, ROOT, REGISTRY), [])

    def _validate_mutation(self, mutate) -> list[str]:
        data = json.loads(READING_LIST.read_text(encoding="utf-8"))
        mutate(data)
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "governance-reading-list.v1.json"
            candidate.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            return validate(SCHEMA, candidate, ROOT, REGISTRY)

    def test_active_nova_without_overlay_fails_closed(self) -> None:
        errors = self._validate_mutation(lambda data: data["module_overlays"].pop("nova"))
        self.assertTrue(any("active module nova has no non-empty governance overlay" in error for error in errors))

    def test_active_protection_mall_without_overlay_fails_closed(self) -> None:
        errors = self._validate_mutation(lambda data: data["module_overlays"].pop("protection-mall"))
        self.assertTrue(
            any("active module protection-mall has no non-empty governance overlay" in error for error in errors)
        )

    def test_empty_overlay_fails_schema_and_activation_gate(self) -> None:
        errors = self._validate_mutation(lambda data: data["module_overlays"].__setitem__("nova", []))
        self.assertTrue(any("should be non-empty" in error for error in errors))
        self.assertTrue(any("active module nova" in error for error in errors))

    def test_missing_overlay_file_fails_closed(self) -> None:
        errors = self._validate_mutation(
            lambda data: data["module_overlays"].__setitem__("nova", ["missing/nova-governance.md"])
        )
        self.assertTrue(any("required governance input is missing" in error for error in errors))

    def test_duplicate_and_unsafe_paths_are_rejected(self) -> None:
        def mutate(data: dict) -> None:
            data["module_overlays"]["nova"] = ["../escape.md", "../escape.md"]

        errors = self._validate_mutation(mutate)
        self.assertTrue(any("non-unique elements" in error for error in errors))
        self.assertTrue(any("unsafe repository-relative" in error for error in errors))

    def test_planned_or_platform_items_do_not_require_module_overlay(self) -> None:
        reading_list = json.loads(READING_LIST.read_text(encoding="utf-8"))
        registry = {
            "work_items": [
                {"work_id": "AIW-PLANNED", "status": "planned", "module_id": "future-module"},
                {"work_id": "AIW-PLATFORM", "status": "active", "module_id": "platform"},
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate_list = root / "reading-list.json"
            candidate_registry = root / "registry.json"
            candidate_list.write_text(json.dumps(reading_list), encoding="utf-8")
            candidate_registry.write_text(json.dumps(registry), encoding="utf-8")
            errors = validate(SCHEMA, candidate_list, ROOT, candidate_registry)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
