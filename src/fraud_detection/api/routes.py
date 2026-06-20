from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response

from fraud_detection._version import get_project_version
from fraud_detection.api.dependencies import get_model_artifact, get_telemetry_client
from fraud_detection.api.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    HealthResponse,
    PredictionResponse,
    ReadinessResponse,
    RecentTelemetryResponse,
    TelemetryEvent,
    TransactionRequest,
    VersionResponse,
)
from fraud_detection.config import get_settings
from fraud_detection.models.predict import predict_transaction
from fraud_detection.telemetry.event_logger import (
    build_prediction_event,
    log_prediction_event,
)
from fraud_detection.telemetry.monitoring_queries import (
    average_risk_score,
    fraud_rate_summary,
    recent_predictions,
)
from fraud_detection.telemetry.nosql_client import MongoTelemetryClient

router = APIRouter()


def request_id_from_header(x_request_id: str | None = Header(default=None)) -> str:
    return x_request_id or str(uuid4())


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if not settings.enable_api_key_auth:
        return
    expected = settings.api_key.get_secret_value() if settings.api_key else None
    if not expected or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


def get_version_payload(artifact: dict | None = None) -> VersionResponse:
    settings = get_settings()
    metadata = artifact.get("metadata", {}) if artifact else {}
    return VersionResponse(
        application=settings.app_name,
        version=get_project_version(),
        model_name=metadata.get("model_name") if artifact else None,
        model_version=metadata.get("model_version") if artifact else None,
        artifact_schema_version=(
            artifact.get("artifact_schema_version") if artifact else None
        ),
        git_commit=metadata.get("git_commit") if artifact else None,
    )


@router.get("/health/live", response_model=HealthResponse)
async def live() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.app_name)


@router.get("/health/ready", response_model=ReadinessResponse)
async def ready() -> ReadinessResponse:
    try:
        await get_model_artifact()
    except Exception:
        return ReadinessResponse(
            status="not_ready",
            model_loaded=False,
            detail="Model artifact is not available.",
        )
    return ReadinessResponse(status="ready", model_loaded=True)


@router.get("/version", response_model=VersionResponse)
async def version() -> VersionResponse:
    try:
        artifact = await get_model_artifact()
    except Exception:
        artifact = None
    return get_version_payload(artifact)


@router.get("/metrics")
async def metrics() -> Response:
    settings = get_settings()
    content = "\n".join(
        [
            "# HELP fraud_api_info API metadata.",
            "# TYPE fraud_api_info gauge",
            (
                f'fraud_api_info{{service="{settings.app_name}",'
                f'version="{get_project_version()}"}} 1'
            ),
        ]
    )
    return Response(content=content + "\n", media_type="text/plain; version=0.0.4")


def build_prediction_response(
    request: TransactionRequest,
    result: dict,
    telemetry_event_id: str | None,
    request_id: str,
) -> PredictionResponse:
    return PredictionResponse(
        transaction_id=request.transaction_id,
        telemetry_event_id=telemetry_event_id,
        request_id=request_id,
        **result,
    )


@router.post("/v1/predict", response_model=PredictionResponse)
async def predict_v1(
    request: TransactionRequest,
    artifact: Annotated[dict, Depends(get_model_artifact)],
    telemetry_client: Annotated[MongoTelemetryClient, Depends(get_telemetry_client)],
    request_id: Annotated[str, Depends(request_id_from_header)],
    _auth: Annotated[None, Depends(require_api_key)],
) -> PredictionResponse:
    request_data = request.model_dump()
    transaction_id = request_data.pop("transaction_id")
    result = predict_transaction(artifact, request_data)
    event = build_prediction_event(transaction_id, request_data, result, request_id)
    event_id = log_prediction_event(telemetry_client, event)
    return build_prediction_response(request, result, event_id, request_id)


@router.post("/v1/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch_v1(
    batch: BatchPredictionRequest,
    artifact: Annotated[dict, Depends(get_model_artifact)],
    telemetry_client: Annotated[MongoTelemetryClient, Depends(get_telemetry_client)],
    request_id: Annotated[str, Depends(request_id_from_header)],
    _auth: Annotated[None, Depends(require_api_key)],
) -> BatchPredictionResponse:
    max_batch_size = get_settings().max_batch_size
    if len(batch.transactions) > max_batch_size:
        raise HTTPException(
            status_code=413,
            detail=f"Batch size exceeds configured limit of {max_batch_size}.",
        )
    responses = []
    for item in batch.transactions:
        request_data = item.model_dump()
        transaction_id = request_data.pop("transaction_id")
        result = predict_transaction(artifact, request_data)
        event = build_prediction_event(transaction_id, request_data, result, request_id)
        event_id = log_prediction_event(telemetry_client, event)
        responses.append(build_prediction_response(item, result, event_id, request_id))
    return BatchPredictionResponse(predictions=responses, request_id=request_id)


@router.get("/v1/telemetry/recent", response_model=RecentTelemetryResponse)
async def telemetry_recent_v1(
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
    return RecentTelemetryResponse(
        events=[TelemetryEvent.model_validate(event) for event in events]
    )


@router.get("/v1/monitoring/summary")
async def monitoring_summary_v1(
    telemetry_client: Annotated[MongoTelemetryClient, Depends(get_telemetry_client)],
) -> dict:
    try:
        fraud = fraud_rate_summary(telemetry_client)
        return {
            "total_predictions": fraud["total"],
            "fraud_predictions": fraud["fraud"],
            "fraud_prediction_rate": fraud["fraud_rate"],
            "average_risk_score": average_risk_score(telemetry_client),
            "timestamp": datetime.now(UTC).isoformat(),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Monitoring unavailable: {exc}",
        ) from exc


@router.get("/health", response_model=HealthResponse, deprecated=True)
async def health_alias() -> HealthResponse:
    return await live()


@router.get("/ready", response_model=ReadinessResponse, deprecated=True)
async def ready_alias() -> ReadinessResponse:
    return await ready()


@router.post("/predict", response_model=PredictionResponse, deprecated=True)
async def predict_alias(
    request: TransactionRequest,
    artifact: Annotated[dict, Depends(get_model_artifact)],
    telemetry_client: Annotated[MongoTelemetryClient, Depends(get_telemetry_client)],
    request_id: Annotated[str, Depends(request_id_from_header)],
    _auth: Annotated[None, Depends(require_api_key)],
) -> PredictionResponse:
    return await predict_v1(request, artifact, telemetry_client, request_id, _auth)


@router.get(
    "/telemetry/recent",
    response_model=RecentTelemetryResponse,
    deprecated=True,
)
async def telemetry_recent_alias(
    telemetry_client: Annotated[MongoTelemetryClient, Depends(get_telemetry_client)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> RecentTelemetryResponse:
    return await telemetry_recent_v1(telemetry_client, limit)
