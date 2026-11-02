import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "WineQT.csv"
MODEL_PATH = BASE_DIR / "wine_quality_model.pkl"
METRICS_PATH = BASE_DIR / "metrics.json"


def main():
    print("Loading WineQT.csv...")
    data = pd.read_csv(DATASET_PATH)

    X = data.drop(columns=["quality", "Id"])
    y = data["quality"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print("Training records:", len(X_train))
    print("Testing records :", len(X_test))

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    print("Training Wine Quality model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("Accuracy:", round(accuracy, 4))

    joblib.dump(model, MODEL_PATH)

    metrics = {
        "accuracy": float(accuracy),
        "training_records": int(len(X_train)),
        "testing_records": int(len(X_test)),
        "classes": [int(value) for value in model.classes_],
    }

    with open(METRICS_PATH, "w") as file:
        json.dump(metrics, file, indent=4)

    print("Model saved as wine_quality_model.pkl")
    print("Metrics saved as metrics.json")


if __name__ == "__main__":
    main()
