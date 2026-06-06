import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from streams.ephemera_weaver.loader import build_hash_manifest, index_fixture_vault, load_markdown_files


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_VAULT = ROOT / "fixtures" / "ephemera-vaults" / "research-notes"


class EphemeraFixtureLoaderTests(unittest.TestCase):
    def test_load_markdown_files_discovers_nested_fixture_notes(self):
        notes = load_markdown_files(FIXTURE_VAULT)

        self.assertEqual(len(notes), 4)
        self.assertEqual(
            [note.relative_path for note in notes],
            [
                "README.md",
                "index.md",
                "projects/local-ai.md",
                "research/contradictions.md",
            ],
        )
        self.assertIn("read-only", notes[2].content)
        self.assertEqual(
            notes[2].sha256,
            hashlib.sha256(notes[2].content.encode("utf-8")).hexdigest(),
        )

    def test_index_fixture_vault_writes_manifest_without_changing_sources(self):
        before = build_hash_manifest(FIXTURE_VAULT)

        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = index_fixture_vault(FIXTURE_VAULT, Path(tmpdir))
            after = build_hash_manifest(FIXTURE_VAULT)

            self.assertEqual(after, before)
            payload = json.loads(index_path.read_text(encoding="utf-8"))

        self.assertEqual(payload["vault_name"], "research-notes")
        self.assertEqual(payload["source_file_count"], 4)
        self.assertEqual(payload["source_hashes"], before)
        self.assertTrue(index_path.name.endswith("-index.json"))


if __name__ == "__main__":
    unittest.main()
