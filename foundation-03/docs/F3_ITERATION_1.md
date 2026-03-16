# F3 Iteration 1 - Data Acquisition

## Goal
Build a runnable GDP/FRED acquisition step that reliably returns observation data and persists a raw artifact for the rest of the pipeline.

## What works
- `pipeline.acquire.fetch_gdp_observations()` returns a structured GDP observation payload.
- The acquisition step supports two modes:
	- sample mode for reliable local execution
	- live FRED API mode when `FRED_API_KEY` is available
- `pipeline.acquire.save_raw_payload()` writes the raw response to `data/raw/gdp_raw.json`.
- The raw artifact is immediately usable as input to the transformation stage.
- Live acquisition now supports configurable timeout, retry, exponential backoff, and optional sample fallback when live calls fail.

## Data sample evidence

The current sample payload contains five GDP-style observations for dates between `2020-01-01` and `2021-01-01`. A successful run writes that payload to `data/raw/gdp_raw.json`.

## How acquisition works

- Default path: use a built-in GDP sample payload so the project remains runnable without network access.
- Optional live path: call the FRED observations endpoint using `FRED_API_KEY`, `FRED_SERIES_ID`, and `FRED_BASE_URL` from `pipeline.config`.
- Optional date filters: `FRED_OBSERVATION_START` and `FRED_OBSERVATION_END` are passed to the live API query when provided.
- Response payloads are expected to include an `observations` collection.

## Error handling
- Retries are attempted for transient failures and retryable statuses, including common server errors and `429` rate-limit responses.
- Network timeouts, malformed JSON, and missing observation payloads are handled and retried based on configured limits.
- If retries are exhausted and `FRED_FALLBACK_TO_SAMPLE_ON_ERROR=true`, acquisition returns a sample fallback payload with failure metadata.
- If fallback is disabled, a `RuntimeError` is raised after the final retry.

## Known limitations

- There is no advanced rate-limit strategy (e.g., adaptive quota management), only retry/backoff.
- Acquisition currently targets a single series (`GDP`) by default.

## Next
Pass the raw observation payload into transformation logic that produces cleaned numeric records for later analysis and reporting.
