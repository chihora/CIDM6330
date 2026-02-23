# Kata 3 — API Consumption (FRED)

## What this kata does
- Fetches paginated results from FRED `series/search` using `limit` + `offset`
- Fetches Real GDP (GDPC1) observations for 10-year history
- Implements retry logic with exponential backoff
- Handles HTTP errors and rate limits (429)
- Writes outputs to `output/` as JSON

## How to run
Set API key:
- PowerShell: `setx FRED_API_KEY "your_32_char_lowercase_key"`

Restart terminal, then:

```bash
python -m pip install requests
python foundation-02/katas/kata-03-api/kata3_api_consume.py
```