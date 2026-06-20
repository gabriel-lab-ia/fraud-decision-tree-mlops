import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from fraud_detection.data.schemas import MODEL_FEATURE_COLUMNS
from fraud_detection.features.feature_engineering import add_engineered_features
from fraud_detection.models.predict import predict_transaction


def test_predict_transaction_returns_expected_payload():
    training_data = pd.DataFrame(
        {
            "transaction_amount": [50.0, 999.0, 120.0, 850.0],
            "transaction_hour": [12, 3, 16, 2],
            "customer_age_days": [500, 12, 700, 20],
            "num_previous_transactions": [10, 1, 8, 0],
            "merchant_risk_score": [0.1, 0.95, 0.2, 0.88],
            "device_risk_score": [0.1, 0.90, 0.3, 0.92],
            "is_fraud": [0, 1, 0, 1],
        }
    )

    training_data = add_engineered_features(training_data)

    model = DecisionTreeClassifier(random_state=42)
    model.fit(training_data[MODEL_FEATURE_COLUMNS], training_data["is_fraud"])

    artifact = {
        "artifact_schema_version": "fraud-model-artifact-v1",
        "model": model,
        "feature_columns": MODEL_FEATURE_COLUMNS,
        "model_name": "decision_tree_fraud_detector",
        "model_version": "0.1.0",
        "decision_threshold": 0.5,
    }

    features = {
        "transaction_amount": 999.0,
        "transaction_hour": 3,
        "customer_age_days": 12,
        "num_previous_transactions": 1,
        "merchant_risk_score": 0.95,
        "device_risk_score": 0.90,
    }

    result = predict_transaction(artifact, features)

    assert "prediction" in result
    assert "label" in result
    assert "risk_score" in result
    assert "decision_threshold" in result
    assert result["model_name"] == "decision_tree_fraud_detector"
    assert result["model_version"] == "0.1.0"
