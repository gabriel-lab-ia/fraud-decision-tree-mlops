from __future__ import annotations

import numpy as np


def population_stability_index(
    expected: list[float],
    actual: list[float],
    buckets: int = 10,
) -> float:
    if len(expected) < buckets or len(actual) < buckets:
        raise ValueError("Not enough samples to compute PSI.")
    expected_array = np.asarray(expected, dtype=float)
    actual_array = np.asarray(actual, dtype=float)
    combined = np.concatenate([expected_array, actual_array])
    quantiles = np.quantile(combined, np.linspace(0, 1, buckets + 1))
    quantiles = np.unique(quantiles)
    if len(quantiles) < 3:
        raise ValueError("Reference distribution has insufficient variation.")
    expected_counts, _ = np.histogram(expected_array, bins=quantiles)
    actual_counts, _ = np.histogram(actual_array, bins=quantiles)
    expected_pct = np.clip(expected_counts / expected_counts.sum(), 1e-6, None)
    actual_pct = np.clip(actual_counts / actual_counts.sum(), 1e-6, None)
    psi_values = (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)
    return float(np.sum(psi_values))


def classify_psi(psi: float) -> str:
    if psi < 0.1:
        return "stable"
    if psi < 0.25:
        return "moderate_drift"
    return "significant_drift"
