"""Line-item extraction for Funeral Price Pages GPL text."""

from __future__ import annotations

from dataclasses import dataclass
import re

from streams.funeral_price_pages.extraction_run import GPLExtractionRun


VERIFY_WITH_PROVIDER_NOTICE = "Verify all prices with the provider."

PRICE_RE = re.compile(r"(?P<description>.+?)\s+\$(?P<amount>[0-9][0-9,]*(?:\.[0-9]{2})?)\s*$")

CATEGORY_HEADINGS = {
    "PROFESSIONAL SERVICES",
    "EMBALMING",
    "OTHER PREPARATION OF REMAINS",
    "USE OF FACILITIES",
    "TRANSPORTATION",
    "DIRECT CREMATION PACKAGE",
    "IMMEDIATE BURIAL PACKAGE",
    "CASKETS",
    "OUTER BURIAL CONTAINERS",
    "URNS",
    "ADDITIONAL SERVICES AND MERCHANDISE",
}


@dataclass(frozen=True)
class GPLLineItem:
    line_item_id: str
    run_id: str
    gpl_id: str
    source_sha256: str
    category: str
    description: str
    price: float
    confidence: float
    extraction_date: str
    verify_notice: str = VERIFY_WITH_PROVIDER_NOTICE

    def validate(self) -> list[str]:
        errors: list[str] = []
        for field_name in (
            "line_item_id",
            "run_id",
            "gpl_id",
            "source_sha256",
            "category",
            "description",
            "extraction_date",
            "verify_notice",
        ):
            if not getattr(self, field_name):
                errors.append(f"{field_name} is required")

        if self.price < 0:
            errors.append("price cannot be negative")
        if not 0 <= self.confidence <= 1:
            errors.append("confidence must be between 0 and 1")
        if self.verify_notice != VERIFY_WITH_PROVIDER_NOTICE:
            errors.append("verify_notice must use the required notice")

        return errors


def normalize_description(value: str) -> str:
    return " ".join(value.strip(" .:-").split())


def confidence_for(category: str, description: str) -> float:
    score = 0.55
    if category != "uncategorized":
        score += 0.2
    if len(description.split()) >= 3:
        score += 0.15
    if any(term in description.lower() for term in ("cremation", "burial", "embalming", "visitation", "hearse")):
        score += 0.05
    return min(score, 0.95)


def extract_line_items(
    text: str,
    run: GPLExtractionRun,
    *,
    extraction_date: str,
) -> list[GPLLineItem]:
    items: list[GPLLineItem] = []
    category = "uncategorized"

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        upper_line = line.upper()
        if upper_line in CATEGORY_HEADINGS:
            category = upper_line.lower().replace(" ", "_")
            continue

        match = PRICE_RE.match(line)
        if not match:
            continue

        description = normalize_description(match.group("description"))
        amount = float(match.group("amount").replace(",", ""))
        confidence = confidence_for(category, description)
        line_number = len(items) + 1
        items.append(
            GPLLineItem(
                line_item_id=f"{run.run_id}:line:{line_number:04d}",
                run_id=run.run_id,
                gpl_id=run.gpl_id,
                source_sha256=run.source_sha256,
                category=category,
                description=description,
                price=amount,
                confidence=confidence,
                extraction_date=extraction_date,
            )
        )

    return items


def line_item_schema_sql() -> str:
    return """
CREATE TABLE IF NOT EXISTS gpl_line_items (
  line_item_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  gpl_id TEXT NOT NULL,
  source_sha256 TEXT NOT NULL,
  category TEXT NOT NULL,
  description TEXT NOT NULL,
  price REAL NOT NULL CHECK (price >= 0),
  confidence REAL NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  extraction_date TEXT NOT NULL,
  verify_notice TEXT NOT NULL,
  publish_status TEXT NOT NULL DEFAULT 'pending_confidence_review',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (run_id) REFERENCES gpl_extraction_runs (run_id),
  FOREIGN KEY (gpl_id) REFERENCES gpl_seed_pdfs (gpl_id)
);

CREATE INDEX IF NOT EXISTS idx_gpl_line_items_gpl_id
  ON gpl_line_items (gpl_id);

CREATE INDEX IF NOT EXISTS idx_gpl_line_items_publish_status
  ON gpl_line_items (publish_status);
""".strip()
