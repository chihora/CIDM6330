# Foundation 2 — Define: Problem + Architecture
**Course:** CIDM 6330 — Software Architecture  
**Student:** Francis Kelechi Njoku  
**Dataset:** FRED Real GDP (GDPC1)  
**Phase:** Define (Foundation 2)

---

## 1) Problem Definition (Commitment)

### Problem Statement
The business problem is that analysts, students, and decision-makers need a reliable way to monitor U.S. economic growth and quickly detect potential downturn signals using Real GDP trends. Today, many users manually pull GDP values, calculate change rates inconsistently, and miss early turning points because the process is not standardized or repeatable. I am building a system that ingests Real GDP data from FRED, transforms it into comparable trend indicators (levels, growth rates, and rolling changes), and produces a consistent output (tables + summary report) that highlights possible turning points.

### Why This Problem (from Foundation 1 discovery)
During Foundation 1 discovery, the dataset supported several candidate problems. I selected macro trend monitoring because it is directly supported by the GDP time series itself (no additional datasets required), yet it still forces meaningful architectural decisions: ingestion cadence, reproducibility, validation, and transformation accuracy. I also learned that even "simple" GDP analysis requires consistent transformation rules (e.g., quarter-over-quarter vs year-over-year changes), which makes a strong case for a structured pipeline.

### Scope Boundaries
**In scope:**
- Pull Real GDP observations from the FRED API for a defined date range
- Validate and normalize observations (types, missing values, ordering)
- Transform GDP into trend indicators:
  - GDP level
  - percent change (QoQ and/or YoY)
  - rolling window changes (e.g., trailing 4 quarters)
- Persist processed data to local storage (CSV and/or SQLite)
- Generate a reproducible markdown report that flags potential downturn signals (e.g., negative growth, consecutive slowdowns)

**Out of scope (Foundation 2 constraints):**
- Multi-indicator correlation discovery across many series
- Machine learning forecasting models (beyond simple baselines)
- Distributed systems concerns (microservices, event-driven coordination)
- Governance, ADRs, enterprise deployment design (later foundations)

### Success Criteria
The system is "working" if:
- It can reliably retrieve GDP observations from FRED and produce the same outputs when re-run with the same inputs (reproducibility)
- Trend indicators are computed correctly and consistently (accuracy)
- The report clearly highlights time periods that meet defined "downturn signal" rules (interpretability)
- The data output is structured so downstream users can visualize or analyze it (CSV/SQLite + markdown summary)

---

## 2) Data Pipeline Definition

### Data Sources
Primary source:
- **FRED API** series observations endpoint for **GDPC1** (Real Gross Domestic Product)

### Data Relationships
This Foundation 2 pipeline is single-series focused. The primary relationship is within the time series itself:
- Each observation is keyed by **date**
- Transformations depend on ordering across dates (previous periods, rolling windows)

### Transformation Requirements
- Parse observation values into numeric types
- Ensure chronological ordering and unique dates
- Handle missing / non-numeric values (drop or log)
- Compute derived fields:
  - QoQ percent change (vs previous quarter)
  - YoY percent change (vs same quarter last year)
  - Rolling change (e.g., trailing 4-quarter change)
- Optional: classify "signals" (e.g., negative growth or consecutive declines)

### Output Shape
Outputs produced for downstream consumers:
- A cleaned dataset containing:
  - `date`
  - `gdp_level`
  - `qoq_pct_change`
  - `yoy_pct_change`
  - `rolling_4q_change`
  - `signal_flag` (true/false or category)
- A markdown report summarizing:
  - date range
  - counts of observations
  - min/max/avg growth rates
  - list of flagged downturn-signal periods

---

## 3) Architecture Characteristics — Driving and Implicit

### Driving Characteristics (Top 3)

#### 1. Analytical Accuracy (Primary)
**Why critical:** Incorrect growth-rate calculations or mis-ordered dates directly produce wrong turning-point signals, which undermines the system's purpose.  
**How to measure:** Unit-level verification of transformation formulas; consistency checks (e.g., recomputation yields same results).  
**If we fail:** Users will not trust outputs; the system becomes worse than manual analysis.

