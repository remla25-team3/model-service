import pandas as pd
import os
import joblib
import urllib.request
from lib_ml.preprocessing import preprocess

class ReviewSentimentPredictor:
    """Predicts sentiment probability from a single restaurant review."""
    def __init__(self):
        """
        Initializes the predictor by dynamically constructing the download URLs from
        environment variables and then loading the models.
        """
        # Read configuration from environment variables, with sensible defaults.
        base_url = os.getenv('RESOURCE_URL', 'https://github.com/remla25-team3/model-training/releases/download/')
        model_version = os.getenv('MODEL_VERSION', 'v0.2.3')
        model_filename = os.getenv('MODEL', 'sentiment_model.pkl')
        vectorizer_filename = os.getenv('CV', 'bow_sentiment_model.pkl')

        # Construct the full URLs dynamically
        model_url = f"{base_url.strip('/')}/{model_version}/{model_filename}"
        vectorizer_url = f"{base_url.strip('/')}/{model_version}/{vectorizer_filename}"

        model_dir = os.getenv("MODEL_DIR", "/tmp/models")

        self.model = self.download_and_load(model_url, model_dir, model_filename)
        self.vectorizer = self.download_and_load(vectorizer_url, model_dir, vectorizer_filename)

    def download_and_load(self, url: str, path: str, filename: str):
        """
        Downloads a file from a URL to a local path if it doesn't exist,
        then loads it with joblib.
        """
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join(path, filename)

        if not os.path.exists(filepath):
            print(f"Downloading {filename} from {url} to {filepath}...")
            urllib.request.urlretrieve(url, filepath)
            print("Download complete.")
        else:
            print(f"Model {filename} already exists at {filepath}. Skipping download.")
        
        return joblib.load(filepath)


    def predict(self, user_input: str):
        """
        Predicts the sentiment of the given user review.
        :param user_input: A single string representing a user's restaurant review
        :Returns:
            float: A probability score between 0.0 and 1.0 that the review is positive.
        """
        if not isinstance(user_input, str) or not user_input.strip():
            raise ValueError("Input must be a non-empty string.")

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
    