import json
import subprocess  # nosec B404
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import mlflow
import mlflow.sklearn
from sklearn.calibration import CalibratedClassifierCV
from sklearn.dummy import DummyClassifier
from sklearn.frozen import FrozenEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from fraud_detection._version import get_project_version
from fraud_detection.config import load_yaml_config
from fraud_detection.data.contract import (
    DATA_SCHEMA_VERSION,
    build_data_quality_report,
    validate_dataset_contract,
)
from fraud_detection.data.pipeline import build_training_dataset
from fraud_detection.data.preprocessing import split_features_target
from fraud_detection.data.repository import TransactionDataRepository
from fraud_detection.data.schemas import MODEL_FEATURE_COLUMNS, TARGET_COLUMN
from fraud_detection.data.splitting import (
    assert_no_split_overlap,
    split_train_validation_test,
)
from fraud_detection.logging import get_logger
from fraud_detection.models.artifact import (
    ARTIFACT_SCHEMA_VERSION,
    ModelArtifactMetadata,
    build_artifact,
    save_artifact_with_manifest,
)
from fraud_detection.models.evaluate import evaluate_classifier, select_threshold

logger = get_logger(__name__)


def get_git_value(args: list[str]) -> str | None:
    try:
        allowed_commands = {
            ("git", "rev-parse", "--short", "HEAD"),
            ("git", "branch", "--show-current"),
        }
        if tuple(args) not in allowed_commands:
            return None
        return subprocess.check_output(args, text=True).strip()  # nosec B603
    except Exception:
        return None


def fit_probability_model(
    model: Any,
    calibration_method: str,
    X_validation: Any,
    y_validation: Any,
) -> Any:
    if calibration_method == "sigmoid":
        calibrated = CalibratedClassifierCV(
            FrozenEstimator(model),
            method="sigmoid",
        )
        calibrated.fit(X_validation, y_validation)
        return calibrated
    return model


