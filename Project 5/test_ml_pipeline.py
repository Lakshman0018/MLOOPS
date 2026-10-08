import unittest

from app import app


FEATURES = {
    "fixed acidity": 7.4,
    "volatile acidity": 0.70,
    "citric acid": 0.00,
    "residual sugar": 1.9,
    "chlorides": 0.076,
    "free sulfur dioxide": 11.0,
    "total sulfur dioxide": 34.0,
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4,
}

HIGH_QUALITY_SAMPLE = {
    "fixed acidity": 7.9,
    "volatile acidity": 0.35,
    "citric acid": 0.46,
    "residual sugar": 3.6,
    "chlorides": 0.078,
    "free sulfur dioxide": 15.0,
    "total sulfur dioxide": 37.0,
    "density": 0.9973,
    "pH": 3.35,
    "sulphates": 0.86,
    "alcohol": 12.8,
}

LOW_QUALITY_SAMPLE = {
    "fixed acidity": 7.1,
    "volatile acidity": 0.71,
    "citric acid": 0.00,
    "residual sugar": 1.9,
    "chlorides": 0.080,
    "free sulfur dioxide": 14.0,
    "total sulfur dioxide": 35.0,
    "density": 0.9972,
    "pH": 3.47,
    "sulphates": 0.55,
    "alcohol": 9.4,
}


class TestPredictionApplication(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_high_performance_prediction(self):
        response = self.client.post("/predict", json=HIGH_QUALITY_SAMPLE)

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.get_json()["prediction"], [3, 4, 5, 6, 7, 8])

    def test_low_performance_prediction(self):
        response = self.client.post("/predict", json=LOW_QUALITY_SAMPLE)

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.get_json()["prediction"], [3, 4, 5, 6, 7, 8])

    def test_missing_field_validation(self):
        response = self.client.post(
            "/predict",
            json={"fixed acidity": 7.4, "volatile acidity": 0.70}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("missing_fields", response.get_json())


if __name__ == "__main__":
    unittest.main()
