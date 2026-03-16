# ADR-002: Local File Output (SQLite Deferred)

## Status
Accepted

## Context
Need clear, inspectable output artifacts during MVP phase.

## Decision
Use JSON output files for raw and transformed data in Foundation 3; defer SQLite integration.

## Consequences
- Easy to inspect and debug outputs
- Minimal dependency and setup burden
- Less efficient querying compared with database storage
