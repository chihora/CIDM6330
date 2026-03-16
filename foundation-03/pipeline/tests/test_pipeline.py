import unittest
from pathlib import Path

from pipeline.run_pipeline import run_pipeline


class TestPipeline(unittest.TestCase):
    def test_run_pipeline_creates_outputs(self):
        result = run_pipeline(use_live=False)
        self.assertGreaterEqual(result["raw_count"], 1)
        self.assertGreaterEqual(result["transformed_count"], 1)
        self.assertTrue(Path(result["raw_file"]).exists())
        self.assertTrue(Path(result["transformed_file"]).exists())


if __name__ == "__main__":
    unittest.main()
