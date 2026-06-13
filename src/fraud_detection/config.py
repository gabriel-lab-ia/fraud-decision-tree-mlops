from functools import lru_cache
from pathlib import Path

import yaml
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "fraud-decision-tree-mlops"
    app_env: str = "development"

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_database: str = "fraud_detection"
    mongo_collection: str = "prediction_events"

    mlflow_tracking_uri: str = "sqlite:///mlflow.db"
    mlflow_experiment_name: str = "fraud_decision_tree_experiment"

    model_path: str = "artifacts/models/decision_tree_model.joblib"
    metrics_path: str = "reports/metrics.json"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()


def load_yaml_config(path: str | Path) -> dict:
    config_path = ROOT_DIR / path if isinstance(path, str) else path

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
