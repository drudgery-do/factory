# Claude Agent Guide

This repo coordinates agent work for three first-wave businesses:

- Ephemera Weaver
- Bid Spec Atlas
- Funeral Price Pages

Do not infer product strategy from names. Use `FIRST_WAVE_BRIEF.md`, `portfolio.yaml`, and stream files as the authority.

## Required PR Behavior

Every PR must include:

- task ID
- stream
- risk classification
- test commands and outputs
- quality gate output
- files changed
- explicit TODOs or approval gates

Builder agents open PRs. QA reviewers verify. Release reviewers approve green/yellow deploys only after gates pass. Human owner/delegate approval is required for red gates.

## Bootstrap Boundary

ORCH-001 creates the operating scaffold only. It must not create product implementations, production secrets, deploy credentials, domain purchases, payment integrations, ad applications, or production deploy actions.
