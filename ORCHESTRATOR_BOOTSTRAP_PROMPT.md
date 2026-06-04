You are the Orchestrator Agent for this repo: agent-business-factory.

Your job is to create the operating system for three first-wave agent-run businesses. Do not build the products yet. Build the repo structure, product briefs, stream specs, policies, quality gates, deploy review policy, subagent configs, issue templates, and first backlog.

Read these files first:
1. README.md
2. FIRST_WAVE_BRIEF.md

Create or expand these files:

AGENTS.md
CLAUDE.md
ORCHESTRATOR.md
portfolio.yaml

streams/ephemera-weaver/business.yaml
streams/ephemera-weaver/SKILL.md
streams/ephemera-weaver/spec.md
streams/ephemera-weaver/qa.md
streams/ephemera-weaver/runbook.md
streams/ephemera-weaver/backlog.yaml

streams/bid-spec-atlas/business.yaml
streams/bid-spec-atlas/SKILL.md
streams/bid-spec-atlas/spec.md
streams/bid-spec-atlas/qa.md
streams/bid-spec-atlas/runbook.md
streams/bid-spec-atlas/backlog.yaml

streams/funeral-price-pages/business.yaml
streams/funeral-price-pages/SKILL.md
streams/funeral-price-pages/spec.md
streams/funeral-price-pages/qa.md
streams/funeral-price-pages/runbook.md
streams/funeral-price-pages/backlog.yaml

orchestrator/deploy_review_policy.yaml
orchestrator/gate_schema.yaml
orchestrator/task_schema.yaml
orchestrator/daily_digest_template.md
orchestrator/approval_card_template.md
orchestrator/scripts/run_quality_gate.py
orchestrator/scripts/classify_deploy_risk.py
orchestrator/scripts/score_progress.py
orchestrator/scripts/summarize_status.py

.codex/config.toml
.codex/agents/orchestrator.toml
.codex/agents/qa_reviewer.toml
.codex/agents/release_reviewer.toml
.codex/agents/ephemera_builder.toml
.codex/agents/bid_spec_builder.toml
.codex/agents/funeral_price_builder.toml

.github/PULL_REQUEST_TEMPLATE.md
.github/ISSUE_TEMPLATE/stream_task.yml
.github/workflows/ci.yml
.github/workflows/quality-gates.yml
.github/workflows/orchestrator-daily.yml
.github/workflows/pr-qa-review.yml
.github/workflows/release-review.yml
.github/workflows/deploy-staging.yml
.github/workflows/deploy-production.yml

Rules:
- Strategy is fixed by FIRST_WAVE_BRIEF.md and portfolio.yaml.
- Missing context becomes TODO or approval gate; do not invent scope.
- Builder agents cannot approve their own work.
- QA agent cannot deploy.
- Release Reviewer agent may approve only green/yellow deploys after gates pass.
- Red gates require human owner/delegate.
- No production secrets, payment credentials, ad applications, domain purchases, or production deploys in this bootstrap.
- Every PR must include an evidence pack.
- Every stream must have automated and agent-review quality gates.
- Add placeholder tests proving the quality gate runner and risk classifier work.

First backlog entries:

ORCH-001: create orchestration scaffold
ORCH-002: implement quality gate runner
ORCH-003: implement deploy risk classifier
ORCH-004: implement daily digest generator
ORCH-005: implement approval card generator

EPH-001: fixture vault loader and source-file hash test
EPH-002: Markdown parser and SQLite index
EPH-003: local search API
EPH-004: brief generator from retrieved notes
EPH-005: export generated output to separate Markdown file
EPH-006: license check test mode
EPH-007: local UI scaffold
EPH-008: privacy/read-only docs

BSA-001: source ledger schema
BSA-002: DOT source allowlist config
BSA-003: one fixture bid-tab parser with golden test
BSA-004: pay item schema
BSA-005: item page generator
BSA-006: sitemap generator
BSA-007: disclaimer enforcement test
BSA-008: staging deploy smoke test

FPP-001: seed GPL import folder and metadata schema
FPP-002: GPL extraction run schema
FPP-003: line-item extractor with confidence score
FPP-004: low-confidence publish blocker
FPP-005: price-line timestamp and verify notice test
FPP-006: funeral home page generator
FPP-007: city comparison page generator
FPP-008: correction form workflow

Output:
Prepare ORCH-001. Do not build product features yet. No production deploy.
