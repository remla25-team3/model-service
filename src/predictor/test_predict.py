from .predict import ReviewSentimentPredictor

if __name__ == "__main__":
    print("Initializing Predictor")
    # This will download and load the models from the URLs.
    predictor = ReviewSentimentPredictor()
    print("Predictor Initialized\n")

    review1 = "The food was absolutely wonderful"
    sentiment1 = predictor.predict(review1)
    print(f"Review: '{review1}'")
    print(f"Predicted positive score: {sentiment1}\n")

    review2 = "It was a terrible experience, very disappointing"
    sentiment2 = predictor.predict(review2)
    print(f"Review: '{review2}'")
    print(f"Predicted positive score: {sentiment2}")