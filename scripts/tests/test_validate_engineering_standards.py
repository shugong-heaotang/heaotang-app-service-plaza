import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_engineering_standards import validate


class EngineeringStandardsValidationTest(unittest.TestCase):
    def make_project(self, root: Path, version: str = "1.2.3") -> tuple[Path, Path]:
        (root / "contracts/foundation").mkdir(parents=True)
        (root / "app").mkdir()
        backend = root / "backend"
        backend.mkdir()
        (root / "contracts/foundation/engineering-standards.v1.json").write_text(json.dumps({"contract_version": "engineering-standards.v1"}), encoding="utf-8")
        package = {"scripts": {"build": "x", "test": "x", "build:test-server": "x"}, "dependencies": {"react": version}, "devDependencies": {}}
        (root / "app/package.json").write_text(json.dumps(package), encoding="utf-8")
        lock = {"packages": {"": {"dependencies": {"react": version}}, "node_modules/react": {"version": version}}}
        (root / "app/package-lock.json").write_text(json.dumps(lock), encoding="utf-8")
        (root / "app/tsconfig.app.json").write_text(json.dumps({"compilerOptions": {"strict": True, "allowJs": False, "noEmit": True}}), encoding="utf-8")
        (backend / "go.mod").write_text("module test\n\ngo 1.25.11\n\nrequire (\n github.com/gofiber/fiber/v2 v2.52.13\n modernc.org/sqlite v1.53.0\n)\n", encoding="utf-8")
        return root, backend

    def test_accepts_pinned_toolchain(self):
        with tempfile.TemporaryDirectory() as directory:
            project, backend = self.make_project(Path(directory))
            self.assertEqual(validate(project, backend), [])

    def test_rejects_latest_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            project, backend = self.make_project(Path(directory), "latest")
            self.assertTrue(any("exact version" in error for error in validate(project, backend)))


if __name__ == "__main__":
    unittest.main()
