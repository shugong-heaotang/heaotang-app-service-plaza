import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(instance: object, schema: object, label: str) -> list[str]:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda error: list(error.path),
    )
    return [
        f"{label}:{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in errors
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Service Plaza integration package")
    parser.add_argument("--manifest-schema", type=Path, required=True)
    parser.add_argument("--action-schema", type=Path)
    parser.add_argument("--manifest", type=Path, action="append", required=True)
    parser.add_argument("--actions", type=Path)
    parser.add_argument(
        "--complete-catalog",
        action="store_true",
        help="Require every service_id referenced by actions to be present in the supplied manifests",
    )
    args = parser.parse_args()

    manifest_schema = load_json(args.manifest_schema)
    Draft202012Validator.check_schema(manifest_schema)
    manifests = [load_json(path) for path in args.manifest]
    errors: list[str] = []
    for path, manifest in zip(args.manifest, manifests, strict=True):
        errors.extend(validate(manifest, manifest_schema, str(path)))

    service_ids = [manifest.get("service_id") for manifest in manifests if isinstance(manifest, dict)]
    if len(service_ids) != len(set(service_ids)):
        errors.append("manifests: duplicate service_id")
    positions = [
        (manifest.get("category"), manifest.get("sort_order"))
        for manifest in manifests
        if isinstance(manifest, dict)
    ]
    if len(positions) != len(set(positions)):
        errors.append("manifests: duplicate category/sort_order position")

    if args.actions:
        if not args.action_schema:
            errors.append("actions: --action-schema is required when --actions is supplied")
        else:
            action_schema = load_json(args.action_schema)
            Draft202012Validator.check_schema(action_schema)
            actions_document = load_json(args.actions)
            errors.extend(validate(actions_document, action_schema, str(args.actions)))
            if args.complete_catalog and isinstance(actions_document, dict):
                known_ids = set(service_ids)
                unknown_ids = sorted(
                    {
                        item["service_id"]
                        for item in actions_document.get("actions", [])
                        if isinstance(item, dict)
                        and item.get("service_id")
                        and item["service_id"] not in known_ids
                    }
                )
                if unknown_ids:
                    errors.append(
                        "actions: unknown service_id references: " + ", ".join(unknown_ids)
                    )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"Service Plaza integration package passed: {len(manifests)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
