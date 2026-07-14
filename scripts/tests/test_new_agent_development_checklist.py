import fnmatch
import hashlib
import json
import re
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

LEGACY_CORE_ONLY_SHA256 = {
    "contracts/modules/network/development-checklists/2026-07-12-network-canonical-owner-r1.json": "dacb7ffd020dc501f4bf9fbc233030f0ab3885a9c1a7ce8547a02eeed21b2293",
    "contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m0-r3-correction.json": "4aa3de76d86099dbc55474c61d35e4bc133b2babd5641bb81f40b52121d5318a",
    "contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m1-contracts.json": "693dda7450d6d8dc7f10b7c9ed7a38952424671dad80c9d6b0b2767bf13addac",
    "contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m1-domain-evidence.json": "b8a7e9ece9b9333144229aef4d0df77a6cdc48dadd23eb13f48f085ecf86276a",
}

FOUNDATION_GATE_BASE = "fb29b857a5476a62cc882bf6bf407e67febcacf9"


def platform_scope_errors(root: Path, relative: str, data: dict, registry: dict) -> list[str]:
    errors: list[str] = []
    if data.get("module_id") is not None:
        return [f"{relative}: foundation checklist must be platform scoped and use module_id=null"]
    record_id = str(data.get("record_id", ""))
    candidate_record_ids = [record_id]
    stripped = re.sub(r"-R[0-9]+$", "", record_id)
    if stripped != record_id:
        candidate_record_ids.append(stripped)
    expected_work_ids = {candidate.replace("IR-", "AIW-", 1) for candidate in candidate_record_ids}
    item = next(
        (entry for entry in registry.get("work_items", []) if entry.get("work_id") in expected_work_ids),
        None,
    )
    if item is None:
        return [f"{relative}: no registry work item proves platform scope for {data.get('record_id')}"]
    if item.get("owner_role") != "平台集成负责人":
        errors.append(f"{relative}: registry owner_role is not the platform integration owner")
    allowed = [str(pattern) for pattern in item.get("allowed_paths", [])]
    if not any(fnmatch.fnmatchcase(relative, pattern) for pattern in allowed):
        errors.append(f"{relative}: registry allowed_paths do not authorize this checklist")
    task_orders = [
        root / pattern
        for pattern in allowed
        if "task-order" in pattern and "*" not in pattern and "?" not in pattern
    ]
    explicit = False
    for task_order in task_orders:
        if not task_order.is_file():
            continue
        text = task_order.read_text(encoding="utf-8")
        has_legacy_marker = "platform scope" in text and "module_id=null" in text
        has_platform_scope_marker = (
            "platform scope" in text
            or "registry-only" in text
            or "平台注册表" in text
        )
        has_structured_platform_identity = (
            item.get("module_id") == "platform"
            and str(item.get("work_id", "")) in text
            and has_platform_scope_marker
        )
        if text.startswith("# 平台") and (has_legacy_marker or has_structured_platform_identity):
            explicit = True
            break
    if not explicit:
        errors.append(f"{relative}: task order does not explicitly declare platform scope with module_id=null")
    return errors


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
    def test_all_registered_modules_use_overlays_with_current_sha(self) -> None:
        reading_list = json.loads(
            (ROOT / "contracts/foundation/governance-reading-list.v1.json").read_text(encoding="utf-8")
        )
        for module_id in (
            "activity",
            "nova",
            "protection-mall",
            "life-navigation",
            "club-alliance",
            "health-manager",
        ):
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
                for item in data["items"]:
                    expected_sha = hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest()
                    self.assertEqual(item["sha256"], expected_sha, item["path"])
                self.assertEqual(data["status"], "pending")
                self.assertTrue(all(not item["checked"] for item in data["items"]))

    def test_unknown_module_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_checklist(SCRIPT, Path(directory) / "checklist.json", "unknown-module")
            self.assertNotEqual(result.returncode, 0)
            self.assertRegex(result.stderr + result.stdout, r"(?i)unknown module overlay.*unknown-module")

    def _temporary_repository(self, overlay: list[str]) -> tuple[tempfile.TemporaryDirectory, Path]:
        context = tempfile.TemporaryDirectory()
        root = Path(context.name)
        (root / "scripts").mkdir(parents=True)
        (root / "contracts/foundation").mkdir(parents=True)
        shutil.copy2(SCRIPT, root / "scripts/New-AgentDevelopmentChecklist.ps1")
        shutil.copy2(ROOT / "scripts/Initialize-PowerShellUtf8.ps1", root / "scripts/Initialize-PowerShellUtf8.ps1")
        shutil.copy2(
            ROOT / "scripts/validate_governance_reading_list.py",
            root / "scripts/validate_governance_reading_list.py",
        )
        shutil.copy2(
            ROOT / "contracts/foundation/governance-reading-list.v1.schema.json",
            root / "contracts/foundation/governance-reading-list.v1.schema.json",
        )
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
            self.assertRegex(result.stderr + result.stdout, r"(?i)module_overlays/activity.*non-empty")

    def test_missing_overlay_file_fails_closed(self) -> None:
        context, root = self._temporary_repository(["missing.md"])
        with context:
            result = run_checklist(root / "scripts/New-AgentDevelopmentChecklist.ps1", root / "out.json", "activity")
            self.assertNotEqual(result.returncode, 0)
            self.assertRegex(result.stderr + result.stdout, r"(?i)module_overlays/activity.*missing")


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

    def test_legacy_exception_bytes_and_core_only_shape_are_immutable(self) -> None:
        reading_list = json.loads(
            (ROOT / "contracts/foundation/governance-reading-list.v1.json").read_text(encoding="utf-8")
        )
        core = reading_list["core"]
        errors = []
        for relative, expected_hash in LEGACY_CORE_ONLY_SHA256.items():
            path = ROOT / relative
            data = json.loads(path.read_text(encoding="utf-8"))
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            actual_paths = [item.get("path") for item in data.get("items", [])]
            if actual_hash != expected_hash:
                errors.append(f"{relative}: immutable SHA-256 changed")
            if data.get("status") != "completed" or data.get("module_id") is not None:
                errors.append(f"{relative}: legacy completed/null identity changed")
            if len(actual_paths) != 26 or actual_paths != core:
                errors.append(f"{relative}: legacy checklist is no longer the exact 26-item core snapshot")
        self.assertEqual(errors, [])

    def test_new_foundation_checklists_require_explicit_platform_scope(self) -> None:
        registry = json.loads(
            (ROOT / "contracts/foundation/agent-collaboration.v1.json").read_text(encoding="utf-8")
        )
        command = [
            "git",
            "-C",
            str(ROOT),
            "diff",
            "--name-only",
            FOUNDATION_GATE_BASE,
            "--",
            "contracts/foundation/development-checklists/*.json",
        ]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(result.returncode, 0, result.stderr)
        errors = []
        for relative in sorted(line for line in result.stdout.splitlines() if line):
            path = ROOT / relative
            if not path.is_file():
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("status") == "completed":
                errors.extend(platform_scope_errors(ROOT, relative, data, registry))
        self.assertEqual(errors, [])

    def test_post_cutoff_module_null_checklist_cannot_hide_in_foundation(self) -> None:
        fake = {
            "record_id": "IR-20260713-ACTIVITY-V3-M0",
            "module_id": None,
            "status": "completed",
        }
        registry = json.loads(
            (ROOT / "contracts/foundation/agent-collaboration.v1.json").read_text(encoding="utf-8")
        )
        errors = platform_scope_errors(
            ROOT,
            "contracts/foundation/development-checklists/2026-07-13-activity-v3-m0.json",
            fake,
            registry,
        )
        self.assertTrue(errors)
        self.assertTrue(any("platform" in error or "authorize" in error for error in errors))

    def test_platform_title_without_structured_platform_identity_fails(self) -> None:
        fake = {
            "record_id": "IR-20260713-ACTIVITY-V3-M0",
            "module_id": None,
            "status": "completed",
        }
        registry = json.loads(
            (ROOT / "contracts/foundation/agent-collaboration.v1.json").read_text(encoding="utf-8")
        )
        item = next(entry for entry in registry["work_items"] if entry["work_id"] == "AIW-20260713-ACTIVITY-V3-M0")
        self.assertNotEqual(item.get("module_id"), "platform")
        errors = platform_scope_errors(
            ROOT,
            "contracts/foundation/development-checklists/2026-07-13-activity-v3-m0.json",
            fake,
            registry,
        )
        self.assertTrue(any("platform scope" in error for error in errors))

    def _synthetic_platform_scope_errors(
        self,
        *,
        owner_role: str = "平台集成负责人",
        module_id: str = "platform",
        allowed_pattern: str = "contracts/foundation/development-checklists/*.json",
        task_work_id: str = "AIW-20260714-PLATFORM-SYNTHETIC",
        task_scope: str = "registry-only 平台注册表治理",
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_order = root / "docs/task-order.md"
            task_order.parent.mkdir(parents=True)
            task_order.write_text(
                f"# 平台合成治理任务\n\n{task_work_id}\n\n{task_scope}\n",
                encoding="utf-8",
            )
            registry = {
                "work_items": [
                    {
                        "work_id": "AIW-20260714-PLATFORM-SYNTHETIC",
                        "owner_role": owner_role,
                        "module_id": module_id,
                        "allowed_paths": [allowed_pattern, "docs/task-order.md"],
                    }
                ]
            }
            return platform_scope_errors(
                root,
                "contracts/foundation/development-checklists/synthetic.json",
                {"record_id": "IR-20260714-PLATFORM-SYNTHETIC", "module_id": None, "status": "completed"},
                registry,
            )

    def test_r7_style_structured_platform_identity_passes(self) -> None:
        self.assertEqual(self._synthetic_platform_scope_errors(), [])

    def test_non_platform_owner_with_null_checklist_fails(self) -> None:
        errors = self._synthetic_platform_scope_errors(owner_role="模块负责人")
        self.assertTrue(any("platform integration owner" in error for error in errors))

    def test_task_order_missing_or_mismatched_work_id_fails(self) -> None:
        errors = self._synthetic_platform_scope_errors(task_work_id="AIW-WRONG")
        self.assertTrue(any("task order" in error for error in errors))

    def test_checklist_outside_allowed_paths_fails(self) -> None:
        errors = self._synthetic_platform_scope_errors(allowed_pattern="contracts/foundation/other/*.json")
        self.assertTrue(any("allowed_paths" in error for error in errors))

    def test_module_semantics_cannot_masquerade_as_platform(self) -> None:
        errors = self._synthetic_platform_scope_errors(module_id="nova")
        self.assertTrue(any("task order" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
