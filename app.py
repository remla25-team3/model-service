import os
import logging
from flask import Flask, request, jsonify
from flasgger import Swagger
from versioning import get_version
from src.predictor.predict import ReviewSentimentPredictor

# Application setup
app = Flask(__name__)
app.config.update({
    'ENV': os.getenv('FLASK_ENV', 'production'),
    'DEBUG': os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1'),
    'HOST': os.getenv('FLASK_HOST', '0.0.0.0'),
    'PORT': int(os.getenv('FLASK_PORT', 5000))
})

# Logging Setup
logging.basicConfig(
    level=logging.DEBUG if app.config['DEBUG'] else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Automatic Versioning
app_version = get_version()
logger.info(f"Service Version: {app_version}")

# Swagger API Documentation
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "REMLA Sentiment Analysis API (Team 3)",
        "description": "API to predict the sentiment of restaurant reviews.",
        "version": app_version # Use the automatically fetched version
    }
}
swagger = Swagger(app, template=swagger_template)

# Model Loading
logger.info("Initializing the ReviewSentimentPredictor...")
predictor = ReviewSentimentPredictor()
logger.info("Predictor initialized successfully.")

# API Endpoints
@app.route("/health", methods=["GET"])
def health_check():
    """
    Checks the health of the service.
    ---
    tags:
      - Monitoring
    responses:
      200:
        description: Service is healthy and running.
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ok"
    """
    logger.info("Health check requested.")
    return jsonify({"status": "ok"})

@app.route("/version", methods=["GET"])
def version():
    """
    Returns the current version of the service.
    ---
    tags:
      - Monitoring
    responses:
      200:
        description: The service version, read automatically from the manifest file.
        schema:
          type: object
          properties:
            version:
              type: string
              example: "0.2.0"
    """
    logger.info(f"Version requested: {app_version}")
    return jsonify({"version": app_version})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predicts the sentiment and confidence score of a review.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [review]
          properties:
            review:
              type: string
              description: The review text to analyze.
              example: "The food was delicious!"
    responses:
      200:
        description: The prediction result with sentiment and confidence score.
        schema:
          type: object
          properties:
            sentiment:
              type: string
              example: "positive"
            confidence_score:
              type: number
              format: float
              example: 0.96
            review:
              type: string
      400:
        description: Bad Request (e.g., missing or invalid 'review' key).
    """
    json_data = request.get_json(silent=True)
    if not json_data or 'review' not in json_data:
        logger.error("Invalid request: 'review' key missing from JSON payload.")
        return jsonify({"error": "Missing 'review' key in request body"}), 400
    try:
        review_text = json_data['review']
        score = predictor.predict(review_text)
        sentiment_label = "positive" if score > 0.5 else "negative"
        response_payload = {
            "sentiment": sentiment_label,
            "confidence_score": score,
            "review": review_text
        }
        return jsonify(response_payload), 200
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred during prediction."}), 500

if __name__ == '__main__':
    logger.info(f"Starting Flask server on {app.config['HOST']}:{app.config['PORT']}...")
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )