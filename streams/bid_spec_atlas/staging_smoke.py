"""Staging smoke-test plan for Bid Spec Atlas."""

from __future__ import annotations


def plan_staging_smoke(base_url: str) -> dict[str, object]:
    if not base_url:
        return {
            "status": "approval_gate",
            "todo": "TODO: approve Bid Spec Atlas staging host before running smoke checks.",
            "checks": [],
            "deploy_performed": False,
        }

    base = base_url.rstrip("/")
    return {
        "status": "ready",
        "todo": None,
        "checks": [
            f"{base}/",
            f"{base}/sitemap.xml",
            f"{base}/items/201-0001-clearing-and-grubbing.html",
        ],
        "deploy_performed": False,
    }
