# ML Lifecycle

1. The repository loads raw CSV data or generates a deterministic synthetic baseline.
2. Cleaning removes duplicates, coerces numeric fields, imputes values, and filters
   invalid ranges.
3. Validation checks required columns, missing values, and binary labels.
4. Shared feature engineering creates fraud-oriented signals.
5. The pipeline persists model-ready data and performs stratified train,
   validation, and test splits.
6. A class-balanced Decision Tree is trained, optionally calibrated, and evaluated.
7. The validation split selects a decision threshold.
8. Parameters, metrics, baselines, tags, and the sklearn model are logged to MLflow.
9. A joblib serving artifact, SHA-256 manifest, metrics JSON, data-quality report,
   reference profile, and evaluation summary are generated locally.
10. Validation gates recall, F1, ROC-AUC, PR-AUC, false-negative rate, calibration,
    and dummy-baseline lift before promotion.

GitHub Actions runs quality checks on every change and a model-validation workflow
when training-related files change.
