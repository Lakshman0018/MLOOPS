import unittest
from app import app
SAMPLE={'fixed acidity':7.9,'volatile acidity':0.35,'citric acid':0.46,'residual sugar':3.6,'chlorides':0.078,'free sulfur dioxide':15,'total sulfur dioxide':37,'density':0.9973,'pH':3.35,'sulphates':0.86,'alcohol':12.8}
class TestPredictionApplication(unittest.TestCase):
    def setUp(self): self.client=app.test_client()
    def test_health_endpoint(self):
        r=self.client.get('/health'); self.assertEqual(r.status_code,200); self.assertEqual(r.get_json()['status'],'healthy')
    def test_prediction_endpoint(self):
        r=self.client.post('/predict',json=SAMPLE); self.assertEqual(r.status_code,200); self.assertIn(r.get_json()['prediction'],[3,4,5,6,7,8])
    def test_missing_field_validation(self):
        r=self.client.post('/predict',json={'fixed acidity':7.9}); self.assertEqual(r.status_code,400)
if __name__=='__main__': unittest.main()
