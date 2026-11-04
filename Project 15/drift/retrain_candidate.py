from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

PROJECT_DIR = Path(__file__).resolve().parents[1]
DRIFT_DIR = PROJECT_DIR / "drift"
HISTORICAL = PROJECT_DIR / "WineQT.csv"
RECENT = DRIFT_DIR / "current_labeled_data.csv"
DRIFT_REPORT = DRIFT_DIR / "drift_report.json"
CANDIDATE_MODEL = DRIFT_DIR / "wine_quality_model_candidate.pkl"
METRICS_FILE = DRIFT_DIR / "retraining_metrics.json"
TARGET = "quality"
ID_COLUMN = "Id"


def main():
    if not DRIFT_REPORT.exists():
        raise FileNotFoundError("Run drift/detect_drift.py first.")

    report = json.loads(DRIFT_REPORT.read_text(encoding="utf-8"))
    if not report.get("overall_drift", False):
        print("No overall Wine Quality data drift detected.")
        print("Retraining skipped.")
        return

    if not RECENT.exists():
        raise FileNotFoundError(
            "Drift detected, but no labeled recent batch exists. "
            "For the classroom example run simulate_current_data.py --mode drift --make-labeled-batch."
        )

    historical = pd.read_csv(HISTORICAL)
    recent = pd.read_csv(RECENT)
    features = [
        column for column in historical.select_dtypes(include="number").columns
        if column not in {TARGET, ID_COLUMN}
    ]
    required = features + [TARGET]

    for label, frame in (("historical", historical), ("recent", recent)):
        missing = [column for column in required if column not in frame.columns]
        if missing:
            raise ValueError(f"{label} Wine Quality data missing columns: {missing}")

    combined = pd.concat([historical[required], recent[required]], ignore_index=True)
    combined = combined.dropna(subset=required)
    X = combined[features]
    y = combined[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Keep the Random Forest model family and settings used by Project 12.
    candidate = RandomForestClassifier(n_estimators=100, random_state=42)
    candidate.fit(X_train, y_train)
    predictions = candidate.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(candidate, CANDIDATE_MODEL)
    metrics = {
        "dataset": "WineQT",
        "candidate_accuracy": round(float(accuracy), 6),
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "historical_rows": int(len(historical)),
        "recent_labeled_rows": int(len(recent)),
        "features": features,
        "target": TARGET,
        "model": "RandomForestClassifier",
        "n_estimators": 100,
        "random_state": 42,
        "candidate_model": str(CANDIDATE_MODEL.name),
        "label_note": "Recent labels are a synthetic classroom demonstration unless replaced with verified production ground truth.",
    }
    METRICS_FILE.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print("Candidate model:", CANDIDATE_MODEL)


if __name__ == "__main__":
    main()
