# Funeral Price Pages Runbook

## Builder Flow

1. Pick a task from `streams/funeral-price-pages/backlog.yaml`.
2. Confirm seed/source approvals before ingest work.
3. Add extraction or publishing tests before implementation.
4. Run stream QA gates.
5. Open a PR with an evidence pack.

## QA Flow

1. Verify every price line has source, timestamp, and verify notice.
2. Verify low-confidence rows are blocked.
3. Verify no funeral planning advice appears.
4. Verify correction workflow creates review issues.
5. Record findings in the PR.

## Release Flow

Staging deploys require gates. Production deploys remain disabled during ORCH-001.
