import json
import sys
from pathlib import Path
from urllib.request import urlopen


def load(source: str) -> object:
    if source.startswith(("https://", "http://")):
        with urlopen(source, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    with Path(source).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare_service_plaza_actions.py BASELINE ACTUAL")
    baseline = load(sys.argv[1])
    actual = load(sys.argv[2])
    expected_actions = baseline["actions"]
    actual_actions = actual.get("data", actual).get("items", actual)
    if actual_actions != expected_actions:
        for index, (expected, received) in enumerate(zip(expected_actions, actual_actions)):
            if expected != received:
                print(
                    f"action {index} ({expected.get('action_id')}): expected "
                    f"{json.dumps(expected, ensure_ascii=False, sort_keys=True)}, received "
                    f"{json.dumps(received, ensure_ascii=False, sort_keys=True)}",
                    file=sys.stderr,
                )
                break
        if len(actual_actions) != len(expected_actions):
            print(
                f"action count: expected {len(expected_actions)}, received {len(actual_actions)}",
                file=sys.stderr,
            )
        return 1
    print(f"Service Plaza runtime actions exactly match the {len(expected_actions)}-action baseline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
