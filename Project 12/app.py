from pathlib import Path
import logging
import sys
import time
import uuid

import joblib
import pandas as pd
from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from werkzeug.exceptions import HTTPException

MODEL_PATH = Path(__file__).resolve().parent / "wine_quality_model.pkl"
FEATURES = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
]

HTTP_REQUESTS = Counter(
    "wine_quality_api_http_requests_total",
    "Total HTTP requests received by the Wine Quality Prediction API",
    ["method", "path", "status"],
)

HTTP_LATENCY = Histogram(
    "wine_quality_api_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)

PREDICTIONS = Counter(
    "wine_quality_api_predictions_total",
    "Total Wine Quality prediction attempts",
    ["result"],
)

MODEL_LOADED = Gauge(
    "wine_quality_api_model_loaded",
    "Whether the Wine Quality model is loaded",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
logger = logging.getLogger("wine-quality-api")
app = Flask(__name__)


def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        MODEL_LOADED.set(1)
        logger.info("event=model_loaded model_file=%s", MODEL_PATH.name)
        return model
    except Exception:
        MODEL_LOADED.set(0)
        logger.exception("event=model_load_failed model_file=%s", MODEL_PATH.name)
        raise


MODEL = load_model()


@app.before_request
def start_request():
    g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    g.request_start = time.perf_counter()


@app.after_request
def observe_request(response):
    request_id = getattr(g, "request_id", str(uuid.uuid4()))
    start = getattr(g, "request_start", None)
    duration = (time.perf_counter() - start) if start is not None else 0.0
    path = request.path
    method = request.method
    status = str(response.status_code)

    if path != "/metrics":
        HTTP_REQUESTS.labels(method=method, path=path, status=status).inc()
        HTTP_LATENCY.labels(method=method, path=path).observe(duration)

    level = logging.WARNING if response.status_code >= 400 else logging.INFO
    logger.log(
        level,
        "event=http_request request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
        request_id,
        method,
        path,
        status,
        duration * 1000,
    )
    response.headers["X-Request-ID"] = request_id
    return response


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(Exception)
def unexpected_error(error):
    if isinstance(error, HTTPException):
        return error
    logger.exception(
        "event=runtime_error request_id=%s error_type=%s",
        getattr(g, "request_id", None),
        type(error).__name__,
    )
    return jsonify({"error": "Internal server error"}), 500


@app.get("/")
def root():
    return jsonify({"status": "ok", "service": "wine-quality-prediction"})


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), headers={"Content-Type": CONTENT_TYPE_LATEST})


@app.post("/predict")
def predict():
    request_id = getattr(g, "request_id", None)
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            logger.warning(
                "event=validation_error request_id=%s path=/predict reason=json_body_required",
                request_id,
            )
            return jsonify({"error": "JSON request body is required"}), 400

        missing = [feature for feature in FEATURES if feature not in data]
        if missing:
            logger.warning(
                "event=validation_error request_id=%s path=/predict missing_fields=%s",
                request_id,
                missing,
            )
            return jsonify({"error": "Missing required fields", "missing_fields": missing}), 400

        sample = pd.DataFrame([{feature: data[feature] for feature in FEATURES}])
        prediction = int(MODEL.predict(sample)[0])
        PREDICTIONS.labels(result="success").inc()
        logger.info(
            "event=prediction_success request_id=%s prediction=%s",
            request_id,
            prediction,
        )
        return jsonify({"prediction": prediction, "prediction_code": prediction})
    except Exception:
        PREDICTIONS.labels(result="error").inc()
        logger.exception("event=prediction_failed request_id=%s", request_id)
        return jsonify({"error": "Prediction failed"}), 500


if __name__ == "__main__":
    logger.info("event=service_start host=0.0.0.0 port=5000")
    app.run(host="0.0.0.0", port=5000)
