import pandas as pd

from fraud_detection.data.schemas import MODEL_FEATURE_COLUMNS


def select_model_features(data: pd.DataFrame) -> pd.DataFrame:
    missing_columns = set(MODEL_FEATURE_COLUMNS) - set(data.columns)

    if missing_columns:
        raise ValueError(f"Missing model feature columns: {sorted(missing_columns)}")

    return data[MODEL_FEATURE_COLUMNS]


def split_features_target(
    data: pd.DataFrame,
    target_column: str,
) -> tuple[pd.DataFrame, pd.Series]:
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")

    features = select_model_features(data)
    target = data[target_column]

    return features, target
