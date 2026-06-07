import unittest

from streams.funeral_price_pages.extraction_run import GPLExtractionRun
from streams.funeral_price_pages.line_item_extractor import extract_line_items
from streams.funeral_price_pages.page_generator import (
    REQUIRED_PRICE_NOTICE,
    city_comparison_path,
    funeral_home_path,
    render_city_comparison_page,
    render_funeral_home_page,
)
from streams.funeral_price_pages.seed_import import load_seed_manifest


class FuneralPricePagesPageGeneratorTests(unittest.TestCase):
    def test_funeral_home_page_includes_source_timestamp_notice_and_schema(self):
        seed = next(seed for seed in load_seed_manifest() if seed.gpl_id == "fpp-seed-008-legends-tri-county")
        run = GPLExtractionRun.pending_for_seed(
            seed,
            started_at="2026-06-07T02:20:00Z",
            extractor_version="text-fixture-v0",
        )
        items = extract_line_items(
            "DIRECT CREMATION PACKAGE\nDirect Cremation with provider container $995.00",
            run,
            extraction_date="2026-06-07",
        )

        html = render_funeral_home_page(seed, items)

        self.assertIn("schema.org", html)
        self.assertIn("LocalBusiness", html)
        self.assertIn(seed.source_url, html)
        self.assertIn("2026-06-07", html)
        self.assertIn(REQUIRED_PRICE_NOTICE, html)
        self.assertIn("low-confidence rows blocked", html)

    def test_city_comparison_page_only_renders_publishable_items(self):
        seed = load_seed_manifest()[0]
        high_run = GPLExtractionRun.pending_for_seed(
            seed,
            started_at="2026-06-07T02:20:00Z",
            extractor_version="text-fixture-v0",
        )
        high = extract_line_items(
            "DIRECT CREMATION PACKAGE\nDirect Cremation with provider container $995.00",
            high_run,
            extraction_date="2026-06-07",
        )[0]
        low = high.__class__(
            line_item_id="low",
            run_id=high.run_id,
            gpl_id=high.gpl_id,
            source_sha256=high.source_sha256,
            category=high.category,
            description="X",
            price=5.0,
            confidence=0.2,
            extraction_date=high.extraction_date,
            verify_notice=high.verify_notice,
        )

        html = render_city_comparison_page(
            city=seed.city,
            state=seed.state,
            service="direct cremation",
            provider_items=[(seed, high), (seed, low)],
        )

        self.assertIn("Direct Cremation with provider container", html)
        self.assertNotIn("<td>X</td>", html)
        self.assertIn(REQUIRED_PRICE_NOTICE, html)

    def test_page_paths_are_stable(self):
        seed = load_seed_manifest()[0]

        self.assertEqual(
            funeral_home_path(seed),
            "/funeral-homes/wa/seattle/bonney-watson/",
        )
        self.assertEqual(
            city_comparison_path("San Francisco", "CA", "Direct Cremation"),
            "/funeral-prices/ca/san-francisco/direct-cremation/",
        )


if __name__ == "__main__":
    unittest.main()
