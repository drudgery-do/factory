import sqlite3
import tempfile
import unittest
from pathlib import Path

from streams.ephemera_weaver.indexer import create_sqlite_index, parse_markdown_note, search_notes


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_VAULT = ROOT / "fixtures" / "ephemera-vaults" / "research-notes"


class EphemeraMarkdownSqliteIndexTests(unittest.TestCase):
    def test_parse_markdown_note_extracts_title_tags_and_links(self):
        note_path = FIXTURE_VAULT / "index.md"
        parsed = parse_markdown_note(note_path, FIXTURE_VAULT)

        self.assertEqual(parsed["relative_path"], "index.md")
        self.assertEqual(parsed["title"], "Index")
        self.assertEqual(parsed["links"], ["projects/local-ai"])
        self.assertEqual(parsed["tags"], [])
        self.assertIn("research fragments", parsed["content"])

    def test_create_sqlite_index_stores_fixture_notes_and_hashes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_sqlite_index(FIXTURE_VAULT, Path(tmpdir) / "ephemera.sqlite3")

            with sqlite3.connect(db_path) as conn:
                rows = conn.execute(
                    "select relative_path, title, sha256 from notes order by relative_path"
                ).fetchall()
                links = conn.execute(
                    "select source_path, target from note_links order by source_path, target"
                ).fetchall()
                tags = conn.execute(
                    "select relative_path, tag from note_tags order by relative_path, tag"
                ).fetchall()

        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[1][0], "index.md")
        self.assertEqual(rows[1][1], "Index")
        self.assertRegex(rows[1][2], r"^[a-f0-9]{64}$")
        self.assertIn(("index.md", "projects/local-ai"), links)
        self.assertIn(("projects/local-ai.md", "local-first"), tags)
        self.assertIn(("projects/local-ai.md", "privacy"), tags)

    def test_search_notes_returns_matching_paths_without_modifying_sources(self):
        before_mtimes = {
            path.relative_to(FIXTURE_VAULT).as_posix(): path.stat().st_mtime_ns
            for path in FIXTURE_VAULT.rglob("*.md")
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_sqlite_index(FIXTURE_VAULT, Path(tmpdir) / "ephemera.sqlite3")
            results = search_notes(db_path, "hidden cloud upload")

        after_mtimes = {
            path.relative_to(FIXTURE_VAULT).as_posix(): path.stat().st_mtime_ns
            for path in FIXTURE_VAULT.rglob("*.md")
        }
        self.assertEqual(after_mtimes, before_mtimes)
        self.assertEqual(results[0]["relative_path"], "research/contradictions.md")
        self.assertEqual(results[0]["title"], "Contradictions")


if __name__ == "__main__":
    unittest.main()
