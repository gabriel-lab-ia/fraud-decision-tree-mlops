from typing import Any

from fraud_detection.telemetry.nosql_client import MongoTelemetryClient


def recent_predictions(
    client: MongoTelemetryClient,
    limit: int = 20,
) -> list[dict[str, Any]]:
    cursor = (
        client.get_collection().find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
    )
    return list(cursor)


def total_prediction_count(client: MongoTelemetryClient) -> int:
    return client.get_collection().count_documents({})


def fraud_rate_summary(client: MongoTelemetryClient) -> dict[str, float | int]:
    total = total_prediction_count(client)
    fraud = client.get_collection().count_documents({"prediction": 1})
    return {
        "total": total,
        "fraud": fraud,
        "fraud_rate": fraud / total if total else 0.0,
    }


def average_risk_score(client: MongoTelemetryClient) -> float:
    results = list(
        client.get_collection().aggregate(
            [{"$group": {"_id": None, "average": {"$avg": "$risk_score"}}}]
        )
    )
    return float(results[0]["average"]) if results else 0.0
