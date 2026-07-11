#!/usr/bin/env python3
"""Deterministic non-production fixtures for CA-SC P0/P1."""

from __future__ import annotations

import hashlib
import json

SEED = "HEAOTANG-CA-SC-20260712-V1"


def synthetic_id(kind: str, index: int) -> str:
    digest = hashlib.sha256(f"{SEED}|{kind}|{index}".encode()).hexdigest()[:12]
    return f"SYN-{kind.upper()}-{digest}"


def club(index: int, club_type: str, category: str, status: str) -> dict[str, object]:
    return {
        "club_id": synthetic_id("club", index),
        "display_name": f"合成自建俱乐部候选-{index:02d}",
        "type": club_type,
        "category": category,
        "status": status,
        "city": "合成城市",
        "synthetic": True,
    }


def build_bundle() -> dict[str, object]:
    clubs = [club(i, "standard", "general", "active") for i in range(1, 6)]
    clubs += [
        club(6, "standard", "charity", "active"),
        club(7, "standard", "health", "active"),
        club(8, "standard", "trade", "active"),
        club(9, "family", "general", "active"),
        club(10, "direct", "general", "active"),
        club(11, "standard", "general", "pending"),
        club(12, "standard", "general", "rejected"),
        club(13, "standard", "general", "dissolved"),
    ]
    actors = {
        "guest": synthetic_id("actor-guest", 1),
        "candidate_a": synthetic_id("actor-candidate", 1),
        "isolated_b": synthetic_id("actor-isolated", 1),
        "existing_member_c": synthetic_id("actor-member", 1),
    }
    scenarios = [
        {"case_id":"SC-SYN-001","kind":"list-page-1","expected":"two-active-standard-general"},
        {"case_id":"SC-SYN-002","kind":"list-page-2","expected":"three-active-standard-general"},
        {"case_id":"SC-SYN-003","kind":"mixed-zero-crossover","expected":"five-only"},
        {"case_id":"SC-SYN-004","kind":"detail-valid","expected":"available"},
        {"case_id":"SC-SYN-005","kind":"detail-charity","expected_error_id":"CLUB_DETAIL_UNAVAILABLE"},
        {"case_id":"SC-SYN-006","kind":"detail-inactive","expected_error_id":"CLUB_DETAIL_UNAVAILABLE"},
        {"case_id":"SC-SYN-007","kind":"join-first","expected_status":201},
        {"case_id":"SC-SYN-008","kind":"join-replay","expected_status":200,"expected_header":"Idempotency-Replayed:true"},
        {"case_id":"SC-SYN-009","kind":"join-key-reused","expected_error_id":"IDEMPOTENCY_KEY_REUSED"},
        {"case_id":"SC-SYN-010","kind":"join-concurrent","expected":"at-most-one-pending"},
        {"case_id":"SC-SYN-011","kind":"existing-pending","expected":"no-duplicate"},
        {"case_id":"SC-SYN-012","kind":"my-three-status","expected":["pending","approved","rejected"]},
        {"case_id":"SC-SYN-013","kind":"cross-user-isolation","expected":"zero-leakage"},
        {"case_id":"SC-SYN-014","kind":"forbidden-response-field","expected_error_id":"CLUB_APPLICATION_ACCESS_DENIED"},
    ]
    return {"contract_version":"ca-sc-synthetic-fixtures.v1","seed":SEED,"synthetic_only":True,"environment":"non-production","page_size":2,"actors":actors,"clubs":clubs,"scenarios":scenarios}


if __name__ == "__main__":
    print(json.dumps(build_bundle(), ensure_ascii=False, indent=2, sort_keys=True))
