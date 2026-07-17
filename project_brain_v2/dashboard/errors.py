from __future__ import annotations


class DashboardFailure(Exception):
    """Stable, fail-closed M3 failure without sensitive implementation detail."""

    def __init__(self, code: str, message: str = "", http_status: int = 503) -> None:
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.http_status = http_status
