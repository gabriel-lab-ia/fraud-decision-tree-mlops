import json
from pathlib import Path

from fraud_detection.config import get_settings

MINIMUM_RECALL = 0.50
MINIMUM_F1 = 0.35
MINIMUM_ROC_AUC = 0.60


def validate_metrics(metrics_path: str | Path) -> dict:
    path = Path(metrics_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Metrics file not found at {path}. Run training first."
        )

    with path.open(encoding="utf-8") as file:
        metrics = json.load(file)

    thresholds = {
        "recall": MINIMUM_RECALL,
        "f1_score": MINIMUM_F1,
        "roc_auc": MINIMUM_ROC_AUC,
    }
    failures = [
        f"{name}={metrics.get(name, 0):.4f} < {minimum:.4f}"
        for name, minimum in thresholds.items()
        if metrics.get(name, 0) < minimum
    ]
    if failures:
        raise RuntimeError("Model validation failed: " + ", ".join(failures))

    print("Model validation passed:", metrics)
    return metrics


if __name__ == "__main__":
    validate_metrics(get_settings().metrics_path)
