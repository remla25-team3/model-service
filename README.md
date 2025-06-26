# Model Service

This repository contains a production-ready Flask web service that serves a sentiment analysis model for restaurant reviews. It is a core component of the REMLA project architecture.

---

### 🏛️ Architecture & Communication

This `model-service` is designed to work as a specialized backend within a larger microservices architecture. It does not have its own user interface. Instead, it exposes a REST API to be consumed another service, the `app-service`, which handles the main user-facing application.

The typical workflow is:
1.  A user interacts with the `app-frontend`, which is a separate single-page application.
2.  The `app-frontend` sends API requests to the `app-service`.
3.  When a sentiment prediction is needed, the `app-service` forwards the review text to this `model-service`.
4.  This service uses a shared `lib-ml` to preprocess the text, then passes it to a pre-trained model to get a prediction score.
5.  A response, including the sentiment and confidence score, is returned to the `app-service`, which then passes it back to the `app-frontend`. 

---

### 🚀 Features

* **Modular Architecture**: Follows a strong **separation of concerns**. The core ML logic is encapsulated in a self-contained `ReviewSentimentPredictor` class, while `app.py` handles web requests and API logic.
* **Dynamic Model Loading & Caching**: Models are downloaded on startup from a specified GitHub Release. A local caching mechanism saves models to a directory (e.g., `/tmp/models`), preventing re-downloads on every application start.
* **Automatic Service Versioning**: The service version is automatically determined from project metadata, providing a single source of truth.
* **Rich REST API**: Provides a clean and intuitive API with three main endpoints.
* **Interactive API Documentation**: Auto-generates an interactive Swagger UI documentation page (`/apidocs`), allowing for easy exploration and testing of the API directly from a browser.
* **Integrated Preprocessing**: Leverages a shared `lib-ml` library to perform text preprocessing, ensuring consistency between training and inference.
* **Continuous Integration**: Unit and API tests are automatically run on every push and pull request via a GitHub Actions workflow.
* **Automated Releases**: New versions of the service are drafted automatically based on Conventional Commits.

---

### 📡 API Endpoints

The service provides three main endpoints:

* `POST /predict`: Analyzes a review and returns a detailed JSON response with a `sentiment` label and a `confidence_score`, which are then displayed to the user.
* `GET /version`: Automatically reports the current version of the deployed service.
* `GET /health`: A simple health check endpoint essential for monitoring in production environments.

---
