"""Smoke-check the generated first-wave staging site."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "dist" / "staging"


STATIC_CONTENT_CHECKS = {
    "index.html": ("First-Wave Staging", "Ephemera Weaver", "Bid Spec Atlas", "Funeral Price Pages"),
    "ephemera-weaver/index.html": ("Ephemera Weaver", "Read-only by default."),
    "ephemera-weaver/research-brief.html": ("Research Brief", "Source Notes"),
    "bid-spec-atlas/index.html": ("Bid Spec Atlas", "CLEARING AND GRUBBING"),
    "funeral-price-pages/index.html": ("Funeral Price Pages", "Verify all prices with the provider."),
    "sitemap.xml": ("bid-spec-atlas", "funeral-price-pages"),
}


def smoke_staging_site(output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, object]:
    manifest_path = output_dir / "staging-manifest.json"
    failed = []
    checks_total = 0

    if not manifest_path.exists():
        return {
            "status": "fail",
            "checks_total": 1,
            "failed": ["staging-manifest.json is missing"],
        }

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative_path in manifest["required_paths"]:
        checks_total += 1
        path = output_dir / relative_path
        if not path.exists():
            failed.append(f"{relative_path} is missing")

    content_checks = dict(STATIC_CONTENT_CHECKS)
    content_checks["sitemap.xml"] = (
        str(manifest.get("base_url", "")),
        *content_checks["sitemap.xml"],
    )

    for relative_path, required_terms in content_checks.items():
        checks_total += 1
        path = output_dir / relative_path
        if not path.exists():
            failed.append(f"{relative_path} is missing for content check")
            continue
        content = path.read_text(encoding="utf-8")
        for term in required_terms:
            checks_total += 1
            if term not in content:
                failed.append(f"{relative_path} is missing required term: {term}")

    return {
        "status": "fail" if failed else "pass",
        "checks_total": checks_total,
        "failed": failed,
        "base_url": manifest.get("base_url", ""),
        "required_path_count": len(manifest.get("required_paths", [])),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    result = smoke_staging_site(args.output_dir)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
