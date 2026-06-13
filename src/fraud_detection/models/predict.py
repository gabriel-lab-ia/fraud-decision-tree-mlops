from pathlib import Path

import joblib
import pandas as pd

from fraud_detection.features.feature_engineering import add_engineered_features


def load_model_artifact(model_path: str | Path) -> dict:
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model artifact not found at {model_path}. Run training first."
        )

    artifact = joblib.load(model_path)

    required_keys = {"model", "feature_columns", "model_name", "model_version"}
    missing_keys = required_keys - set(artifact.keys())

    if missing_keys:
        raise ValueError(f"Invalid model artifact. Missing keys: {missing_keys}")

    return artifact


def predict_transaction(artifact: dict, features: dict) -> dict:
    data = pd.DataFrame([features])
    data = add_engineered_features(data)

    feature_columns = artifact["feature_columns"]
    model = artifact["model"]

    missing_columns = set(feature_columns) - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing prediction feature columns: {sorted(missing_columns)}"
        )

    data = data[feature_columns]

    prediction = int(model.predict(data)[0])
    probability = float(model.predict_proba(data)[0][1])

    return {
        "prediction": prediction,
        "label": "fraud" if prediction == 1 else "legitimate",
        "risk_score": probability,
        "model_name": artifact["model_name"],
        "model_version": artifact["model_version"],
    }
