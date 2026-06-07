import unittest

from streams.funeral_price_pages.correction_form import (
    CorrectionRequest,
    correction_request_schema_sql,
)


class FuneralPricePagesCorrectionFormTests(unittest.TestCase):
    def test_correction_request_creates_review_issue_payload(self):
        request = CorrectionRequest(
            request_id="corr-001",
            provider_name="Legends Tri-County Funeral Services",
            source_url="https://s3.amazonaws.com/CFSV2/fileuploads/13269/GPLFall2025PDF.pdf",
            submitted_by="provider@example.test",
            message="The direct cremation price has changed.",
            created_at="2026-06-07T02:25:00Z",
        )

        self.assertEqual(request.validate(), [])
        self.assertEqual(request.review_issue_title(), "FPP correction review: Legends Tri-County Funeral Services")
        self.assertIn("The direct cremation price has changed.", request.review_issue_body())

    def test_correction_request_rejects_missing_source_url(self):
        request = CorrectionRequest(
            request_id="corr-001",
            provider_name="Legends Tri-County Funeral Services",
            source_url="",
            submitted_by="provider@example.test",
            message="The direct cremation price has changed.",
            created_at="2026-06-07T02:25:00Z",
        )

        errors = request.validate()

        self.assertIn("source_url is required", errors)
        self.assertIn("source_url must be https", errors)

    def test_correction_schema_routes_requests_to_review(self):
        sql = correction_request_schema_sql()

        self.assertIn("CREATE TABLE IF NOT EXISTS correction_requests", sql)
        self.assertIn("status TEXT NOT NULL CHECK", sql)
        self.assertIn("review_required", sql)
        self.assertIn("review_issue_url TEXT NOT NULL DEFAULT ''", sql)


if __name__ == "__main__":
    unittest.main()

