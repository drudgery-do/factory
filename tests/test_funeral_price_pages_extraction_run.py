import unittest

from streams.funeral_price_pages.extraction_run import (
    REQUIRED_EXTRACTION_RUN_COLUMNS,
    GPLExtractionRun,
    extraction_run_schema_sql,
)
from streams.funeral_price_pages.seed_import import load_seed_manifest


class FuneralPricePagesExtractionRunTests(unittest.TestCase):
    def test_extraction_run_schema_requires_lineage_to_seed_pdf(self):
        required = {
            "run_id",
            "gpl_id",
            "source_sha256",
            "extractor_version",
            "started_at",
            "status",
        }

        self.assertTrue(required.issubset(REQUIRED_EXTRACTION_RUN_COLUMNS))
        sql = extraction_run_schema_sql()
        self.assertIn("CREATE TABLE IF NOT EXISTS gpl_extraction_runs", sql)
        self.assertIn("FOREIGN KEY (gpl_id) REFERENCES gpl_seed_pdfs", sql)
        self.assertIn("source_sha256 TEXT NOT NULL", sql)
        self.assertIn("low_confidence_count <= line_items_extracted", sql)

    def test_pending_run_can_be_created_from_seed_manifest_row(self):
        seed = load_seed_manifest()[0]

        run = GPLExtractionRun.pending_for_seed(
            seed,
            started_at="2026-06-07T02:05:00Z",
            extractor_version="fixture-v0",
        )

        self.assertEqual(run.validate(), [])
        self.assertEqual(run.gpl_id, seed.gpl_id)
        self.assertEqual(run.source_sha256, seed.content_sha256)
        self.assertEqual(run.status, "pending")

    def test_completed_run_requires_completed_at(self):
        run = GPLExtractionRun(
            run_id="run-1",
            gpl_id="fpp-seed-001",
            source_sha256="abc",
            extractor_version="fixture-v0",
            started_at="2026-06-07T02:05:00Z",
            status="completed",
            line_items_extracted=10,
            low_confidence_count=2,
        )

        self.assertIn("completed_at is required for completed runs", run.validate())

    def test_low_confidence_count_cannot_exceed_extracted_count(self):
        run = GPLExtractionRun(
            run_id="run-1",
            gpl_id="fpp-seed-001",
            source_sha256="abc",
            extractor_version="fixture-v0",
            started_at="2026-06-07T02:05:00Z",
            status="review_required",
            line_items_extracted=2,
            low_confidence_count=3,
        )

        self.assertIn("low_confidence_count cannot exceed line_items_extracted", run.validate())


if __name__ == "__main__":
    unittest.main()
