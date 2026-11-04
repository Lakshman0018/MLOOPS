from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_DIR / "WineQT.csv"
DRIFT_DIR = PROJECT_DIR / "drift"
OUTPUT = DRIFT_DIR / "reference_data.csv"

TARGET = "quality"
ID_COLUMN = "Id"


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Wine Quality dataset not found: {SOURCE}")

    DRIFT_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(SOURCE)

    if TARGET not in data.columns:
        raise ValueError(f"Expected target column '{TARGET}' in WineQT.csv")

    features = data.drop(columns=[TARGET, ID_COLUMN], errors="ignore")
    numeric_features = features.select_dtypes(include="number")
    if numeric_features.empty:
        raise ValueError("No numeric Wine Quality input features were found.")

    reference = numeric_features.dropna().copy()
    reference.to_csv(OUTPUT, index=False)

    print("Wine Quality reference dataset created.")
    print("Rows:", len(reference))
    print("Features:", list(reference.columns))
    print("File:", OUTPUT)


if __name__ == "__main__":
    main()
