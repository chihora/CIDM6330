import unittest

from pipeline.acquire import fetch_gdp_observations


class TestAcquire(unittest.TestCase):
    def test_fetch_sample_payload(self):
        payload = fetch_gdp_observations(use_live=False)
        self.assertIn("observations", payload)
        self.assertGreater(len(payload["observations"]), 0)


if __name__ == "__main__":
    unittest.main()
