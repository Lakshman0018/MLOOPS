from pathlib import Path
import json
import shutil
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
DRIFT_DIR = PROJECT_DIR / "drift"
CANDIDATE = DRIFT_DIR / "wine_quality_model_candidate.pkl"
METRICS = DRIFT_DIR / "retraining_metrics.json"
APPROVED = PROJECT_DIR / "wine_quality_model_approved.pkl"

# Reuse the repository's established Project 03 minimum-accuracy quality gate.
MIN_ACCURACY = 0.70


def main():
    if not CANDIDATE.exists() or not METRICS.exists():
        raise FileNotFoundError("Candidate model/metrics missing. Run retrain_candidate.py first.")

    metrics = json.loads(METRICS.read_text(encoding="utf-8"))
    accuracy = float(metrics["candidate_accuracy"])

    print("Wine Quality candidate accuracy:", round(accuracy, 4))
    print("Required accuracy:", MIN_ACCURACY)

    if accuracy < MIN_ACCURACY:
        print("QUALITY GATE: FAIL")
        print("No approved Project 15 model was updated.")
        sys.exit(1)

    shutil.copy2(CANDIDATE, APPROVED)
    print("QUALITY GATE: PASS")
    print("Approved Project 15 model:", APPROVED)
    print("Project 12 production model and deployment files remain untouched.")


if __name__ == "__main__":
    main()
