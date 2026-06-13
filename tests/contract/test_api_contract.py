import pytest
from pydantic import ValidationError

from fraud_detection.api.schemas import PredictionResponse, TransactionRequest


def test_transaction_request_rejects_invalid_risk_score():
    with pytest.raises(ValidationError):
        TransactionRequest(
            transaction_id="txn_1",
            transaction_amount=10,
            transaction_hour=12,
            customer_age_days=10,
            num_previous_transactions=1,
            merchant_risk_score=1.2,
            device_risk_score=0.2,
        )


def test_prediction_response_contract():
    response = PredictionResponse(
        transaction_id="txn_1",
        prediction=1,
        label="fraud",
        risk_score=0.8,
        model_name="tree",
        model_version="0.1.0",
    )
    assert response.model_dump()["telemetry_event_id"] is None
