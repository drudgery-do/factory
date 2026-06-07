import unittest

from streams.funeral_price_pages.line_item_extractor import GPLLineItem, VERIFY_WITH_PROVIDER_NOTICE
from streams.funeral_price_pages.publish_policy import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    decide_line_item_publication,
    partition_publishable_items,
)


def make_item(*, confidence: float, verify_notice: str = VERIFY_WITH_PROVIDER_NOTICE) -> GPLLineItem:
    return GPLLineItem(
        line_item_id=f"line-{confidence}",
        run_id="run-1",
        gpl_id="fpp-seed-001",
        source_sha256="abc",
        category="direct_cremation_package",
        description="Direct Cremation",
        price=995.0,
        confidence=confidence,
        extraction_date="2026-06-07",
        verify_notice=verify_notice,
    )


class FuneralPricePagesPublishPolicyTests(unittest.TestCase):
    def test_low_confidence_item_is_blocked_from_publication(self):
        decision = decide_line_item_publication(make_item(confidence=0.79))

        self.assertFalse(decision.can_publish)
        self.assertEqual(decision.publish_status, "blocked_low_confidence")
        self.assertEqual(decision.threshold, DEFAULT_CONFIDENCE_THRESHOLD)
        self.assertEqual(decision.reason, "confidence below publication threshold")

    def test_item_at_threshold_is_publishable(self):
        decision = decide_line_item_publication(make_item(confidence=0.8))

        self.assertTrue(decision.can_publish)
        self.assertEqual(decision.publish_status, "publishable")

    def test_missing_verify_notice_is_blocked_even_when_confidence_is_high(self):
        decision = decide_line_item_publication(make_item(confidence=0.95, verify_notice=""))

        self.assertFalse(decision.can_publish)
        self.assertEqual(decision.publish_status, "blocked_missing_notice")

    def test_partition_publishable_items_returns_only_green_items(self):
        low = make_item(confidence=0.6)
        high = make_item(confidence=0.9)

        publishable, blocked = partition_publishable_items([low, high])

        self.assertEqual(publishable, [high])
        self.assertEqual([decision.line_item_id for decision in blocked], [low.line_item_id])


if __name__ == "__main__":
    unittest.main()
