from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import joblib
import sklearn

ARTIFACT_SCHEMA_VERSION = "fraud-model-artifact-v1"


class ModelArtifactError(ValueError):
    pass


@dataclass(frozen=True)
class ModelArtifactMetadata:
    artifact_schema_version: str
    model_name: str
    model_version: str
    project_version: str
    feature_columns: list[str]
    decision_threshold: float
    calibration_method: str
    dataset_fingerprint: str
    data_schema_version: str
    training_timestamp_utc: str
    training_run_id: str | None
    git_commit: str | None
    metrics_summary: dict[str, float]
    sklearn_version: str = sklearn.__version__
    python_version: str = platform.python_version()

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_schema_version": self.artifact_schema_version,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "project_version": self.project_version,
            "feature_columns": self.feature_columns,
            "decision_threshold": self.decision_threshold,
            "calibration_method": self.calibration_method,
            "dataset_fingerprint": self.dataset_fingerprint,
            "data_schema_version": self.data_schema_version,
            "training_timestamp_utc": self.training_timestamp_utc,
            "training_run_id": self.training_run_id,
            "git_commit": self.git_commit,
            "metrics_summary": self.metrics_summary,
            "sklearn_version": self.sklearn_version,
            "python_version": self.python_version,
        }


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_artifact(
    *,
    model: Any,
    uncalibrated_model: Any,
    metadata: ModelArtifactMetadata,
) -> dict[str, Any]:
    return {
        "artifact_schema_version": metadata.artifact_schema_version,
        "model": model,
        "uncalibrated_model": uncalibrated_model,
        "metadata": metadata.to_dict(),
        "feature_columns": metadata.feature_columns,
        "model_name": metadata.model_name,
        "model_version": metadata.model_version,
        "decision_threshold": metadata.decision_threshold,
    }


def validate_artifact(artifact: dict[str, Any]) -> None:
    required = {
        "artifact_schema_version",
        "model",
        "metadata",
        "feature_columns",
        "model_name",
        "model_version",
        "decision_threshold",
    }
    missing = required - set(artifact)
    if missing:
        raise ModelArtifactError(f"Artifact missing required keys: {sorted(missing)}")
    if artifact["artifact_schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise ModelArtifactError("Unsupported model artifact schema version.")
    metadata = artifact["metadata"]
    if metadata.get("feature_columns") != artifact["feature_columns"]:
        raise ModelArtifactError("Artifact feature order is inconsistent.")
    if not 0 <= float(artifact["decision_threshold"]) <= 1:
        raise ModelArtifactError("Artifact decision threshold must be between 0 and 1.")


def save_artifact_with_manifest(
    artifact: dict[str, Any],
    model_path: Path,
    manifest_path: Path,
) -> dict[str, Any]:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, model_path)
    manifest = {
        "artifact_schema_version": artifact["artifact_schema_version"],
        "path": str(model_path),
        "size_bytes": model_path.stat().st_size,
        "sha256": file_sha256(model_path),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "metadata": artifact["metadata"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def load_artifact_with_validation(
    model_path: str | Path,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model artifact not found at {model_path}.")
    try:
        artifact = joblib.load(model_path)
    except Exception as exc:
        raise ModelArtifactError("Model artifact could not be deserialized.") from exc
    artifact = cast(dict[str, Any], artifact)
    validate_artifact(artifact)
    if manifest_path:
        manifest_file = Path(manifest_path)
        if manifest_file.exists():
            manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
            if manifest.get("sha256") != file_sha256(model_path):
                raise ModelArtifactError(
                    "Model artifact SHA-256 does not match manifest."
                )
    return artifact
