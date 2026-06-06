import tempfile
import unittest
from pathlib import Path

from streams.ephemera_weaver.exporter import export_generated_markdown


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_VAULT = ROOT / "fixtures" / "ephemera-vaults" / "research-notes"


class EphemeraMarkdownExportTests(unittest.TestCase):
    def test_export_generated_markdown_writes_only_to_output_directory(self):
        before_mtimes = {
            path.relative_to(FIXTURE_VAULT).as_posix(): path.stat().st_mtime_ns
            for path in FIXTURE_VAULT.rglob("*.md")
        }
        brief = {
            "title": "Research Brief: Local AI Project",
            "markdown": "# Research Brief\n\nGenerated output.\n",
            "sources": ["projects/local-ai.md"],
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            export_path = export_generated_markdown(brief, Path(tmpdir))
            exported = export_path.read_text(encoding="utf-8")

        after_mtimes = {
            path.relative_to(FIXTURE_VAULT).as_posix(): path.stat().st_mtime_ns
            for path in FIXTURE_VAULT.rglob("*.md")
        }
        self.assertEqual(after_mtimes, before_mtimes)
        self.assertEqual(export_path.name, "research-brief-local-ai-project.md")
        self.assertIn("# Research Brief", exported)
        self.assertIn("Generated output.", exported)

    def test_export_generated_markdown_rejects_path_traversal_title(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            export_path = export_generated_markdown(
                {"title": "../../Secrets", "markdown": "# Safe\n", "sources": []},
                Path(tmpdir),
            )

            self.assertEqual(export_path.parent, Path(tmpdir).resolve())
            self.assertEqual(export_path.name, "secrets.md")


if __name__ == "__main__":
    unittest.main()
