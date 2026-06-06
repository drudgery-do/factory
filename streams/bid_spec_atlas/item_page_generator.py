"""Static item page generator for Bid Spec Atlas."""

from __future__ import annotations

from html import escape
import re

from streams.bid_spec_atlas.pay_item_schema import PayItemRow


REQUIRED_FOOTER = (
    "Informational archive only. Cross-reference with official state DOT letting "
    "files before submitting bids."
)


def slug_for_item(item_code: str, description: str) -> str:
    text = f"{item_code}-{description}".lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def render_item_page(row: PayItemRow, source_url: str) -> str:
    title = f"{row.item_code} {row.description}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escape(title)}</title>
</head>
<body>
  <main>
    <h1>{escape(title)}</h1>
    <dl>
      <dt>State</dt><dd>{escape(row.state)}</dd>
      <dt>Letting date</dt><dd>{escape(row.letting_date)}</dd>
      <dt>Project</dt><dd>{escape(row.project_id)}</dd>
      <dt>Unit</dt><dd>{escape(row.unit)}</dd>
      <dt>Quantity</dt><dd>{row.quantity:g}</dd>
      <dt>Unit price</dt><dd>{row.unit_price:.2f}</dd>
      <dt>Total</dt><dd>{row.total:.2f}</dd>
    </dl>
    <p><a href="{escape(source_url)}">Official source file</a></p>
  </main>
  <footer>{escape(REQUIRED_FOOTER)}</footer>
</body>
</html>
"""
