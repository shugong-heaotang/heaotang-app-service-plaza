import json
import sqlite3
import sys
from pathlib import Path


def require_one(root: Path, pattern: str) -> Path:
    matches = list(root.glob(pattern))
    if len(matches) != 1:
        raise RuntimeError(f"expected one {pattern}, found {len(matches)}")
    return matches[0]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_test_server_backup.py EXTRACTED_ROOT")
    root = Path(sys.argv[1])
    database = require_one(root, "*/acceptance/runtime/data/heao.db")
    binary = require_one(root, "*/acceptance/server")
    start_script = require_one(root, "*/acceptance/start-acceptance.sh")
    actions_path = require_one(
        root,
        "*/acceptance/service-plaza/contracts/service-plaza/service-plaza-actions.v1.json",
    )

    if binary.stat().st_size <= 0 or start_script.stat().st_size <= 0:
        raise RuntimeError("backup contains an empty server binary or startup script")
    with sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity check failed: {integrity}")
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
    required_tables = {
        "users",
        "life_navigation_records",
        "club_join_applications",
        "consultations",
        "api_idempotency_keys",
    }
    missing = sorted(required_tables - tables)
    if missing:
        raise RuntimeError("backup database is missing tables: " + ", ".join(missing))

    with actions_path.open("r", encoding="utf-8") as handle:
        actions = json.load(handle)
    if actions.get("contract_version") != "service-plaza.action.v1" or len(actions.get("actions", [])) != 20:
        raise RuntimeError("backup action baseline is missing or invalid")

    print(
        json.dumps(
            {
                "sqlite_integrity": integrity,
                "required_tables": len(required_tables),
                "action_count": 20,
                "binary_bytes": binary.stat().st_size,
                "startup_script_bytes": start_script.stat().st_size,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
