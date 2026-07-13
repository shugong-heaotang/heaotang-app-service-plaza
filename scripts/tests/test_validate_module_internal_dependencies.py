import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_module_internal_dependencies import validate


ROOT = Path(__file__).resolve().parents[2]
V1_SCHEMA = ROOT / "contracts/foundation/module-internal-dependencies.v1.schema.json"


class ModuleInternalDependenciesVersioningTests(unittest.TestCase):
    def test_v1_and_v2_are_validated_together(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            v1 = ROOT / "contracts/modules/life-navigation/internal-dependencies.v1.json"
            contract = root / "contract.json"
            evidence = root / "evidence.md"
            contract.write_text("{}", encoding="utf-8")
            evidence.write_text("ok", encoding="utf-8")
            v2 = root / "v2.json"
            v2.write_text(json.dumps({
                "contract_version": "module-internal-dependencies.v2",
                "module_id": "club-alliance", "module_version": "v1", "slice_id": "ca-f0-h0",
                "readiness": {"governance": "go", "development": "partial-go", "acceptance": "pending", "release": "pending", "operations": "pending"},
                "dependencies": [{
                    "dependency_id": "decision.sc-general", "kind": "decision", "description": "local pending decision",
                    "status": "blocked-local", "required_for_slice": False, "depends_on": [],
                    "contracts": [str(contract)], "evidence": [str(evidence)], "unresolved": ["D-CA-003"],
                    "owner": "项目负责人", "blocks": ["sc.selector"], "does_not_block": ["h0.base"]
                }]
            }, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(validate(V1_SCHEMA, [v1, v2], ROOT), [])

    def test_v2_rejects_missing_owner_and_unknown_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"contract_version":"module-internal-dependencies.v3"}', encoding="utf-8")
            errors = validate(V1_SCHEMA, [path], ROOT)
            self.assertTrue(any("unsupported contract_version" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
