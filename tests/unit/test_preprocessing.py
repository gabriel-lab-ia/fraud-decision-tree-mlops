import pandas as pd
import pytest

from fraud_detection.data.preprocessing import split_features_target
from fraud_detection.data.schemas import TARGET_COLUMN
from fraud_detection.features.feature_engineering import add_engineered_features


def test_split_features_target_returns_features_and_target():
    data = pd.DataFrame(
        {
            "transaction_amount": [100.0, 999.0],
            "transaction_hour": [12, 3],
            "customer_age_days": [100, 12],
            "num_previous_transactions": [5, 1],
            "merchant_risk_score": [0.2, 0.91],
            "device_risk_score": [0.3, 0.87],
            "is_fraud": [0, 1],
        }
    )

    data = add_engineered_features(data)

    features, target = split_features_target(data, TARGET_COLUMN)

    assert TARGET_COLUMN not in features.columns
    assert target.tolist() == [0, 1]


def test_split_features_target_raises_error_when_target_is_missing():
    data = pd.DataFrame(
        {
            "transaction_amount": [100.0],
            "transaction_hour": [12],
            "customer_age_days": [100],
            "num_previous_transactions": [5],
            "merchant_risk_score": [0.2],
            "device_risk_score": [0.3],
        }
    )

    data = add_engineered_features(data)

    with pytest.raises(ValueError, match="Target column"):
        split_features_target(data, TARGET_COLUMN)
