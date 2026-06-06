# Bid Spec Atlas Spec

## V0 Scope

- one or two state DOT sources
- allowlisted crawler for official bid tab/download pages
- source-file storage
- extraction runs table
- source ledger
- pay item parser
- PostgreSQL schema
- item-level pages
- state/location pages
- generated sitemap
- stale-source detector
- parser golden tests
- staging deploy

## Source Ledger Schema

- Source ledger implementation: `streams/bid_spec_atlas/source_ledger.py`
- Source classes remain approval-gated until BSA-002 chooses allowed DOT sources.

## DOT Source Allowlist

- Allowlist config: `streams/bid-spec-atlas/source_allowlist.toml`
- Allowlist loader: `streams/bid_spec_atlas/source_allowlist.py`
- Approved external DOT sources remain empty until source terms and robots are reviewed.

## Fixture Bid-Tab Parser

- Fixture input: `fixtures/bid-spec-atlas/sample_bid_tab.txt`
- Golden output: `fixtures/bid-spec-atlas/sample_bid_tab.golden.json`
- Parser: `streams/bid_spec_atlas/bid_tab_parser.py`

## Pay Item Schema

- Pay item schema implementation: `streams/bid_spec_atlas/pay_item_schema.py`
- Every pay item row requires `source_file_id`.

## Item Page Generator

- Item page generator: `streams/bid_spec_atlas/item_page_generator.py`
- Every generated item page must link to the source file and include the required footer disclaimer.

## Sitemap Generator

- Sitemap generator: `streams/bid_spec_atlas/sitemap_generator.py`

## Explicitly Not V0

- paid API
- nationwide coverage
- contractor bidding advice
- bid recommendation engine
- account system
- marketplace
- private customer data

## Done For V0

- at least 500 indexed pay-item rows
- at least 100 generated SEO pages
- source URLs stored for all rows
- parser has golden tests
- source ledger coverage is 100%
- sitemap builds cleanly
- staging deploy passes link check
- disclaimer appears on every public page

## TODOs

- TODO: choose first one or two approved DOT sources.
- TODO: choose DOT source class values during BSA-002 approval work.
- TODO: choose staging host only after deploy approval.
