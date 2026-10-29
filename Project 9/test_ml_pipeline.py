import json
import os
import unittest
class TestMLPipeline(unittest.TestCase):
    def test_dataset_loaded(self): self.assertTrue(os.path.exists('WineQT.csv'))
    def test_model_created(self): self.assertTrue(os.path.exists('wine_quality_model.pkl'))
    def test_metrics_created(self): self.assertTrue(os.path.exists('metrics.json'))
    def test_accuracy_is_valid(self):
        with open('metrics.json') as f: m=json.load(f)
        self.assertGreaterEqual(m['accuracy'],0.0); self.assertLessEqual(m['accuracy'],1.0)
if __name__=='__main__': unittest.main()
