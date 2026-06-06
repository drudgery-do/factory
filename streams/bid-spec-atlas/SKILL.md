# Bid Spec Atlas Skill

Use this skill for Bid Spec Atlas tasks.

## Read First

1. `FIRST_WAVE_BRIEF.md`
2. `streams/bid-spec-atlas/business.yaml`
3. `streams/bid-spec-atlas/spec.md`
4. `streams/bid-spec-atlas/qa.md`

## Boundaries

- Use only approved official source classes.
- Every row needs `source_file_id`.
- Every generated fact must link to a source file.
- Failed parses create review issues.
- Do not publish bidding advice.
- Do not remove or change the required disclaimer without human approval.

## Missing Context

Create a TODO or approval gate instead of inventing scope.
