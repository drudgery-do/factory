#!/usr/bin/env python3
"""Deploy risk classifier for ORCH-003."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable


RED_RULES = {
    "payments": ["payment", "payments", "kyc"],
    "domain": ["domain purchase", "domain transfer", "domain choice"],
    "ads": ["ad network", "affiliate application", "affiliate"],
    "policy": ["privacy", "terms", "license", "refund"],
    "disclaimer": ["disclaimer"],
    "auth": ["auth", "permission", "permissions", "secret", "secrets"],
    "cloud_upload": ["cloud upload", "upload user data"],
    "writeback": ["writeback", "write to user files", "modify user files"],
    "deletion": ["delete user files", "deletion"],
    "dispute": ["provider dispute"],
    "legal": ["legal threat", "reputation complaint"],
    "incident": ["security incident", "incident response"],
    "first_gpl": ["first gpl", "seed gpl approval"],
}

RED_FILE_RULES = {
    "production_deploy_workflow": [".github/workflows/deploy-production.yml"],
    "codex_config": [".codex/config.toml"],
    "github_workflow_permissions": [".github/workflows/"],
    "agent_permissions": [".codex/agents/"],
}

YELLOW_RULES = {
    "parser": ["new parser", "existing approved source class"],
    "background_job": ["background job"],
    "migration": ["migration", "non-destructive migration"],
    "template": ["page template"],
    "license_server": ["license server"],
    "confidence": ["confidence threshold"],
}

GREEN_RULES = {
    "docs": ["docs", "documentation", "copy"],
    "parser_bugfix": ["parser bugfix", "golden tests"],
    "sitemap": ["sitemap"],
    "schema": ["non-destructive schema"],
    "ui": ["ui change"],
}


def match_rules(text: str, rules: dict[str, list[str]]) -> list[str]:
    normalized = text.lower()
    return [
        name
        for name, phrases in rules.items()
        if any(phrase in normalized for phrase in phrases)
    ]


def match_file_rules(paths: Iterable[str]) -> list[str]:
    matches: list[str] = []
    for path in paths:
        normalized = path.lower()
        for name, prefixes in RED_FILE_RULES.items():
            if any(normalized == prefix or normalized.startswith(prefix) for prefix in prefixes):
                matches.append(name)
    return sorted(set(matches))


def classify(summary: str, stream: str | None = None, changed_files: list[str] | None = None) -> dict[str, object]:
    changed_files = changed_files or []
    context = f"{summary} {stream or ''}"
    red_matches = sorted(set(match_rules(context, RED_RULES) + match_file_rules(changed_files)))
    yellow_matches = match_rules(context, YELLOW_RULES)
    green_matches = match_rules(context, GREEN_RULES)

    if red_matches:
        risk = "red"
        matches = red_matches
    elif yellow_matches:
        risk = "yellow"
        matches = yellow_matches
    elif green_matches:
        risk = "green"
        matches = green_matches
    else:
        risk = "yellow"
        matches = ["unclassified_requires_release_review"]

    if risk == "red":
        required_roles = ["human_owner", "delegate"]
        approval_required = "human"
        release_reviewer_can_approve = False
    else:
        required_roles = ["release_reviewer"]
        approval_required = "release_reviewer"
        release_reviewer_can_approve = True

    return {
        "task_id": "ORCH-003",
        "risk": risk,
        "matched_rules": matches,
        "approval_required": approval_required,
        "required_approver_roles": required_roles,
        "release_reviewer_can_approve": release_reviewer_can_approve,
        "requires_human_approval": risk == "red",
        "requires_release_reviewer": risk in {"green", "yellow"},
        "summary": summary,
        "stream": stream,
        "changed_files": changed_files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--stream")
    parser.add_argument("--changed-file", action="append", default=[])
    args = parser.parse_args()
    print(json.dumps(classify(args.summary, args.stream, args.changed_file), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
