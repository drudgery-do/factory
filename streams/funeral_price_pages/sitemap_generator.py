"""Sitemap generation for Funeral Price Pages."""

from __future__ import annotations

from xml.sax.saxutils import escape


def generate_sitemap_xml(base_url: str, paths: list[str]) -> str:
    if not base_url.startswith("https://"):
        raise ValueError("base_url must be an https URL")

    normalized_base = base_url.rstrip("/")
    url_entries = []
    for path in paths:
        normalized_path = "/" + path.strip("/")
        url_entries.append(f"  <url><loc>{escape(normalized_base + normalized_path)}</loc></url>")

    return "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            *url_entries,
            "</urlset>",
        ]
    )

