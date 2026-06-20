from pathlib import Path

import pandas as pd

from fraud_detection.features.feature_engineering import add_engineered_features
from fraud_detection.models.artifact import load_artifact_with_validation


def load_model_artifact(
    model_path: str | Path,
    manifest_path: str | Path | None = None,
) -> dict:
    return load_artifact_with_validation(model_path, manifest_path)


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

    probability = float(model.predict_proba(data)[0][1])
    threshold = float(artifact.get("decision_threshold", 0.5))
    prediction = int(probability >= threshold)

    return {
        "prediction": prediction,
        "label": "fraud" if prediction == 1 else "legitimate",
        "risk_score": probability,
        "decision_threshold": threshold,
        "model_name": artifact["model_name"],
        "model_version": artifact["model_version"],
        "artifact_schema_version": artifact.get("artifact_schema_version"),
    }
