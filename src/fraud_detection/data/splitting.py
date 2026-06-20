from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split


def split_train_validation_test(
    data: pd.DataFrame,
    target_column: str,
    validation_size: float,
    test_size: float,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if validation_size <= 0 or test_size <= 0 or validation_size + test_size >= 1:
        raise ValueError(
            "validation_size and test_size must be positive and sum to < 1."
        )

    train_validation, test = train_test_split(
        data,
        test_size=test_size,
        random_state=random_state,
        stratify=data[target_column],
    )
    adjusted_validation_size = validation_size / (1 - test_size)
    train, validation = train_test_split(
        train_validation,
        test_size=adjusted_validation_size,
        random_state=random_state,
        stratify=train_validation[target_column],
    )
    return train.copy(), validation.copy(), test.copy()


def assert_no_split_overlap(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
) -> None:
    train_index = set(train.index)
    validation_index = set(validation.index)
    test_index = set(test.index)
    if (
        train_index & validation_index
        or train_index & test_index
        or validation_index & test_index
    ):
        raise ValueError("Train, validation, and test splits overlap.")
