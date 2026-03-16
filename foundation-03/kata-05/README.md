# Kata 5 - Concurrent Data Fetching

Foundation 3, Sprint Week 1

## Required Implementation

This kata fetches data from multiple URLs concurrently using Python threads.

### Checklist
- Uses `concurrent.futures.ThreadPoolExecutor`
- Reads URLs and runtime settings from `config.json`
- Supports configurable `thread_pool_size`
- Applies request timeout handling with `timeout_seconds`
- Handles individual request failures without stopping the whole run
- Uses a lock for thread-safe writes to shared result and error collections
- Writes successful responses to the configured output file
- Writes failed responses to the configured error log file

## Configuration

The `config.json` file contains:
- `thread_pool_size`
- `timeout_seconds`
- `urls`
- `output_file`
- `error_log_file`

## Run

From the `kata-05` directory:

```bash
python fetch_data.py
```

## Output

- Successful results are written to the file named in `output_file`
- Failed requests are written line-by-line to the file named in `error_log_file`

## Stretch (Optional)

### Asyncio Version

An optional asyncio implementation is included in `fetch_data_async.py`.

Run:

```bash
python fetch_data_async.py
```

### Performance Comparison

Use `compare_performance.py` to run both implementations and compare elapsed time.

Run:

```bash
python compare_performance.py
```

### Stretch Dependency

```bash
pip install -r requirements.txt
```
