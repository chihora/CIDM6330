# ADR-001: Pipeline Style

## Status
Accepted

## Context
Need a runnable MVP pipeline for acquisition, transformation, and integration with low setup overhead.

## Decision
Use a modular monolith pipeline with clear module boundaries.

## Consequences
- Fast development and simple runtime
- Lower operational complexity
- Future distributed scaling requires additional refactoring
