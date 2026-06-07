"""Correction request workflow for Funeral Price Pages."""

from __future__ import annotations

from dataclasses import dataclass


CORRECTION_STATUSES = ("review_required", "accepted", "rejected", "duplicate")


@dataclass(frozen=True)
class CorrectionRequest:
    request_id: str
    provider_name: str
    source_url: str
    submitted_by: str
    message: str
    created_at: str
    status: str = "review_required"

    def validate(self) -> list[str]:
        errors: list[str] = []
        for field_name in ("request_id", "provider_name", "source_url", "submitted_by", "message", "created_at"):
            if not getattr(self, field_name):
                errors.append(f"{field_name} is required")
        if self.status not in CORRECTION_STATUSES:
            errors.append("status is invalid")
        if not self.source_url.startswith("https://"):
            errors.append("source_url must be https")
        return errors

    def review_issue_title(self) -> str:
        return f"FPP correction review: {self.provider_name}"

    def review_issue_body(self) -> str:
        return (
            f"Provider: {self.provider_name}\n"
            f"Source URL: {self.source_url}\n"
            f"Submitted by: {self.submitted_by}\n"
            f"Created at: {self.created_at}\n\n"
            f"{self.message}\n"
        )


def correction_request_schema_sql() -> str:
    return """
CREATE TABLE IF NOT EXISTS correction_requests (
  request_id TEXT PRIMARY KEY,
  provider_name TEXT NOT NULL,
  source_url TEXT NOT NULL,
  submitted_by TEXT NOT NULL,
  message TEXT NOT NULL,
  created_at TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('review_required', 'accepted', 'rejected', 'duplicate')),
  review_issue_url TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_correction_requests_status
  ON correction_requests (status);
""".strip()

