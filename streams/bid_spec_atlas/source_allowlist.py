"""DOT source allowlist for Bid Spec Atlas."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
import tomllib


DEFAULT_ALLOWLIST_PATH = (
    Path(__file__).resolve().parents[1] / "bid-spec-atlas" / "source_allowlist.toml"
)


@dataclass(frozen=True)
class SourceAllowlist:
    approved_sources: tuple[dict[str, str], ...]
    approval_required: bool
    notes: tuple[str, ...] = ()

    def is_url_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        for source in self.approved_sources:
            if parsed.netloc != source["host"]:
                continue
            if not url.startswith(source["url_prefix"]):
                continue
            return True
        return False


def load_source_allowlist(path: Path = DEFAULT_ALLOWLIST_PATH) -> SourceAllowlist:
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    return SourceAllowlist(
        approved_sources=tuple(payload.get("approved_sources", ())),
        approval_required=bool(payload.get("approval_required", True)),
        notes=tuple(payload.get("notes", ())),
    )
