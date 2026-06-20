from functools import lru_cache
from pathlib import Path
from typing import Any, Literal, cast

import yaml
from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "fraud-decision-tree-mlops"
    app_env: Literal["development", "test", "production"] = "development"

    api_key: SecretStr | None = None
    enable_api_key_auth: bool = False
    cors_allow_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:8000"]
    )
    max_batch_size: int = Field(default=100, ge=1, le=1000)

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_database: str = "fraud_detection"
    mongo_collection: str = "prediction_events"

    mlflow_tracking_uri: str = "sqlite:///mlflow.db"
    mlflow_experiment_name: str = "fraud_decision_tree_experiment"

    model_path: Path = Path("artifacts/models/decision_tree_model.joblib")
    model_manifest_path: Path = Path(
        "artifacts/models/decision_tree_model.manifest.json"
    )
    metrics_path: Path = Path("reports/metrics.json")

    enable_prometheus_metrics: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def validate_security_posture(self) -> "Settings":
        if self.app_env == "production":
            if not self.enable_api_key_auth:
                raise ValueError(
                    "API key authentication must be enabled in production."
                )
            if not self.api_key or not self.api_key.get_secret_value():
                raise ValueError("API_KEY must be configured in production.")
            if "*" in self.cors_allow_origins:
                raise ValueError("Wildcard CORS origins are not allowed in production.")
        return self

    def safe_dict(self) -> dict[str, Any]:
        data = self.model_dump(mode="json")
        if self.api_key:
            data["api_key"] = "***redacted***"
        return data


@lru_cache
def get_settings() -> Settings:
    return Settings()


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    config_path = ROOT_DIR / path if isinstance(path, str) else path

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        return cast(dict[str, Any], yaml.safe_load(file))
