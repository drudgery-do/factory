import unittest

from streams.bid_spec_atlas.sitemap_generator import generate_sitemap_xml


class BidSpecSitemapGeneratorTests(unittest.TestCase):
    def test_generate_sitemap_xml_includes_item_urls(self):
        xml = generate_sitemap_xml(
            base_url="https://bid-spec.example.test",
            slugs=("201-0001-clearing-and-grubbing", "304-1200-aggregate-base-course"),
        )

        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', xml)
        self.assertIn("<urlset", xml)
        self.assertIn(
            "<loc>https://bid-spec.example.test/items/201-0001-clearing-and-grubbing.html</loc>",
            xml,
        )
        self.assertIn(
            "<loc>https://bid-spec.example.test/items/304-1200-aggregate-base-course.html</loc>",
            xml,
        )

    def test_generate_sitemap_xml_requires_base_url(self):
        with self.assertRaises(ValueError):
            generate_sitemap_xml(base_url="", slugs=("201-0001-clearing-and-grubbing",))


if __name__ == "__main__":
    unittest.main()
