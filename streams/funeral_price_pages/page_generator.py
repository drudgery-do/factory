"""Static page generation for Funeral Price Pages."""

from __future__ import annotations

import html
import json
import re

from streams.funeral_price_pages.line_item_extractor import GPLLineItem
from streams.funeral_price_pages.publish_policy import partition_publishable_items
from streams.funeral_price_pages.seed_import import GPLSeedPDF


REQUIRED_PRICE_NOTICE = "Verify all prices with the provider."


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "page"


def funeral_home_path(seed: GPLSeedPDF) -> str:
    return f"/funeral-homes/{seed.state.lower()}/{slugify(seed.city)}/{slugify(seed.provider_name)}/"


def city_comparison_path(city: str, state: str, service: str) -> str:
    return f"/funeral-prices/{state.lower()}/{slugify(city)}/{slugify(service)}/"


def render_price_rows(items: list[GPLLineItem]) -> str:
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{html.escape(item.description)}</td>"
            f"<td>${item.price:,.2f}</td>"
            f"<td>{html.escape(item.extraction_date)}</td>"
            f"<td>{html.escape(item.verify_notice)}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def local_business_schema(seed: GPLSeedPDF) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": seed.provider_name,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": seed.city,
            "addressRegion": seed.state,
            "addressCountry": "US",
        },
        "url": seed.source_url,
    }
    return json.dumps(payload, sort_keys=True)


def render_funeral_home_page(seed: GPLSeedPDF, items: list[GPLLineItem]) -> str:
    publishable, blocked = partition_publishable_items(items)
    source_url = html.escape(seed.source_url, quote=True)
    page_title = html.escape(f"{seed.provider_name} funeral prices")
    rows = render_price_rows(publishable)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{page_title}</title>
  <script type="application/ld+json">{local_business_schema(seed)}</script>
</head>
<body>
  <main>
    <h1>{html.escape(seed.provider_name)}</h1>
    <p>{html.escape(seed.city)}, {html.escape(seed.state)}</p>
    <p>Automatically extracted public funeral price-list archive. Verify all prices with the provider.</p>
    <p>Source: <a href="{source_url}">{source_url}</a></p>
    <table>
      <thead>
        <tr><th>Service</th><th>Price</th><th>Extracted</th><th>Notice</th></tr>
      </thead>
      <tbody>
{rows}
      </tbody>
    </table>
    <p>{len(blocked)} low-confidence rows blocked from publication.</p>
  </main>
</body>
</html>"""


def render_city_comparison_page(
    *,
    city: str,
    state: str,
    service: str,
    provider_items: list[tuple[GPLSeedPDF, GPLLineItem]],
) -> str:
    rows = []
    for seed, item in provider_items:
        publishable, _blocked = partition_publishable_items([item])
        if not publishable:
            continue
        rows.append(
            "<tr>"
            f"<td>{html.escape(seed.provider_name)}</td>"
            f"<td>{html.escape(item.description)}</td>"
            f"<td>${item.price:,.2f}</td>"
            f"<td>{html.escape(item.extraction_date)}</td>"
            f"<td>{html.escape(item.verify_notice)}</td>"
            f"<td><a href=\"{html.escape(seed.source_url, quote=True)}\">Source GPL</a></td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(city)} {html.escape(service)} comparison</title>
</head>
<body>
  <main>
    <h1>{html.escape(city)}, {html.escape(state)} {html.escape(service)} prices</h1>
    <p>Automatically extracted public funeral price-list archive. Verify all prices with the provider.</p>
    <table>
      <thead>
        <tr><th>Provider</th><th>Service</th><th>Price</th><th>Extracted</th><th>Notice</th><th>Source</th></tr>
      </thead>
      <tbody>
{chr(10).join(rows)}
      </tbody>
    </table>
  </main>
</body>
</html>"""

