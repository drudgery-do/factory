# Approval Card

Task: FPP-001
Stream: funeral-price-pages
Requested by: orchestrator
Risk classification: red
Decision owner: Human Owner or Delegate

## Decision

- Approve
- Reject
- Request changes

## Why Approval Is Needed

Matched rules: first_gpl
Required approver roles: human_owner, delegate

FPP-001 requires the first 10 seed GPL approvals before any seed import folder,
metadata schema tied to real PDFs, crawler work, or extraction work proceeds.

## What To Approve

Approve exactly one seed list containing 10 public funeral home General Price
List sources. Each source must be a direct PDF URL or an official provider page
that links to a GPL PDF.

For each of the 10 seed GPLs, approval must include:

- provider name
- city and state
- source URL
- source type: direct PDF or official provider page
- access check: public, no login, no payment wall
- terms/robots check: no known restriction blocking archive/extraction review
- approval owner
- approval date
- approval decision: approved or rejected

Do not approve a source if any of these are unclear:

- whether the source is the provider's official public GPL
- whether the source can be accessed without login or payment
- whether site terms or robots instructions prohibit the planned access
- whether the provider/location is identifiable

## Approval Table

| # | Provider name | City, state | Source URL | Source type | Public access check | Terms/robots check | Approval owner | Approval date | Decision |
|---|---|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |  |  |

## Copy-Paste Approval Statement

Approved for FPP-001: use the 10 GPL sources listed above as the seed set for
local import-folder and metadata-schema work. This approval covers local source
download/storage for the seed set, metadata indexing, extraction fixture work,
and staging-only verification. It does not approve production deploy, domain
selection, ad/affiliate applications, broad scraping, or outreach to providers.

## Evidence Pack

- PR: PR that adds the completed approval table.
- Tests: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Quality gate output: `python3 orchestrator/scripts/run_quality_gate.py`
- Artifacts: completed approval table with 10 approved GPL source URLs.
- Rollback plan: revert the approval-table PR and keep `FPP-001` blocked.

## Explicit Non-Actions

- No seed GPLs imported.
- No production secrets added.
- No production deploy executed.
- No payment, ad, affiliate, KYC, or domain action executed.
