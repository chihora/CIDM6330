import json
from pathlib import Path


def transform_observations(raw_payload):
    observations = raw_payload.get("observations", [])
    transformed = []

    for item in observations:
        value = item.get("value")
        date = item.get("date")

        if date is None or value in (None, "."):
            continue

        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            continue

        transformed.append({"date": date, "value": numeric_value})

    return transformed


def save_transformed_data(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)
