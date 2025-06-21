import unittest
from .predict import ReviewSentimentPredictor

class TestReviewSentimentPredictor(unittest.TestCase):
    """
    Test suite for the ReviewSentimentPredictor class.
    """

    predictor = None

    @classmethod
    def setUpClass(cls):
        if cls.predictor is None:
            print("\nInitializing ReviewSentimentPredictor")
            cls.predictor = ReviewSentimentPredictor()
            print("Predictor initialized")

    def test_positive_review_returns_high_score(self):
        """
        Tests that a clearly positive review returns a score > 0.5.
        """
        review = "The food was absolutely wonderful"
        
        score = self.predictor.predict(review)
        
        # Assert that the score is a float and is greater than 0.5
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0.5, "A positive review should have a score greater than 0.5")

    def test_negative_review_returns_low_score(self):
        review = "It was a terrible experience, very disappointing"
        
        score = self.predictor.predict(review)
        
        self.assertIsInstance(score, float)
        self.assertLess(score, 0.5, "A negative review should have a score less than 0.5")

    def test_empty_input_raises_value_error(self):
        """
        Tests that calling predict with an empty string raises a ValueError.
        """
        # Use a context manager to assert that the correct exception is raised.
        with self.assertRaises(ValueError, msg="Empty input should raise a ValueError"):
            self.predictor.predict("")

if __name__ == '__main__':
    unittest.main()