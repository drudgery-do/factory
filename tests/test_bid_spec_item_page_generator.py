import unittest

from streams.bid_spec_atlas.item_page_generator import (
    REQUIRED_FOOTER,
    render_item_page,
    slug_for_item,
)
from streams.bid_spec_atlas.pay_item_schema import PayItemRow


class BidSpecItemPageGeneratorTests(unittest.TestCase):
    def test_render_item_page_includes_source_link_and_required_disclaimer(self):
        row = PayItemRow(
            pay_item_id="fixture:sample_bid_tab:201-0001",
            source_file_id="fixture:sample_bid_tab",
            item_code="201-0001",
            description="CLEARING AND GRUBBING",
            unit="ACRE",
            quantity=2.5,
            unit_price=1200.0,
            total=3000.0,
            letting_date="2026-04-15",
            state="Fixture DOT",
            project_id="BR-2026-001",
            bidder="North Road Builders",
        )

        html = render_item_page(row, source_url="https://dot.example.test/bid-tabs/2026.pdf")

        self.assertIn("<title>201-0001 CLEARING AND GRUBBING</title>", html)
        self.assertIn("https://dot.example.test/bid-tabs/2026.pdf", html)
        self.assertIn(REQUIRED_FOOTER, html)
        self.assertNotIn("should bid", html.lower())

    def test_slug_for_item_is_stable_and_readable(self):
        self.assertEqual(
            slug_for_item("201-0001", "CLEARING AND GRUBBING"),
            "201-0001-clearing-and-grubbing",
        )


if __name__ == "__main__":
    unittest.main()
