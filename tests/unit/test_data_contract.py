import pandas as pd
import pytest

from fraud_detection.data.contract import (
    build_data_quality_report,
    dataset_fingerprint,
    validate_dataset_contract,
)


def valid_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "transaction_amount": [10.0, 900.0, 30.0, 1200.0],
            "transaction_hour": [12, 2, 14, 3],
            "customer_age_days": [100, 10, 500, 4],
            "num_previous_transactions": [5, 0, 10, 1],
            "merchant_risk_score": [0.1, 0.9, 0.2, 0.95],
            "device_risk_score": [0.1, 0.9, 0.2, 0.95],
            "is_fraud": [0, 1, 0, 1],
        }
    )


def test_contract_accepts_valid_data_and_fingerprint_is_deterministic():
    data = valid_data()
    validate_dataset_contract(data)
    assert dataset_fingerprint(data) == dataset_fingerprint(data.copy())
    assert build_data_quality_report(data).record_count == 4


def test_contract_rejects_extra_columns_and_invalid_ranges():
    data = valid_data()
    data["leakage_score"] = data["is_fraud"]
    with pytest.raises(ValueError, match="Unexpected columns"):
        validate_dataset_contract(data)

    invalid = valid_data()
    invalid.loc[0, "transaction_hour"] = 99
    with pytest.raises(ValueError, match="transaction_hour"):
        validate_dataset_contract(invalid)
