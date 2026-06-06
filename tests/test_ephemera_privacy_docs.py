from pathlib import Path
import unittest


DOC_PATH = Path("streams/ephemera-weaver/privacy-read-only.md")


class EphemeraPrivacyDocsTests(unittest.TestCase):
    def test_privacy_read_only_docs_cover_required_user_promises(self):
        self.assertTrue(DOC_PATH.exists(), "privacy/read-only docs file is missing")

        docs = DOC_PATH.read_text(encoding="utf-8").lower()

        for required in (
            "read-only by default",
            "no hidden cloud upload",
            "no automatic writeback",
            "does not delete source notes",
            "generated outputs are separate files",
            "approval gate",
        ):
            self.assertIn(required, docs)


if __name__ == "__main__":
    unittest.main()
