from pathlib import Path
import unittest

from streams.funeral_price_pages.seed_import import (
    REQUIRED_GPL_METADATA_COLUMNS,
    GPLSeedPDF,
    gpl_metadata_schema_sql,
    load_seed_manifest,
    validate_seed_corpus,
)


MANIFEST = Path("fixtures/funeral-price-pages/seed-gpls/manifest.json")


class FuneralPricePagesSeedImportTests(unittest.TestCase):
    def test_seed_manifest_contains_10_clean_direct_pdf_fixtures(self):
        seeds = load_seed_manifest(MANIFEST)

        self.assertEqual(len(seeds), 10)
        self.assertEqual(validate_seed_corpus(MANIFEST), [])
        self.assertTrue(all(seed.source_type == "direct_pdf" for seed in seeds))
        self.assertTrue(all(seed.storage_path.endswith(".pdf") for seed in seeds))

    def test_seed_metadata_schema_requires_lineage_and_pdf_fixture_columns(self):
        required = {
            "gpl_id",
            "provider_name",
            "city",
            "state",
            "source_url",
            "source_type",
            "retrieved_at",
            "effective_date",
            "content_sha256",
            "storage_path",
            "parse_status",
        }

        self.assertTrue(required.issubset(REQUIRED_GPL_METADATA_COLUMNS))
        sql = gpl_metadata_schema_sql()
        self.assertIn("CREATE TABLE IF NOT EXISTS gpl_seed_pdfs", sql)
        self.assertIn("source_type TEXT NOT NULL CHECK (source_type = 'direct_pdf')", sql)
        self.assertIn("content_sha256 TEXT NOT NULL", sql)
        self.assertIn("storage_path TEXT NOT NULL", sql)

    def test_seed_metadata_rejects_non_pdf_source_type(self):
        seed = GPLSeedPDF(
            gpl_id="fixture:bad",
            provider_name="Bad Fixture",
            city="Nowhere",
            state="NA",
            source_url="https://example.test/gpl.html",
            source_type="official_provider_page",
            retrieved_at="2026-06-07T00:00:00Z",
            effective_date="unknown",
            content_sha256="abc",
            storage_path="fixtures/funeral-price-pages/seed-gpls/bad.html",
            parse_status="pending",
        )

        errors = seed.validate_metadata()

        self.assertIn("source_type must be direct_pdf", errors)
        self.assertIn("storage_path must point to a PDF", errors)


if __name__ == "__main__":
    unittest.main()
