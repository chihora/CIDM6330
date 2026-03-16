# F3 Iteration 3 - Pipeline Integration

## Goal
Run acquisition and transformation as a single coherent pipeline that produces meaningful output and makes execution traceable.

## What works
- End-to-end run via `python -m pipeline.run_pipeline`.
- Produces raw and transformed artifacts.
- Writes run summary to `output/reports/pipeline_run_summary.md`.
- Returns a simple execution summary with raw and transformed record counts.

## Observability
- Stage-level logging for acquisition, transformation, and report output.
- The logger reports when the pipeline starts, when raw data is written, when transformed data is written, and when the summary report is created.
- If something goes wrong in acquisition or transformation, those stages are the first place to inspect.

## Configuration
- Controlled through `pipeline/config.py` and environment variables.
- `USE_LIVE_FRED` toggles live acquisition mode.
- `FRED_API_KEY` controls live API access.
- `FRED_SERIES_ID` defaults to `GDP`.
- `FRED_OBSERVATION_START` and `FRED_OBSERVATION_END` apply date-range filters in live mode.
- Reliability controls are environment-based: `FRED_REQUEST_TIMEOUT_SECONDS`, `FRED_MAX_RETRIES`, `FRED_RETRY_BACKOFF_SECONDS`, `FRED_FALLBACK_TO_SAMPLE_ON_ERROR`.
- File output paths are centralized in `pipeline.config`.

## Output demonstration

The integrated run currently produces:
- `data/raw/gdp_raw.json`
- `data/transformed/gdp_transformed.json`
- `output/reports/pipeline_run_summary.md`

The current report shows five raw observations and five transformed records, demonstrating a successful end-to-end pipeline run.
The run summary also records whether live mode was used and what series/date range were requested.

## Known limitations

- The run command currently defaults to sample mode instead of live mode.
- Runtime configuration is limited and not yet exposed through a CLI.
- Observability is sufficient for an MVP but not yet detailed enough for production support.
