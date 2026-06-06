import tempfile
import unittest
from pathlib import Path

from streams.ephemera_weaver.ui import render_local_ui, write_local_ui


class EphemeraUiScaffoldTests(unittest.TestCase):
    def test_render_local_ui_contains_expected_controls_and_privacy_copy(self):
        html = render_local_ui()

        self.assertIn("<title>Ephemera Weaver</title>", html)
        self.assertIn('type="file"', html)
        self.assertIn("webkitdirectory", html)
        self.assertIn('name="prompt"', html)
        self.assertIn("Generate Brief", html)
        self.assertIn("Export Markdown", html)
        self.assertIn("Read-only by default", html)
        self.assertIn("No hidden cloud upload", html)

    def test_write_local_ui_writes_static_html(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_local_ui(Path(tmpdir))

            self.assertEqual(path.name, "index.html")
            self.assertIn("Ephemera Weaver", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
