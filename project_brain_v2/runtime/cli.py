from __future__ import annotations

import argparse
import json
from pathlib import Path
from .engine import RefreshEngine

def main() -> int:
    parser = argparse.ArgumentParser(description="Project Brain v2 offline M2 refresh")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--state-root", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--fact-id", required=True)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--actor", required=True)
    args = parser.parse_args()
    result = RefreshEngine(args.repo_root, args.state_root, args.policy).run(args.run_id, args.fact_id, args.fixture, args.role, args.actor)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "Trusted" else 2

if __name__ == "__main__": raise SystemExit(main())
