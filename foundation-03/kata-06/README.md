# Kata 6 - Process-Based Parallelism

Foundation 3, Sprint Week 2

## Required Implementation

This kata demonstrates CPU-bound parallel data processing using process-based concurrency.

### Checklist
- Uses `concurrent.futures.ProcessPoolExecutor`
- Generates a large dataset and splits it into chunks
- Processes chunks in separate worker processes
- Combines chunk results into one final output
- Handles worker process failure per chunk without stopping all work
- Reports progress as chunks complete

## Configuration

`config.json` keys:
- `dataset_size`
- `chunk_size`
- `max_workers`
- `simulate_worker_failures`
- `fail_chunk_indices`
- `output_file`
- `error_log_file`

## Run

From `foundation-03/kata-06`:

```bash
python process_data.py
```

## Output

- `results.json`: aggregated and per-chunk processing output
- `errors.log`: one JSON record per failed chunk

## Git Bisect Documentation (Required)

Use a commit where processing works as a known-good state, then test after introducing a bug commit.

```bash
git bisect start
git bisect bad
git bisect good <known-good-commit>
```

Git will check out a middle commit each step.
Run your test command at each step, then mark:

```bash
git bisect good
# or
git bisect bad
```

When bisect finishes, document:
- The commit hash identified by bisect
- The bug introduced in that commit
- The fix commit that resolves it

Reset bisect after completion:

```bash
git bisect reset
```

## Stretch (Optional): Shared State with Manager

This implementation uses `multiprocessing.Manager` to maintain shared progress counters (`completed`, `failed`) while worker futures finish.
