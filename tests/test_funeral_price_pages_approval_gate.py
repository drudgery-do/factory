from pathlib import Path
import unittest


BACKLOG = Path("streams/funeral-price-pages/backlog.yaml")
APPROVAL_CARD = Path("orchestrator/approvals/FPP-001-seed-gpl-approvals.md")


class FuneralPricePagesApprovalGateTests(unittest.TestCase):
    def test_fpp_001_is_blocked_until_seed_gpl_approvals_exist(self):
        backlog = BACKLOG.read_text(encoding="utf-8")
        card = APPROVAL_CARD.read_text(encoding="utf-8")

        self.assertIn("id: FPP-001", backlog)
        self.assertIn("status: blocked", backlog)
        self.assertIn("approval_gate: first 10 seed GPL approvals", backlog)
        self.assertIn("Risk classification: red", card)
        self.assertIn("## What To Approve", card)
        self.assertIn("source-suitability approval", card)
        self.assertIn("Approval does not mean", card)
        self.assertIn("How To Review This Without Being A Funeral Pricing Expert", card)
        self.assertIn("Price accuracy is handled later", card)
        self.assertIn("## Approval Table", card)
        self.assertIn("provider name", card)
        self.assertIn("source URL", card)
        self.assertIn("Copy-Paste Approval Statement", card)
        self.assertIn("does not certify that listed prices are accurate or current", card)
        self.assertIn("California Cremation & Burial", card)
        self.assertIn("Kern Funeral Home", card)
        self.assertIn("Walker Sanderson Funeral Home & Crematory", card)
        self.assertEqual(card.count("| PENDING | PENDING | PENDING |"), 10)
        self.assertIn("No seed GPLs imported.", card)


if __name__ == "__main__":
    unittest.main()
