import json
import unittest
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent


class TestMLPipeline(unittest.TestCase):
    def test_dataset_exists_and_has_rows(self):
        path = BASE_DIR / "WineQT.csv"
        self.assertTrue(path.exists())
        data = pd.read_csv(path)
        self.assertGreater(len(data), 1000)
        self.assertIn("quality", data.columns)
        self.assertIn("Id", data.columns)

    def test_model_exists_after_training(self):
        path = BASE_DIR / "wine_quality_model.pkl"
        self.assertTrue(path.exists())
        model = joblib.load(path)
        self.assertTrue(hasattr(model, "predict"))

    def test_metrics_exist_and_have_accuracy(self):
        path = BASE_DIR / "metrics.json"
        self.assertTrue(path.exists())
        with path.open() as f:
            metrics = json.load(f)
        self.assertIn("accuracy", metrics)
        self.assertGreaterEqual(metrics["accuracy"], 0.70)

    def test_metrics_records_are_positive(self):
        with (BASE_DIR / "metrics.json").open() as f:
            metrics = json.load(f)
        self.assertGreater(metrics["training_records"], 0)
        self.assertGreater(metrics["testing_records"], 0)


if __name__ == "__main__":
    unittest.main()
