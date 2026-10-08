import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split


DATASET_PATH = Path(__file__).resolve().parents[1] / "Project 1" / "WineQT.csv"
MODEL_PATH = Path(__file__).resolve().parent / "wine_quality_model.pkl"
METRICS_PATH = Path(__file__).resolve().parent / "metrics.json"


def load_data():
    print("Loading WineQT.csv...")
    data = pd.read_csv(DATASET_PATH)

    required_columns = {"quality", "Id"}
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    X = data.drop(columns=["quality", "Id"])
    y = data["quality"]

    print("Dataset loaded successfully.")
    print("Number of records:", len(data))
    print("Number of features:", len(X.columns))

    return X, y


def train_model():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("Training records:", len(X_train))
    print("Testing records :", len(X_test))

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    print("Training Wine Quality model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)

    print("\nModel Evaluation")
    print("----------------")
    print("Accuracy:", round(accuracy, 4))
    print("\nConfusion Matrix:")
    print(matrix)

    joblib.dump(model, MODEL_PATH)
    print("\nModel saved as wine_quality_model.pkl")

    metrics = {
        "accuracy": float(accuracy),
        "training_records": int(len(X_train)),
        "testing_records": int(len(X_test)),
        "classes": [int(value) for value in model.classes_]
    }

    with open(METRICS_PATH, "w") as file:
        json.dump(metrics, file, indent=4)

    print("Metrics saved as metrics.json")
    return accuracy


if __name__ == "__main__":
    train_model()
