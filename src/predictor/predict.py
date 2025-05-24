import numpy as np
import joblib
from urllib.request import urlopen
from lib_ml.preprocessing import preprocess_text

class ReviewSentimentPredictor:
    def __init__(self):
        # Load trained model to generate predictions with
        model_file = urlopen(
            'https://raw.githubusercontent.com/remla25-team3/model-training/refs/heads/main' +
            '/models/sentiment_model.pkl'
        )
        self.prediction_model = joblib.load(model_file)

        # Sentiments model to transform string inputs into numbers
        sentiments_file = urlopen(
            'https://raw.githubusercontent.com/remla25-team3/model-training/refs/heads/main' +
            '/models/bow_sentiment_model.pkl'
        )
        self.sentiment_model = joblib.load(sentiments_file)

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

        preprocessed = [preprocess_text(user_input)] # Apply lib-ml preprocessing
        transformed = self.sentiment_model.transform(preprocessed).toarray()
        x = np.array(transformed, dtype=object).reshape(1, -1)
        predictions = self.prediction_model.predict(x)

        if len(predictions) == 0:
            raise Exception('Error generating prediction')

        sentiment = "positive" if predictions[0] == 1 else "negative"
        return sentiment
