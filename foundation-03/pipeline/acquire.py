import json
from datetime import datetime, UTC
from pathlib import Path
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from .config import (
    FRED_API_KEY,
    FRED_BASE_URL,
    FRED_SERIES_ID,
    FRED_FALLBACK_TO_SAMPLE_ON_ERROR,
    FRED_MAX_RETRIES,
    FRED_REQUEST_TIMEOUT_SECONDS,
    FRED_RETRY_BACKOFF_SECONDS,
)


def sample_gdp_payload(source="sample", fallback_reason=None):
    payload = {
        "realtime_start": "2026-01-01",
        "realtime_end": "2026-01-01",
        "observation_start": "2020-01-01",
        "observation_end": "2021-01-01",
        "units": "lin",
        "output_type": 1,
        "file_type": "json",
        "order_by": "observation_date",
        "sort_order": "asc",
        "count": 5,
        "offset": 0,
        "limit": 100000,
        "observations": [
            {"date": "2020-01-01", "value": "21439.453"},
            {"date": "2020-04-01", "value": "19477.444"},
            {"date": "2020-07-01", "value": "21138.574"},
            {"date": "2020-10-01", "value": "21477.597"},
            {"date": "2021-01-01", "value": "22038.226"},
        ],
        "metadata": {
            "source": source,
            "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        },
    }

    if fallback_reason:
        payload["metadata"]["fallback_reason"] = fallback_reason

    return payload


def fetch_gdp_observations(
    use_live=False,
    series_id=None,
    observation_start=None,
    observation_end=None,
):
    if not use_live or not FRED_API_KEY:
        return sample_gdp_payload()

    target_series = series_id or FRED_SERIES_ID
    query_params = {
        "series_id": target_series,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "asc",
    }

    if observation_start:
        query_params["observation_start"] = observation_start
    if observation_end:
        query_params["observation_end"] = observation_end

    query = urlencode(query_params)
    url = f"{FRED_BASE_URL}?{query}"

    last_error = None
    retryable_statuses = {429, 500, 502, 503, 504}

    for attempt in range(FRED_MAX_RETRIES + 1):
        try:
            with urlopen(url, timeout=FRED_REQUEST_TIMEOUT_SECONDS) as response:
                payload = json.loads(response.read().decode("utf-8"))

            if "observations" not in payload:
                raise ValueError("FRED response missing 'observations'")

            return payload
        except HTTPError as exc:
            status_code = getattr(exc, "code", None)
            retryable = status_code in retryable_statuses
            last_error = f"HTTPError {status_code}: {exc}"

            if retryable and attempt < FRED_MAX_RETRIES:
                sleep(FRED_RETRY_BACKOFF_SECONDS * (2 ** attempt))
                continue
            break
        except (URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < FRED_MAX_RETRIES:
                sleep(FRED_RETRY_BACKOFF_SECONDS * (2 ** attempt))
                continue
            break

    if FRED_FALLBACK_TO_SAMPLE_ON_ERROR:
        return sample_gdp_payload(source="sample_fallback", fallback_reason=last_error)

    raise RuntimeError(f"FRED acquisition failed after retries: {last_error}")


def save_raw_payload(payload, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)
