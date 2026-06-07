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

Approve whether this list is acceptable as a seed corpus for local import and
extraction development. This is a source-suitability approval, not a price,
legal, medical, financial, or consumer-advice certification.

Approval means:

- the listed sources are acceptable inputs for FPP-001 local seed import work
- the builder may download/store local copies for test fixtures and metadata
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

## How To Review This Without Being A Funeral Pricing Expert

For each candidate, check only these source-suitability questions:

1. Does the provider/source name match the linked URL well enough to be plausible?
2. Is the URL public and reachable without login or payment?
3. Does the page/PDF identify itself as a General Price List, GPL, or funeral price list?
4. Is the provider location identifiable?
5. Is there any obvious reason this source should not be used as a development seed?

If the answer is yes for 1-4 and no for 5, the candidate can be approved for
seed development. Price accuracy is handled later by source citations,
timestamps, confidence scoring, and verify-with-provider notices.

## Required Approval Fields

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
| 1 | California Cremation & Burial | San Diego / National City, CA | https://www.californiacremation.com/general-price-list | Official provider GPL page | Public page observed; no login or payment wall | No blocker observed in public page; human review required | PENDING | PENDING | PENDING |
| 2 | Kern Funeral Home | Mount Vernon, WA | https://fh-content.s3.amazonaws.com/release/Content/Media/KernFuneralHome/Kern%20GPL%20Dec%201%2C%202025.pdf | Direct GPL PDF linked from official provider page | Public PDF observed; no login or payment wall | No blocker observed in public page/PDF; human review required | PENDING | PENDING | PENDING |
| 3 | Hawthorne Funeral Home & Memorial Park | Mount Vernon, WA | https://www.hawthornefh.com/general-price-list | Official provider GPL page with PDF download | Public page observed; no login or payment wall | No blocker observed in public page; human review required | PENDING | PENDING | PENDING |
| 4 | Bunker Family Funerals - Garden Chapel | Mesa, AZ | https://www.bunkerfuneral.com/wp-content/uploads/2025/10/2025-Garden-Chapel-General-Price-List-r5.pdf | Direct GPL PDF from provider domain | Public PDF observed; no login or payment wall | No blocker observed in public PDF; human review required | PENDING | PENDING | PENDING |
| 5 | Simple Cremation Montana & Sunset Funeral Service | Helena, MT | https://www.simplecremationmt.com/gpl | Official provider GPL page with PDF download | Public page observed; no login or payment wall | No blocker observed in public page; human review required | PENDING | PENDING | PENDING |
| 6 | Lanman Funeral Home, Inc. | Cherokee / Helena / Okeene / Medford, OK | https://www.lanmanfuneralhome.com/services/general-price-list | Official provider GPL page | Public page observed; no login or payment wall | No blocker observed in public page; human review required | PENDING | PENDING | PENDING |
| 7 | Joldersma & Klein Funeral Home | Kalamazoo, MI | https://joldersma-klein.com/wp-content/uploads/2023/04/JK-GPL-04.01.23-Letter-Orientation.pdf | Direct GPL PDF linked from official provider page | Public PDF observed; no login or payment wall | No blocker observed in public page/PDF; human review required | PENDING | PENDING | PENDING |
| 8 | Remick & Gendron Funeral Home | Hampton, NH | https://www.remickgendron.com/funeral-pricing/general-price-list | Official provider GPL page | Public page observed; no login or payment wall | No blocker observed in public page; human review required | PENDING | PENDING | PENDING |
| 9 | Coyle Funeral and Cremation Services | Toledo, OH | https://www.coylefuneralhome.com/our-pricing-and-resources/general-price-list | Official provider GPL page with PDF link | Public page observed; no login or payment wall | No blocker observed in public page; human review required | PENDING | PENDING | PENDING |
| 10 | Walker Sanderson Funeral Home & Crematory | Provo, UT | https://www.walkersanderson.com/price-list | Official provider GPL page with PDF download | Public page observed; no login or payment wall | No blocker observed in public page; human review required | PENDING | PENDING | PENDING |

## Copy-Paste Approval Statement

Approved for FPP-001: use the 10 GPL sources listed above as the seed set for
local import-folder and metadata-schema work. This approval covers local source
download/storage for the seed set, metadata indexing, extraction fixture work,
and staging-only verification. It does not approve production deploy, domain
selection, ad/affiliate applications, broad scraping, or outreach to providers.
This approval does not certify that listed prices are accurate or current.

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
