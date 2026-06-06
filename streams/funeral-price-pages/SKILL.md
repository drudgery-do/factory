# Funeral Price Pages Skill

Use this skill for Funeral Price Pages tasks.

## Read First

1. `FIRST_WAVE_BRIEF.md`
2. `streams/funeral-price-pages/business.yaml`
3. `streams/funeral-price-pages/spec.md`
4. `streams/funeral-price-pages/qa.md`

## Boundaries

- Publish no low-confidence extracted data.
- Publish no invented prices.
- Every price line needs source file, extraction date, and verify-with-provider notice.
- Provider corrections create review issues.
- Do not add funeral planning advice.
- First 10 seed GPL approvals are red gates.

## Missing Context

Create a TODO or approval gate instead of inventing scope.
