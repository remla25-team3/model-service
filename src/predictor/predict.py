import joblib
from importlib import resources
from . import models

class ReviewSentimentPredictor:
    def __init__(self):
        # Load trained models to retrieve predictions from
        dummy_model = (resources.files(models) / 'dummy_model.pkl')
        with dummy_model.open('rb') as f:
            self.prediction_model = joblib.load(f)

        sentiments = (resources.files(models) / 'c1_BoW_Sentiment_Model.pkl')
        with sentiments.open('rb') as f:
            self.sentiment_model = joblib.load(f)

    def predict(self, user_input: str):
        """
        Predicts the sentiment of the given user review.
        :param user_input: A single string representing a user's restaurant review
        :return: 'positive' or 'negative'
        :raises:
            - `TypeError` if `user_input` is not a string
            - `ValueError` if `user_input` is an empty string
            - `Exception` if no valid predictions could be made
        """
        if not isinstance(user_input, str):
            raise ValueError('Input must be a string')
        if user_input == '':
            raise ValueError('Input should not be empty')

        # TODO: This is pre-processing and should be handled in lib-ml. Included here temporarily for initial testing.
        X = self.sentiment_model.transform([user_input]).toarray()
        predictions = self.prediction_model.predict(X)

        if len(predictions) == 0:
            raise Exception('Error generating prediction')

        sentiment = "positive" if predictions[0] == 1 else "negative"
        return sentiment
