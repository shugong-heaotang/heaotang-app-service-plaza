import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "New-AgentDevelopmentChecklist.ps1"
POWERSHELL = shutil.which("powershell") or "powershell"

LEGACY_CORE_ONLY = {
    "contracts/modules/network/development-checklists/2026-07-12-network-canonical-owner-r1.json",
    "contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m0-r3-correction.json",
    "contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m1-contracts.json",
    "contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m1-domain-evidence.json",
}


def run_checklist(script: Path, output: Path, module_id: str = "") -> subprocess.CompletedProcess[str]:
    command = [
        POWERSHELL,
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        "-RecordId",
        "IR-20260713-CHECKLIST-TEST",
        "-Task",
        "dynamic module registry test",
        "-Actor",
        "governance test",
        "-OutputPath",
        str(output),
    ]
    if module_id:
        command.extend(["-ModuleId", module_id])
    return subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")


class DynamicModuleChecklistTests(unittest.TestCase):
    def test_activity_and_existing_modules_use_registered_overlays(self) -> None:
        reading_list = json.loads(
            (ROOT / "contracts/foundation/governance-reading-list.v1.json").read_text(encoding="utf-8")
        )
        for module_id in ("activity", "life-navigation", "club-alliance", "health-manager"):
            with self.subTest(module_id=module_id), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "checklist.json"
                result = run_checklist(SCRIPT, output, module_id)
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                data = json.loads(output.read_text(encoding="utf-8"))
                expected = list(
                    dict.fromkeys(reading_list["core"] + reading_list["module_overlays"][module_id])
                )
                self.assertEqual(data["module_id"], module_id)
                self.assertEqual([item["path"] for item in data["items"]], expected)
                self.assertEqual(data["status"], "pending")
                self.assertTrue(all(not item["checked"] for item in data["items"]))

    def test_unknown_module_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_checklist(SCRIPT, Path(directory) / "checklist.json", "unknown-module")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unknown module overlay", result.stderr + result.stdout)

    def _temporary_repository(self, overlay: list[str]) -> tuple[tempfile.TemporaryDirectory, Path]:
        context = tempfile.TemporaryDirectory()
        root = Path(context.name)
        (root / "scripts").mkdir(parents=True)
        (root / "contracts/foundation").mkdir(parents=True)
        shutil.copy2(SCRIPT, root / "scripts/New-AgentDevelopmentChecklist.ps1")
        shutil.copy2(ROOT / "scripts/Initialize-PowerShellUtf8.ps1", root / "scripts/Initialize-PowerShellUtf8.ps1")
        (root / "core.md").write_text("core\n", encoding="utf-8")
        reading_list = {
            "contract_version": "governance-reading-list.v1",
            "core": ["core.md"],
            "module_overlays": {"activity": overlay},
        }
        (root / "contracts/foundation/governance-reading-list.v1.json").write_text(
            json.dumps(reading_list, ensure_ascii=False), encoding="utf-8"
        )
        return context, root

    def test_empty_overlay_fails_closed(self) -> None:
        context, root = self._temporary_repository([])
        with context:
            result = run_checklist(root / "scripts/New-AgentDevelopmentChecklist.ps1", root / "out.json", "activity")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must contain at least one", result.stderr + result.stdout)

    def test_missing_overlay_file_fails_closed(self) -> None:
        context, root = self._temporary_repository(["missing.md"])
        with context:
            result = run_checklist(root / "scripts/New-AgentDevelopmentChecklist.ps1", root / "out.json", "activity")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Required governance input is missing", result.stderr + result.stdout)


class SharedModuleChecklistGateTests(unittest.TestCase):
    def test_completed_module_checklists_have_registered_overlay(self) -> None:
        reading_list = json.loads(
            (ROOT / "contracts/foundation/governance-reading-list.v1.json").read_text(encoding="utf-8")
        )
        errors: list[str] = []
        for path in sorted((ROOT / "contracts/modules").glob("*/development-checklists/*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("status") != "completed":
                continue
            relative = path.relative_to(ROOT).as_posix()
            module_id = data.get("module_id")
            if not module_id:
                if relative not in LEGACY_CORE_ONLY:
                    errors.append(f"{relative}: completed module checklist must set module_id")
                continue
            overlay = reading_list.get("module_overlays", {}).get(module_id)
            if not overlay:
                errors.append(f"{relative}: module_id is not dynamically registered: {module_id}")
                continue
            actual = {item.get("path") for item in data.get("items", [])}
            missing = sorted(set(overlay) - actual)
            if missing:
                errors.append(f"{relative}: missing module overlay inputs: {missing}")
        self.assertEqual(errors, [])

    def test_legacy_exception_set_is_exact_and_cannot_grow_silently(self) -> None:
        observed = set()
        for path in sorted((ROOT / "contracts/modules").glob("*/development-checklists/*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("status") == "completed" and not data.get("module_id"):
                observed.add(path.relative_to(ROOT).as_posix())
        self.assertEqual(observed, LEGACY_CORE_ONLY)


if __name__ == "__main__":
    unittest.main()
