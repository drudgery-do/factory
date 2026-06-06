# Bid Spec Atlas Runbook

## Builder Flow

1. Pick a task from `streams/bid-spec-atlas/backlog.yaml`.
2. Confirm source scope is approved.
3. Add parser or page tests before implementation.
4. Run stream QA gates.
5. Open a PR with an evidence pack.

## QA Flow

1. Verify every extracted row has source lineage.
2. Verify no bidding advice appears.
3. Run parser golden tests.
4. Run disclaimer checks.
5. Record findings in the PR.

## Release Flow

Only staging deploy scaffolds may be prepared during ORCH-001. Production deploys remain disabled.
