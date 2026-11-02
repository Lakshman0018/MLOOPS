from pathlib import Path
import logging
import sys
import time
import uuid

import joblib
import pandas as pd
from flask import Flask, g, jsonify, request
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
logger = logging.getLogger("wine-quality-api")

app = Flask(__name__)
SAFE_INPUT_FIELDS = set()

def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        logger.info("event=model_loaded model_file=%s", MODEL_PATH.name)
        return model
    except Exception:
        logger.exception("event=model_load_failed model_file=%s", MODEL_PATH.name)
        raise

MODEL = load_model()

@app.before_request
def start_request():
    g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    g.request_start = time.perf_counter()

@app.after_request
def log_request(response):
    request_id = getattr(g, "request_id", str(uuid.uuid4()))
    start = getattr(g, "request_start", None)
    duration_ms = ((time.perf_counter() - start) * 1000) if start is not None else 0.0
    level = logging.WARNING if response.status_code >= 400 else logging.INFO
    logger.log(
        level,
        "event=http_request request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
        request_id,
        request.method,
        request.path,
        response.status_code,
        duration_ms,
    )
    response.headers["X-Request-ID"] = request_id
    return response

@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def internal_error(_error):
    return jsonify({"error": "Internal server error"}), 500

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
    return jsonify({'status': 'ok', 'service': 'wine-quality-prediction'})

@app.get("/health")
def health():
    return jsonify({'status': 'healthy'})

@app.post("/predict")
def predict():
    request_id = getattr(g, "request_id", None)
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            logger.warning("event=validation_error request_id=%s path=/predict reason=json_body_required", request_id)
            return jsonify({"error": "JSON request body is required"}), 400
        missing = [feature for feature in FEATURES if feature not in data]
        if missing:
            logger.warning("event=validation_error request_id=%s path=/predict missing_fields=%s", request_id, missing)
            return jsonify({"error": "Missing required fields", "missing_fields": missing}), 400
        safe_input = {key: data[key] for key in SAFE_INPUT_FIELDS if key in data}
        logger.info("event=prediction_request request_id=%s feature_names=%s safe_input=%s", request_id, sorted(data.keys()), safe_input)
        sample = pd.DataFrame([{feature: data[feature] for feature in FEATURES}])
        prediction = int(MODEL.predict(sample)[0])
        logger.info("event=prediction_success request_id=%s prediction=%s", request_id, prediction)
        return jsonify({"prediction": prediction, "prediction_code": prediction})
    except Exception:
        logger.exception("event=prediction_failed request_id=%s", request_id)
        return jsonify({"error": "Prediction failed"}), 500

if __name__ == "__main__":
    logger.info("event=service_start host=0.0.0.0 port=5000")
    app.run(host="0.0.0.0", port=5000)
