from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request


app = Flask(__name__)

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


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "wine_quality_model.pkl was not found. Run train_model.py first."
        )
    return joblib.load(MODEL_PATH)


@app.get("/")
def health_check():
    return jsonify({
        "status": "ok",
        "service": "wine-quality-prediction",
    })


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON request body is required"}), 400

    missing_fields = [feature for feature in FEATURES if feature not in data]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields,
        }), 400

    sample = pd.DataFrame([{feature: data[feature] for feature in FEATURES}])

    model = load_model()
    prediction = int(model.predict(sample)[0])

    return jsonify({
        "prediction": prediction,
        "prediction_code": prediction,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
