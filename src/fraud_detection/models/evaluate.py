from typing import Any

import numpy as np
import numpy.typing as npt
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    fbeta_score,
    log_loss,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_classifier(
    y_true: npt.NDArray[np.integer[Any]],
    y_proba: npt.NDArray[np.floating[Any]],
    threshold: float = 0.5,
) -> dict[str, Any]:
    y_pred = (y_proba >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    specificity = tn / (tn + fp) if tn + fp else 0.0
    false_positive_rate = fp / (fp + tn) if fp + tn else 0.0
    false_negative_rate = fn / (fn + tp) if fn + tp else 0.0
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "specificity": float(specificity),
        "f1_score": float(f1_score(y_true, y_pred, zero_division=0)),
        "fbeta_2": float(fbeta_score(y_true, y_pred, beta=2, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_proba)),
        "pr_auc": float(average_precision_score(y_true, y_proba)),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
        "false_positive_rate": float(false_positive_rate),
        "false_negative_rate": float(false_negative_rate),
        "brier_score": float(brier_score_loss(y_true, y_proba)),
        "log_loss": float(log_loss(y_true, y_proba, labels=[0, 1])),
        "prediction_rate": float(y_pred.mean()),
        "threshold": float(threshold),
        "support_0": int((y_true == 0).sum()),
        "support_1": int((y_true == 1).sum()),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
    }


def select_threshold(
    y_true: npt.NDArray[np.integer[Any]],
    y_proba: npt.NDArray[np.floating[Any]],
    strategy: str = "max_f1",
    fixed_threshold: float = 0.5,
    false_positive_cost: float = 1.0,
    false_negative_cost: float = 5.0,
) -> float:
    if strategy == "fixed":
        return fixed_threshold
    thresholds = [index / 100 for index in range(1, 100)]
    best_threshold = fixed_threshold
    best_score = float("-inf")
    for threshold in thresholds:
        y_pred = (y_proba >= threshold).astype(int)
        if strategy == "expected_cost":
            _tn, fp, fn, _tp = confusion_matrix(
                y_true,
                y_pred,
                labels=[0, 1],
            ).ravel()
            score = -((fp * false_positive_cost) + (fn * false_negative_cost))
        else:
            score = f1_score(y_true, y_pred, zero_division=0)
        if score > best_score:
            best_score = float(score)
            best_threshold = threshold
    return float(best_threshold)
