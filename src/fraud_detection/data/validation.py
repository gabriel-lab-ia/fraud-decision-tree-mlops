import pandas as pd

from fraud_detection.data.schemas import FEATURE_COLUMNS, TARGET_COLUMN


def validate_training_data(data: pd.DataFrame) -> None:
    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing_columns = set(required_columns) - set(data.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    if data[required_columns].isnull().any().any():
        raise ValueError("Dataset contains missing values.")

    unique_target_values = set(data[TARGET_COLUMN].unique())

    if not unique_target_values.issubset({0, 1}):
        raise ValueError(
            f"Target column must be binary. Found values: {unique_target_values}"
        )
