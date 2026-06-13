from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from fraud_detection.api.dependencies import get_model_artifact, get_telemetry_client
from fraud_detection.api.schemas import (
    HealthResponse,
    PredictionResponse,
    ReadinessResponse,
    RecentTelemetryResponse,
    TransactionRequest,
)
from fraud_detection.config import get_settings
from fraud_detection.models.predict import predict_transaction
from fraud_detection.telemetry.event_logger import (
    build_prediction_event,
    log_prediction_event,
)
from fraud_detection.telemetry.monitoring_queries import recent_predictions
from fraud_detection.telemetry.nosql_client import MongoTelemetryClient

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.app_name)


@router.get("/ready", response_model=ReadinessResponse)
async def ready() -> ReadinessResponse:
    try:
        await get_model_artifact()
    except Exception as exc:
        return ReadinessResponse(
            status="not_ready",
            model_loaded=False,
            detail=str(exc),
        )
    return ReadinessResponse(status="ready", model_loaded=True)


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: TransactionRequest,
    artifact: Annotated[dict, Depends(get_model_artifact)],
    telemetry_client: Annotated[MongoTelemetryClient, Depends(get_telemetry_client)],
) -> PredictionResponse:
    request_data = request.model_dump()
    transaction_id = request_data.pop("transaction_id")
    result = predict_transaction(artifact, request_data)
    event = build_prediction_event(transaction_id, request_data, result)
    event_id = log_prediction_event(telemetry_client, event)
    return PredictionResponse(
        transaction_id=transaction_id,
        telemetry_event_id=event_id,
        **result,
    )


@router.get("/telemetry/recent", response_model=RecentTelemetryResponse)
async def telemetry_recent(
    telemetry_client: Annotated[MongoTelemetryClient, Depends(get_telemetry_client)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> RecentTelemetryResponse:
    try:
        events = recent_predictions(telemetry_client, limit)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Telemetry store unavailable: {exc}",
        ) from exc
    return RecentTelemetryResponse(events=events)
