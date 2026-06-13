import pandas as pd

from fraud_detection.features.feature_engineering import add_engineered_features


def test_add_engineered_features_creates_expected_columns():
    data = pd.DataFrame(
        {
            "transaction_amount": [100.0, 999.0],
            "transaction_hour": [2, 14],
            "customer_age_days": [10, 100],
            "num_previous_transactions": [0, 5],
            "merchant_risk_score": [0.9, 0.2],
            "device_risk_score": [0.8, 0.3],
        }
    )

    output = add_engineered_features(data)

    assert "is_night_transaction" in output.columns
    assert "is_new_customer" in output.columns
    assert "has_low_transaction_history" in output.columns
    assert "high_amount_transaction" in output.columns
    assert "combined_risk_score" in output.columns


def test_add_engineered_features_values_are_correct():
    data = pd.DataFrame(
        {
            "transaction_amount": [999.0],
            "transaction_hour": [3],
            "customer_age_days": [12],
            "num_previous_transactions": [1],
            "merchant_risk_score": [0.9],
            "device_risk_score": [0.7],
        }
    )

    output = add_engineered_features(data)

    assert output.loc[0, "is_night_transaction"] == 1
    assert output.loc[0, "is_new_customer"] == 1
    assert output.loc[0, "has_low_transaction_history"] == 1
    assert output.loc[0, "high_amount_transaction"] == 1
    assert output.loc[0, "combined_risk_score"] == 0.8
