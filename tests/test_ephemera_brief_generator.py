import tempfile
import unittest
from pathlib import Path

from streams.ephemera_weaver.brief_generator import generate_research_brief
from streams.ephemera_weaver.indexer import create_sqlite_index
from streams.ephemera_weaver.search_api import LocalSearchAPI


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_VAULT = ROOT / "fixtures" / "ephemera-vaults" / "research-notes"


class EphemeraBriefGeneratorTests(unittest.TestCase):
    def test_generate_research_brief_uses_retrieved_notes_and_cites_sources(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_sqlite_index(FIXTURE_VAULT, Path(tmpdir) / "ephemera.sqlite3")
            results = LocalSearchAPI(db_path).search("read-only source notes")["results"]

        brief = generate_research_brief(
            prompt="Draft a product note about local-first privacy.",
            retrieved_notes=results,
        )

        self.assertEqual(brief["kind"], "research_brief")
        self.assertEqual(brief["prompt"], "Draft a product note about local-first privacy.")
        self.assertIn("Local AI Project", brief["title"])
        self.assertIn("read-only", brief["summary"])
        self.assertEqual(brief["sources"], ["projects/local-ai.md"])
        self.assertIn("projects/local-ai.md", brief["markdown"])
        self.assertIn("## Source Notes", brief["markdown"])

    def test_generate_research_brief_handles_no_retrieved_notes(self):
        brief = generate_research_brief(
            prompt="Draft a product note about missing context.",
            retrieved_notes=[],
        )

        self.assertEqual(brief["sources"], [])
        self.assertIn("No retrieved notes were available", brief["summary"])
        self.assertIn("TODO", brief["markdown"])


if __name__ == "__main__":
    unittest.main()
