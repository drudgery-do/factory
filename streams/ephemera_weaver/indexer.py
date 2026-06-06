"""Markdown parser and SQLite index for Ephemera Weaver."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from streams.ephemera_weaver.loader import load_markdown_files


WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
TAG_RE = re.compile(r"(?<!\w)#([A-Za-z][A-Za-z0-9_-]*)")


def parse_markdown_note(note_path: Path, vault_path: Path) -> dict[str, object]:
    vault_path = vault_path.resolve()
    note_path = note_path.resolve()
    content = note_path.read_text(encoding="utf-8")
    title = note_path.stem

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            break

    return {
        "relative_path": note_path.relative_to(vault_path).as_posix(),
        "title": title,
        "content": content,
        "links": [link.strip() for link in WIKI_LINK_RE.findall(content)],
        "tags": sorted(set(TAG_RE.findall(content))),
    }


def create_sqlite_index(vault_path: Path, db_path: Path) -> Path:
    vault_path = vault_path.resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    notes = load_markdown_files(vault_path)

    with sqlite3.connect(db_path) as conn:
        conn.executescript(
            """
            drop table if exists notes;
            drop table if exists note_links;
            drop table if exists note_tags;

            create table notes (
                relative_path text primary key,
                title text not null,
                content text not null,
                sha256 text not null
            );

            create table note_links (
                source_path text not null,
                target text not null
            );

            create table note_tags (
                relative_path text not null,
                tag text not null
            );
            """
        )

        for note in notes:
            parsed = parse_markdown_note(vault_path / note.relative_path, vault_path)
            conn.execute(
                "insert into notes(relative_path, title, content, sha256) values (?, ?, ?, ?)",
                (note.relative_path, parsed["title"], note.content, note.sha256),
            )
            conn.executemany(
                "insert into note_links(source_path, target) values (?, ?)",
                [(note.relative_path, target) for target in parsed["links"]],
            )
            conn.executemany(
                "insert into note_tags(relative_path, tag) values (?, ?)",
                [(note.relative_path, tag) for tag in parsed["tags"]],
            )

    return db_path


def search_notes(db_path: Path, query: str, limit: int = 10) -> list[dict[str, str]]:
    terms = [term for term in re.split(r"\s+", query.strip()) if term]
    if not terms:
        return []

    where = " and ".join(["lower(content) like ?"] * len(terms))
    params = [f"%{term.lower()}%" for term in terms]

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            f"""
            select relative_path, title, content, sha256
            from notes
            where {where}
            order by relative_path
            limit ?
            """,
            [*params, limit],
        ).fetchall()

    return [
        {
            "relative_path": row[0],
            "title": row[1],
            "content": row[2],
            "sha256": row[3],
        }
        for row in rows
    ]
