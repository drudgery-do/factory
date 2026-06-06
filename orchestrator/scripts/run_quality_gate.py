#!/usr/bin/env python3
"""Placeholder quality gate runner for ORCH-001 scaffold checks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "README.md",
    "FIRST_WAVE_BRIEF.md",
    "AGENTS.md",
    "CLAUDE.md",
    "ORCHESTRATOR.md",
    "portfolio.yaml",
    "orchestrator/deploy_review_policy.yaml",
    "orchestrator/gate_schema.yaml",
    "orchestrator/task_schema.yaml",
    "orchestrator/daily_digest_template.md",
    "orchestrator/approval_card_template.md",
    "orchestrator/scripts/classify_deploy_risk.py",
    "orchestrator/scripts/score_progress.py",
    "orchestrator/scripts/summarize_status.py",
    ".codex/config.toml",
    ".codex/agents/orchestrator.toml",
    ".codex/agents/qa_reviewer.toml",
    ".codex/agents/release_reviewer.toml",
    ".codex/agents/ephemera_builder.toml",
    ".codex/agents/bid_spec_builder.toml",
    ".codex/agents/funeral_price_builder.toml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/stream_task.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/quality-gates.yml",
    ".github/workflows/orchestrator-daily.yml",
    ".github/workflows/pr-qa-review.yml",
    ".github/workflows/release-review.yml",
    ".github/workflows/deploy-staging.yml",
    ".github/workflows/deploy-production.yml",
]

STREAMS = [
    "streams/ephemera-weaver",
    "streams/bid-spec-atlas",
    "streams/funeral-price-pages",
]

STREAM_FILES = [
    "business.yaml",
    "SKILL.md",
    "spec.md",
    "qa.md",
    "runbook.md",
    "backlog.yaml",
]


def check_file(path: str) -> dict[str, object]:
    file_path = ROOT / path
    return {
        "name": path,
        "exists": file_path.is_file(),
        "nonempty": file_path.is_file() and file_path.stat().st_size > 0,
    }


def main() -> int:
    checks = {path: check_file(path) for path in REQUIRED_FILES}

    for stream in STREAMS:
        for filename in STREAM_FILES:
            path = f"{stream}/{filename}"
            checks[path] = check_file(path)

    aliases = {
        "portfolio.yaml": checks["portfolio.yaml"],
        "deploy_review_policy": checks["orchestrator/deploy_review_policy.yaml"],
    }
    checks.update(aliases)

    failed = [
        name
        for name, result in checks.items()
        if not result["exists"] or not result["nonempty"]
    ]

    payload = {
        "status": "pass" if not failed else "fail",
        "checks_total": len(checks),
        "failed": failed,
        "checks": checks,
        "note": "ORCH-001 placeholder gate only; product gates remain TODO.",
    }

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
