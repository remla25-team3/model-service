# model-service

`model-service` represents a wrapper service for the released ML model.
It is to be queried by `app-service` to pass model predictions to the front-end.

## Features

- Contains a pre-trained model for restaurant review sentiment prediction
- Integrates `lib-ml` for query pre-processing
- Automatic artifact release through a GitHub Actions workflow
- Unit tests are run automatically on each push through another workflow

## API usage

`model-service` exposes a REST API on port 5000 (_todo: configure DNS name and port in ENV variable_).
The following endpoint is available:

### `POST`

- `http://[domain]:[port]/predict`

  - Payload: `{"review": "some user review"}`
  - Returns: `"positive"` or `"negative"` classification

## How it works

This service uses a pre-trained model following the guidance in the [Restaurant Sentiment Analysis](https://github.com/proksch/restaurant-sentiment) project, available through the `model-training` service.
Input is first processed through the `lib-ml` service and then passed to the model for prediction.
The prediction is then returned.