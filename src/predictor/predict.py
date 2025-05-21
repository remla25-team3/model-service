import numpy as np
import joblib
from urllib.request import urlopen
from lib_ml.preprocessing import preprocess_text

class ReviewSentimentPredictor:
    def __init__(self):
        # Load trained model to generate predictions with
        model_file = urlopen(
            'https://github.com/remla25-team3/model-training/raw/refs/heads/main' +
            '/model_training/models/sentiment_model.pkl'
        )
        self.prediction_model = joblib.load(model_file)

        # Sentiments model to transform string inputs into numbers
        sentiments_file = urlopen(
            'https://github.com/remla25-team3/model-training/raw/refs/heads/main' +
            '/model_training/models/bow_sentiment_model.pkl'
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

        preprocessed = [preprocess_text(user_input)]
        transformed = self.sentiment_model.transform(preprocessed).toarray()
        X = np.array(transformed, dtype=object).reshape(1, -1) # Apply lib-ml preprocessing
        predictions = self.prediction_model.predict(X)

        if len(predictions) == 0:
            raise Exception('Error generating prediction')

        sentiment = "positive" if predictions[0] == 1 else "negative"
        return sentiment
