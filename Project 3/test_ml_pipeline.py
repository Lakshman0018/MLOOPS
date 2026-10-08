import json
import os
import unittest

import joblib
import pandas as pd

from train_model import DATASET_PATH


MODEL_FILE = "wine_quality_model.pkl"
METRICS_FILE = "metrics.json"


class TestMLPipeline(unittest.TestCase):

    def test_dataset_loaded(self):
        self.assertTrue(os.path.exists(DATASET_PATH))

        data = pd.read_csv(DATASET_PATH)
        self.assertGreater(len(data), 0)
        self.assertIn("quality", data.columns)

    def test_model_created(self):
        self.assertTrue(os.path.exists(MODEL_FILE))

    def test_metrics_created(self):
        self.assertTrue(os.path.exists(METRICS_FILE))

    def test_accuracy_is_valid(self):
        with open(METRICS_FILE, "r") as file:
            metrics = json.load(file)

        accuracy = metrics["accuracy"]
        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)

    def test_model_prediction(self):
        model = joblib.load(MODEL_FILE)
        data = pd.read_csv(DATASET_PATH)

        sample = data.drop(columns=["quality", "Id"]).iloc[[0]]
        prediction = model.predict(sample)[0]

        self.assertIn(int(prediction), [int(value) for value in model.classes_])

    def test_model_accuracy_threshold(self):
        with open(METRICS_FILE, "r") as file:
            metrics = json.load(file)

        self.assertGreaterEqual(metrics["accuracy"], 0.50)

    def test_training_and_testing_records(self):
        with open(METRICS_FILE, "r") as file:
            metrics = json.load(file)

        self.assertGreater(metrics["training_records"], 0)
        self.assertGreater(metrics["testing_records"], 0)


if __name__ == "__main__":
    unittest.main()
