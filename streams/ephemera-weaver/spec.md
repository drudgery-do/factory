# Ephemera Weaver Spec

## V0 Scope

- local app or local web app
- folder picker
- Markdown folder support
- Obsidian vault support
- local SQLite index
- local search
- prompt box where user pastes current draft/project
- generated research brief
- generated outline
- generated contradiction map
- export generated output as separate Markdown
- license-key check in test mode
- direct-download landing page
- docs
- regression tests

## User-Facing Docs

- `streams/ephemera-weaver/privacy-read-only.md`

## Explicitly Not V0

- mobile app
- team collaboration
- cloud sync
- browser extension
- every-app connector layer
- Zotero connector
- marketplace
- automatic writeback into vault
- deletion or modification of source notes

## Done For V0

- fixture vault indexes successfully
- source-file hash test proves no input files changed
- brief generation works on at least 5 fixture vaults
- output exports to separate Markdown file
- docs clearly explain read-only behavior
- license check works in test mode
- install path works on clean machine

## TODOs

- TODO: choose local app framework after approval.
- TODO: define fixture vault format before EPH-001.
- TODO: define license test-mode contract before EPH-006.
