from pathlib import Path
import argparse

import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DRIFT_DIR = PROJECT_DIR / "drift"
SOURCE = PROJECT_DIR / "WineQT.csv"
REFERENCE = DRIFT_DIR / "reference_data.csv"
CURRENT = DRIFT_DIR / "current_data.csv"
LABELED_CURRENT = DRIFT_DIR / "current_labeled_data.csv"
TARGET = "quality"
ID_COLUMN = "Id"


def main():
    parser = argparse.ArgumentParser(
        description="Create a stable or synthetic drifted Wine Quality batch."
    )
    parser.add_argument("--mode", choices=["stable", "drift"], default="stable")
    parser.add_argument(
        "--make-labeled-batch",
        action="store_true",
        help="Also write a classroom-only batch with sampled source quality labels.",
    )
    args = parser.parse_args()

    if not SOURCE.exists() or not REFERENCE.exists():
        raise FileNotFoundError("Run python drift/prepare_reference.py first.")

    source = pd.read_csv(SOURCE)
    reference = pd.read_csv(REFERENCE)
    features = list(reference.columns)
    n = min(200, len(source))
    sampled = source.sample(n=n, replace=False, random_state=42).reset_index(drop=True)

    current = sampled[features].copy()
    rng = np.random.default_rng(42)

    # Small perturbation for both classroom modes.
    for column in features:
        scale = float(reference[column].std())
        noise_std = max(scale * 0.01, 1e-8)
        current[column] = current[column] + rng.normal(0, noise_std, size=len(current))

    if args.mode == "drift":
        # Deliberate synthetic shifts in selected wine-chemistry inputs.
        shifts = {
            "volatile acidity": 0.25,
            "alcohol": -1.25,
            "sulphates": 0.15,
        }
        for column, shift in shifts.items():
            if column in current.columns:
                current[column] = current[column] + shift

    current.to_csv(CURRENT, index=False)

    print("Wine Quality simulation mode:", args.mode)
    print("Rows:", len(current))
    print("Feature columns:", len(features))
    print("Current feature batch:", CURRENT)

    if args.make_labeled_batch:
        if TARGET not in sampled.columns:
            raise ValueError(f"Source dataset does not contain '{TARGET}'.")
        labeled = current.copy()
        # Labels are copied from the corresponding sampled WineQT rows.
        # This is only a controlled classroom demonstration, not real new ground truth.
        labeled[TARGET] = sampled[TARGET].to_numpy()
        labeled.to_csv(LABELED_CURRENT, index=False)
        print("CLASSROOM-ONLY labeled batch:", LABELED_CURRENT)
        print("Do not treat synthetic shifted rows/labels as production observations.")


if __name__ == "__main__":
    main()
