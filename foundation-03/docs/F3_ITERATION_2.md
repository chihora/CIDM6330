# F3 Iteration 2 - Data Transformation

## Goal
Transform raw GDP/FRED observations into cleaned records that are usable for downstream analysis and reporting.

## What works
- `pipeline.transform.transform_observations()` reads the raw `observations` collection and normalizes each valid row into a simple structure:
	- `date`
	- `value`
- Numeric values are converted from strings to floats.
- Invalid rows are filtered before output is written.
- `pipeline.transform.save_transformed_data()` writes cleaned records to `data/transformed/gdp_transformed.json`.

## Transformation logic

- Ignore any row where the date is missing.
- Ignore any row where the value is `None` or `.`.
- Ignore rows where the value cannot be parsed as a float.
- Preserve valid date/value pairs in a smaller, cleaner output structure.

These transformations support the project goal by converting source-oriented API payloads into analysis-ready records.

## Data quality assumptions
- Rows with `.` or non-numeric values are dropped.
- Rows with missing dates are dropped.
- Valid numeric values are assumed to be interpretable as GDP observations without further unit conversion in this MVP.

## Output artifact

The transformed artifact is stored in `data/transformed/gdp_transformed.json`. In the current sample run, all five sample observations remain valid after transformation.

## Known limitations

- There is no outlier analysis yet.
- There is no imputation strategy for missing values; invalid rows are simply removed.
- The current transform does not add derived metrics such as percent change or rolling averages.

## Next
Integrate acquisition and transformation into one coherent pipeline command with logging, summary output, and reusable configuration.
