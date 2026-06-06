import unittest

from streams.bid_spec_atlas.staging_smoke import plan_staging_smoke


class BidSpecStagingSmokeTests(unittest.TestCase):
    def test_staging_smoke_requires_approved_base_url(self):
        payload = plan_staging_smoke(base_url="")

        self.assertEqual(payload["status"], "approval_gate")
        self.assertIn("TODO: approve Bid Spec Atlas staging host", payload["todo"])
        self.assertEqual(payload["checks"], [])

    def test_staging_smoke_plans_required_paths_without_deploying(self):
        payload = plan_staging_smoke(base_url="https://bid-spec-staging.example.test")

        self.assertEqual(payload["status"], "ready")
        self.assertEqual(
            payload["checks"],
            [
                "https://bid-spec-staging.example.test/",
                "https://bid-spec-staging.example.test/sitemap.xml",
                "https://bid-spec-staging.example.test/items/201-0001-clearing-and-grubbing.html",
            ],
        )
        self.assertFalse(payload["deploy_performed"])


if __name__ == "__main__":
    unittest.main()
