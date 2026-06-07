"""Build the deterministic first-wave staging site."""

from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from streams.bid_spec_atlas.bid_tab_parser import parse_bid_tab_text
from streams.bid_spec_atlas.item_page_generator import render_item_page, slug_for_item
from streams.bid_spec_atlas.pay_item_schema import PayItemRow
from streams.ephemera_weaver.brief_generator import generate_research_brief
from streams.ephemera_weaver.indexer import create_sqlite_index
from streams.ephemera_weaver.search_api import LocalSearchAPI
from streams.ephemera_weaver.ui import render_local_ui
from streams.funeral_price_pages.extraction_run import GPLExtractionRun
from streams.funeral_price_pages.line_item_extractor import extract_line_items
from streams.funeral_price_pages.page_generator import (
    city_comparison_path,
    funeral_home_path,
    render_city_comparison_page,
    render_funeral_home_page,
)
from streams.funeral_price_pages.seed_import import GPLSeedPDF, load_seed_manifest


DEFAULT_OUTPUT_DIR = ROOT / "dist" / "staging"
DEFAULT_BASE_URL = "https://staging.example.test"


def build_staging_site(
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    base_url: str = DEFAULT_BASE_URL,
) -> dict[str, object]:
    if not base_url.startswith("https://"):
        raise ValueError("base_url must be an https URL")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    required_paths = [
        "index.html",
        *_build_ephemera(output_dir),
        *_build_bid_spec(output_dir, base_url),
        *_build_funeral_pages(output_dir),
    ]
    required_paths.append("sitemap.xml")

    _write_text(output_dir / "index.html", _render_home_page())
    _write_text(output_dir / "sitemap.xml", _render_sitemap(base_url, required_paths))

    manifest = {
        "status": "ready_for_staging_review",
        "base_url": base_url.rstrip("/"),
        "required_paths": sorted(set(required_paths)),
        "streams": {
            "ephemera-weaver": "static local-first UI and fixture research brief",
            "bid-spec-atlas": "fixture bid tab item pages and sitemap",
            "funeral-price-pages": "seed GPL funeral home and city comparison pages",
        },
        "non_actions": [
            "No production deploy performed.",
            "No production secrets added.",
            "No paid ads, affiliate, payment, provider outreach, or scraping expansion performed.",
        ],
    }
    _write_text(output_dir / "staging-manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def _build_ephemera(output_dir: Path) -> list[str]:
    stream_dir = output_dir / "ephemera-weaver"
    stream_dir.mkdir(parents=True)

    fixture_vault = ROOT / "fixtures" / "ephemera-vaults" / "research-notes"
    db_path = create_sqlite_index(fixture_vault, stream_dir / "ephemera.sqlite3")
    results = LocalSearchAPI(db_path).search("read-only source notes")["results"]
    brief = generate_research_brief(
        prompt="Draft a staging product note about local-first privacy.",
        retrieved_notes=results,
    )

    _write_text(stream_dir / "index.html", render_local_ui())
    _write_text(stream_dir / "research-brief.html", _render_markdown_page(str(brief["title"]), str(brief["markdown"])))
    _write_text(stream_dir / "research-brief.md", str(brief["markdown"]) + "\n")

    return [
        "ephemera-weaver/index.html",
        "ephemera-weaver/research-brief.html",
        "ephemera-weaver/research-brief.md",
    ]


def _build_bid_spec(output_dir: Path, base_url: str) -> list[str]:
    stream_dir = output_dir / "bid-spec-atlas"
    items_dir = stream_dir / "items"
    items_dir.mkdir(parents=True)

    fixture_path = ROOT / "fixtures" / "bid-spec-atlas" / "sample_bid_tab.txt"
    rows = [
        PayItemRow.from_parser_row(row)
        for row in parse_bid_tab_text(fixture_path.read_text(encoding="utf-8"), "fixture-bid-tab")
    ]
    item_paths = []
    links = []
    for row in rows:
        slug = slug_for_item(row.item_code, row.description)
        relative_path = f"bid-spec-atlas/items/{slug}.html"
        source_url = f"{base_url.rstrip('/')}/fixtures/bid-spec-atlas/sample_bid_tab.txt"
        _write_text(output_dir / relative_path, render_item_page(row, source_url))
        item_paths.append(relative_path)
        links.append(f'<li><a href="items/{html.escape(slug)}.html">{html.escape(row.item_code)} {html.escape(row.description)}</a></li>')

    _write_text(
        stream_dir / "index.html",
        _page(
            "Bid Spec Atlas",
            "<p>Fixture DOT bid-tab pages generated for staging smoke review.</p>"
            f"<ul>{''.join(links)}</ul>"
            '<p><a href="sitemap.xml">Stream sitemap</a></p>',
        ),
    )
    _write_text(stream_dir / "sitemap.xml", _render_sitemap(base_url, item_paths))

    return ["bid-spec-atlas/index.html", "bid-spec-atlas/sitemap.xml", *item_paths]


def _build_funeral_pages(output_dir: Path) -> list[str]:
    stream_dir = output_dir / "funeral-price-pages"
    stream_dir.mkdir(parents=True)

    seed = _legends_seed()
    run = GPLExtractionRun(
        run_id="legends-tri-county:fixture-extractor:2026-06-07",
        gpl_id=seed.gpl_id,
        source_sha256=seed.content_sha256,
        extractor_version="fixture-extractor",
        started_at="2026-06-07T00:00:00Z",
        completed_at="2026-06-07T00:00:01Z",
        status="completed",
        pages_total=1,
    )
    fixture_text = (
        ROOT / "fixtures" / "funeral-price-pages" / "extracted-text" / "legends_tri_county_2025_gpl.txt"
    ).read_text(encoding="utf-8")
    items = extract_line_items(fixture_text, run, extraction_date="2026-06-07")
    home_path = funeral_home_path(seed).strip("/") + "/index.html"
    comparison_path = city_comparison_path(seed.city, seed.state, "direct cremation").strip("/") + "/index.html"

    _write_text(output_dir / home_path, render_funeral_home_page(seed, items))
    _write_text(
        output_dir / comparison_path,
        render_city_comparison_page(
            city=seed.city,
            state=seed.state,
            service="direct cremation",
            provider_items=[(seed, item) for item in items],
        ),
    )
    _write_text(
        stream_dir / "index.html",
        _page(
            "Funeral Price Pages",
            "<p>Seed GPL pages generated for staging smoke review. Verify all prices with the provider.</p>"
            f'<ul><li><a href="/{html.escape(home_path)}">Funeral home page</a></li>'
            f'<li><a href="/{html.escape(comparison_path)}">City comparison page</a></li></ul>',
        ),
    )

    return [
        "funeral-price-pages/index.html",
        home_path,
        comparison_path,
    ]


def _legends_seed() -> GPLSeedPDF:
    for seed in load_seed_manifest(ROOT / "fixtures" / "funeral-price-pages" / "seed-gpls" / "manifest.json"):
        if seed.provider_name == "Legends Tri-County Funeral Services":
            return seed
    raise ValueError("Legends Tri-County Funeral Services seed fixture is missing")


def _render_home_page() -> str:
    links = [
        ("Ephemera Weaver", "ephemera-weaver/"),
        ("Bid Spec Atlas", "bid-spec-atlas/"),
        ("Funeral Price Pages", "funeral-price-pages/"),
    ]
    items = "".join(
        f'<li><a href="{html.escape(href)}">{html.escape(label)}</a></li>'
        for label, href in links
    )
    return _page(
        "First-Wave Staging",
        "<p>Static staging build for first-wave stream review.</p>"
        f"<ul>{items}</ul>"
        "<p>No production deploy, production secrets, paid ads, affiliate activation, or payment processing is included.</p>",
    )


def _render_markdown_page(title: str, markdown: str) -> str:
    escaped = html.escape(markdown)
    return _page(title, f"<pre>{escaped}</pre>")


def _render_sitemap(base_url: str, paths: list[str]) -> str:
    base = base_url.rstrip("/")
    entries = []
    for path in sorted(set(paths)):
        if path.endswith(".md") or path.endswith(".json"):
            continue
        entries.append(f"  <url><loc>{html.escape(base + '/' + path.strip('/'))}</loc></url>")
    return "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            *entries,
            "</urlset>",
            "",
        ]
    )


def _page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; max-width: 920px; line-height: 1.5; }}
    a {{ color: #064f8f; }}
    pre {{ white-space: pre-wrap; border: 1px solid #bbb; padding: 1rem; overflow-wrap: anywhere; }}
  </style>
</head>
<body>
  <main>
    <h1>{html.escape(title)}</h1>
    {body}
  </main>
</body>
</html>
"""


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = parser.parse_args()

    manifest = build_staging_site(output_dir=args.output_dir, base_url=args.base_url)
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
