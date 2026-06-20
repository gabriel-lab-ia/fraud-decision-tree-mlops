# Model Governance

## Promotion Criteria

A candidate model is promotable only after `make train-ci` completes and
`scripts/validate_model.py` accepts the metrics in `reports/metrics.json`.

Current gates check recall, F1, ROC-AUC, PR-AUC, false-negative rate, Brier score,
and improvement over the dummy baseline.

## Artifact Contract

Serving artifacts use schema `fraud-model-artifact-v1`. Each artifact stores the
model, optional uncalibrated model, feature order, threshold, calibration method,
dataset fingerprint, training timestamp, Git metadata, metrics summary, and
runtime versions.

The sidecar manifest stores a SHA-256 hash. The API loader refuses incompatible
artifact schemas and manifest hash mismatches.

## Human Review

Every production promotion should include:

- Metrics review against the previous approved model.
- Data-quality report review.
- Drift and calibration review.
- Security review for artifact provenance.
- Clear rollback target.
