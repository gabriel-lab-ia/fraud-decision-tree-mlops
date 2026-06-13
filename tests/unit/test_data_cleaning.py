import pandas as pd

from fraud_detection.data.cleaning import clean_transaction_data


def test_clean_transaction_data_removes_duplicates_and_invalid_ranges():
    data = pd.DataFrame(
        [
            {
                "transaction_amount": 100,
                "transaction_hour": 12,
                "customer_age_days": 90,
                "num_previous_transactions": 3,
                "merchant_risk_score": 0.2,
                "device_risk_score": 0.3,
                "is_fraud": 0,
            },
            {
                "transaction_amount": 100,
                "transaction_hour": 12,
                "customer_age_days": 90,
                "num_previous_transactions": 3,
                "merchant_risk_score": 0.2,
                "device_risk_score": 0.3,
                "is_fraud": 0,
            },
            {
                "transaction_amount": -50,
                "transaction_hour": 25,
                "customer_age_days": -1,
                "num_previous_transactions": -3,
                "merchant_risk_score": 2.0,
                "device_risk_score": -1.0,
                "is_fraud": 1,
            },
        ]
    )

    cleaned = clean_transaction_data(data)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["transaction_amount"] == 100
    assert cleaned.iloc[0]["transaction_hour"] == 12


def test_clean_transaction_data_coerces_numeric_columns():
    data = pd.DataFrame(
        [
            {
                "transaction_amount": "150.5",
                "transaction_hour": "13",
                "customer_age_days": "45",
                "num_previous_transactions": "2",
                "merchant_risk_score": "0.4",
                "device_risk_score": "0.6",
                "is_fraud": 1,
            }
        ]
    )

    cleaned = clean_transaction_data(data)

    assert cleaned.iloc[0]["transaction_amount"] == 150.5
    assert cleaned.iloc[0]["transaction_hour"] == 13
    assert cleaned.iloc[0]["merchant_risk_score"] == 0.4


def test_clean_transaction_data_handles_missing_values():
    data = pd.DataFrame(
        [
            {
                "transaction_amount": 100,
                "transaction_hour": 10,
                "customer_age_days": 30,
                "num_previous_transactions": 1,
                "merchant_risk_score": 0.2,
                "device_risk_score": 0.3,
                "is_fraud": 0,
            },
            {
                "transaction_amount": None,
                "transaction_hour": 12,
                "customer_age_days": 60,
                "num_previous_transactions": 2,
                "merchant_risk_score": 0.4,
                "device_risk_score": 0.5,
                "is_fraud": 1,
            },
            {
                "transaction_amount": 200,
                "transaction_hour": 14,
                "customer_age_days": 90,
                "num_previous_transactions": 3,
                "merchant_risk_score": 0.6,
                "device_risk_score": 0.7,
                "is_fraud": None,
            },
        ]
    )

    cleaned = clean_transaction_data(data)

    assert len(cleaned) == 2
    assert cleaned["transaction_amount"].isna().sum() == 0
    assert cleaned["is_fraud"].isna().sum() == 0
