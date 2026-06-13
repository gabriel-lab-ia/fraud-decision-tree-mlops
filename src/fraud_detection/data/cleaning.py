from __future__ import annotations

import pandas as pd

NUMERIC_COLUMNS = [
    "transaction_amount",
    "transaction_hour",
    "customer_age_days",
    "num_previous_transactions",
    "merchant_risk_score",
    "device_risk_score",
]


def remove_duplicate_rows(data: pd.DataFrame) -> pd.DataFrame:
    return data.drop_duplicates().reset_index(drop=True)


def coerce_numeric_columns(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    for column in NUMERIC_COLUMNS:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    return data


def clean_invalid_ranges(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    if "transaction_amount" in data.columns:
        data = data[data["transaction_amount"] >= 0]

    if "transaction_hour" in data.columns:
        data = data[data["transaction_hour"].between(0, 23)]

    if "customer_age_days" in data.columns:
        data = data[data["customer_age_days"] >= 0]

    if "num_previous_transactions" in data.columns:
        data = data[data["num_previous_transactions"] >= 0]

    for column in ["merchant_risk_score", "device_risk_score"]:
        if column in data.columns:
            data = data[data[column].between(0, 1)]

    return data.reset_index(drop=True)


def handle_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    for column in NUMERIC_COLUMNS:
        if column in data.columns:
            data[column] = data[column].fillna(data[column].median())

    if "is_fraud" in data.columns:
        data = data.dropna(subset=["is_fraud"])

    return data.reset_index(drop=True)


def clean_transaction_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data = remove_duplicate_rows(data)
    data = coerce_numeric_columns(data)
    data = handle_missing_values(data)
    data = clean_invalid_ranges(data)

    return data.reset_index(drop=True)
