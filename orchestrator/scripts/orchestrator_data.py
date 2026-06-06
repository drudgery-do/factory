"""Shared repo readers for orchestrator bootstrap scripts."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

STREAMS = {
    "ephemera-weaver": {
        "name": "Ephemera Weaver",
        "backlog": "streams/ephemera-weaver/backlog.yaml",
    },
    "bid-spec-atlas": {
        "name": "Bid Spec Atlas",
        "backlog": "streams/bid-spec-atlas/backlog.yaml",
    },
    "funeral-price-pages": {
        "name": "Funeral Price Pages",
        "backlog": "streams/funeral-price-pages/backlog.yaml",
    },
}


def read_repo_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def parse_backlog_text(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        id_match = re.match(r"- id:\s*([A-Z]+-\d{3})\s*$", line)
        if id_match:
            if current:
                items.append(current)
            current = {"id": id_match.group(1)}
            continue
        if current is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        current[key.strip()] = value.strip().strip('"')

    if current:
        items.append(current)

    return items


def load_orchestrator_backlog() -> list[dict[str, str]]:
    return [
        item
        for item in parse_backlog_text(read_repo_text("portfolio.yaml"))
        if item["id"].startswith("ORCH-")
    ]


def load_stream_backlogs() -> dict[str, list[dict[str, str]]]:
    return {
        stream: parse_backlog_text(read_repo_text(config["backlog"]))
        for stream, config in STREAMS.items()
    }


def load_all_backlogs() -> dict[str, list[dict[str, str]]]:
    return {
        "orchestrator": load_orchestrator_backlog(),
        **load_stream_backlogs(),
    }


def summarize_items(items: list[dict[str, str]]) -> dict[str, int]:
    counts = {"total": len(items), "done": 0, "todo": 0, "in_progress": 0, "blocked": 0, "review": 0}
    for item in items:
        status = item.get("status", "todo")
        counts[status] = counts.get(status, 0) + 1
    return counts


def next_item_id(items: list[dict[str, str]]) -> str | None:
    for item in items:
        if item.get("status", "todo") != "done":
            return item["id"]
    return None
