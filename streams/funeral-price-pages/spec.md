# Funeral Price Pages Spec

## V0 Scope

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

## Explicitly Not V0

- lead resale
- call center
- funeral planning advice
- provider dashboard
- nationwide scraping
- paid customer accounts
- automated outreach to funeral homes

## Done For V0

- 10 seed GPLs imported
- 90%+ extraction accuracy on seed set
- low-confidence rows blocked
- 50 local pages generated
- correction form works
- every price line has timestamp and verify-with-provider notice
- sitemap validates
- schema.org markup validates
- staging deploy passes link check

## TODOs

- TODO: define low-confidence threshold before FPP-004.
- TODO: choose domain only through red-gate approval.
