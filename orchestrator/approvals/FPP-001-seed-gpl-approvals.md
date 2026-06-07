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

FPP-001 requires the first 10 clean seed GPL PDF approvals before any seed
import folder, metadata schema tied to real PDFs, crawler work, or extraction
work proceeds.

## What To Approve

Approve whether a final list of 10 direct GPL PDF sources is acceptable as the
seed corpus for local import and extraction development. This is a
source-suitability approval, not a price, legal, medical, financial, or
consumer-advice certification.

The table below is not the approved seed corpus. It is a Codex-assessed source
discovery shortlist. It contains useful public GPL/price-list candidates, but
some entries are official HTML pages or browser-readable sources rather than
clean direct PDF fixtures. FPP-001 remains blocked until this shortlist is
converted into, or replaced by, 10 clean direct PDF fixture sources.

Approval means:

- the listed final direct PDF sources are acceptable inputs for FPP-001 local seed import work
- the builder may download/store local PDF copies for test fixtures and metadata
- the builder may write extraction code against these seed sources
- extracted facts must still cite the source file and carry the verify-with-provider notice

Approval does not mean:

- the approver certifies that any price is current or accurate
- the approver endorses any provider
- the approver approves publication of extracted prices
- the approver approves production deploy, domain choice, ads, affiliates, outreach, or scraping expansion

The approver should reject or request changes if the seed list is not a
reasonable starting corpus, if a listed source does not look like an official
public GPL source, or if a listed source creates legal/reputation discomfort.

## Codex Assessment Scope

Codex can and should assess the objective source checks before this reaches a
human owner. For this seed list, Codex assessed:

- whether the provider/source name matches the linked URL well enough to be plausible
- whether the URL is publicly reachable through normal browser or HTTP access
- whether the page/PDF identifies itself as a General Price List, GPL, or funeral price list
- whether provider location is identifiable from the source page or linked official provider context
- whether robots.txt showed an obvious block for the listed GPL/price-list source path
- whether command-line access has an implementation constraint, such as a Cloudflare challenge

Codex did not assess, and cannot approve on behalf of the owner:

- whether the final PDF source list is strategically acceptable for the business
- whether the listed providers should be included in the first seed corpus
- whether any extracted prices are accurate, current, or suitable for publication
- whether production crawling, publication, outreach, ads, affiliates, or deployment should happen

## How To Review The Remaining Approval

Codex has already checked the mechanical source-suitability questions below and
recorded the evidence in the table. This table should be used as a source
discovery shortlist, not as approval for FPP-001. The remaining work before
approval is:

1. Convert or replace the shortlist with 10 clean direct GPL PDF sources.
2. Confirm each final source can be stored as a local PDF fixture.
3. Reject any source that requires browser challenge bypass, scraping expansion, or manual HTML capture for the seed import.
4. Keep only sources that remain acceptable for business, reputation, legal, and strategy reasons.

If all four are true, the final PDF seed corpus can be approved for FPP-001
development. Price accuracy is handled later by source citations, timestamps,
confidence scoring, and verify-with-provider notices.

## Required Approval Fields

Approve exactly one seed list containing 10 public funeral home General Price
List PDF sources. Each final source must resolve to a direct PDF that can be
stored locally as a fixture without login, payment, browser challenge bypass,
or manual HTML capture.

For each of the 10 seed GPLs, approval must include:

- provider name
- city and state
- source URL
- source type: direct PDF
- access check: public, no login, no payment wall
- terms/robots check: no known restriction blocking archive/extraction review
- local PDF fixture path
- Codex source assessment evidence
- approval owner
- approval date
- approval decision: approved or rejected

Do not approve the seed corpus if any of these are unclear after Codex's source
assessment:

- whether the source is the provider's official public GPL
- whether the source can be accessed without login or payment
- whether site terms or robots instructions prohibit the planned access
- whether the provider/location is identifiable
- whether the final source is a clean PDF fixture source

## Discovery Shortlist

