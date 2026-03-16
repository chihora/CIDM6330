# Foundation 3 - GDP/FRED Pipeline

This folder contains the Foundation 3 sprint deliverables for a GDP/FRED-style data pipeline. The project is intentionally built as a small modular pipeline rather than a distributed system because the current assignment scope values runnable software, iteration evidence, and architectural reflection over infrastructure complexity.

## Current scope

The current MVP pipeline does three things:
- acquires GDP-style observation data from a sample payload or the live FRED API
- transforms raw observations into cleaned date/value records
- runs an end-to-end pipeline that saves raw data, transformed data, and a short run summary

## What is working

- `pipeline.acquire.fetch_gdp_observations()` returns a sample GDP payload by default and can call the live FRED observations endpoint when `FRED_API_KEY` is present.
- Live acquisition supports configurable timeout, retry, backoff, and fallback-to-sample behavior.
- `pipeline.transform.transform_observations()` cleans invalid rows and converts numeric strings to floats.
- `pipeline.run_pipeline.run_pipeline()` chains acquisition and transformation and writes artifacts to `data/raw`, `data/transformed`, and `output/reports`.
- Pipeline runs now include series/date-range configuration context in the summary report.
- Basic tests pass for acquisition, transformation, and pipeline integration.

## What is not yet working

- There is no advanced retry strategy (jitter/circuit breaker) for live API requests.
- Configuration is environment-variable based and not yet exposed through a dedicated CLI.
- Output is written to JSON files rather than a database.
- Logging is basic stage-level observability rather than structured operational logging.

## Run

From `foundation-03`:

```bash
python -m pipeline.run_pipeline
```

If you want to use live FRED acquisition, set `.env` values based on `.env.example`:
- `USE_LIVE_FRED`
- `FRED_API_KEY`
- `FRED_SERIES_ID`
- `FRED_OBSERVATION_START`
- `FRED_OBSERVATION_END`
- `FRED_REQUEST_TIMEOUT_SECONDS`
- `FRED_MAX_RETRIES`
- `FRED_RETRY_BACKOFF_SECONDS`
- `FRED_FALLBACK_TO_SAMPLE_ON_ERROR`

## Test

```bash
python -m unittest discover -s pipeline/tests -p "test_*.py"
```

## Key outputs

- `data/raw/gdp_raw.json`
- `data/transformed/gdp_transformed.json`
- `output/reports/pipeline_run_summary.md`

## Deliverable map

- Iteration 1: `docs/F3_ITERATION_1.md`
- Iteration 2: `docs/F3_ITERATION_2.md`
- Iteration 3: `docs/F3_ITERATION_3.md`
- Architecture reality check: `docs/F3_ARCHITECTURE_REALITY_CHECK.md`
- Distributed considerations: `docs/F3_DISTRIBUTED_CONSIDERATIONS.md`
- Risk identification: `docs/F3_RISK_IDENTIFICATION.md`
- AI process documentation: `AI_LOG.md`

## Structure

- `pipeline/`: runnable acquisition, transformation, configuration, logging, and orchestration code
- `pipeline/tests/`: basic tests for working code
- `docs/`: sprint deliverables and ADRs
- `data/raw/`: raw acquisition artifacts
- `data/transformed/`: transformed pipeline artifacts
- `output/reports/`: run summaries and report outputs
- `AI_LOG.md`: documented AI collaboration process
