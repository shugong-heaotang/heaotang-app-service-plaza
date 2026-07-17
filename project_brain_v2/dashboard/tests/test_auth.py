from __future__ import annotations

import unittest

from project_brain_v2.dashboard.auth import ServerSessionVerifier
from project_brain_v2.dashboard.errors import DashboardFailure
from project_brain_v2.dashboard.tests._support import DashboardTestCase


class ServerSessionTests(DashboardTestCase):
    def test_valid_short_lived_server_session(self):
        claims = self.verifier.verify(self.session())
        self.assertEqual("boss-1", claims["sub"])

    def test_forged_signature_is_rejected(self):
        forged = self.session()[:-1] + ("A" if self.session()[-1] != "A" else "B")
        with self.assertRaisesRegex(DashboardFailure, "SESSION_INVALID"):
            self.verifier.verify(forged)

    def test_expired_session_is_rejected(self):
        with self.assertRaisesRegex(DashboardFailure, "SESSION_EXPIRED"):
            self.verifier.verify(self.session(issued_at=self.NOW - 400, expires_at=self.NOW - 40))

    def test_future_session_is_rejected(self):
        with self.assertRaisesRegex(DashboardFailure, "SESSION_NOT_YET_VALID"):
            self.verifier.verify(self.session(issued_at=self.NOW + 31, expires_at=self.NOW + 100))

    def test_wrong_audience_or_issuer_is_rejected(self):
        for value in (self.session(audience="other"), self.session(issuer="other")):
            with self.subTest(value=value[:20]):
                with self.assertRaisesRegex(DashboardFailure, "SESSION_INVALID"):
                    self.verifier.verify(value)

    def test_session_exceeding_ttl_is_rejected(self):
        with self.assertRaisesRegex(DashboardFailure, "SESSION_INVALID"):
            self.verifier.verify(self.session(expires_at=self.NOW + 901))

    def test_unauthorized_role_is_rejected(self):
        with self.assertRaisesRegex(DashboardFailure, "ROLE_FORBIDDEN"):
            self.verifier.verify(self.session(roles=["ordinary_member"]))

    def test_unknown_claim_is_rejected(self):
        with self.assertRaisesRegex(DashboardFailure, "SESSION_INVALID"):
            self.verifier.verify(self.session(extra={"admin": True}))

    def test_malformed_tokens_are_rejected(self):
        for value in ("", "Bearer x", "pbv2s1.a", "other.a.b", "pbv2s1.@@@.@@@"):
            with self.subTest(value=value):
                with self.assertRaises(DashboardFailure):
                    self.verifier.verify(value)

    def test_key_must_be_injected_and_at_least_32_bytes(self):
        with self.assertRaisesRegex(DashboardFailure, "SESSION_KEY_INVALID"):
            ServerSessionVerifier(self.repo, self.policy, b"short", lambda _sub, _nonce, _exp: True)

    def test_nonce_must_be_accepted_by_server_side_validator(self):
        verifier = ServerSessionVerifier(self.repo, self.policy, self.SECRET, lambda _sub, _nonce, _exp: False, clock=lambda: self.NOW)
        with self.assertRaisesRegex(DashboardFailure, "SESSION_INVALID"):
            verifier.verify(self.session())


if __name__ == "__main__":
    unittest.main()
