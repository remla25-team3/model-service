from flask import Flask, request
from flasgger import Swagger
from libversion.version_util import VersionUtil

from src.predictor import ReviewSentimentPredictor

app = Flask(__name__)
swagger = Swagger(app)

predictor = ReviewSentimentPredictor()


@app.route('/predict', methods=['POST'])
def get_prediction():
	"""
	Predicts the sentiment of an input review.
	---
	parameters:
	  - name: input
	    in: body
	    description: JSON with 'review' key and the user review as value.
	    required: true
	responses:
		200:
			description: Prediction result ("positive" or "negative").
		500:
			description: Exception description.
	"""
	msg = request.get_json()
	if not 'review' in msg:
		return 'JSON payload should contain "review" key', 400

	review = msg['review']
	try:
		prediction = predictor.predict(review)
		return prediction
	except Exception as e:
		return str(e), 500


app.run(host="0.0.0.0", port=5000)
