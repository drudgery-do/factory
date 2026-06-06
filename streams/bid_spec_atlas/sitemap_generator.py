"""Sitemap generator for Bid Spec Atlas."""

from __future__ import annotations

from html import escape


def generate_sitemap_xml(base_url: str, slugs: tuple[str, ...]) -> str:
    if not base_url:
        raise ValueError("base_url is required")

    base = base_url.rstrip("/")
    urls = "\n".join(
        "  <url><loc>"
        f"{escape(base)}/items/{escape(slug)}.html"
        "</loc></url>"
        for slug in slugs
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )
