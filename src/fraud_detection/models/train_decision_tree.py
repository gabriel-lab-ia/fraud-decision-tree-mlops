import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from fraud_detection.config import load_yaml_config
from fraud_detection.data.load_data import generate_synthetic_fraud_data, load_dataset
from fraud_detection.data.preprocessing import split_features_target
from fraud_detection.data.schemas import MODEL_FEATURE_COLUMNS, TARGET_COLUMN
from fraud_detection.data.validation import validate_training_data
from fraud_detection.features.feature_engineering import add_engineered_features
from fraud_detection.logging import get_logger
from fraud_detection.models.evaluate import evaluate_classifier

logger = get_logger(__name__)


def train_decision_tree(config_path: str = "configs/train_config.yaml") -> dict:
    config = load_yaml_config(config_path)

    sample_path = Path(config["data"]["sample_path"])
    processed_path = Path(config["data"]["processed_path"])
    model_path = Path(config["artifacts"]["model_path"])
    metrics_path = Path(config["artifacts"]["metrics_path"])

    if not sample_path.exists():
        logger.info("Synthetic dataset not found. Generating dataset.")
        generate_synthetic_fraud_data(
            output_path=sample_path,
            n_samples=config["data"]["n_samples"],
            random_state=config["data"]["random_state"],
        )

    data = load_dataset(sample_path)
    validate_training_data(data)

    data = add_engineered_features(data)

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(processed_path, index=False)

    X, y = split_features_target(data, TARGET_COLUMN)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config["data"]["test_size"],
        random_state=config["data"]["random_state"],
        stratify=y,
    )

    model_config = config["model"]

    model = DecisionTreeClassifier(
        max_depth=model_config["max_depth"],
        min_samples_split=model_config["min_samples_split"],
        min_samples_leaf=model_config["min_samples_leaf"],
        class_weight=model_config["class_weight"],
        random_state=model_config["random_state"],
    )

    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])

    experiment_name = config["mlflow"]["experiment_name"]
    artifact_location = config["mlflow"].get("artifact_location")

    experiment = mlflow.get_experiment_by_name(experiment_name)

    if experiment is None:
        mlflow.create_experiment(
            name=experiment_name,
            artifact_location=artifact_location,
        )

    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        metrics = evaluate_classifier(y_test, y_pred, y_proba)

        mlflow.log_params(
            {
                "model_type": "DecisionTreeClassifier",
                "max_depth": model_config["max_depth"],
                "min_samples_split": model_config["min_samples_split"],
                "min_samples_leaf": model_config["min_samples_leaf"],
                "class_weight": model_config["class_weight"],
                "feature_count": len(MODEL_FEATURE_COLUMNS),
            }
        )

        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, artifact_path="model")

        model_path.parent.mkdir(parents=True, exist_ok=True)
        metrics_path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(
            {
                "model": model,
                "feature_columns": MODEL_FEATURE_COLUMNS,
                "model_name": model_config["name"],
                "model_version": config["project"]["version"],
            },
            model_path,
        )

        with metrics_path.open("w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=2)

    logger.info("Model trained successfully.")
    logger.info("Metrics: %s", metrics)

    return metrics


if __name__ == "__main__":
    train_decision_tree()
