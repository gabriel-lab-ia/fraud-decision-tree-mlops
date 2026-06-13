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


class PredictionResponse(BaseModel):
    transaction_id: str
    prediction: int
    label: str
    risk_score: float
    model_name: str
    model_version: str
    telemetry_event_id: str | None = None


class HealthResponse(BaseModel):
    status: str
    service: str


class ReadinessResponse(BaseModel):
    status: str
    model_loaded: bool
    detail: str | None = None


class TelemetryEvent(BaseModel):
    model_config = ConfigDict(extra="allow")

    transaction_id: str
    prediction: int
    label: str
    risk_score: float
    model_name: str
    model_version: str
    timestamp: datetime


class RecentTelemetryResponse(BaseModel):
    events: list[TelemetryEvent]
