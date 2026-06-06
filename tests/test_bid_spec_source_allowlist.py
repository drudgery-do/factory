import unittest

from streams.bid_spec_atlas.source_allowlist import (
    DEFAULT_ALLOWLIST_PATH,
    SourceAllowlist,
    load_source_allowlist,
)


class BidSpecSourceAllowlistTests(unittest.TestCase):
    def test_default_allowlist_is_deny_by_default_until_sources_are_approved(self):
        allowlist = load_source_allowlist(DEFAULT_ALLOWLIST_PATH)

        self.assertEqual(allowlist.approved_sources, ())
        self.assertTrue(allowlist.approval_required)
        self.assertFalse(allowlist.is_url_allowed("https://example.test/bid-tabs.pdf"))

    def test_allowlist_requires_explicit_host_and_url_prefix_match(self):
        allowlist = SourceAllowlist(
            approved_sources=(
                {
                    "source_class": "fixture-dot",
                    "host": "dot.example.test",
                    "url_prefix": "https://dot.example.test/bid-tabs/",
                },
            ),
            approval_required=False,
        )

        self.assertTrue(allowlist.is_url_allowed("https://dot.example.test/bid-tabs/2026.pdf"))
        self.assertFalse(allowlist.is_url_allowed("https://dot.example.test/other/2026.pdf"))
        self.assertFalse(allowlist.is_url_allowed("https://mirror.example.test/bid-tabs/2026.pdf"))

    def test_default_allowlist_documents_missing_dot_source_approval(self):
        allowlist = load_source_allowlist(DEFAULT_ALLOWLIST_PATH)

        self.assertIn("TODO: approve first one or two DOT source classes", allowlist.notes)


if __name__ == "__main__":
    unittest.main()