def train_decision_tree(config_path: str = "configs/train_config.yaml") -> dict:
    start = time.perf_counter()
    config = load_yaml_config(config_path)
    project_version = get_project_version()

    data_config = config["data"]
    model_config = config["model"]
    training_config = config.get("training", {})
    artifact_config = config["artifacts"]

    model_path = Path(artifact_config["model_path"])
    metrics_path = Path(artifact_config["metrics_path"])
    manifest_path = Path(
        artifact_config.get("manifest_path", model_path.with_suffix(".manifest.json"))
    )
    data_quality_report_path = Path(
        artifact_config.get(
            "data_quality_report_path",
            metrics_path.with_name("data_quality_report.json"),
        )
    )
    reference_profile_path = Path(
        artifact_config.get(
            "reference_profile_path",
            metrics_path.with_name("reference_profile.json"),
        )
    )
    evaluation_summary_path = Path(
        artifact_config.get(
            "evaluation_summary_path",
            metrics_path.with_name("evaluation_summary.md"),
        )
    )

    repository = TransactionDataRepository(
        raw_path=data_config["sample_path"],
        processed_path=data_config["processed_path"],
    )

    data = build_training_dataset(
        repository=repository,
        n_samples=data_config["n_samples"],
        random_state=data_config["random_state"],
    )
    validate_dataset_contract(
        data,
        allow_engineered=True,
        minimum_class_count=data_config.get("minimum_class_count", 2),
    )
    data_quality_report = build_data_quality_report(data)

    train_data, validation_data, test_data = split_train_validation_test(
        data,
        target_column=TARGET_COLUMN,
        validation_size=data_config.get("validation_size", data_config["test_size"]),
        test_size=data_config["test_size"],
        random_state=data_config["random_state"],
    )
    assert_no_split_overlap(train_data, validation_data, test_data)

    X_train, y_train = split_features_target(train_data, TARGET_COLUMN)
    X_validation, y_validation = split_features_target(validation_data, TARGET_COLUMN)
    X_test, y_test = split_features_target(test_data, TARGET_COLUMN)

    model = DecisionTreeClassifier(
        max_depth=model_config["max_depth"],
        min_samples_split=model_config["min_samples_split"],
        min_samples_leaf=model_config["min_samples_leaf"],
        class_weight=model_config["class_weight"],
        random_state=model_config["random_state"],
    )
    model.fit(X_train, y_train)

    probability_model = fit_probability_model(
        model,
        model_config.get("calibration_method", "none"),
        X_validation,
        y_validation,
    )
    validation_proba = probability_model.predict_proba(X_validation)[:, 1]
    threshold = select_threshold(
        y_validation,
        validation_proba,
        strategy=model_config.get("threshold_strategy", "max_f1"),
        fixed_threshold=model_config.get("fixed_threshold", 0.5),
        false_positive_cost=model_config.get("false_positive_cost", 1.0),
        false_negative_cost=model_config.get("false_negative_cost", 5.0),
    )

    test_proba = probability_model.predict_proba(X_test)[:, 1]
    metrics = evaluate_classifier(y_test, test_proba, threshold)
    validation_metrics = evaluate_classifier(y_validation, validation_proba, threshold)

    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    dummy_metrics = evaluate_classifier(
        y_test,
        dummy.predict_proba(X_test)[:, 1],
        threshold,
    )
    logistic = LogisticRegression(max_iter=5000, class_weight="balanced").fit(
        X_train,
        y_train,
    )
    logistic_metrics = evaluate_classifier(
        y_test,
        logistic.predict_proba(X_test)[:, 1],
        threshold,
    )

    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
    experiment_name = config["mlflow"]["experiment_name"]
    if mlflow.get_experiment_by_name(experiment_name) is None:
        mlflow.create_experiment(
            name=experiment_name,
            artifact_location=config["mlflow"].get("artifact_location"),
        )
    mlflow.set_experiment(experiment_name)

    git_commit = get_git_value(["git", "rev-parse", "--short", "HEAD"])
    git_branch = get_git_value(["git", "branch", "--show-current"])
    training_profile = training_config.get("profile", "ci")

    with mlflow.start_run() as run:
        run_id = run.info.run_id
        mlflow.set_tags(
            {
                "project": config["project"]["name"],
                "project_version": project_version,
                "model_name": model_config["name"],
                "model_version": project_version,
                "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
                "training_profile": training_profile,
                "git_commit": git_commit or "",
                "git_branch": git_branch or "",
                "dataset_fingerprint": data_quality_report.dataset_fingerprint,
                "data_schema_version": DATA_SCHEMA_VERSION,
                "run_purpose": "v0.3-governed-training",
            }
        )
        mlflow.log_params(
            {
                "model_type": "DecisionTreeClassifier",
                "threshold_strategy": model_config.get("threshold_strategy", "max_f1"),
                "decision_threshold": threshold,
                "calibration_method": model_config.get("calibration_method", "none"),
                "feature_count": len(MODEL_FEATURE_COLUMNS),
                "train_size": len(train_data),
                "validation_size": len(validation_data),
                "test_size": len(test_data),
                **{key: value for key, value in model_config.items() if key != "type"},
            }
        )
        numeric_metrics = {
            key: value
            for key, value in metrics.items()
            if isinstance(value, int | float)
        }
        mlflow.log_metrics(numeric_metrics)
        mlflow.log_metrics(
            {
                f"validation_{key}": value
                for key, value in validation_metrics.items()
                if isinstance(value, int | float)
            }
        )
        mlflow.log_metrics(
            {
                "dummy_pr_auc": dummy_metrics["pr_auc"],
                "logistic_pr_auc": logistic_metrics["pr_auc"],
                "training_duration_seconds": time.perf_counter() - start,
            }
        )

        metadata = ModelArtifactMetadata(
            artifact_schema_version=ARTIFACT_SCHEMA_VERSION,
            model_name=model_config["name"],
            model_version=project_version,
            project_version=project_version,
            feature_columns=MODEL_FEATURE_COLUMNS,
            decision_threshold=threshold,
            calibration_method=model_config.get("calibration_method", "none"),
            dataset_fingerprint=data_quality_report.dataset_fingerprint,
            data_schema_version=DATA_SCHEMA_VERSION,
            training_timestamp_utc=datetime.now(UTC).isoformat(),
            training_run_id=run_id,
            git_commit=git_commit,
            metrics_summary={
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "roc_auc": metrics["roc_auc"],
                "pr_auc": metrics["pr_auc"],
                "brier_score": metrics["brier_score"],
            },
        )
        artifact = build_artifact(
            model=probability_model,
            uncalibrated_model=model,
            metadata=metadata,
        )
        manifest = save_artifact_with_manifest(artifact, model_path, manifest_path)

        metrics_payload = {
            **metrics,
            "validation": validation_metrics,
            "baselines": {
                "dummy": dummy_metrics,
                "logistic_regression": logistic_metrics,
            },
        }
        for path, payload in [
            (metrics_path, metrics_payload),
            (data_quality_report_path, data_quality_report.to_dict()),
            (reference_profile_path, data_quality_report.to_dict()),
        ]:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        evaluation_summary_path.parent.mkdir(parents=True, exist_ok=True)
        evaluation_summary_path.write_text(
            "\n".join(
                [
                    "# Evaluation Summary",
                    f"- threshold: {threshold:.3f}",
                    f"- recall: {metrics['recall']:.4f}",
                    f"- f1_score: {metrics['f1_score']:.4f}",
                    f"- roc_auc: {metrics['roc_auc']:.4f}",
                    f"- pr_auc: {metrics['pr_auc']:.4f}",
                    f"- dummy_pr_auc: {dummy_metrics['pr_auc']:.4f}",
                ]
            ),
            encoding="utf-8",
        )
        mlflow.log_dict(data_quality_report.to_dict(), "data_quality_report.json")
        mlflow.log_dict(manifest, "artifact_manifest.json")
        mlflow.sklearn.log_model(probability_model, artifact_path="model")

    logger.info("Model trained successfully.")
    logger.info("Metrics: %s", metrics)
    return metrics


if __name__ == "__main__":
    train_decision_tree()
