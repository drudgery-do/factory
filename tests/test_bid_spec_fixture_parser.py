import json
from pathlib import Path
import unittest

from streams.bid_spec_atlas.bid_tab_parser import parse_bid_tab_text


FIXTURE = Path("fixtures/bid-spec-atlas/sample_bid_tab.txt")
GOLDEN = Path("fixtures/bid-spec-atlas/sample_bid_tab.golden.json")


class BidSpecFixtureParserTests(unittest.TestCase):
    def test_parse_fixture_bid_tab_matches_golden_rows(self):
        rows = parse_bid_tab_text(
            FIXTURE.read_text(encoding="utf-8"),
            source_file_id="fixture:sample_bid_tab",
        )
        expected = json.loads(GOLDEN.read_text(encoding="utf-8"))

        self.assertEqual(rows, expected)
        self.assertTrue(all(row["source_file_id"] for row in rows))


if __name__ == "__main__":
    unittest.main()
