from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from fraud_detection.data.schemas import (
    FEATURE_COLUMNS,
    MODEL_FEATURE_COLUMNS,
    TARGET_COLUMN,
)

DATA_SCHEMA_VERSION = "transaction-dataset-v1"


@dataclass(frozen=True)
class DataQualityReport:
    schema_version: str
    record_count: int
    dataset_fingerprint: str
    target_distribution: dict[str, int]
    missing_percentages: dict[str, float]
    descriptive_statistics: dict[str, dict[str, float]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "record_count": self.record_count,
            "dataset_fingerprint": self.dataset_fingerprint,
            "target_distribution": self.target_distribution,
            "missing_percentages": self.missing_percentages,
            "descriptive_statistics": self.descriptive_statistics,
        }


def dataset_fingerprint(
    data: pd.DataFrame,
    schema_version: str = DATA_SCHEMA_VERSION,
) -> str:
    normalized = data.copy()
    normalized = normalized.reindex(sorted(normalized.columns), axis=1)
    payload = {
        "schema_version": schema_version,
        "columns": list(normalized.columns),
        "data": normalized.to_json(orient="split", index=False, double_precision=12),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def validate_dataset_contract(
    data: pd.DataFrame,
    *,
    allow_engineered: bool = False,
    minimum_class_count: int = 2,
) -> None:
    expected = {*FEATURE_COLUMNS, TARGET_COLUMN}
    if allow_engineered:
        expected |= set(MODEL_FEATURE_COLUMNS)

    missing = expected - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    unexpected = set(data.columns) - expected
    if unexpected:
        raise ValueError(f"Unexpected columns: {sorted(unexpected)}")

    if data.duplicated().any():
        raise ValueError("Dataset contains duplicate rows.")

    contract_columns = [*FEATURE_COLUMNS, TARGET_COLUMN]
    if data[contract_columns].isna().any().any():
        raise ValueError("Dataset contains missing values.")

    numeric = data[contract_columns].apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any():
        raise ValueError("Dataset contains non-numeric values in numeric columns.")
    if not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("Dataset contains infinite values.")

    if (numeric["transaction_amount"] < 0).any():
        raise ValueError("transaction_amount must be non-negative.")
    if (~numeric["transaction_hour"].between(0, 23)).any():
        raise ValueError("transaction_hour must be between 0 and 23.")
    if (numeric["customer_age_days"] < 0).any():
        raise ValueError("customer_age_days must be non-negative.")
    if (numeric["num_previous_transactions"] < 0).any():
        raise ValueError("num_previous_transactions must be non-negative.")
    for column in ["merchant_risk_score", "device_risk_score"]:
        if (~numeric[column].between(0, 1)).any():
            raise ValueError(f"{column} must be between 0 and 1.")

    target_values = set(numeric[TARGET_COLUMN].astype(int).unique())
    if not target_values.issubset({0, 1}):
        raise ValueError("Target column must be binary.")

    counts = numeric[TARGET_COLUMN].astype(int).value_counts()
    if set(counts.index) != {0, 1}:
        raise ValueError("Dataset must contain both target classes.")
    if int(counts.min()) < minimum_class_count:
        raise ValueError("Dataset has an extreme class imbalance for this profile.")


def build_data_quality_report(data: pd.DataFrame) -> DataQualityReport:
    numeric = data.select_dtypes(include=["number"])
    descriptive = {
        column: {
            "mean": float(values.mean()),
            "std": float(values.std(ddof=0)),
            "min": float(values.min()),
            "max": float(values.max()),
        }
        for column, values in numeric.items()
    }
    target_counts = data[TARGET_COLUMN].value_counts().sort_index()
    return DataQualityReport(
        schema_version=DATA_SCHEMA_VERSION,
        record_count=len(data),
        dataset_fingerprint=dataset_fingerprint(data),
        target_distribution={str(int(k)): int(v) for k, v in target_counts.items()},
        missing_percentages={
            column: float(value) for column, value in data.isna().mean().items()
        },
        descriptive_statistics=descriptive,
    )
