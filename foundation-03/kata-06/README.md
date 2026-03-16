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

### Bisect Evidence from This Assignment

Validation command used while bisecting:

```bash
python check_kata6_output.py
```

Known-good commit:
- `2b90245` - `feat: add kata 6 multiprocessing chunk processor with progress and failure handling`

Known-bad commit (intentional bug):
- `d408b57` - `test: intentionally introduce kata6 aggregation bug for bisect exercise`

Commands executed:

```bash
git bisect start
git bisect bad d408b57
git bisect good 2b90245
git bisect log
git bisect reset
```

Bisect result:
- First bad commit identified: `d408b57a005a53539d124d3e66e1eb6a2733fcd8`

Bug introduced:
- In `combine_results`, `total_count` was incorrectly changed to `len(chunk_results)` instead of summing each chunk's item count.

Fix commit:
- `cc21e1e` - `fix: restore correct kata6 total_count aggregation`

## Stretch (Optional): Shared State with Manager

This implementation uses `multiprocessing.Manager` to maintain shared progress counters (`completed`, `failed`) while worker futures finish.
