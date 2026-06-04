# First Wave Brief

This file is the source of truth. Agents must not infer product strategy from names alone. Missing context becomes a TODO or approval gate, not invented scope.

## Stream 1 — Local-First Cross-App Ephemera Weaver

Plain-English product:
A local AI tool for people with too many Markdown/Obsidian notes. It indexes local folders and turns forgotten fragments into useful outputs: article outlines, research briefs, argument maps, project plans, contradiction checks, and “you already wrote this before” reminders.

Positioning:
Local AI that finds useful forgotten notes in your Obsidian/Markdown vault and turns them into briefs, outlines, and draft material without uploading your files.

Primary buyer:
Independent researchers, authors, academics, consultants, technical writers, and serious note-takers.

V0 scope:
- local app or local web app
- folder picker
- Markdown folder support
- Obsidian vault support
- local SQLite index
- local search
- prompt box where user pastes current draft/project
- generated research brief
- generated outline
- generated contradiction map
- export generated output as separate Markdown
- license-key check in test mode
- direct-download landing page
- docs
- regression tests

Explicitly not v0:
- mobile app
- team collaboration
- cloud sync
- browser extension
- every-app connector layer
- Zotero connector
- marketplace
- automatic writeback into vault
- deletion or modification of source notes

Non-negotiables:
- read-only by default
- no automatic writeback
- no hidden cloud upload
- no deletion
- generated outputs saved to a separate folder
- no source note may be modified during indexing or generation

Revenue model:
Paid license / direct download.

Red gates:
- any feature that writes to user files
- any feature that uploads user data
- security-sensitive bug
- privacy/license/terms changes
- pricing changes
- refund exceptions
- public incident response

Done for v0:
- fixture vault indexes successfully
- source-file hash test proves no input files changed
- brief generation works on at least 5 fixture vaults
- output exports to separate Markdown file
- docs clearly explain read-only behavior
- license check works in test mode
- install path works on clean machine

---

## Stream 2 — Bid Spec Atlas

Plain-English product:
A public-data/programmatic SEO site that ingests state DOT bid tabulations, extracts pay items and historical bid prices, stores them in a structured database, and generates item/state/location pages.

Positioning:
Historical DOT bid-price archive for researching pay items and prior letting results. Informational only.

Primary users:
Civil contractors, estimators, suppliers, construction researchers, and people searching state DOT bid item history.

V0 scope:
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

Explicitly not v0:
- paid API
- nationwide coverage
- contractor bidding advice
- bid recommendation engine
- account system
- marketplace
- private customer data

Non-negotiables:
- every extracted row requires source_file_id
- every generated fact links back to source file
- failed parse creates a review issue, not fake data
- no bidding advice
- footer on every page:
  “Informational archive only. Cross-reference with official state DOT letting files before submitting bids.”

Revenue model:
Display ads later, data licensing later. No monetization gate in v0.

Red gates:
- ad network application
- data marketplace application
- source class expansion where terms/robots are unclear
- legal/reputation complaint
- removing or changing the disclaimer

Done for v0:
- at least 500 indexed pay-item rows
- at least 100 generated SEO pages
- source URLs stored for all rows
- parser has golden tests
- source ledger coverage is 100%
- sitemap builds cleanly
- staging deploy passes link check
- disclaimer appears on every public page

---

## Stream 3 — Funeral Price Pages

Plain-English product:
A public-data/programmatic SEO site that ingests public funeral home General Price List PDFs, extracts structured service and casket/cremation line items, and generates local comparison pages with schema.org markup.

Positioning:
Automatically extracted public funeral price-list archive. Verify all prices with the provider.

Primary users:
Families comparing funeral costs, researchers, and local search traffic.

V0 scope:
- seed import folder for 10 approved GPL PDFs
- GPL PDF metadata table
- extraction runs table
- line-item extraction
- confidence scoring
- low-confidence blocking
- funeral home pages
- city/service comparison pages
- schema.org LocalBusiness markup
- extraction timestamp
- correction form
- sitemap
- staging deploy

Explicitly not v0:
- lead resale
- call center
- funeral planning advice
- provider dashboard
- nationwide scraping
- paid customer accounts
- automated outreach to funeral homes

Non-negotiables:
- every price line has extraction date
- every price line says verify with provider
- low-confidence extracted data does not publish
- provider corrections create review issues
- no funeral planning advice
- no invented prices
- no price line without source file

Revenue model:
Display ads later, affiliate/lead testing later only after human approval.

Red gates:
- first 10 seed GPL approvals
- domain choice
- ad/affiliate applications
- provider disputes
- legal/reputation complaint
- broad scraper expansion

Done for v0:
- 10 seed GPLs imported
- 90%+ extraction accuracy on seed set
- low-confidence rows blocked
- 50 local pages generated
- correction form works
- every price line has timestamp and verify-with-provider notice
- sitemap validates
- schema.org markup validates
- staging deploy passes link check

---

# Deploy Review Policy

No builder may approve or deploy its own work.

Roles:
- Builder Agent: implements tasks and opens PRs.
- QA Agent: reviews PRs, runs tests, verifies evidence packs.
- Release Reviewer Agent: approves green/yellow deploys if all gates pass.
- OpenClaw Operator: runs deploy workflow, monitors canary, rolls back on failure, sends digest.
- Human Owner or Delegate: only handles red-gate approvals.

Green deploys:
- docs
- copy
- parser bugfix with passing golden tests
- sitemap regeneration
- non-destructive schema addition
- UI change with no policy/payment/security impact

Yellow deploys:
- new parser for existing approved source class
- new background job
- non-destructive migration
- page template change
- license server bugfix
- confidence threshold tuning

Red deploys:
- payments/KYC
- domain purchase/transfer
- ad network/affiliate application
- privacy policy/terms/disclaimer change
- auth/permissions/secrets change
- cloud upload feature
- user-file writeback feature
- deletion/modification of user files
- provider dispute response
- legal threat response
- security incident response
- first GPL seed approval
