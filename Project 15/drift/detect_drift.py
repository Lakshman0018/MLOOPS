from pathlib import Path
import json

import pandas as pd
from scipy.stats import ks_2samp

PROJECT_DIR = Path(__file__).resolve().parents[1]
DRIFT_DIR = PROJECT_DIR / "drift"
REFERENCE = DRIFT_DIR / "reference_data.csv"
CURRENT = DRIFT_DIR / "current_data.csv"
REPORT = DRIFT_DIR / "drift_report.json"

P_VALUE_THRESHOLD = 0.05
MIN_DRIFTED_FEATURES = 2


def main():
    if not REFERENCE.exists() or not CURRENT.exists():
        raise FileNotFoundError(
            "Reference/current data missing. Run prepare_reference.py and simulate_current_data.py first."
        )

    reference = pd.read_csv(REFERENCE)
    current = pd.read_csv(CURRENT)

    if list(reference.columns) != list(current.columns):
        raise ValueError("Reference and current batches must have identical feature columns.")

    results = {}
    drifted_features = []

    for feature in reference.columns:
        ref_values = pd.to_numeric(reference[feature], errors="coerce").dropna()
        cur_values = pd.to_numeric(current[feature], errors="coerce").dropna()
        if len(ref_values) < 2 or len(cur_values) < 2:
            raise ValueError(f"Not enough numeric observations for feature: {feature}")

        statistic, p_value = ks_2samp(ref_values, cur_values)
        flagged = bool(p_value < P_VALUE_THRESHOLD)

        results[feature] = {
            "ks_statistic": round(float(statistic), 6),
            "p_value": round(float(p_value), 8),
            "drift_detected": flagged,
            "reference_mean": round(float(ref_values.mean()), 6),
            "current_mean": round(float(cur_values.mean()), 6),
            "reference_rows": int(len(ref_values)),
            "current_rows": int(len(cur_values)),
        }
        if flagged:
            drifted_features.append(feature)

    overall_drift = len(drifted_features) >= MIN_DRIFTED_FEATURES
    report = {
        "dataset": "WineQT",
        "target_column": "quality",
        "method": "two-sample Kolmogorov-Smirnov test",
        "p_value_threshold": P_VALUE_THRESHOLD,
        "min_drifted_features": MIN_DRIFTED_FEATURES,
        "drifted_feature_count": len(drifted_features),
        "drifted_features": drifted_features,
        "overall_drift": overall_drift,
        "features": results,
    }

    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print("Drift report:", REPORT)


if __name__ == "__main__":
    main()
