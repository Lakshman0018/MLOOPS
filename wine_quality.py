import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def load_data():
    df = pd.read_csv("WineQT.csv")

    X = df.drop(columns=["quality", "Id"])
    y = df["quality"]

    return X, y


def train_model():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model, X_test, y_test


def evaluate_model():
    model, X_test, y_test = train_model()

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    return accuracy


if __name__ == "__main__":
    accuracy = evaluate_model()
    print("Wine Quality Model Accuracy:", accuracy)
