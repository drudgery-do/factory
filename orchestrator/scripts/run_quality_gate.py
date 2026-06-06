#!/usr/bin/env python3
"""ORCH-002 quality gate runner for orchestration scaffold validation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[2]

TOP_LEVEL_FILES = [
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

STREAMS = {
    "ephemera-weaver": {
        "code": "EPH",
        "expected_ids": [f"EPH-{index:03d}" for index in range(1, 9)],
        "red_gate_terms": ["writeback", "upload", "privacy", "incident"],
    },
    "bid-spec-atlas": {
        "code": "BSA",
        "expected_ids": [f"BSA-{index:03d}" for index in range(1, 9)],
        "red_gate_terms": ["ad network", "marketplace", "robots", "disclaimer"],
    },
    "funeral-price-pages": {
        "code": "FPP",
        "expected_ids": [f"FPP-{index:03d}" for index in range(1, 9)],
        "red_gate_terms": ["gpl", "domain", "affiliate", "provider disputes"],
    },
}

STREAM_FILES = [
    "business.yaml",
    "SKILL.md",
    "spec.md",
    "qa.md",
    "runbook.md",
    "backlog.yaml",
]

ORCH_BACKLOG_IDS = [f"ORCH-{index:03d}" for index in range(1, 6)]

TEXT_EXTENSIONS = {".md", ".yaml", ".yml", ".toml", ".py"}
SECRET_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"prod(?:uction)?[_-]?(?:api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}",
        r"(?:stripe|paypal|adsense|google_ads)[_-]?(?:secret|token|key)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}",
        r"AWS_SECRET_ACCESS_KEY\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{20,}",
    ]
]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def file_ok(path: str) -> bool:
    target = ROOT / path
    return target.is_file() and target.stat().st_size > 0


def make_check(status: bool, message: str, evidence: object | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "status": "pass" if status else "fail",
        "message": message,
    }
    if evidence is not None:
        result["evidence"] = evidence
    return result


def extract_ids(text: str, prefix: str) -> list[str]:
    return sorted(set(re.findall(rf"\b{re.escape(prefix)}-\d{{3}}\b", text)))


def check_scaffold_files() -> dict[str, object]:
    missing = [path for path in TOP_LEVEL_FILES if not file_ok(path)]
    return make_check(
        not missing,
        "All required top-level orchestration files are present and nonempty.",
        {"missing": missing, "required_count": len(TOP_LEVEL_FILES)},
    )


def check_stream_files() -> dict[str, object]:
    required = [
        f"streams/{stream}/{filename}"
        for stream in STREAMS
        for filename in STREAM_FILES
    ]
    missing = [path for path in required if not file_ok(path)]
    return make_check(
        not missing,
        "All stream scaffold files are present and nonempty.",
        {"missing": missing, "required_count": len(required)},
    )


def first_backlog_entries() -> dict[str, list[str]]:
    entries = {
        "orchestrator": extract_ids(read_text("portfolio.yaml"), "ORCH"),
    }
    for stream, config in STREAMS.items():
        entries[stream] = extract_ids(
            read_text(f"streams/{stream}/backlog.yaml"),
            config["code"],
        )
    return entries


def check_backlog_ids() -> dict[str, object]:
    entries = first_backlog_entries()
    expected = {
        "orchestrator": ORCH_BACKLOG_IDS,
        **{stream: config["expected_ids"] for stream, config in STREAMS.items()},
    }
    mismatches = {
        name: {"expected": expected[name], "actual": entries.get(name, [])}
        for name in expected
        if entries.get(name, []) != expected[name]
    }
    return make_check(
        not mismatches,
        "Backlog files contain the required first task IDs.",
        {"mismatches": mismatches, "entries": entries},
    )


def check_deploy_review_policy() -> dict[str, object]:
    text = read_text("orchestrator/deploy_review_policy.yaml").lower()
    required_terms = [
        "builder_may_approve_own_work: false",
        "qa_may_deploy: false",
        "release_reviewer_may_approve",
        "green",
        "yellow",
        "red_requires",
        "human_owner",
        "delegate",
        "privacy policy/terms/disclaimer change",
        "auth/permissions/secrets change",
        "cloud upload feature",
        "user-file writeback feature",
        "first gpl seed approval",
    ]
    missing = [term for term in required_terms if term not in text]
    return make_check(
        not missing,
        "Deploy review policy enforces role separation and red-gate routing.",
        {"missing_terms": missing},
    )


def check_pr_evidence_pack() -> dict[str, object]:
    text = read_text(".github/PULL_REQUEST_TEMPLATE.md").lower()
    required_sections = [
        "task",
        "risk classification",
        "summary",
        "tests run",
        "quality gates",
        "files changed",
        "approval gates / todos",
        "explicit non-actions",
        "no production secrets added",
        "no production deploy executed",
        "no product strategy changed",
    ]
    missing = [section for section in required_sections if section not in text]
    return make_check(
        not missing,
        "PR template requires the ORCH evidence pack and explicit non-actions.",
        {"missing_sections": missing},
    )


def check_codex_agent_boundaries() -> dict[str, object]:
    expectations = {
        ".codex/agents/orchestrator.toml": ["forbidden_actions", "deploy_production", "change_strategy"],
        ".codex/agents/qa_reviewer.toml": ["forbidden_actions", "deploy_production", "approve_red_gate"],
        ".codex/agents/release_reviewer.toml": ["approve_green_deploy", "approve_yellow_deploy", "approve_red_gate"],
        ".codex/agents/ephemera_builder.toml": ["approve_own_work", "upload_user_data", "writeback_user_files"],
        ".codex/agents/bid_spec_builder.toml": ["approve_own_work", "publish_unsourced_facts", "remove_disclaimer"],
        ".codex/agents/funeral_price_builder.toml": ["approve_own_work", "publish_low_confidence_data", "invent_prices"],
    }
    missing: dict[str, list[str]] = {}
    for path, terms in expectations.items():
        text = read_text(path)
        missing_terms = [term for term in terms if term not in text]
        if missing_terms:
            missing[path] = missing_terms
    return make_check(
        not missing,
        "Codex agent configs preserve builder, QA, and release-review boundaries.",
        {"missing_terms": missing},
    )


def check_workflow_deploy_safety() -> dict[str, object]:
    production = read_text(".github/workflows/deploy-production.yml").lower()
    staging = read_text(".github/workflows/deploy-staging.yml").lower()
    config = read_text(".codex/config.toml").lower()
    failures = []
    if "exit 1" not in production:
        failures.append("production workflow must exit 1 during bootstrap")
    if "production deploys are disabled" not in production:
        failures.append("production workflow must state deploys are disabled")
    if "placeholder" not in staging:
        failures.append("staging workflow must remain placeholder-only")
    if "production_deploys_enabled = false" not in config:
        failures.append("codex config must disable production deploys")
    if "production_secrets_allowed = false" not in config:
        failures.append("codex config must disallow production secrets")
    return make_check(
        not failures,
        "Deploy workflows remain blocked or placeholder-only during bootstrap.",
        {"failures": failures},
    )


def check_stream_red_gates() -> dict[str, object]:
    missing: dict[str, list[str]] = {}
    for stream, config in STREAMS.items():
        text = (
            read_text(f"streams/{stream}/business.yaml")
            + "\n"
            + read_text(f"streams/{stream}/qa.md")
        ).lower()
        missing_terms = [term for term in config["red_gate_terms"] if term not in text]
        if missing_terms:
            missing[stream] = missing_terms
    return make_check(
        not missing,
        "Each stream records its required red-gate triggers.",
        {"missing_terms": missing},
    )


def check_no_production_secrets() -> dict[str, object]:
    findings = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if not path.is_file() or path.suffix not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(str(path.relative_to(ROOT)))
                break
    return make_check(
        not findings,
        "No production secret-like assignments found in scaffold text files.",
        {"findings": findings},
    )


def run_checks() -> dict[str, dict[str, object]]:
    checkers: dict[str, Callable[[], dict[str, object]]] = {
        "scaffold_files": check_scaffold_files,
        "stream_files": check_stream_files,
        "backlog_ids": check_backlog_ids,
        "deploy_review_policy": check_deploy_review_policy,
        "pr_evidence_pack": check_pr_evidence_pack,
        "codex_agent_boundaries": check_codex_agent_boundaries,
        "workflow_deploy_safety": check_workflow_deploy_safety,
        "stream_red_gates": check_stream_red_gates,
        "no_production_secrets": check_no_production_secrets,
    }
    checks = {name: checker() for name, checker in checkers.items()}

    for path in TOP_LEVEL_FILES:
        checks[path] = make_check(file_ok(path), f"{path} exists and is nonempty.")
    for stream in STREAMS:
        for filename in STREAM_FILES:
            path = f"streams/{stream}/{filename}"
            checks[path] = make_check(file_ok(path), f"{path} exists and is nonempty.")

    return checks


def main() -> int:
    checks = run_checks()
    failed = [
        name
        for name, result in checks.items()
        if result["status"] != "pass"
    ]
    payload = {
        "task_id": "ORCH-002",
        "status": "pass" if not failed else "fail",
        "checks_total": len(checks),
        "failed": failed,
        "checks": checks,
        "first_backlog_entries": first_backlog_entries(),
        "note": "ORCH-002 validates scaffold structure, policy boundaries, evidence requirements, backlog seeds, and deploy safety.",
    }

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
