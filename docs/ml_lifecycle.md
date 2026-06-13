# ML Lifecycle

1. The repository loads raw CSV data or generates a deterministic synthetic baseline.
2. Cleaning removes duplicates, coerces numeric fields, imputes values, and filters
   invalid ranges.
3. Validation checks required columns, missing values, and binary labels.
4. Shared feature engineering creates fraud-oriented signals.
5. The pipeline persists model-ready data and performs a stratified train/test split.
6. A class-balanced Decision Tree is trained and evaluated.
7. Parameters, metrics, and the sklearn model are logged to SQLite-backed MLflow.
8. A joblib serving artifact and metrics JSON are generated locally.
9. Validation gates recall, F1, and ROC-AUC before promotion.

GitHub Actions runs quality checks on every change and a model-validation workflow
when training-related files change.
