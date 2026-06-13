from fastapi import FastAPI

from fraud_detection.api.routes import router
from fraud_detection.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Decision Tree fraud detection inference API",
)
app.include_router(router)
