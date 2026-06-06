#!/usr/bin/env python3
"""Daily digest generator for ORCH-004."""

from __future__ import annotations

import argparse
import json
from datetime import date

from orchestrator_data import STREAMS
from score_progress import score_progress


def build_markdown(run_date: str) -> str:
    progress = score_progress()
    portfolio = progress["portfolio"]
    next_backlog = progress["next_backlog"]

    lines = [
        "# Daily Digest",
        "",
        f"Date: {run_date}",
        "",
        "## Portfolio Status",
        "",
    ]

    for name, counts in portfolio.items():
        label = "Orchestrator" if name == "orchestrator" else STREAMS[name]["name"]
        lines.append(
            f"- {label}: {counts['done']} done / {counts['total']} total; next: {next_backlog[name] or 'none'}"
        )

    lines.extend(["", "## Stream Updates", ""])
    for stream, config in STREAMS.items():
        counts = portfolio[stream]
        lines.extend(
            [
                f"### {config['name']}",
                "",
                f"- Progress: {counts['done']} done / {counts['total']} total",
                f"- Next backlog item: {next_backlog[stream] or 'none'}",
                "- PRs: TODO via GitHub integration",
                "- Gates: run `python3 orchestrator/scripts/run_quality_gate.py`",
                "",
            ]
        )

    lines.extend(
        [
            "## Approval Cards Needed",
            "",
            "- Generate with `python3 orchestrator/scripts/generate_approval_card.py` for yellow/red work.",
            "",
            "## Operator Notes",
            "",
            "- No production deploys without explicit approval.",
            "- No production secrets added by bootstrap tools.",
            "- No product features built by ORCH-003 through ORCH-005.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    if args.format == "markdown":
        print(build_markdown(args.date))
    else:
        print(json.dumps({"task_id": "ORCH-004", "status": "ok", "markdown": build_markdown(args.date)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
