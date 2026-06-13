from functools import lru_cache

from fraud_detection.config import get_settings
from fraud_detection.models.predict import load_model_artifact
from fraud_detection.telemetry.nosql_client import MongoTelemetryClient


@lru_cache
def _get_model_artifact() -> dict:
    return load_model_artifact(get_settings().model_path)


@lru_cache
def _get_telemetry_client() -> MongoTelemetryClient:
    return MongoTelemetryClient(get_settings())


async def get_model_artifact() -> dict:
    return _get_model_artifact()


async def get_telemetry_client() -> MongoTelemetryClient:
    return _get_telemetry_client()
