# Model Service

This repository contains a production-ready Flask web service that serves a sentiment analysis model for restaurant reviews.

### System Architecture & How It Works

This `model-service` is designed to work as a specialized backend within a larger microservices architecture. It does not have its own user interface. Instead, it exposes a REST API to be consumed by other services, primarily the `app-service` which handles the main user-facing application.

The typical workflow is:
1.  A user interacts with the front-end, which is managed by the `app-service`.
2.  When a sentiment prediction is needed, the `app-service` sends the review text in a JSON payload to this `model-service`'s `/predict` endpoint.
3.  This service uses the shared `lib-ml` to preprocess the text, then passes it to the pre-trained model (downloaded from the `model-training` repository's releases) to get a prediction score.
4.  A structured JSON response, including the sentiment and confidence score, is returned to the `app-service`.



### 🚀 Features

* **Modular Architecture**: Follows a strong **separation of concerns**. The core ML logic is encapsulated in a self-contained `ReviewSentimentPredictor` class, while `app.py` handles web requests and API logic.
* **Dynamic Model Loading & Caching**: Models are downloaded on startup from a specified GitHub Release. A local caching mechanism saves models to a directory (e.g., `/tmp/models`), preventing re-downloads on every application start.
* **Automatic Service Versioning**: The service version is automatically read from the `.release-please-manifest.json` file in the project root, providing a single source of truth.
* **Rich REST API**: Provides a clean and intuitive API with three main endpoints:
    * `POST /predict`: Analyzes a review and returns a detailed JSON response with a `sentiment` label, a `confidence_score`, and the original `review`.
    * `GET /health`: A simple health check endpoint essential for monitoring in production environments.
    * `GET /version`: Automatically reports the current version of the deployed service.
* **Interactive API Documentation**: Auto-generates an interactive Swagger UI documentation page, available at `/apidocs`, allowing for easy testing directly from the browser.
* **Integrated Preprocessing**: Leverages the shared `lib-ml` library to perform text preprocessing, ensuring consistency between training and inference.
* **Continuous Integration**: Unit and API tests are automatically run on every push and pull request via a GitHub Actions workflow.
* **Automated Releases**: New versions of the service are drafted automatically based on Conventional Commits.

---

### Getting started with Docker

This application is designed to be run also as a Docker container using Docker Compose, which simplifies configuration and management.

#### Prerequisites
- Docker and Docker Compose must be installed and running on your system. (Docker Desktop includes both).

#### 1. Start the Service

With Docker Compose, you only need one command to build the image (if needed) and start the service. Run this from the project's root directory.

```bash
# This will start the service and show you the live logs.
docker-compose up

# To run the service in the background (detached mode), use:
docker-compose up -d
```

The first time you run this, it will take a moment to download the ML models. On subsequent runs, it will use the cached models instantly.

#### 2. Test the Running Service

Once the container is running, you can interact with the API.

A. **View the Interactive API Docs**:

  Open your web browser and navigate to the following URL:

  http://localhost:5000/apidocs

B. **Test with curl**:

Open a new terminal and send a request to the /predict endpoint:
```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"review": "The food was good."}'
```

#### 3. View Logs and Stop the Service

To view the logs (especially if running in detached -d mode):

```bash
docker-compose logs -f
```

To stop and remove the container and network completely:
```bash
docker-compose down # or press CTRL+C
```
