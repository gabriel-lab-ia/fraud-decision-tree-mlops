from pymongo import MongoClient
from pymongo.collection import Collection

from fraud_detection.config import Settings


class MongoTelemetryClient:
    def __init__(
        self,
        settings: Settings,
        client: MongoClient | None = None,
    ) -> None:
        self.settings = settings
        self.client = client or MongoClient(
            settings.mongo_uri,
            serverSelectionTimeoutMS=1000,
            connectTimeoutMS=1000,
        )

    def ping(self) -> bool:
        self.client.admin.command("ping")
        return True

    def get_collection(self) -> Collection:
        return self.client[self.settings.mongo_database][self.settings.mongo_collection]

    def close(self) -> None:
        self.client.close()
