"""Local search API for Ephemera Weaver."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path


class LocalSearchAPI:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def search(self, query: str, limit: int = 10) -> dict[str, object]:
        terms = [term.lower() for term in re.split(r"\s+", query.strip()) if term]
        if not terms:
            raise ValueError("query must contain at least one term")

        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                select relative_path, title, content, sha256
                from notes
                order by relative_path
                """
            ).fetchall()

        scored = []
        for relative_path, title, content, sha256 in rows:
            normalized = content.lower()
            if any(term not in normalized for term in terms):
                continue
            score = sum(normalized.count(term) for term in terms)
            scored.append(
                {
                    "relative_path": relative_path,
                    "title": title,
                    "snippet": self._snippet(content, terms),
                    "sha256": sha256,
                    "score": score,
                }
            )

        results = sorted(scored, key=lambda item: (-item["score"], item["relative_path"]))[:limit]
        return {
            "query": query,
            "result_count": len(results),
            "results": results,
        }

    @staticmethod
    def _snippet(content: str, terms: list[str], window: int = 80) -> str:
        normalized = content.lower()
        positions = [normalized.find(term) for term in terms if normalized.find(term) >= 0]
        start = min(positions) if positions else 0
        left = max(0, start - window // 2)
        right = min(len(content), start + window)
        return " ".join(content[left:right].split())
