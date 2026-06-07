"""Extraction run schema for Funeral Price Pages GPL processing."""

from __future__ import annotations

from dataclasses import dataclass

from streams.funeral_price_pages.seed_import import GPLSeedPDF


RUN_STATUSES = ("pending", "running", "completed", "failed", "review_required")

REQUIRED_EXTRACTION_RUN_COLUMNS = (
    "run_id",
    "gpl_id",
    "source_sha256",
    "extractor_version",
    "started_at",
    "status",
)


@dataclass(frozen=True)
class GPLExtractionRun:
    run_id: str
    gpl_id: str
    source_sha256: str
    extractor_version: str
    started_at: str
    status: str
    completed_at: str = ""
    pages_total: int = 0
    line_items_extracted: int = 0
    low_confidence_count: int = 0
    error_message: str = ""

    @classmethod
    def pending_for_seed(
        cls,
        seed: GPLSeedPDF,
        *,
        started_at: str,
        extractor_version: str,
    ) -> "GPLExtractionRun":
        return cls(
            run_id=f"{seed.gpl_id}:{extractor_version}:{started_at}",
            gpl_id=seed.gpl_id,
            source_sha256=seed.content_sha256,
            extractor_version=extractor_version,
            started_at=started_at,
            status="pending",
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        for field_name in REQUIRED_EXTRACTION_RUN_COLUMNS:
            value = getattr(self, field_name)
            if not value:
                errors.append(f"{field_name} is required")

        if self.status not in RUN_STATUSES:
            errors.append("status is invalid")
        if self.pages_total < 0:
            errors.append("pages_total cannot be negative")
        if self.line_items_extracted < 0:
            errors.append("line_items_extracted cannot be negative")
        if self.low_confidence_count < 0:
            errors.append("low_confidence_count cannot be negative")
        if self.low_confidence_count > self.line_items_extracted:
            errors.append("low_confidence_count cannot exceed line_items_extracted")
        if self.status == "completed" and not self.completed_at:
            errors.append("completed_at is required for completed runs")
        if self.status == "failed" and not self.error_message:
            errors.append("error_message is required for failed runs")

        return errors


def extraction_run_schema_sql() -> str:
    return """
CREATE TABLE IF NOT EXISTS gpl_extraction_runs (
  run_id TEXT PRIMARY KEY,
  gpl_id TEXT NOT NULL,
  source_sha256 TEXT NOT NULL,
  extractor_version TEXT NOT NULL,
  started_at TEXT NOT NULL,
  completed_at TEXT,
  status TEXT NOT NULL CHECK (status IN ('pending', 'running', 'completed', 'failed', 'review_required')),
  pages_total INTEGER NOT NULL DEFAULT 0,
  line_items_extracted INTEGER NOT NULL DEFAULT 0,
  low_confidence_count INTEGER NOT NULL DEFAULT 0,
  error_message TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (gpl_id) REFERENCES gpl_seed_pdfs (gpl_id),
  CHECK (pages_total >= 0),
  CHECK (line_items_extracted >= 0),
  CHECK (low_confidence_count >= 0),
  CHECK (low_confidence_count <= line_items_extracted)
);

CREATE INDEX IF NOT EXISTS idx_gpl_extraction_runs_gpl_id
  ON gpl_extraction_runs (gpl_id);

CREATE INDEX IF NOT EXISTS idx_gpl_extraction_runs_status
  ON gpl_extraction_runs (status);
""".strip()
