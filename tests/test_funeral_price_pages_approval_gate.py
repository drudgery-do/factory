from pathlib import Path
import unittest


BACKLOG = Path("streams/funeral-price-pages/backlog.yaml")
APPROVAL_CARD = Path("orchestrator/approvals/FPP-001-seed-gpl-approvals.md")


class FuneralPricePagesApprovalGateTests(unittest.TestCase):
    def test_fpp_001_records_approved_seed_pdf_fixtures(self):
        backlog = BACKLOG.read_text(encoding="utf-8")
        card = APPROVAL_CARD.read_text(encoding="utf-8")

        self.assertIn("id: FPP-001", backlog)
        self.assertIn("status: completed", backlog)
        self.assertIn("approval_gate: completed with 10 clean direct GPL PDF fixtures", backlog)
        self.assertIn("Risk classification: red", card)
        self.assertIn("Decision: Approve", card)
        self.assertIn("Approved PDF Seed Fixtures", card)
        self.assertIn("local PDF fixture storage", card)
        self.assertIn("certification that listed prices are accurate or current", card)
        self.assertIn("verify-with-provider notice", card)
        self.assertIn("Manifest: `fixtures/funeral-price-pages/seed-gpls/manifest.json`", card)
        self.assertIn("Bonney Watson", card)
        self.assertIn("Kern Funeral Home", card)
        self.assertIn("Sinai Memorial", card)
        self.assertEqual(card.count("| approved |"), 10)
        self.assertIn("No production deploy executed.", card)


if __name__ == "__main__":
    unittest.main()
