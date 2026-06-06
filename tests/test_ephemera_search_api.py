import tempfile
import unittest
from pathlib import Path

from streams.ephemera_weaver.indexer import create_sqlite_index
from streams.ephemera_weaver.search_api import LocalSearchAPI


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_VAULT = ROOT / "fixtures" / "ephemera-vaults" / "research-notes"


class EphemeraSearchApiTests(unittest.TestCase):
    def test_search_api_returns_ranked_structured_results(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_sqlite_index(FIXTURE_VAULT, Path(tmpdir) / "ephemera.sqlite3")
            api = LocalSearchAPI(db_path)

            response = api.search("read-only source notes")

        self.assertEqual(response["query"], "read-only source notes")
        self.assertEqual(response["result_count"], 1)
        self.assertEqual(response["results"][0]["relative_path"], "projects/local-ai.md")
        self.assertEqual(response["results"][0]["title"], "Local AI Project")
        self.assertGreater(response["results"][0]["score"], 0)
        self.assertIn("read-only", response["results"][0]["snippet"])

    def test_search_api_rejects_blank_query(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_sqlite_index(FIXTURE_VAULT, Path(tmpdir) / "ephemera.sqlite3")
            api = LocalSearchAPI(db_path)

            with self.assertRaises(ValueError):
                api.search("   ")

    def test_search_api_returns_empty_results_for_miss(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = create_sqlite_index(FIXTURE_VAULT, Path(tmpdir) / "ephemera.sqlite3")
            api = LocalSearchAPI(db_path)

            response = api.search("nonexistent phrase")

        self.assertEqual(response["result_count"], 0)
        self.assertEqual(response["results"], [])


if __name__ == "__main__":
    unittest.main()
