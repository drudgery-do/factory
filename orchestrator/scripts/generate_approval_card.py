#!/usr/bin/env python3
"""Approval card generator for ORCH-005."""

from __future__ import annotations

import argparse

from classify_deploy_risk import classify


def build_card(task: str, stream: str, summary: str, requested_by: str) -> str:
    risk = classify(summary, stream)
    if risk["risk"] == "red":
        decision_owner = "Human Owner or Delegate"
    else:
        decision_owner = "Release Reviewer Agent"

    lines = [
        "# Approval Card",
        "",
        f"Task: {task}",
        f"Stream: {stream}",
        f"Requested by: {requested_by}",
        f"Risk classification: {risk['risk']}",
        f"Decision owner: {decision_owner}",
        "",
        "## Decision",
        "",
        "- Approve",
        "- Reject",
        "- Request changes",
        "",
        "## Why Approval Is Needed",
        "",
        f"Matched rules: {', '.join(risk['matched_rules'])}",
        f"Required approver roles: {', '.join(risk['required_approver_roles'])}",
        "",
        "## Evidence Pack",
        "",
        "- PR: TODO",
        "- Tests: TODO",
        "- Quality gate output: TODO",
        "- Artifacts: TODO",
        "- Rollback plan: TODO",
        "",
        "## Explicit Non-Actions",
        "",
        "- No production secrets added.",
        "- No production deploy executed.",
        "- No payment, ad, affiliate, KYC, or domain action executed.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--stream", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--requested-by", required=True)
    args = parser.parse_args()

    print(build_card(args.task, args.stream, args.summary, args.requested_by))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
