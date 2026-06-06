# Ephemera Weaver Privacy And Read-Only Behavior

Ephemera Weaver is read-only by default. It indexes Markdown and Obsidian vault
folders so generated briefs, outlines, and contradiction maps can cite local
notes without changing those source notes.

## Source Files

- The indexer reads Markdown files and records metadata, content, and hashes in
  a local SQLite index.
- Ephemera Weaver has no automatic writeback into the selected vault or Markdown
  folder.
- Ephemera Weaver does not delete source notes.
- Any feature that writes to user files is an approval gate before build,
  release, or deploy work continues.

## Uploads

- Ephemera Weaver has no hidden cloud upload.
- Source notes stay local unless a future approved feature explicitly says
  otherwise in user-facing docs and release evidence.
- Any upload of user data is an approval gate before build, release, or deploy
  work continues.

## Generated Outputs

- Generated outputs are separate files.
- Exports must be written to an output folder chosen by the app flow, not back
  into the source vault by default.
- Generated content should cite source paths from the local index so users can
  review where claims came from.

## Release Review

Privacy, license, terms, pricing, refund, incident-response, source-writeback,
and user-data-upload changes are approval gates. If any of those appear in a
task, the builder must stop and create an approval card instead of inventing
policy or shipping the change.