| # | Provider name | City, state | Source URL | Source type | Codex source assessment | Access / robots evidence | Approval owner | Approval date | Decision |
|---|---|---|---|---|---|---|---|---|---|
| 1 | California Cremation & Burial | San Diego / National City, CA | https://www.californiacremation.com/general-price-list | Official provider GPL page | Assessed 2026-06-07: browser-readable GPL page; page title and location footer match provider and San Diego / National City locations. | Browser fetch found public GPL content and prices; command-line HEAD returned 403, so use browser/manual fixture capture if needed. robots.txt disallows `/pax/` only; no GPL path block observed. | PENDING | PENDING | PENDING |
| 2 | Kern Funeral Home | Mount Vernon, WA | https://fh-content.s3.amazonaws.com/release/Content/Media/KernFuneralHome/Kern%20GPL%20Dec%201%2C%202025.pdf | Direct GPL PDF linked from official provider page | Assessed 2026-06-07: direct PDF URL includes Kern GPL Dec 1, 2025; official Kern GPL page references this PDF and provider address. | HTTP GET returned 200 `application/pdf`, 314,958 bytes. Kern robots.txt has no block for `/services/general-price-list`; S3 PDF was public. | PENDING | PENDING | PENDING |
| 3 | Hawthorne Funeral Home & Memorial Park | Mount Vernon, WA | https://www.hawthornefh.com/general-price-list | Official provider GPL page with PDF download | Assessed 2026-06-07: page title and content identify general price list and PDF download; provider name matches official domain. | HTTP HEAD returned 200 HTML. robots.txt allows `/`; no GPL path block observed. | PENDING | PENDING | PENDING |
| 4 | Bunker Family Funerals | Mesa, AZ | https://www.bunkerfuneral.com/general-price-list/ | Official provider GPL page with PDF downloads | Assessed 2026-06-07: corrected from stale direct PDF path to official GPL page; page identifies General Price List and Garden Chapel / University Chapel PDF downloads. | HTTP HEAD returned 200 HTML. robots.txt allows `/` except obituary flower/photo paths; no GPL path block observed. | PENDING | PENDING | PENDING |
| 5 | Simple Cremation Montana & Sunset Funeral Service | Helena, MT | https://www.simplecremationmt.com/gpl | Official provider GPL page with PDF download | Assessed 2026-06-07: page title identifies General Price List for Simple Cremation Montana & Sunset Funeral Service. | HTTP HEAD returned 200 HTML. robots.txt allows `/`; no GPL path block observed. | PENDING | PENDING | PENDING |
| 6 | Lanman Funeral Home, Inc. | Cherokee / Helena / Okeene / Medford, OK | https://www.lanmanfuneralhome.com/services/general-price-list | Official provider GPL page | Assessed 2026-06-07: page identifies General Price List; page lists Lanman locations including Helena, Cherokee, Okeene, and Medford. | HTTP HEAD returned 200 HTML. robots.txt allows `/`; no GPL path block observed. | PENDING | PENDING | PENDING |
| 7 | Joldersma & Klein Funeral Home | Kalamazoo, MI | https://joldersma-klein.com/wp-content/uploads/2023/04/JK-GPL-04.01.23-Letter-Orientation.pdf | Direct GPL PDF linked from official provider page | Assessed 2026-06-07: direct PDF URL includes JK GPL; provider domain matches Joldersma & Klein. | HTTP GET returned 200 `application/pdf`, 235,339 bytes. robots.txt has empty `Disallow` with crawl-delay 10; no GPL PDF path block observed. | PENDING | PENDING | PENDING |
| 8 | Remick & Gendron Funeral Home | Hampton, NH | https://www.remickgendron.com/funeral-pricing/general-price-list | Official provider GPL page with PDF link | Assessed 2026-06-07: browser-readable page identifies General Price List, effective January 1, 2025, and Hampton, NH location. | Browser fetch found public GPL content; command-line HEAD returned Cloudflare challenge 403. robots.txt does not block `/funeral-pricing/general-price-list`; respect listed bot crawl delays and do not bypass challenge automation. | PENDING | PENDING | PENDING |
| 9 | Coyle Funeral and Cremation Services | Toledo, OH | https://www.coylefuneralhome.com/our-pricing-and-resources/general-price-list | Official provider GPL page with PDF link | Assessed 2026-06-07: browser-readable page identifies General Price List and provider branding for Coyle Funeral and Cremation Services. | Browser fetch found public GPL/PDF link; command-line HEAD returned Cloudflare challenge 403. robots.txt does not block the pricing resource path; respect listed bot crawl delays and do not bypass challenge automation. | PENDING | PENDING | PENDING |
| 10 | Walker Sanderson Funeral Home & Crematory | Provo, UT | https://www.walkersanderson.com/price-list | Official provider GPL page with PDF download | Assessed 2026-06-07: page title identifies Price List for Walker Sanderson Funeral Home & Crematory in Provo, UT; page navigation lists Provo and Orem locations. | HTTP HEAD returned 200 HTML. robots.txt allows `/`; no price-list path block observed. | PENDING | PENDING | PENDING |

## Copy-Paste Approval Statement

Approved for FPP-001 only after this card contains 10 final direct GPL PDF
sources with local fixture paths: use those 10 GPL PDFs as the seed set for
local import-folder and metadata-schema work. This approval covers local PDF
download/storage for the seed set, metadata indexing, extraction fixture work,
and staging-only verification. It does not approve production deploy, domain
selection, ad/affiliate applications, broad scraping, browser challenge bypass,
manual HTML capture, or outreach to providers. This approval does not certify
that listed prices are accurate or current.

## Evidence Pack

- PR: PR that adds the completed final PDF approval table and Codex source assessment.
- Tests: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Quality gate output: `python3 orchestrator/scripts/run_quality_gate.py`
- Artifacts: completed final approval table with 10 direct GPL PDF source URLs,
  local fixture paths, and remaining owner decision fields.
- Rollback plan: revert the approval-table PR and keep `FPP-001` blocked.

## Explicit Non-Actions

- No seed GPLs imported.
- No production secrets added.
- No production deploy executed.
- No payment, ad, affiliate, KYC, or domain action executed.
