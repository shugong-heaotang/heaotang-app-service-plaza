import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_foundation_dependencies import validate


class FoundationDependencyValidationTest(unittest.TestCase):
    def write_registry(self, root: Path, capabilities: list[dict]) -> Path:
        schema_root = Path(__file__).parents[2] / "contracts" / "foundation"
        for name in ("foundation-capabilities.v1.schema.json", "module-dependencies.v1.schema.json"):
            (root / name).write_text((schema_root / name).read_text(encoding="utf-8"), encoding="utf-8")
        path = root / "registry.json"
        path.write_text(json.dumps({"contract_version": "foundation-capabilities.v1", "capabilities": capabilities}), encoding="utf-8")
        return path

    def capability(self, capability_id: str, depends_on=None, evidence=None):
        return {
            "capability_id": capability_id,
            "version": "v1",
            "name": capability_id,
            "layer": "L1",
            "status": "verified",
            "owner_role": "test-owner",
            "depends_on": depends_on or [],
            "provides": ["test capability"],
            "gates": [{"gate_id": "FG-" + capability_id.upper().replace(".", "-"), "description": "test gate", "evidence": evidence or ["proof.txt"]}],
            "compatibility_policy": "backward-compatible",
            "last_verified_at": "2026-07-10",
        }

    def test_accepts_acyclic_graph_with_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "proof.txt").write_text("ok", encoding="utf-8")
            path = self.write_registry(root, [self.capability("foundation.base"), self.capability("foundation.api", ["foundation.base"])])
            self.assertEqual(validate(path, root), [])

    def test_rejects_missing_dependency_cycle_and_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            capabilities = [
                self.capability("foundation.a", ["foundation.b"], ["missing.txt"]),
                self.capability("foundation.b", ["foundation.a"]),
                self.capability("foundation.c", ["foundation.unknown"]),
            ]
            errors = validate(self.write_registry(root, capabilities), root)
            self.assertTrue(any("missing evidence" in error for error in errors))
            self.assertTrue(any("dependency cycle" in error for error in errors))
            self.assertTrue(any("unknown dependency" in error for error in errors))

    def test_module_requires_existing_ready_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "proof.txt").write_text("ok", encoding="utf-8")
            registry = self.write_registry(root, [self.capability("foundation.base")])
            module = root / "module.json"
            module.write_text(json.dumps({
                "contract_version": "module-dependencies.v1",
                "module_id": "life-navigation",
                "module_version": "v1",
                "requires": [{"capability_id": "foundation.base", "minimum_version": "v2"}],
            }), encoding="utf-8")
            errors = validate(registry, root, [module])
            self.assertTrue(any("only v1 is available" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
