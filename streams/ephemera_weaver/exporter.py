"""Export generated Ephemera Weaver outputs to separate Markdown files."""

from __future__ import annotations

import re
from pathlib import Path


def export_generated_markdown(generated_output: dict[str, object], output_dir: Path) -> Path:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    title = str(generated_output.get("title") or "generated-output")
    markdown = str(generated_output.get("markdown") or "")
    filename = f"{_slugify(title)}.md"
    export_path = output_dir / filename
    export_path.write_text(markdown, encoding="utf-8")
    return export_path


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "generated-output"
