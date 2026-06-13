import pandas as pd


def add_engineered_features(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    data["is_night_transaction"] = data["transaction_hour"].between(0, 5).astype(int)
    data["is_new_customer"] = (data["customer_age_days"] < 30).astype(int)
    data["has_low_transaction_history"] = (
        data["num_previous_transactions"] <= 1
    ).astype(int)
    data["high_amount_transaction"] = (data["transaction_amount"] > 500).astype(int)
    data["combined_risk_score"] = (
        data["merchant_risk_score"] + data["device_risk_score"]
    ) / 2

    return data
