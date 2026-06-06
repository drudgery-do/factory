"""Static local UI scaffold for Ephemera Weaver."""

from __future__ import annotations

from pathlib import Path


def render_local_ui() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ephemera Weaver</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; max-width: 920px; }
    label { display: block; font-weight: 700; margin-top: 1rem; }
    textarea { width: 100%; min-height: 10rem; }
    button { margin-top: 1rem; margin-right: .5rem; }
    .notice { border: 1px solid #999; padding: 1rem; margin: 1rem 0; }
  </style>
</head>
<body>
  <main>
    <h1>Ephemera Weaver</h1>
    <section class="notice">
      <strong>Read-only by default.</strong>
      Source notes are indexed locally. No hidden cloud upload. Generated outputs are exported separately.
    </section>
    <form>
      <label for="vault">Markdown or Obsidian vault folder</label>
      <input id="vault" name="vault" type="file" webkitdirectory directory multiple>

      <label for="prompt">Current draft or project prompt</label>
      <textarea id="prompt" name="prompt"></textarea>

      <button type="button">Generate Brief</button>
      <button type="button">Generate Outline</button>
      <button type="button">Generate Contradiction Map</button>
      <button type="button">Export Markdown</button>
    </form>
  </main>
</body>
</html>
"""


def write_local_ui(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "index.html"
    path.write_text(render_local_ui(), encoding="utf-8")
    return path
