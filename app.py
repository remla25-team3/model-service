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
    'PORT': int(os.getenv('PORT', 5000))
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
        "title":       "Model Service: REMLA Team 3",
        "description": "Model Service APIs",
        "version":     app_version,
    },
    "basePath": "/model",
}
# swagger = Swagger(app, template=swagger_template)
swagger_config = {
    "headers": [],
    "specs_route": "/model/apidocs",
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/model/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True
        }
    ],
    "static_url_path": "/model/flasgger_static"
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Model Loading
logger.info("Initializing the ReviewSentimentPredictor...")
predictor = ReviewSentimentPredictor()
logger.info("Predictor initialized successfully.")

# API Endpoints
@app.route("/health", methods=["GET"])
def health_check():
    """
    Health Check Endpoint
    ---
    summary: Check service health
    description: Returns the status of the model-service to verify it's running.
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
    Service Version Endpoint
    ---
    summary: Get current service version
    description: Returns the current version of the model-service, auto-read from the manifest file.
    tags:
      - Monitoring
    responses:
      200:
        description: The service version details.
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
    Sentiment Prediction Endpoint
    ---
    summary: Predict sentiment of a restaurant review
    description: |
      Accepts a JSON payload containing a 'review' string and returns a
      sentiment label (positive/negative) along with a confidence score.
    tags:
      - Prediction
    parameters:
      - name: review
        in: body
        required: true
        description: The review text to analyze.
        schema:
          type: object
          required:
            - review
          properties:
            review:
              type: string
              example: "The food was delicious!"
    responses:
      200:
        description: Prediction result with sentiment and confidence score.
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
        description: Bad Request (missing or invalid 'review' key).
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing 'review' key in request body"
      500:
        description: Internal Server Error during prediction.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An internal error occurred during prediction."
    """
    json_data = request.get_json(silent=True)
    if not json_data or 'review' not in json_data:
        logger.error("Invalid request: 'review' key missing from JSON payload.")
        return jsonify({"error": "Missing 'review' key in request body"}), 400
    try:
        review_text = json_data['review']
        raw_score = predictor.predict(review_text)
        
        if raw_score > 0.5:
            sentiment_label = "positive"
            confidence = raw_score
        else:
            sentiment_label = "negative"
            # For a negative prediction, the confidence is 1 minus the raw score
            confidence = 1 - raw_score
            
        response_payload = {
            "sentiment": sentiment_label,
            "confidence_score": confidence,
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