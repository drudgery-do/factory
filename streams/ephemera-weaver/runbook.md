# Ephemera Weaver Runbook

## Builder Flow

1. Pick a task from `streams/ephemera-weaver/backlog.yaml`.
2. Confirm task scope matches `FIRST_WAVE_BRIEF.md`.
3. Add tests before implementation.
4. Run stream QA gates.
5. Open a PR with an evidence pack.

## QA Flow

1. Verify no source note modification.
2. Verify no cloud upload behavior.
3. Run automated tests.
4. Review `streams/ephemera-weaver/privacy-read-only.md` for read-only and privacy language.
5. Record findings in the PR.

## Release Flow

Ephemera releases remain disabled during ORCH-001. Create approval cards for yellow or red work.
