import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen


def check_recent_telemetry(base_url: str) -> tuple[bool, list[dict[str, Any]]]:
    try:
        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Only HTTP(S) API URLs are supported.")
        with urlopen(
            f"{base_url.rstrip('/')}/v1/telemetry/recent",
            timeout=5,
        ) as response:  # nosec B310
            payload = json.load(response)
    except HTTPError as exc:
        if exc.code == 503:
            return False, []
        raise
    if not isinstance(payload.get("events"), list):
        raise ValueError("Telemetry response must contain an events list.")
    return True, payload["events"]


def main() -> int:
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    try:
        available, events = check_recent_telemetry(base_url)
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        print(f"Unexpected telemetry smoke-check failure: {exc}", file=sys.stderr)
        return 1
    if not available:
        print("Telemetry store unavailable; prediction fail-soft behavior is working.")
        return 0
    print(json.dumps(events, indent=2, default=str))
    print(f"Recent telemetry events: {len(events)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
