#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ACTIVE_MODULE_STATUSES = {"active", "handoff-ready"}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _path_errors(relative: str, project_root: Path) -> list[str]:
    errors: list[str] = []
    posix = PurePosixPath(relative)
    if posix.is_absolute() or "\\" in relative or ".." in posix.parts:
        errors.append(f"unsafe repository-relative governance path: {relative}")
        return errors
    candidate = (project_root / Path(*posix.parts)).resolve()
    try:
        candidate.relative_to(project_root.resolve())
    except ValueError:
        errors.append(f"governance path escapes project root: {relative}")
        return errors
    if not candidate.is_file():
        errors.append(f"required governance input is missing or not a file: {relative}")
    return errors


def validate(
    schema_path: Path,
    reading_list_path: Path,
    project_root: Path,
    registry_path: Path | None = None,
) -> list[str]:
    schema = _load_json(schema_path)
    reading_list = _load_json(reading_list_path)
    Draft202012Validator.check_schema(schema)
    errors: list[str] = []
    for error in sorted(Draft202012Validator(schema).iter_errors(reading_list), key=lambda item: list(item.path)):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{location}: {error.message}")

    all_paths: list[tuple[str, str]] = [("core", value) for value in reading_list.get("core", [])]
    for module_id, overlay in reading_list.get("module_overlays", {}).items():
        all_paths.extend((f"module_overlays/{module_id}", value) for value in overlay)
    for owner, relative in all_paths:
        if isinstance(relative, str):
            errors.extend(f"{owner}: {message}" for message in _path_errors(relative, project_root))

    if registry_path is not None:
        registry = _load_json(registry_path)
        overlays = reading_list.get("module_overlays", {})
        for item in registry.get("work_items", []):
            if item.get("status") not in ACTIVE_MODULE_STATUSES:
                continue
            module_id = item.get("module_id")
            if not module_id or module_id == "platform":
                continue
            overlay = overlays.get(module_id)
            if not isinstance(overlay, list) or not overlay:
                errors.append(
                    f"{item.get('work_id', '<unknown-work-item>')}: "
                    f"{item.get('status')} module {module_id} has no non-empty governance overlay"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("reading_list", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--registry", type=Path)
    args = parser.parse_args()
    errors = validate(
        args.schema,
        args.reading_list,
        args.project_root.resolve(),
        args.registry,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    suffix = " and active/handoff-ready module activation gate" if args.registry else ""
    print(f"Governance reading list satisfies schema, file integrity{suffix}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
