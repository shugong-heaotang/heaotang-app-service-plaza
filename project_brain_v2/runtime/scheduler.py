from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from .engine import RefreshEngine


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError("scheduler timestamps must be UTC")
    return parsed


class OfflineScheduler:
    """A deterministic scheduler tick; an external production timer is not included."""

    def __init__(self, engine: RefreshEngine) -> None:
        self.engine = engine

    def _last_completed(self) -> datetime | None:
        records = self.engine.verify_run_history()
        completed: list[datetime] = []
        for record in records:
            if record.get("completed_at"):
                completed.append(parse_utc(record["completed_at"]))
        return max(completed) if completed else None

    def decision(self, now: datetime) -> dict[str, Any]:
        if now.tzinfo is None or now.utcoffset() != timedelta(0):
            raise ValueError("scheduler clock must be UTC")
        policy, _ = self.engine._policy()
        last = self._last_completed()
        due_at = last + timedelta(seconds=policy["schedule_interval_seconds"]) if last else now
        return {"contract_version": "project-brain-schedule-decision.v1", "evaluated_at": now.isoformat().replace("+00:00", "Z"),
                "last_completed_at": last.isoformat().replace("+00:00", "Z") if last else None,
                "due_at": due_at.isoformat().replace("+00:00", "Z"), "due": now >= due_at,
                "production_timer_present": False}

    def tick(self, now: datetime, run_id: str, fact_id: str, fixture_path: str, role: str,
             actor: str = "project_brain_v2_scheduler") -> dict[str, Any]:
        decision = self.decision(now)
        if not decision["due"]:
            return {"schedule": decision, "run": None}
        return {"schedule": decision, "run": self.engine.run(run_id, fact_id, fixture_path, role, actor)}