#### 2. Reproducibility
**Why critical:** Users must be able to rerun the pipeline and get the same results for the same parameters (date range, series, transformation rules).  
**How to measure:** Running twice yields identical CSV/SQLite and identical report for the same inputs.  
**If we fail:** Analysis cannot be audited and results cannot be explained or defended.

#### 3. Data Quality & Consistency
**Why critical:** The system depends on clean numeric observations and stable ordering across time.  
**How to measure:** Validation checks (missing values, parse failures, monotonic dates) and logging of rejected records.  
**If we fail:** Transformations break or silently produce misleading results.

### Implicit Characteristics
These are expected but not differentiating for Foundation 2:
- Basic reliability (no crashing on typical errors)
- Basic security hygiene (API keys via environment variables)
- Maintainability (readable modules/functions)

### Characteristic Trade-offs
- **Accuracy vs Speed:** Strong validation and careful transformations cost compute time, but correctness matters more than fast execution for this project stage.
- **Reproducibility vs Flexibility:** Allowing many ad-hoc transformation options can reduce repeatability. I prioritize standardized rules and parameterized configuration over unlimited flexibility.

---

## 4) Architecture Style Selection

### Selected Style: Pipeline Architecture
I selected a **pipeline architecture** (extract → validate → transform → load → report) because it matches the sequential nature of time-series processing and supports my driving characteristics:
- Accuracy: each stage can be tested/verified independently
- Reproducibility: deterministic stages produce repeatable outputs
- Data quality: validation is an explicit stage, not an afterthought

### Alternatives Considered (and why rejected)

#### Layered Architecture
A layered architecture is good for UI/business/data separation, but my system's core complexity is the transformation flow rather than interactive application layers. Pipeline more directly models the work.

#### Microkernel (Plug-in) Architecture
A microkernel could support many analysis plug-ins, but that is premature. Foundation 2 scope is to define one committed problem and a fitting style, not design a large plugin ecosystem.

#### Service-based / Microservices
Distributed styles add operational complexity and coordination trade-offs that are explicitly out of scope for Foundation 2.

### Style-specific Trade-offs
Pipeline costs:
- Changes to transformation logic can affect downstream steps (tight sequential dependency)
- Debugging requires clear logging at each stage
- Adding new analyses may require additional pipeline stages or branching logic

### Quantum Analysis
This design has **one architecture quantum**. The pipeline is deployed as a single cohesive system where components share the same data model and are tightly coupled by the sequential workflow. There is no independent deployable subsystem yet.

---

## 5) Component Identification

### Component Inventory
1. **FRED Client (Extract)**
   - Responsibility: fetch GDP observations from FRED endpoint
   - Owns/processes: raw JSON response

2. **Validation / Normalization**
   - Responsibility: parse values, enforce date ordering, handle missing/bad records
   - Owns/processes: cleaned time series table

3. **Transformation Engine**
   - Responsibility: compute growth rates, rolling metrics, signal flags
   - Owns/processes: enriched analytical dataset

4. **Storage (Load)**
   - Responsibility: write outputs to CSV and/or SQLite in repeatable form
   - Owns/processes: persisted analytical dataset

5. **Report Generator**
   - Responsibility: produce markdown summary report and key statistics
   - Owns/processes: report artifact derived from transformed dataset

### Partitioning Approach
I am using **domain partitioning by capability**, aligned to pipeline stages (extract/validate/transform/load/report). This improves cohesion because each component has a single purpose and clear boundary.

### Boundaries and Cohesion
- Each pipeline stage is **functionally cohesive** (one reason to change per stage)
- Boundaries are enforced through explicit inputs/outputs between stages (dataframes/records/files)

---

## 6) AI Collaboration Log (Summary)
Details are recorded in `AI_LOG.md`, including:
- Style selection dialogue and evaluation against driving characteristics
- How AI helped refine the problem statement and clarify scope boundaries
- Where AI suggestions were rejected or modified due to course scope constraints
