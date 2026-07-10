#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

EXACT_SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")


def validate(project_root: Path, backend_root: Path) -> list[str]:
    errors: list[str] = []
    standards = json.loads((project_root / "contracts/foundation/engineering-standards.v1.json").read_text(encoding="utf-8"))
    if standards.get("contract_version") != "engineering-standards.v1":
        errors.append("invalid engineering standards contract version")

    package = json.loads((project_root / "app/package.json").read_text(encoding="utf-8"))
    lock = json.loads((project_root / "app/package-lock.json").read_text(encoding="utf-8"))
    lock_root = lock.get("packages", {}).get("", {})
    for group in ("dependencies", "devDependencies"):
        for name, version in package.get(group, {}).items():
            if not EXACT_SEMVER.fullmatch(version):
                errors.append(f"app/package.json: {name} must use an exact version, got {version!r}")
            if lock_root.get(group, {}).get(name) != version:
                errors.append(f"app/package-lock.json: root {name} version does not match package.json")
            resolved = lock.get("packages", {}).get(f"node_modules/{name}", {}).get("version")
            if resolved != version:
                errors.append(f"app/package-lock.json: resolved {name}={resolved!r}, expected {version!r}")
    for script in ("build", "test", "build:test-server"):
        if script not in package.get("scripts", {}):
            errors.append(f"app/package.json: missing required script {script}")

    tsconfig = json.loads((project_root / "app/tsconfig.app.json").read_text(encoding="utf-8"))
    options = tsconfig.get("compilerOptions", {})
    if options.get("strict") is not True or options.get("allowJs") is not False or options.get("noEmit") is not True:
        errors.append("app/tsconfig.app.json must enforce strict TypeScript, allowJs=false and noEmit=true")

    go_mod = (backend_root / "go.mod").read_text(encoding="utf-8")
    if not re.search(r"(?m)^go [0-9]+\.[0-9]+\.[0-9]+$", go_mod):
        errors.append("backend go.mod must pin a full Go toolchain version")
    for dependency in ("github.com/gofiber/fiber/v2", "modernc.org/sqlite"):
        if dependency not in go_mod:
            errors.append(f"backend go.mod missing approved dependency {dependency}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--backend-root", type=Path, required=True)
    args = parser.parse_args()
    errors = validate(args.project_root.resolve(), args.backend_root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Engineering toolchain is pinned and conforms to the approved per-layer standard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
