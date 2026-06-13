from datetime import UTC, datetime
from typing import Any

from fraud_detection.logging import get_logger
from fraud_detection.telemetry.nosql_client import MongoTelemetryClient

logger = get_logger(__name__)


def build_prediction_event(
    transaction_id: str,
    request_features: dict[str, Any],
    prediction_result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "transaction_id": transaction_id,
        "request_features": request_features,
        "prediction": prediction_result["prediction"],
        "label": prediction_result["label"],
        "risk_score": prediction_result["risk_score"],
        "model_name": prediction_result["model_name"],
        "model_version": prediction_result["model_version"],
        "timestamp": datetime.now(UTC),
    }


def log_prediction_event(
    client: MongoTelemetryClient,
    event: dict[str, Any],
) -> str | None:
    try:
        result = client.get_collection().insert_one(event)
        return str(result.inserted_id)
    except Exception as exc:
        logger.warning("Prediction telemetry unavailable: %s", exc)
        return None
