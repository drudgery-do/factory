"""Publication policy for extracted GPL line items."""

from __future__ import annotations

from dataclasses import dataclass

from streams.funeral_price_pages.line_item_extractor import GPLLineItem


DEFAULT_CONFIDENCE_THRESHOLD = 0.8

PUBLISH_STATUSES = ("publishable", "blocked_low_confidence", "blocked_missing_notice")


@dataclass(frozen=True)
class PublishDecision:
    line_item_id: str
    publish_status: str
    confidence: float
    threshold: float
    reason: str

    @property
    def can_publish(self) -> bool:
        return self.publish_status == "publishable"


def decide_line_item_publication(
    item: GPLLineItem,
    *,
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> PublishDecision:
    if not item.verify_notice:
        return PublishDecision(
            line_item_id=item.line_item_id,
            publish_status="blocked_missing_notice",
            confidence=item.confidence,
            threshold=threshold,
            reason="verify notice is required before publication",
        )

    if item.confidence < threshold:
        return PublishDecision(
            line_item_id=item.line_item_id,
            publish_status="blocked_low_confidence",
            confidence=item.confidence,
            threshold=threshold,
            reason="confidence below publication threshold",
        )

    return PublishDecision(
        line_item_id=item.line_item_id,
        publish_status="publishable",
        confidence=item.confidence,
        threshold=threshold,
        reason="confidence meets publication threshold",
    )


def partition_publishable_items(
    items: list[GPLLineItem],
    *,
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> tuple[list[GPLLineItem], list[PublishDecision]]:
    publishable: list[GPLLineItem] = []
    blocked: list[PublishDecision] = []

    for item in items:
        decision = decide_line_item_publication(item, threshold=threshold)
        if decision.can_publish:
            publishable.append(item)
        else:
            blocked.append(decision)

    return publishable, blocked
