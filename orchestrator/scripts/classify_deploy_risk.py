#!/usr/bin/env python3
"""Placeholder deploy risk classifier for ORCH-001."""

from __future__ import annotations

import argparse
import json


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


def match_rules(summary: str, rules: dict[str, list[str]]) -> list[str]:
    normalized = summary.lower()
    return [
        name
        for name, phrases in rules.items()
        if any(phrase in normalized for phrase in phrases)
    ]


def classify(summary: str) -> dict[str, object]:
    red_matches = match_rules(summary, RED_RULES)
    yellow_matches = match_rules(summary, YELLOW_RULES)
    green_matches = match_rules(summary, GREEN_RULES)

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

    return {
        "risk": risk,
        "matched_rules": matches,
        "requires_human_approval": risk == "red",
        "requires_release_reviewer": risk in {"green", "yellow"},
        "summary": summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()
    print(json.dumps(classify(args.summary), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
