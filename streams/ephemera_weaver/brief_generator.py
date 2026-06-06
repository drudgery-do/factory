"""Deterministic local brief generation from retrieved notes."""

from __future__ import annotations

import re


def generate_research_brief(prompt: str, retrieved_notes: list[dict[str, object]]) -> dict[str, object]:
    if not retrieved_notes:
        summary = "No retrieved notes were available for this prompt."
        markdown = "\n".join(
            [
                "# Research Brief",
                "",
                f"Prompt: {prompt}",
                "",
                "## Summary",
                "",
                summary,
                "",
                "## TODO",
                "",
                "- Add relevant source notes before drafting a grounded brief.",
                "",
            ]
        )
        return {
            "kind": "research_brief",
            "prompt": prompt,
            "title": "Research Brief",
            "summary": summary,
            "sources": [],
            "markdown": markdown,
        }

    sources = [str(note["relative_path"]) for note in retrieved_notes]
    first = retrieved_notes[0]
    first_title = str(first["title"])
    summary = _first_sentence(str(first.get("snippet") or first.get("content") or ""))
    title = f"Research Brief: {first_title}"

    markdown = "\n".join(
        [
            f"# {title}",
            "",
            f"Prompt: {prompt}",
            "",
            "## Summary",
            "",
            summary,
            "",
            "## Source Notes",
            "",
            *[f"- {source}" for source in sources],
            "",
        ]
    )
    return {
        "kind": "research_brief",
        "prompt": prompt,
        "title": title,
        "summary": summary,
        "sources": sources,
        "markdown": markdown,
    }


def _first_sentence(text: str) -> str:
    compact = " ".join(text.split())
    if not compact:
        return "Retrieved notes did not include preview text."
    match = re.search(r"(.+?[.!?])(?:\s|$)", compact)
    return match.group(1) if match else compact
