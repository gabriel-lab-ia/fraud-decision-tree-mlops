import json
import math
from pathlib import Path
from typing import Any, cast

from fraud_detection.config import load_yaml_config


def validate_metrics(
    metrics_path: str | Path = "reports/metrics.json",
    config_path: str | Path = "configs/train_config.yaml",
) -> dict:
    path = Path(metrics_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Metrics file not found at {path}. Run training first."
        )

    metrics = cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    gates = load_yaml_config(config_path)["validation_gates"]
    failures = []
    comparisons = {
        "recall": (metrics.get("recall"), gates["minimum_recall"], ">="),
        "f1_score": (metrics.get("f1_score"), gates["minimum_f1"], ">="),
        "roc_auc": (metrics.get("roc_auc"), gates["minimum_roc_auc"], ">="),
        "pr_auc": (metrics.get("pr_auc"), gates["minimum_pr_auc"], ">="),
        "false_negative_rate": (
            metrics.get("false_negative_rate"),
            gates["maximum_false_negative_rate"],
            "<=",
        ),
        "brier_score": (metrics.get("brier_score"), gates["maximum_brier_score"], "<="),
    }
    for name, (value, threshold, operator) in comparisons.items():
        if value is None or not math.isfinite(float(value)):
            failures.append(f"{name} is missing or non-finite")
        elif operator == ">=" and value < threshold:
            failures.append(f"{name}={value:.4f} < {threshold:.4f}")
        elif operator == "<=" and value > threshold:
            failures.append(f"{name}={value:.4f} > {threshold:.4f}")

    dummy_pr_auc = metrics.get("baselines", {}).get("dummy", {}).get("pr_auc", 0)
    if metrics.get("pr_auc", 0) <= dummy_pr_auc:
        failures.append("Decision Tree PR-AUC must exceed DummyClassifier PR-AUC")

    if failures:
        raise RuntimeError("Model validation failed: " + ", ".join(failures))

    print("Model validation passed:", metrics)
    return metrics


if __name__ == "__main__":
    validate_metrics()
