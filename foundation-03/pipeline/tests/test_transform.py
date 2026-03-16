import unittest

from pipeline.transform import transform_observations


class TestTransform(unittest.TestCase):
    def test_transform_filters_invalid_rows(self):
        raw = {
            "observations": [
                {"date": "2021-01-01", "value": "100.5"},
                {"date": "2021-04-01", "value": "."},
                {"date": "2021-07-01", "value": "abc"},
                {"date": None, "value": "200"},
            ]
        }

        rows = transform_observations(raw)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "2021-01-01")
        self.assertEqual(rows[0]["value"], 100.5)


if __name__ == "__main__":
    unittest.main()
