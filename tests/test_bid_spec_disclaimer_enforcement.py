from pathlib import Path
import unittest

from streams.bid_spec_atlas.item_page_generator import REQUIRED_FOOTER, render_item_page
from streams.bid_spec_atlas.pay_item_schema import PayItemRow


BUSINESS = Path("streams/bid-spec-atlas/business.yaml")


class BidSpecDisclaimerEnforcementTests(unittest.TestCase):
    def test_required_footer_matches_business_non_negotiable(self):
        business_text = BUSINESS.read_text(encoding="utf-8")

        self.assertIn(f"required_footer: {REQUIRED_FOOTER}", business_text)

    def test_rendered_item_page_always_includes_required_footer(self):
        row = PayItemRow(
            pay_item_id="fixture:sample_bid_tab:304-1200",
            source_file_id="fixture:sample_bid_tab",
            item_code="304-1200",
            description="AGGREGATE BASE COURSE",
            unit="TON",
            quantity=150.0,
            unit_price=42.5,
            total=6375.0,
            letting_date="2026-04-15",
            state="Fixture DOT",
            project_id="BR-2026-001",
            bidder="North Road Builders",
        )

        html = render_item_page(row, source_url="https://dot.example.test/bid-tabs/2026.pdf")

        self.assertIn(REQUIRED_FOOTER, html)


if __name__ == "__main__":
    unittest.main()
