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
        self.assertIn("not the approved seed corpus", card)
        self.assertIn("10 clean direct PDF fixture sources", card)
        self.assertIn("Approval does not mean", card)
        self.assertIn("Codex Assessment Scope", card)
        self.assertIn("How To Review The Remaining Approval", card)
        self.assertIn("discovery shortlist, not as approval for FPP-001", card)
        self.assertIn("Reject any source that requires browser challenge bypass", card)
        self.assertIn("Price accuracy is handled later", card)
        self.assertIn("## Discovery Shortlist", card)
        self.assertIn("provider name", card)
        self.assertIn("source URL", card)
        self.assertIn("local PDF fixture path", card)
        self.assertIn("Codex source assessment", card)
        self.assertIn("Copy-Paste Approval Statement", card)
        self.assertIn("does not certify", card)
        self.assertIn("listed prices are accurate or current", card)
        self.assertIn("only after this card contains 10 final direct GPL PDF", card)
        self.assertIn("California Cremation & Burial", card)
        self.assertIn("Kern Funeral Home", card)
        self.assertIn("https://www.bunkerfuneral.com/general-price-list/", card)
        self.assertIn("command-line HEAD returned Cloudflare challenge 403", card)
        self.assertIn("Walker Sanderson Funeral Home & Crematory", card)
        self.assertEqual(card.count("| PENDING | PENDING | PENDING |"), 10)
        self.assertIn("No seed GPLs imported.", card)


if __name__ == "__main__":
    unittest.main()
