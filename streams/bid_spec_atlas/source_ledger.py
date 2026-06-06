"""Source ledger schema for Bid Spec Atlas."""

from __future__ import annotations

from dataclasses import dataclass


# BSA-002 must replace this placeholder only after DOT source approval.
APPROVED_SOURCE_CLASSES = ("approval-gate",)

PARSE_STATUSES = ("pending", "parsed", "failed", "review_required")

REQUIRED_LEDGER_COLUMNS = (
    "source_file_id",
    "source_url",
    "source_class",
    "retrieved_at",
    "content_sha256",
    "storage_path",
    "parse_status",
)


@dataclass(frozen=True)
class SourceLedgerEntry:
    source_file_id: str
    source_url: str
    source_class: str
    retrieved_at: str
    content_sha256: str
    storage_path: str
    parse_status: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        for field_name in REQUIRED_LEDGER_COLUMNS:
            value = getattr(self, field_name)
            if not value:
                errors.append(f"{field_name} is required")

        if self.source_class not in APPROVED_SOURCE_CLASSES:
            errors.append("source_class requires approval")
        if self.parse_status not in PARSE_STATUSES:
            errors.append("parse_status is invalid")

        return errors


def source_ledger_schema_sql() -> str:
    return """
CREATE TABLE IF NOT EXISTS source_files (
  source_file_id TEXT PRIMARY KEY,
  source_url TEXT NOT NULL,
  source_class TEXT NOT NULL,
  retrieved_at TEXT NOT NULL,
  content_sha256 TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  parse_status TEXT NOT NULL CHECK (parse_status IN ('pending', 'parsed', 'failed', 'review_required')),
  review_issue_url TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_source_files_source_class
  ON source_files (source_class);

CREATE INDEX IF NOT EXISTS idx_source_files_parse_status
  ON source_files (parse_status);
""".strip()
