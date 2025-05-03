import unittest
from ..predict import ReviewSentimentPredictor


class TestPredictor(unittest.TestCase):

    def test_init_loads_models(self):
        predictor = ReviewSentimentPredictor()
        self.assertIsNotNone(predictor.prediction_model)
        self.assertIsNotNone(predictor.sentiment_model)

    def test_bad_input_raises_error(self):
        predictor = ReviewSentimentPredictor()
        with self.assertRaises(ValueError):
            predictor.predict(1)
        with self.assertRaises(ValueError):
            predictor.predict('')

    def test_predictor_outputs_pos_or_neg(self):
        predictor = ReviewSentimentPredictor()
        prediction = predictor.predict("Some restaurant review")
        self.assertIn(prediction, ['positive', 'negative'])


if __name__ == '__main__':
    unittest.main()
