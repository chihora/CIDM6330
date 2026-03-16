# F3 Risk Identification

## Technical risks
- External API availability or latency
- Schema drift in source payload
- Silent data quality degradation
- Environment-variable misconfiguration for live runs

## Data risks
- Missing or non-numeric values
- Unexpected date gaps
- Backfilled historical revisions
- Differences between sample payload structure and live payload behavior

## Architectural risks
- Tight coupling if orchestration grows in one module
- Limited observability in failure scenarios
- Local file output may become limiting if historical comparisons or multiple datasets are introduced

## Mitigations
- Explicit payload validation
- Transformation filters and tests
- Stage-level logging and run summaries
- Keeping raw and transformed artifacts separate so errors can be traced to the correct stage

## Highest-priority risks right now

1. Live API fragility. The project can run without the network, but live mode is still the least mature part of the design.
2. Hidden data quality issues. Dropping invalid rows is safe for an MVP, but it can hide how much data quality loss is happening.
3. Pipeline growth pressure. The current modular monolith is the right trade-off now, but adding more stages without clearer boundaries would increase refactoring cost later.
