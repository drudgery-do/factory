"""Seed GPL PDF import metadata for Funeral Price Pages."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST = Path("fixtures/funeral-price-pages/seed-gpls/manifest.json")

REQUIRED_GPL_METADATA_COLUMNS = (
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
)

PARSE_STATUSES = ("pending", "parsed", "failed", "review_required")


@dataclass(frozen=True)
class GPLSeedPDF:
    gpl_id: str
    provider_name: str
    city: str
    state: str
    source_url: str
    source_type: str
    retrieved_at: str
    effective_date: str
    content_sha256: str
    storage_path: str
    parse_status: str = "pending"

    @classmethod
    def from_manifest_row(cls, row: dict[str, Any]) -> "GPLSeedPDF":
        return cls(
            gpl_id=str(row["gpl_id"]),
            provider_name=str(row["provider_name"]),
            city=str(row["city"]),
            state=str(row["state"]),
            source_url=str(row["source_url"]),
            source_type=str(row["source_type"]),
            retrieved_at=str(row["retrieved_at"]),
            effective_date=str(row["effective_date"]),
            content_sha256=str(row["content_sha256"]),
            storage_path=str(row["storage_path"]),
            parse_status=str(row.get("parse_status", "pending")),
        )

    def validate_metadata(self) -> list[str]:
        errors: list[str] = []
        for field_name in REQUIRED_GPL_METADATA_COLUMNS:
            value = getattr(self, field_name)
            if not value:
                errors.append(f"{field_name} is required")

        if self.source_type != "direct_pdf":
            errors.append("source_type must be direct_pdf")
        if self.parse_status not in PARSE_STATUSES:
            errors.append("parse_status is invalid")
        if not self.source_url.lower().startswith("https://"):
            errors.append("source_url must be https")
        if not self.storage_path.lower().endswith(".pdf"):
            errors.append("storage_path must point to a PDF")

        return errors


def compute_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_pdf(path: Path) -> bool:
    with path.open("rb") as handle:
        return handle.read(5) == b"%PDF-"


def load_seed_manifest(path: Path = DEFAULT_MANIFEST) -> list[GPLSeedPDF]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [GPLSeedPDF.from_manifest_row(row) for row in payload["seeds"]]


def validate_seed_corpus(
    manifest_path: Path = DEFAULT_MANIFEST,
    repo_root: Path = Path("."),
) -> list[str]:
    errors: list[str] = []
    seeds = load_seed_manifest(manifest_path)

    if len(seeds) != 10:
        errors.append("seed corpus must contain exactly 10 GPL PDFs")

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for seed in seeds:
        errors.extend(f"{seed.gpl_id}: {error}" for error in seed.validate_metadata())

        if seed.gpl_id in seen_ids:
            errors.append(f"{seed.gpl_id}: duplicate gpl_id")
        seen_ids.add(seed.gpl_id)

        if seed.storage_path in seen_paths:
            errors.append(f"{seed.gpl_id}: duplicate storage_path")
        seen_paths.add(seed.storage_path)

        pdf_path = repo_root / seed.storage_path
        if not pdf_path.exists():
            errors.append(f"{seed.gpl_id}: fixture PDF is missing")
            continue
        if not is_pdf(pdf_path):
            errors.append(f"{seed.gpl_id}: fixture does not start with %PDF-")
        actual_sha = compute_sha256(pdf_path)
        if actual_sha != seed.content_sha256:
            errors.append(f"{seed.gpl_id}: content_sha256 mismatch")

    return errors


def gpl_metadata_schema_sql() -> str:
    return """
CREATE TABLE IF NOT EXISTS gpl_seed_pdfs (
  gpl_id TEXT PRIMARY KEY,
  provider_name TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  source_url TEXT NOT NULL,
  source_type TEXT NOT NULL CHECK (source_type = 'direct_pdf'),
  retrieved_at TEXT NOT NULL,
  effective_date TEXT NOT NULL,
  content_sha256 TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  parse_status TEXT NOT NULL CHECK (parse_status IN ('pending', 'parsed', 'failed', 'review_required')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_gpl_seed_pdfs_state
  ON gpl_seed_pdfs (state);

CREATE INDEX IF NOT EXISTS idx_gpl_seed_pdfs_parse_status
  ON gpl_seed_pdfs (parse_status);
""".strip()

