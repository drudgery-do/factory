import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.scripts.build_staging_site import build_staging_site
from orchestrator.scripts.smoke_staging_site import smoke_staging_site


class StagingSiteBuilderTests(unittest.TestCase):
    def test_build_staging_site_writes_all_stream_surfaces_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "site"
            manifest = build_staging_site(
                output_dir=output_dir,
                base_url="https://staging.example.test",
            )

            self.assertEqual(manifest["base_url"], "https://staging.example.test")
            self.assertEqual(manifest["status"], "ready_for_staging_review")
            self.assertIn("index.html", manifest["required_paths"])
            self.assertIn("ephemera-weaver/index.html", manifest["required_paths"])
            self.assertIn("bid-spec-atlas/index.html", manifest["required_paths"])
            self.assertIn("funeral-price-pages/index.html", manifest["required_paths"])
            self.assertIn(
                "funeral-homes/tx/seguin/legends-tri-county-funeral-services/index.html",
                manifest["required_paths"],
            )
            self.assertIn(
                "funeral-prices/tx/seguin/direct-cremation/index.html",
                manifest["required_paths"],
            )
            self.assertIn("sitemap.xml", manifest["required_paths"])

            for relative_path in manifest["required_paths"]:
                self.assertTrue((output_dir / relative_path).exists(), relative_path)

            payload = json.loads((output_dir / "staging-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(payload, manifest)

    def test_staging_smoke_requires_expected_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "site"
            build_staging_site(
                output_dir=output_dir,
                base_url="https://staging.example.test",
            )

            result = smoke_staging_site(output_dir)

            self.assertEqual(result["status"], "pass")
            self.assertEqual(result["failed"], [])
            self.assertGreaterEqual(result["checks_total"], 8)

    def test_staging_builder_requires_https_base_url(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(ValueError):
                build_staging_site(
                    output_dir=Path(tmpdir) / "site",
                    base_url="http://staging.example.test",
                )


if __name__ == "__main__":
    unittest.main()
