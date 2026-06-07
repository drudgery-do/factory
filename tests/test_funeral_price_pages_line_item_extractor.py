from pathlib import Path
import unittest

from streams.funeral_price_pages.extraction_run import GPLExtractionRun
from streams.funeral_price_pages.line_item_extractor import (
    VERIFY_WITH_PROVIDER_NOTICE,
    extract_line_items,
    line_item_schema_sql,
)
from streams.funeral_price_pages.seed_import import load_seed_manifest


TEXT_FIXTURE = Path("fixtures/funeral-price-pages/extracted-text/legends_tri_county_2025_gpl.txt")


class FuneralPricePagesLineItemExtractorTests(unittest.TestCase):
    def test_extract_line_items_returns_prices_with_confidence_and_required_notice(self):
        seed = next(seed for seed in load_seed_manifest() if seed.gpl_id == "fpp-seed-008-legends-tri-county")
        run = GPLExtractionRun.pending_for_seed(
            seed,
            started_at="2026-06-07T02:10:00Z",
            extractor_version="text-fixture-v0",
        )

        items = extract_line_items(
            TEXT_FIXTURE.read_text(encoding="utf-8"),
            run,
            extraction_date="2026-06-07",
        )

        self.assertGreaterEqual(len(items), 10)
        self.assertEqual(items[0].description, "Basic Services of the Funeral Director and Staff")
        self.assertEqual(items[0].price, 1400.00)
        self.assertEqual(items[0].verify_notice, VERIFY_WITH_PROVIDER_NOTICE)
        self.assertEqual(items[0].validate(), [])
        self.assertTrue(all(item.extraction_date == "2026-06-07" for item in items))
        self.assertTrue(all(item.source_sha256 == seed.content_sha256 for item in items))
        self.assertTrue(all(item.confidence >= 0.7 for item in items))

    def test_line_item_schema_enforces_source_lineage_confidence_and_verify_notice(self):
        sql = line_item_schema_sql()

        self.assertIn("CREATE TABLE IF NOT EXISTS gpl_line_items", sql)
        self.assertIn("FOREIGN KEY (run_id) REFERENCES gpl_extraction_runs", sql)
        self.assertIn("FOREIGN KEY (gpl_id) REFERENCES gpl_seed_pdfs", sql)
        self.assertIn("source_sha256 TEXT NOT NULL", sql)
        self.assertIn("confidence REAL NOT NULL CHECK", sql)
        self.assertIn("verify_notice TEXT NOT NULL", sql)
        self.assertIn("publish_status TEXT NOT NULL DEFAULT 'pending_confidence_review'", sql)

    def test_line_item_rejects_missing_verify_notice(self):
        seed = load_seed_manifest()[0]
        run = GPLExtractionRun.pending_for_seed(
            seed,
            started_at="2026-06-07T02:10:00Z",
            extractor_version="text-fixture-v0",
        )
        item = extract_line_items("Direct Cremation $995.00", run, extraction_date="2026-06-07")[0]
        bad_item = item.__class__(
            line_item_id=item.line_item_id,
            run_id=item.run_id,
            gpl_id=item.gpl_id,
            source_sha256=item.source_sha256,
            category=item.category,
            description=item.description,
            price=item.price,
            confidence=item.confidence,
            extraction_date=item.extraction_date,
            verify_notice="",
        )

        self.assertIn("verify_notice is required", bad_item.validate())


if __name__ == "__main__":
    unittest.main()
