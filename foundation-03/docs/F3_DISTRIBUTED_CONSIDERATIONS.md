# F3 Distributed Considerations

## Current state
The pipeline is monolithic and local. Acquisition, transformation, and output all run in a single process on one machine.

## Why not distributed yet
- Dataset size and throughput needs are modest.
- Team and assignment scope prioritize runnable correctness over infrastructure complexity.
- A distributed design would add coordination, deployment, and debugging cost without improving the current MVP enough to justify the trade-off.

## Future distribution path
- Split acquisition into scheduled worker.
- Queue transformed jobs for asynchronous processing.
- Move output into managed storage and event notifications.
- Introduce message-based handoff only when pipeline stages need to scale independently.

## Communication style if distributed later

If this pipeline were distributed, asynchronous messaging would likely fit better than synchronous service chaining. Acquisition could publish raw payload availability, and transformation could consume that event and write normalized data. That would reduce direct coupling between stages.

## Data ownership
Current source of truth is the raw payload in `data/raw`. The transformed data in `data/transformed` is derived output. If the system were distributed later, preserving that distinction would matter: acquisition owns source capture, transformation owns derived representations, and downstream reporting should not overwrite the raw source of truth.
