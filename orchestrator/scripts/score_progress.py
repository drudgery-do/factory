#!/usr/bin/env python3
"""Progress scorer for ORCH-004."""

from __future__ import annotations

import json

from orchestrator_data import load_all_backlogs, next_item_id, summarize_items


def score_progress() -> dict[str, object]:
    backlogs = load_all_backlogs()
    return {
        "task_id": "ORCH-004",
        "status": "ok",
        "portfolio": {
            name: summarize_items(items)
            for name, items in backlogs.items()
        },
        "items": {
            name: [item["id"] for item in items]
            for name, items in backlogs.items()
        },
        "next_backlog": {
            name: next_item_id(items)
            for name, items in backlogs.items()
        },
    }


def main() -> int:
    print(json.dumps(score_progress(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
