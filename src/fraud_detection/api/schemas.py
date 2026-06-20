from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TransactionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transaction_id: str = Field(min_length=1, max_length=128)
    transaction_amount: float = Field(ge=0)
    transaction_hour: int = Field(ge=0, le=23)
    customer_age_days: int = Field(ge=0)
    num_previous_transactions: int = Field(ge=0)
    merchant_risk_score: float = Field(ge=0, le=1)
    device_risk_score: float = Field(ge=0, le=1)


class BatchPredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transactions: list[TransactionRequest] = Field(min_length=1)


class PredictionResponse(BaseModel):
    transaction_id: str
    prediction: int
    label: str
    risk_score: float
    decision_threshold: float
    model_name: str
    model_version: str
    artifact_schema_version: str | None = None
    telemetry_event_id: str | None = None
    request_id: str | None = None


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]
    request_id: str


class HealthResponse(BaseModel):
    status: str
    service: str


class ReadinessResponse(BaseModel):
    status: str
    model_loaded: bool
    detail: str | None = None


class VersionResponse(BaseModel):
    application: str
    version: str
    model_name: str | None
    model_version: str | None
    artifact_schema_version: str | None
    git_commit: str | None


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    error: ErrorDetail


class TelemetryEvent(BaseModel):
    model_config = ConfigDict(extra="allow")

    transaction_id: str | None = None
    transaction_id_hash: str | None = None
    prediction: int
    label: str
    risk_score: float
    model_name: str
    model_version: str
    timestamp: datetime


class RecentTelemetryResponse(BaseModel):
    events: list[TelemetryEvent]
