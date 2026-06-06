import unittest

from streams.bid_spec_atlas.bid_tab_parser import parse_bid_tab_text
from streams.bid_spec_atlas.pay_item_schema import (
    REQUIRED_PAY_ITEM_COLUMNS,
    PayItemRow,
    pay_item_schema_sql,
)


class BidSpecPayItemSchemaTests(unittest.TestCase):
    def test_pay_item_schema_requires_lineage_and_price_columns(self):
        required = {
            "pay_item_id",
            "source_file_id",
            "item_code",
            "description",
            "unit",
            "quantity",
            "unit_price",
            "total",
        }

        self.assertTrue(required.issubset(REQUIRED_PAY_ITEM_COLUMNS))
        sql = pay_item_schema_sql()
        self.assertIn("CREATE TABLE IF NOT EXISTS pay_items", sql)
        self.assertIn("source_file_id TEXT NOT NULL", sql)
        self.assertIn("FOREIGN KEY (source_file_id)", sql)

    def test_pay_item_row_validation_rejects_missing_source_file_id(self):
        row = PayItemRow(
            pay_item_id="fixture:sample_bid_tab:201-0001",
            source_file_id="",
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

        self.assertIn("source_file_id is required", row.validate())

    def test_fixture_parser_rows_can_be_promoted_to_pay_item_rows(self):
        text = (
            "Letting: 2026-04-15\n"
            "State: Fixture DOT\n"
            "Project: BR-2026-001\n\n"
            "ITEM CODE | DESCRIPTION | UNIT | QUANTITY | BIDDER | UNIT PRICE | TOTAL\n"
            "201-0001 | CLEARING AND GRUBBING | ACRE | 2.5 | North Road Builders | 1200.00 | 3000.00\n"
        )

        parsed = parse_bid_tab_text(text, source_file_id="fixture:sample_bid_tab")
        row = PayItemRow.from_parser_row(parsed[0])

        self.assertEqual(row.validate(), [])
        self.assertEqual(row.pay_item_id, "fixture:sample_bid_tab:201-0001")


if __name__ == "__main__":
    unittest.main()
