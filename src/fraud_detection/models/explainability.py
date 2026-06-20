from typing import Any


def extract_feature_importances(
    artifact: dict[str, Any],
) -> list[dict[str, float | str]]:
    model = artifact.get("uncalibrated_model") or artifact["model"]
    feature_columns = artifact["feature_columns"]

    if not hasattr(model, "feature_importances_"):
        raise ValueError("Model does not expose feature_importances_.")

    importances = model.feature_importances_
    if len(importances) != len(feature_columns):
        raise ValueError("Feature names and importance values have different lengths.")

    rows = [
        {"feature": feature, "importance": float(importance)}
        for feature, importance in zip(feature_columns, importances, strict=True)
    ]
    return sorted(rows, key=lambda row: row["importance"], reverse=True)


def format_feature_importances(rows: list[dict[str, float | str]]) -> str:
    header = f"{'Feature':<32} {'Importance':>10}"
    separator = "-" * len(header)
    values = [
        f"{row['feature']!s:<32} {float(row['importance']):>10.4f}" for row in rows
    ]
    return "\n".join([header, separator, *values])


def explain_local_decision(
    artifact: dict[str, Any],
    features: dict[str, float],
) -> dict:
    rows = extract_feature_importances(artifact)
    top_features = [row["feature"] for row in rows[:3]]
    return {
        "model_name": artifact["model_name"],
        "model_version": artifact["model_version"],
        "top_global_features": top_features,
        "provided_feature_count": len(features),
    }
