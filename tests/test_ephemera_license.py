import unittest

from streams.ephemera_weaver.license import check_license_key


class EphemeraLicenseTests(unittest.TestCase):
    def test_test_mode_accepts_known_test_license_key(self):
        result = check_license_key("EPH-TEST-VALID", mode="test")

        self.assertTrue(result["valid"])
        self.assertEqual(result["mode"], "test")
        self.assertEqual(result["reason"], "accepted_test_key")

    def test_test_mode_rejects_unknown_license_key(self):
        result = check_license_key("EPH-LIVE-SECRET", mode="test")

        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "unknown_test_key")

    def test_live_mode_is_an_approval_gate_placeholder(self):
        result = check_license_key("anything", mode="live")

        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "live_license_check_not_configured")
        self.assertEqual(result["approval_gate"], "license provider and secret storage approval required")


if __name__ == "__main__":
    unittest.main()
