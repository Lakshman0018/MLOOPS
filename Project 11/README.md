# Project 11 - Wine Quality Logging and Error Tracking

Practical 11 adds application logging and error tracking to the deployed Wine Quality Flask API from Project 10.

## New observability features

- INFO, WARNING and ERROR style logging
- Model load/startup events
- Request ID generation and propagation through X-Request-ID
- HTTP method, path, status and response-time logging
- Safe prediction request logging
- Validation-error logging for invalid /predict requests
- Missing-route (404) tracking
- Runtime and prediction failure logging
- Docker stdout logging for Render collection

## Continuity

The same Wine Quality dataset, RandomForest model, Flask API routes, Docker image pattern, GHCR package and Render service are reused. The ML model itself is not changed.

## API

- GET /
- GET /health
- POST /predict

## CI/CD

The separate Project 11 GitHub Actions workflow trains the model, runs tests, builds the Docker image, verifies logging events, and publishes the tested image to the existing GHCR package.

Package:
ghcr.io/lakshman0018/wine-quality-ml:latest
