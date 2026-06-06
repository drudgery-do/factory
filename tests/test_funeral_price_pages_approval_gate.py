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
        self.assertIn("No seed GPLs imported.", card)


if __name__ == "__main__":
    unittest.main()
