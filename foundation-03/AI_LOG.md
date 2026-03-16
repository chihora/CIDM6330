# AI_LOG

## Foundation 3

### Process Description
- I used AI primarily for project scaffolding, implementation planning, draft code generation, and documentation structure.
- I worked iteratively: define the deliverable, ask AI for a practical implementation path, run the code locally, then revise anything that was too generic or did not fit the GDP/FRED pipeline scope.
- I did not accept AI suggestions blindly. I treated AI output as a starting point and verified behavior by running the pipeline and unit tests.

### Decision Log
- Decision: keep Foundation 3 as a modular monolith instead of distributing components.
	- Asked AI: whether to start with a service split or a local pipeline.
	- AI suggested: keep the first MVP local and modular because working code matters more than premature infrastructure.
	- What I did: accepted the modular local pipeline approach.
	- Why: it fits the assignment scope and makes iteration evidence easier to show.

- Decision: use sample GDP data by default with optional live FRED mode.
	- Asked AI: how to keep the code runnable without depending on external network access.
	- AI suggested: add a sample payload path and allow live API mode when an API key exists.
	- What I did: accepted and implemented that design.
	- Why: it guarantees runnable code for grading while still showing a realistic FRED integration path.

- Decision: output raw and transformed JSON files instead of adding a database in Foundation 3.
	- Asked AI: whether SQLite should be introduced immediately.
	- AI suggested: defer database output and keep artifacts inspectable in files.
	- What I did: accepted that suggestion for Foundation 3.
	- Why: it keeps the MVP simple and makes transformation results easy to inspect in the repo.

- Decision: add retry/backoff and fallback behavior for live FRED acquisition.
	- Asked AI: how to strengthen API/network/rate-limit handling without over-engineering the MVP.
	- AI suggested: configurable retries, exponential backoff, and optional fallback to sample payload.
	- What I did: accepted and implemented this pattern in acquisition/config.
	- Why: it improves reliability and aligns better with the assignment rubric while keeping the pipeline runnable.

### AI Failures
- AI initially generated documentation that was too generic and not tied closely enough to my actual GDP/FRED code. I rewrote the docs to reference the real modules, outputs, and current limitations.
- AI also tended to suggest broader architecture options, including more structure than the assignment needed. I reduced that to a practical modular pipeline because working code was more important than speculative design.
- In earlier work during Foundation 3, AI-generated git and PR suggestions needed adjustment because they were not always aligned with my instructor's requirement that each assignment be submitted individually.

### Verification Practices
- I verify AI-generated code by running the pipeline locally with `python -m pipeline.run_pipeline`.
- I verify correctness at a basic level by running `python -m unittest discover -s pipeline/tests -p "test_*.py"`.
- I inspect generated artifacts in `data/raw`, `data/transformed`, and `output/reports` to confirm the pipeline produced the expected files.
- I compare documentation claims against the current implementation before treating them as final submission content.

### Judgment Patterns
- I usually override AI when it introduces more complexity than the assignment needs.
- I also override AI when suggestions are too abstract and not grounded in the current codebase.
- A recurring pattern is that AI is useful for generating first drafts quickly, but I need to tighten scope, remove unnecessary architecture, and align the final work to the exact rubric language.
