import unittest
from wine_quality import load_data, train_model, evaluate_model


class TestWineQuality(unittest.TestCase):

    def test_dataset_loaded(self):
        X, y = load_data()
        self.assertGreater(len(X), 0)
        self.assertEqual(len(X), len(y))

    def test_model_training(self):
        model, X_test, y_test = train_model()
        self.assertIsNotNone(model)
        self.assertGreater(len(X_test), 0)
        self.assertGreater(len(y_test), 0)

    def test_model_accuracy(self):
        accuracy = evaluate_model()
        self.assertGreaterEqual(accuracy, 0.50)
        self.assertLessEqual(accuracy, 1.0)


if __name__ == "__main__":
    unittest.main()
