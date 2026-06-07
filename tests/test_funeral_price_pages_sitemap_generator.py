import unittest

from streams.funeral_price_pages.page_generator import city_comparison_path, funeral_home_path
from streams.funeral_price_pages.seed_import import load_seed_manifest
from streams.funeral_price_pages.sitemap_generator import generate_sitemap_xml


class FuneralPricePagesSitemapGeneratorTests(unittest.TestCase):
    def test_sitemap_includes_funeral_home_and_city_paths(self):
        seed = load_seed_manifest()[0]
        paths = [
            funeral_home_path(seed),
            city_comparison_path(seed.city, seed.state, "direct cremation"),
        ]

        xml = generate_sitemap_xml("https://funeral-prices.example", paths)

        self.assertIn("<urlset", xml)
        self.assertIn("https://funeral-prices.example/funeral-homes/wa/seattle/bonney-watson", xml)
        self.assertIn("https://funeral-prices.example/funeral-prices/wa/seattle/direct-cremation", xml)

    def test_sitemap_requires_https_base_url(self):
        with self.assertRaises(ValueError):
            generate_sitemap_xml("http://funeral-prices.example", ["/"])


if __name__ == "__main__":
    unittest.main()

