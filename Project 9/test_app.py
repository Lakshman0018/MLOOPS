import unittest

from app import app

SAMPLE = {
    "fixed acidity": 7.9,
    "volatile acidity": 0.35,
    "citric acid": 0.46,
    "residual sugar": 3.6,
    "chlorides": 0.078,
    "free sulfur dioxide": 15,
    "total sulfur dioxide": 37,
    "density": 0.9973,
    "pH": 3.35,
    "sulphates": 0.86,
    "alcohol": 12.8,
}

class TestPredictionApplication(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")
        self.assertTrue(response.headers.get("X-Request-ID"))

    def test_request_id_is_traceable(self):
        response = self.client.get("/health", headers={"X-Request-ID": "lab-request-001"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("X-Request-ID"), "lab-request-001")

    def test_prediction_endpoint(self):
        response = self.client.post("/predict", json=SAMPLE)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.get_json()["prediction"], [3, 4, 5, 6, 7, 8])
        self.assertTrue(response.headers.get("X-Request-ID"))

    def test_missing_field_validation(self):
        response = self.client.post("/predict", json={"fixed acidity": 7.9})
        self.assertEqual(response.status_code, 400)
        self.assertIn("missing_fields", response.get_json())

    def test_missing_json_body_validation(self):
        response = self.client.post("/predict")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "JSON request body is required")

    def test_unknown_route(self):
        response = self.client.get("/not-a-real-route")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Route not found")

if __name__ == '__main__':
    unittest.main()
