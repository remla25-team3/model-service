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


@app.route("/version", methods=["GET"])
def get_lib_version():
	"""
	Gets the version from the lib-version package.
	---
	responses:
		200:
			description: Version (v#.#.#) from lib-version.
		500:
			description: Version could not be retrieved.
	"""
	try:
		return VersionUtil.get_version()
	except Exception as e:
		print(e)
		return "Version not found", 500

app.run(host="0.0.0.0", port=8080)
