from pathlib import Path

import yaml

from fraud_detection.models.train_decision_tree import train_decision_tree


def test_training_writes_model_metrics_and_mlflow_run(tmp_path):
    config = {
        "project": {"name": "test", "version": "0.1.0"},
        "data": {
            "sample_path": str(tmp_path / "sample.csv"),
            "processed_path": str(tmp_path / "processed.csv"),
            "target_column": "is_fraud",
            "n_samples": 300,
            "test_size": 0.2,
            "random_state": 42,
        },
        "model": {
            "name": "decision_tree_fraud_detector",
            "max_depth": 6,
            "min_samples_split": 10,
            "min_samples_leaf": 5,
            "class_weight": "balanced",
            "random_state": 42,
        },
        "mlflow": {
            "tracking_uri": f"sqlite:///{tmp_path / 'mlflow.db'}",
            "artifact_location": str(tmp_path / "mlartifacts"),
            "experiment_name": "test_experiment",
        },
        "artifacts": {
            "model_path": str(tmp_path / "model.joblib"),
            "metrics_path": str(tmp_path / "metrics.json"),
        },
    }
    config_path = tmp_path / "train.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

    metrics = train_decision_tree(config_path)

    assert Path(config["artifacts"]["model_path"]).exists()
    assert Path(config["artifacts"]["metrics_path"]).exists()
    assert set(metrics) == {"accuracy", "precision", "recall", "f1_score", "roc_auc"}
