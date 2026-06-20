import time
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from fraud_detection._version import get_project_version
from fraud_detection.api.routes import router
from fraud_detection.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=get_project_version(),
    description="Decision Tree fraud detection inference API",
)
app.include_router(router)


@app.middleware("http")
async def add_request_context(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = request.headers.get("x-request-id", str(uuid4()))
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Unexpected internal error.",
                    "request_id": request_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            },
        )
    response.headers["x-request-id"] = request_id
    elapsed_ms = (time.perf_counter() - started) * 1000
    response.headers["x-response-time-ms"] = f"{elapsed_ms:.2f}"
    return response
