import joblib
import pandas as pd
import pytest
from sklearn.tree import DecisionTreeClassifier

from fraud_detection.models.artifact import (
    ARTIFACT_SCHEMA_VERSION,
    ModelArtifactError,
    ModelArtifactMetadata,
    build_artifact,
    load_artifact_with_validation,
    save_artifact_with_manifest,
)


def make_artifact():
    model = DecisionTreeClassifier(random_state=42).fit(
        pd.DataFrame({"amount": [1, 2, 100, 200]}),
        [0, 0, 1, 1],
    )
    metadata = ModelArtifactMetadata(
        artifact_schema_version=ARTIFACT_SCHEMA_VERSION,
        model_name="tree",
        model_version="0.3.0",
        project_version="0.3.0",
        feature_columns=["amount"],
        decision_threshold=0.5,
        calibration_method="none",
        dataset_fingerprint="abc",
        data_schema_version="schema",
        training_timestamp_utc="2026-06-20T00:00:00+00:00",
        training_run_id=None,
        git_commit=None,
        metrics_summary={"recall": 1.0},
    )
    return build_artifact(model=model, uncalibrated_model=model, metadata=metadata)


def test_valid_artifact_roundtrip(tmp_path):
    model_path = tmp_path / "model.joblib"
    manifest_path = tmp_path / "model.manifest.json"
    save_artifact_with_manifest(make_artifact(), model_path, manifest_path)
    loaded = load_artifact_with_validation(model_path, manifest_path)
    assert loaded["model_name"] == "tree"


def test_artifact_hash_mismatch_is_rejected(tmp_path):
    model_path = tmp_path / "model.joblib"
    manifest_path = tmp_path / "model.manifest.json"
    save_artifact_with_manifest(make_artifact(), model_path, manifest_path)
    joblib.dump({"bad": True}, model_path)
    with pytest.raises(ModelArtifactError):
        load_artifact_with_validation(model_path, manifest_path)


def test_old_schema_is_rejected(tmp_path):
    model_path = tmp_path / "model.joblib"
    joblib.dump({"model": object(), "artifact_schema_version": "old"}, model_path)
    with pytest.raises(ModelArtifactError):
        load_artifact_with_validation(model_path)
