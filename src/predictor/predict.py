import pandas as pd
import joblib
from urllib.request import urlopen
from lib_ml.preprocessing import preprocess

class ReviewSentimentPredictor:
    """Predicts sentiment probability from a single restaurant review."""
    def __init__(self):
        """
        Initializes the predictor by downloading and loading the sentiment model
        and the Bag-of-Words vectorizer from the v0.2.3 release.
        """
        # URLs pointing to the specific assets from the v0.2.3 release
        model_url = 'https://github.com/remla25-team3/model-training/releases/download/v0.2.3/sentiment_model.pkl'
        vectorizer_url = 'https://github.com/remla25-team3/model-training/releases/download/v0.2.3/bow_sentiment_model.pkl'

        # Load the prediction model from the URL
        model_file = urlopen(model_url)
        self.model = joblib.load(model_file)

        # Load the BoW vectorizer from the URL
        vectorizer_file = urlopen(vectorizer_url)
        self.vectorizer = joblib.load(vectorizer_file)


    def predict(self, user_input: str):
        """
        Predicts the sentiment of the given user review.
        :param user_input: A single string representing a user's restaurant review
        :Returns:
            float: A probability score between 0.0 and 1.0 that the review is positive.
        """
        if not isinstance(user_input, str):
            raise ValueError('Input must be a string')
        if user_input == '':
            raise ValueError('Input should not be empty')

        # Create a DataFrame to match the expected input format of the new `preprocess` function.
        input_df = pd.DataFrame([user_input], columns=['Review'])
        corpus, _ = preprocess(input_df, inference=True)

        if not corpus:
            raise Exception("Text preprocessing resulted in an empty corpus.")

        cleaned_text = corpus[0]

        # Transform the preprocessed text into a feature array.
        features_array = self.vectorizer.transform([cleaned_text]).toarray()
        feature_names = self.vectorizer.get_feature_names_out()
        features_df = pd.DataFrame(features_array, columns=feature_names)
        probabilities = self.model.predict_proba(features_df)[0]

        return probabilities[1]
    