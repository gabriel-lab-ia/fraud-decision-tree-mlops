FEATURE_COLUMNS = [
    "transaction_amount",
    "transaction_hour",
    "customer_age_days",
    "num_previous_transactions",
    "merchant_risk_score",
    "device_risk_score",
]

ENGINEERED_FEATURE_COLUMNS = [
    "is_night_transaction",
    "is_new_customer",
    "has_low_transaction_history",
    "high_amount_transaction",
    "combined_risk_score",
]

MODEL_FEATURE_COLUMNS = FEATURE_COLUMNS + ENGINEERED_FEATURE_COLUMNS

TARGET_COLUMN = "is_fraud"
