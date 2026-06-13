import pandas as pd
import pytest
from httpx import ASGITransport, AsyncClient
from sklearn.tree import DecisionTreeClassifier

from fraud_detection.api.dependencies import get_model_artifact, get_telemetry_client
from fraud_detection.api.main import app
from fraud_detection.data.schemas import MODEL_FEATURE_COLUMNS
from fraud_detection.features.feature_engineering import add_engineered_features


class OfflineTelemetry:
    def get_collection(self):
        raise ConnectionError("MongoDB offline")


async def make_artifact():
    data = add_engineered_features(
        pd.DataFrame(
            [
                {
                    "transaction_amount": 20.0,
                    "transaction_hour": 12,
                    "customer_age_days": 500,
                    "num_previous_transactions": 20,
                    "merchant_risk_score": 0.1,
                    "device_risk_score": 0.1,
                    "is_fraud": 0,
                },
                {
                    "transaction_amount": 900.0,
                    "transaction_hour": 2,
                    "customer_age_days": 5,
                    "num_previous_transactions": 0,
                    "merchant_risk_score": 0.9,
                    "device_risk_score": 0.9,
                    "is_fraud": 1,
                },
            ]
        )
    )
    model = DecisionTreeClassifier(random_state=42).fit(
        data[MODEL_FEATURE_COLUMNS], data["is_fraud"]
    )
    return {
        "model": model,
        "feature_columns": MODEL_FEATURE_COLUMNS,
        "model_name": "decision_tree_fraud_detector",
        "model_version": "0.1.0",
    }


app.dependency_overrides[get_model_artifact] = make_artifact


async def offline_telemetry():
    return OfflineTelemetry()


app.dependency_overrides[get_telemetry_client] = offline_telemetry


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield async_client


@pytest.mark.anyio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.anyio
async def test_ready(client):
    response = await client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] in {"ready", "not_ready"}
    assert isinstance(response.json()["model_loaded"], bool)


@pytest.mark.anyio
async def test_predict_succeeds_when_telemetry_is_offline(client):
    response = await client.post(
        "/predict",
        json={
            "transaction_id": "txn_001",
            "transaction_amount": 750.0,
            "transaction_hour": 2,
            "customer_age_days": 14,
            "num_previous_transactions": 1,
            "merchant_risk_score": 0.82,
            "device_risk_score": 0.74,
        },
    )
    assert response.status_code == 200
    assert response.json()["transaction_id"] == "txn_001"
    assert response.json()["telemetry_event_id"] is None


@pytest.mark.anyio
async def test_recent_telemetry_returns_503_when_store_is_offline(client):
    response = await client.get("/telemetry/recent")
    assert response.status_code == 503
