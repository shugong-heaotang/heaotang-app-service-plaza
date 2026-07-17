from __future__ import annotations

import json
import unittest

from project_brain_v2.dashboard.app import API_PATH, DASHBOARD_PATH, DashboardApplication, Request
from project_brain_v2.dashboard.auth import ServerSessionVerifier
from project_brain_v2.dashboard.policy import DashboardPolicy
from project_brain_v2.dashboard.render import render_dashboard
from project_brain_v2.dashboard.tests._support import DashboardTestCase


class DashboardApplicationTests(DashboardTestCase):
    def request(self, path=DASHBOARD_PATH, method="GET", session=None, headers=None):
        values = dict(headers or {})
        if session is not None:
            values["Authorization"] = f"Bearer {session}"
        return Request(method=method, path=path, headers=values)

    def test_authorized_html_dashboard(self):
        self.run_g1()
        response = self.app().handle(self.request(session=self.session(roles=["project_brain_reviewer"])))
        text = response.body.decode("utf-8")
        self.assertEqual(200, response.status)
        self.assertIn("Boss Dashboard", text)
        self.assertIn("Synthetic only", text)
        self.assertIn("Trusted", text)
        self.assertEqual("no-store, max-age=0", response.headers["Cache-Control"])
        self.assertIn("default-src 'none'", response.headers["Content-Security-Policy"])
        self.assertNotIn("Set-Cookie", response.headers)

    def test_authorized_api_returns_only_overview_contract(self):
        self.run_g1()
        response = self.app().handle(self.request(path=API_PATH, session=self.session(roles=["project_brain_reviewer"])))
        value = json.loads(response.body)
        self.assertEqual(200, response.status)
        self.assertEqual("project-brain-dashboard-overview.v1", value["contract_version"])
        self.assertFalse(value["decision_usable"])
        self.assertFalse(value["production_enabled"])
        self.assertEqual("synthetic_only", value["data_mode"])

    def test_direct_url_without_session_is_rejected(self):
        for path in (DASHBOARD_PATH, API_PATH):
            with self.subTest(path=path):
                response = self.app().handle(self.request(path=path))
                self.assertEqual(401, response.status)
                self.assertEqual("SESSION_REQUIRED", json.loads(response.body)["error"]["code"])

    def test_forged_and_expired_sessions_are_rejected(self):
        forged = self.session()[:-1] + "A"
        expired = self.session(issued_at=self.NOW - 500, expires_at=self.NOW - 100)
        for session in (forged, expired):
            with self.subTest(session=session[:20]):
                self.assertEqual(401, self.app().handle(self.request(session=session)).status)

    def test_unauthorized_role_is_forbidden(self):
        response = self.app().handle(self.request(session=self.session(roles=["ordinary_member"])))
        self.assertEqual(403, response.status)
        self.assertEqual("ROLE_FORBIDDEN", json.loads(response.body)["error"]["code"])

    def test_ambiguous_authorization_headers_are_rejected(self):
        response = self.app().handle(self.request(headers={
            "Authorization": f"Bearer {self.session()}",
            "authorization": f"Bearer {self.session()}",
        }))
        self.assertEqual(401, response.status)

    def test_export_routes_are_always_forbidden(self):
        for path in ("/dashboard/export", "/dashboard/api/v1/export"):
            with self.subTest(path=path):
                response = self.app().handle(self.request(path=path, session=self.session()))
                self.assertEqual(403, response.status)
                self.assertEqual("EXPORT_DISABLED", json.loads(response.body)["error"]["code"])

    def test_write_methods_are_rejected_after_server_authorization(self):
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            with self.subTest(method=method):
                response = self.app().handle(self.request(method=method, session=self.session()))
                self.assertEqual(405, response.status)
                self.assertEqual("METHOD_NOT_ALLOWED", json.loads(response.body)["error"]["code"])

    def test_unknown_and_query_paths_are_not_routes(self):
        for path in ("/", "/dashboard/other", "/dashboard?export=1"):
            with self.subTest(path=path):
                self.assertEqual(404, self.app().handle(self.request(path=path, session=self.session())).status)

    def test_shipped_default_policy_hides_dashboard(self):
        raw = json.loads((self.repo / "contracts/project-brain/v2/dashboard/dashboard-policy.disabled.v1.json").read_text(encoding="utf-8"))
        disabled = DashboardPolicy.from_mapping(self.repo, raw)
        verifier = ServerSessionVerifier(self.repo, disabled, self.SECRET, lambda _sub, _nonce, _exp: True, clock=lambda: self.NOW)
        app = DashboardApplication(disabled, verifier, self.reader(disabled))
        self.assertEqual(404, app.handle(self.request(session=self.session())).status)

    def test_evidence_failure_returns_stable_non_sensitive_error(self):
        self.run_g1()
        audit = self.state / "audit.jsonl"
        audit.write_bytes(b"not json\n")
        response = self.app().handle(self.request(session=self.session()))
        self.assertEqual(503, response.status)
        body = json.loads(response.body)
        self.assertEqual("EVIDENCE_UNAVAILABLE", body["error"]["code"])
        self.assertNotIn(str(self.state), response.body.decode("utf-8"))

    def test_html_contains_no_script_form_link_or_export_control(self):
        self.run_g1()
        text = self.app().handle(self.request(session=self.session(roles=["project_brain_reviewer"]))).body.decode("utf-8").lower()
        for forbidden in ("<script", "<form", "href=", "download=", "type=\"file\""):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)

    def test_renderer_escapes_untrusted_text(self):
        overview = {
            "generated_at": "now", "as_of": None,
            "status_counts": {"Trusted": 0, "Unknown": 0, "No-Go": 0}, "facts": [],
        }
        text = render_dashboard(overview, '<img src=x onerror="alert(1)">')
        self.assertNotIn("<img", text)
        self.assertIn("&lt;img", text)


if __name__ == "__main__":
    unittest.main()
