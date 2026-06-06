import unittest

from streams.bid_spec_atlas.source_ledger import (
    APPROVED_SOURCE_CLASSES,
    REQUIRED_LEDGER_COLUMNS,
    SourceLedgerEntry,
    source_ledger_schema_sql,
)


class BidSpecSourceLedgerTests(unittest.TestCase):
    def test_source_ledger_schema_includes_required_lineage_columns(self):
        required = {
            "source_file_id",
            "source_url",
            "source_class",
            "retrieved_at",
            "content_sha256",
            "storage_path",
            "parse_status",
        }

        self.assertTrue(required.issubset(REQUIRED_LEDGER_COLUMNS))
        sql = source_ledger_schema_sql()
        self.assertIn("CREATE TABLE IF NOT EXISTS source_files", sql)
        self.assertIn("source_file_id TEXT PRIMARY KEY", sql)
        self.assertIn("content_sha256 TEXT NOT NULL", sql)
        self.assertIn("CHECK (parse_status IN", sql)

    def test_source_ledger_entry_requires_source_lineage(self):
        entry = SourceLedgerEntry(
            source_file_id="sha256:abc",
            source_url="https://example.test/bid-tabs.pdf",
            source_class="approval-gate",
            retrieved_at="2026-06-06T00:00:00Z",
            content_sha256="abc",
            storage_path="sources/abc.pdf",
            parse_status="pending",
        )

        self.assertEqual(entry.validate(), [])

        missing_url = SourceLedgerEntry(
            source_file_id="sha256:abc",
            source_url="",
            source_class="approval-gate",
            retrieved_at="2026-06-06T00:00:00Z",
            content_sha256="abc",
            storage_path="sources/abc.pdf",
            parse_status="pending",
        )

        self.assertIn("source_url is required", missing_url.validate())

    def test_source_classes_remain_approval_gated_until_dot_sources_chosen(self):
        self.assertEqual(APPROVED_SOURCE_CLASSES, ("approval-gate",))


if __name__ == "__main__":
    unittest.main()
