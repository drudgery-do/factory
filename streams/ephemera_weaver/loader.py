"""Fixture vault loader for Ephemera Weaver.

EPH-001 keeps this deliberately small: discover Markdown fixture files, hash
their source contents, and write a separate index manifest without modifying
the source vault.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class MarkdownNote:
    relative_path: str
    content: str
    sha256: str


def load_markdown_files(vault_path: Path) -> list[MarkdownNote]:
    vault_path = vault_path.resolve()
    markdown_paths = sorted(path for path in vault_path.rglob("*.md") if path.is_file())

    notes = []
    for path in markdown_paths:
        content = path.read_text(encoding="utf-8")
        notes.append(
            MarkdownNote(
                relative_path=path.relative_to(vault_path).as_posix(),
                content=content,
                sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
            )
        )
    return notes


def build_hash_manifest(vault_path: Path) -> dict[str, str]:
    return {
        note.relative_path: note.sha256
        for note in load_markdown_files(vault_path)
    }


def index_fixture_vault(vault_path: Path, output_dir: Path) -> Path:
    vault_path = vault_path.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    notes = load_markdown_files(vault_path)
    index_path = output_dir / f"{vault_path.name}-index.json"
    payload = {
        "vault_name": vault_path.name,
        "source_file_count": len(notes),
        "source_hashes": {note.relative_path: note.sha256 for note in notes},
        "notes": [asdict(note) for note in notes],
    }
    index_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return index_path
