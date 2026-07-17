from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Mapping

from .auth import ServerSessionVerifier
from .errors import DashboardFailure
from .policy import DashboardPolicy
from .reader import DashboardReader, canonical
from .render import render_dashboard

DASHBOARD_PATH = "/dashboard"
API_PATH = "/dashboard/api/v1/overview"
EXPORT_PATHS = {"/dashboard/export", "/dashboard/api/v1/export"}
KNOWN_PATHS = {DASHBOARD_PATH, API_PATH, *EXPORT_PATHS}


@dataclass(frozen=True)
class Request:
    method: str
    path: str
    headers: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Response:
    status: int
    headers: dict[str, str]
    body: bytes


class DashboardApplication:
    """In-process request handler only; M3 intentionally exposes no network listener."""

    def __init__(self, policy: DashboardPolicy, verifier: ServerSessionVerifier, reader: DashboardReader) -> None:
        self.policy = policy
        self.verifier = verifier
        self.reader = reader

    @staticmethod
    def _headers(content_type: str) -> dict[str, str]:
        headers = {
            "Content-Type": content_type,
            "Cache-Control": "no-store, max-age=0",
            "Pragma": "no-cache",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
        }
        if content_type.startswith("text/html"):
            headers["Content-Security-Policy"] = "default-src 'none'; style-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"
        return headers

    @classmethod
    def _json_response(cls, status: int, code: str, message: str) -> Response:
        body = canonical({"error": {"code": code, "message": message}})
        return Response(status, cls._headers("application/json; charset=utf-8"), body)

    @staticmethod
    def _authorization(headers: Mapping[str, str]) -> str:
        matches = [value for key, value in headers.items() if key.casefold() == "authorization"]
        if len(matches) != 1 or not matches[0].startswith("Bearer ") or matches[0].count(" ") != 1:
            raise DashboardFailure("SESSION_REQUIRED", http_status=401)
        return matches[0][7:]

    def handle(self, request: Request) -> Response:
        if request.path not in KNOWN_PATHS:
            return self._json_response(404, "NOT_FOUND", "Not found")
        if not self.policy.enabled or self.policy.environment != "offline_synthetic_test":
            return self._json_response(404, "NOT_FOUND", "Not found")
        try:
            claims = self.verifier.verify(self._authorization(request.headers))
            if request.path in EXPORT_PATHS:
                raise DashboardFailure("EXPORT_DISABLED", http_status=403)
            if request.method != "GET":
                raise DashboardFailure("METHOD_NOT_ALLOWED", http_status=405)
            overview = self.reader.overview(claims["roles"])
            if request.path == API_PATH:
                return Response(200, self._headers("application/json; charset=utf-8"), canonical(overview))
            document = render_dashboard(overview, claims["sub"]).encode("utf-8")
            return Response(200, self._headers("text/html; charset=utf-8"), document)
        except DashboardFailure as exc:
            public = {
                "SESSION_REQUIRED": "Authentication required",
                "SESSION_INVALID": "Authentication failed",
                "SESSION_EXPIRED": "Session expired",
                "SESSION_NOT_YET_VALID": "Authentication failed",
                "ROLE_FORBIDDEN": "Forbidden",
                "EXPORT_DISABLED": "Export is disabled",
                "METHOD_NOT_ALLOWED": "Method not allowed",
                "DASHBOARD_DISABLED": "Not found",
            }
            status = exc.http_status
            code = exc.code if exc.code in public else "EVIDENCE_UNAVAILABLE"
            message = public.get(code, "Verified dashboard evidence is unavailable")
            return self._json_response(status, code, message)
