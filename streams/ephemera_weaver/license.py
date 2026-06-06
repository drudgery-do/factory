"""License-key checks for Ephemera Weaver.

Only test mode is implemented here. Live licensing requires an approved provider
and secret-storage path before any production credentials are introduced.
"""

from __future__ import annotations


TEST_LICENSE_KEYS = {"EPH-TEST-VALID"}


def check_license_key(license_key: str, mode: str = "test") -> dict[str, object]:
    if mode == "test":
        valid = license_key in TEST_LICENSE_KEYS
        return {
            "valid": valid,
            "mode": "test",
            "reason": "accepted_test_key" if valid else "unknown_test_key",
        }

    return {
        "valid": False,
        "mode": mode,
        "reason": "live_license_check_not_configured",
        "approval_gate": "license provider and secret storage approval required",
    }
