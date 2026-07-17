from __future__ import annotations

import base64
import hashlib
import hmac
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from project_brain_v2.dashboard.app import DashboardApplication
from project_brain_v2.dashboard.auth import TOKEN_PREFIX, ServerSessionVerifier
from project_brain_v2.dashboard.policy import DashboardPolicy
from project_brain_v2.dashboard.reader import DashboardReader
from project_brain_v2.runtime.engine import RefreshEngine

G0_FACT = "governance.work_items.status_counts"
G0_FIXTURE = "contracts/project-brain/v2/examples/trusted-g0-synthetic.json"
G1_FACT = "synthetic.operations.completed_services.count"
G1_FIXTURE = "contracts/project-brain/v2/examples/trusted-g1-synthetic.json"


def b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def token(secret: bytes, now: int, *, subject: str = "boss-1", roles: list[str] | None = None,
          issuer: str = "project-brain-v2-server-session", audience: str = "project-brain-v2-boss-dashboard",
          issued_at: int | None = None, expires_at: int | None = None, extra: dict[str, Any] | None = None) -> str:
    claims: dict[str, Any] = {
        "contract_version": "project-brain-server-session-claims.v1",
        "iss": issuer,
        "aud": audience,
        "sub": subject,
        "roles": roles or ["project_owner"],
        "iat": now if issued_at is None else issued_at,
        "exp": now + 300 if expires_at is None else expires_at,
        "nonce": "abcdefghijklmnop",
    }
    if extra:
        claims.update(extra)
    payload = b64(json.dumps(claims, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{TOKEN_PREFIX}.{payload}".encode("ascii")
    signature = b64(hmac.new(secret, signing_input, hashlib.sha256).digest())
    return f"{TOKEN_PREFIX}.{payload}.{signature}"


class DashboardTestCase(unittest.TestCase):
    NOW = 1_800_000_000
    SECRET = b"m3-offline-test-key-32-bytes-long!!"

    def setUp(self) -> None:
        self.repo = Path(__file__).resolve().parents[3]
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.state = self.root / "state"
        self.runtime_policy_path = self.root / "runtime-policy.json"
        runtime_policy = json.loads((self.repo / "contracts/project-brain/v2/runtime/runtime-policy.disabled.v1.json").read_text(encoding="utf-8"))
        runtime_policy["enabled"] = True
        runtime_policy["allowed_fixtures"] = [
            G0_FIXTURE,
            G1_FIXTURE,
            "contracts/project-brain/v2/examples/unknown-source-missing.json",
            "contracts/project-brain/v2/examples/missing-for-m3-test.json",
        ]
        self.runtime_policy_path.write_text(json.dumps(runtime_policy), encoding="utf-8")
        self.engine = RefreshEngine(self.repo, self.state, self.runtime_policy_path)
        raw_policy = json.loads((self.repo / "contracts/project-brain/v2/dashboard/dashboard-policy.disabled.v1.json").read_text(encoding="utf-8"))
        raw_policy["environment"] = "offline_synthetic_test"
        raw_policy["enabled"] = True
        self.raw_policy = raw_policy
        self.policy = DashboardPolicy.from_mapping(self.repo, raw_policy)
        self.verifier = ServerSessionVerifier(self.repo, self.policy, self.SECRET, lambda _sub, _nonce, _exp: True, clock=lambda: self.NOW)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def reader(self, policy: DashboardPolicy | None = None) -> DashboardReader:
        return DashboardReader(self.repo, self.state, policy or self.policy)

    def app(self, policy: DashboardPolicy | None = None) -> DashboardApplication:
        selected = policy or self.policy
        verifier = ServerSessionVerifier(self.repo, selected, self.SECRET, lambda _sub, _nonce, _exp: True, clock=lambda: self.NOW)
        return DashboardApplication(selected, verifier, self.reader(selected))

    def run_g0(self, run_id: str = "g0") -> dict[str, Any]:
        return self.engine.run(run_id, G0_FACT, G0_FIXTURE, "project_owner", actor="m3-test-runtime")

    def run_g1(self, run_id: str = "g1") -> dict[str, Any]:
        return self.engine.run(run_id, G1_FACT, G1_FIXTURE, "project_brain_reviewer", actor="m3-test-runtime")

    def session(self, **kwargs: Any) -> str:
        return token(self.SECRET, self.NOW, **kwargs)
