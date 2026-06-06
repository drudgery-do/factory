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
- TODO: define source ledger schema details before BSA-001.
- TODO: choose staging host only after deploy approval.
