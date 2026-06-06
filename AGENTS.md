# Agent Instructions

This repository is the orchestration layer for the first-wave agent-run businesses. It is not a product implementation repo yet.

## Sources Of Truth

Read these before changing scope:

1. `README.md`
2. `FIRST_WAVE_BRIEF.md`
3. `portfolio.yaml`
4. The relevant `streams/*/business.yaml`

Strategy is fixed by `FIRST_WAVE_BRIEF.md` and `portfolio.yaml`. Missing context becomes a TODO or an approval gate. Do not invent scope.

## Operating Rules

- Do not build product features during orchestration bootstrap work.
- Do not add production secrets, payment credentials, ad applications, domain purchases, or production deploy behavior.
- Builder agents cannot approve their own work.
- QA agents cannot deploy.
- Release Reviewer agents may approve only green/yellow deploys after gates pass.
- Red gates require the Human Owner or Delegate.
- Every PR must include an evidence pack.
- Every stream must include automated and agent-review quality gates.

## Context7

Use Context7 MCP to fetch current documentation whenever a task asks about a library, framework, SDK, API, CLI tool, or cloud service. Start with `resolve-library-id`, then use `query-docs` with the selected library ID and the full user question.

## CodeGraph

Use CodeGraph for structural questions about symbols, callers, callees, impact, and file layout. Use native shell search only for literal text queries or when reading specific requested files.
