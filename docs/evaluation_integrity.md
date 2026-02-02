# Evaluation Integrity

Principles and practices for maintaining consistent, comparable, and auditable evaluations over time within the Leah Contract Review Evaluation Framework.

---

## Core Principles

### 1. Separation of Concerns

| Layer | Purpose | Mutability | Visibility |
|-------|---------|------------|------------|
| **Source** | Ground truth, model outputs, rubrics | Versioned | Shared |
| **Internal** | Exceptions, overrides, processing logs | Mutable during review | Private |
| **Deliverables** | Workbooks, reports | Immutable after finalisation | Stakeholders |

**Why:**
- Prevents contamination between source data and artifacts
- Keeps working files separate from clean outputs
- Deliverables contain no process artifacts, confidence markers, or intermediate state

### 2. Single Source of Truth

- One scoring function per mode, parameterised
- One ground truth file per contract/mode, versioned
- One rubric per mode, documented
- Evaluation JSONs are the source of truth; workbooks are derived views
- Configuration over duplication

**Why:** Fixes propagate everywhere. Divergence is impossible.

### 3. Temporal Consistency

Evaluations are snapshots in time. When comparing results:
- Same ground truth version
- Same rubric version
- Same extraction pipeline
- Same scoring logic

**Why:** "Model X improved by 5%" is only meaningful if the measuring stick did not change.

### 4. Audit Trail

Every evaluation must answer:
- What ground truth version was used?
- What model output source was evaluated?
- What extraction date/method was applied?
- What exceptions were reviewed?
- Who reviewed and approved the results?

**Why:** Enables debugging, dispute resolution, and confidence in results.

---

## Scoring Model

Evaluations produce four independent scores. No combined "overall score" is computed -- weighting is deferred to analysis.

### Recall (R)

Measures ground truth issue detection.

**Formula:**
```
R = SUM(Detection Points) / Max Possible Points

Where:
- T1: Y=8, P=4, N=0, NMI=0
- T2: Y=5, P=2.5, N=0, NMI=0
- T3: Y=1, P=0.5, N=0, NMI=0
```

**Reported as:** Percentage (0--100%)

### Precision (P)

Measures signal quality of additional issues (beyond ground truth).

**Formula:**
```
P = Valid Additional / (Valid Additional + Not Material)
```

Where:
- **Valid Additional** = Genuine legal issues not in ground truth
- **Not Material** = Noise, hallucinations, over-flagging

**Note:** "Valid - Overlaps GT" is excluded from the precision calculation. It indicates a matching issue and triggers reconciliation back to the ground truth.

**Reported as:** Percentage (0--100%)

### Quality -- Rationale (Q-Rat)

Measures quality of legal reasoning when issues are detected.

**Scale:** 0--3
- 3 = Excellent: Legal risk + business impact + specific values
- 2 = Adequate: Risk + context, missing specifics
- 1 = Weak: States problem, no substance
- 0 = Missing/Wrong: No rationale or contradicts issue

**Reported as:** Average (0.0--3.0)

### Quality -- Amendment (Q-Amd)

Measures quality of proposed fixes when issues are detected.

**Scale:** 0--3
- 3 = Comprehensive: Legally sound, immediately usable
- 2 = Adequate: Core issue addressed, minor gaps
- 1 = Weak: Acknowledges problem, fix incomplete
- 0 = Missing/Wrong: No amendment or makes worse

**Reported as:** Average (0.0--3.0)

### Score Independence

**Primary view:** Four columns, no single rank.

| Model | R | P | Q-Rat | Q-Amd |
|-------|---|---|-------|-------|
| Model A | 91% | 85% | 2.9 | 2.9 |
| Model B | 93% | 72% | 2.8 | 2.8 |

**Secondary view (if ranking required):** F1 score as tiebreaker.

```
F1 = 2 * (R * P) / (R + P)
```

F1 balances recall and precision. It is a standard metric, defensible, and does not require arbitrary weights.

See [scoring methodology](scoring_methodology.md) for detailed formulae and per-mode scoring differences.

---

## Data Immutability Rules

| Data | When Immutable |
|------|----------------|
| Model outputs (canonical JSON) | After extraction validated |
| Ground truth | After version tagged as LOCKED |
| Evaluation JSONs | After finalisation |
| Archived evaluations | Always |

**Never:**
- Include internal fields in deliverables
- Edit ground truth while evaluations are in progress
- Modify archived evaluations
- Commit internal working files to shared repositories

**Always:**
- Lock ground truth version before starting evaluation
- Archive before ground truth updates
- Strip internal fields before generating deliverables
- Log all processing steps for audit

---

## Ground Truth Versioning

**Version scheme** (aligned with [ground truth principles](ground_truth_principles.md)):

```
{major}.{minor}_{status}

Examples:
- 1.0_DRAFT      (initial development)
- 1.0_LOCKED     (frozen for evaluation)
- 2.0_LOCKED     (structural changes, re-evaluation required)
- 2.1_LOCKED     (minor fixes applied)
```

**Increment rules:**
- **Major:** Issues added/removed, tier changes
- **Minor:** Wording refinements, key_elements updates, clause reference corrections
- **Status:** DRAFT (in development), LOCKED (frozen for evaluation)

### Changelog Tracking

Each mode maintains a changelog in machine-readable format:

```json
{
  "current_version": "1.0_LOCKED",
  "history": [
    {
      "version": "1.0_LOCKED",
      "date": "2026-01-01",
      "total_issues": 160,
      "changes": "Initial GT locked for evaluation"
    }
  ]
}
```

### Locking Rules

- **LOCKED versions are immutable.** No modifications permitted once a version is tagged LOCKED.
- Any change, however minor, requires a new version number.
- Changes must be documented with rationale.
- Impact on existing evaluations must be assessed.
- Affected model runs must be re-scored if tier changes affect T1 gates.

### Rubric Versioning

Rubric changes are tracked via dated version annotations. Major rubric changes require a new ground truth version to maintain comparability.

---

## Temporal Consistency

When comparing results across time or across model versions, the following must be held constant:

| Component | Requirement |
|-----------|-------------|
| Ground truth version | Identical |
| Scoring rubric | Identical |
| Extraction pipeline | Same version |
| Quality rubric | Same scale and criteria |

If any component changes between evaluations, results are not directly comparable and must be noted as such.

---

## Pipeline Integrity and Data Governance

Evaluation results should be **traceable, reproducible, and free from process artifacts**. This means:

### Traceability

- Every score can be traced back to a specific ground truth issue, model output, and evaluation decision
- Override decisions are logged with evidence and rationale
- Version information is embedded in every evaluation record

### Reproducibility

- Given the same inputs (ground truth, model outputs, rubric), the same scores should be produced
- Deterministic pipeline steps produce identical output on re-run
- Non-deterministic steps (quality scoring) are logged for audit

### Clean Deliverables

Deliverables delivered to stakeholders must NOT contain:
- Confidence flags or levels
- Match type indicators (EXACT/ADJACENT/KEYWORD)
- Processing analysis or intermediate suggestions
- Exception classifications
- Internal field markers (anything prefixed with `_`)

Deliverables should present clean, authoritative evaluation results without exposing the mechanics of the evaluation pipeline.

---

## Exception-Based Review Model

The evaluation pipeline flags exceptions for human review rather than requiring review of all items.

### Exception Categories

| Level | Criteria | Action Required |
|-------|----------|-----------------|
| **CRITICAL** | T1 detection N/NMI; keyword-only match on T1/T2 | Must review |
| **WARNING** | Adjacent clause match; zero quality score on detected issue | Spot-check |
| **CLEAN** | Exact match, high confidence | Audit sample only |

### Review Requirements

- All CRITICAL exceptions must have an explicit decision (accept or override)
- WARNING exceptions should be spot-checked (10--20% sample)
- CLEAN items are auto-accepted unless audit reveals systematic errors
- Decisions are recorded in override files
- Overrides applied deterministically at finalisation

---

## Additional Issue Classification

Model outputs that do not match any ground truth issue are classified as:

| Classification | Definition | Impact |
|----------------|------------|--------|
| **Valid - Truly Additional** | Legitimate legal concern not in GT | Counted in Precision numerator |
| **Valid - Overlaps GT** | Matches GT semantically but not by clause reference | Triggers reconciliation; flags matching gap |
| **Not Material** | Noise, hallucination, or non-issue | Counted in Precision denominator only |

### Reconciliation

When "Valid - Overlaps GT" is identified:
1. GT detection upgraded from N/NMI to P (partial)
2. Points recalculated
3. Reconciliation logged with evidence
4. Matching rules reviewed for improvement

**Important:** High reconciliation rates indicate matching rule gaps, not model quality issues.

---

## Zero-Score Validation

### Principle

**A score of zero indicates a data issue, not model performance.**

No model should score 0 on any contract under normal conditions. A zero score means the pipeline failed to process the inputs correctly.

### Zero Score Locations and Likely Causes

| Zero Score Location | Likely Cause |
|---------------------|--------------|
| Part A = 0 | Model output not parsed, counterparty redlines not found |
| Part B = 0 | Model output missing or malformed |
| Part C = 0 | Redline document not loaded |
| All models = 0 on same item | Ground truth issue (wrong clause reference) |
| Single model = 0 | File missing or format different |

### Validation Protocol

```
1. STOP -- Do not aggregate
2. Diagnose: model output --> ground truth --> source files
3. Fix the data issue
4. Re-validate before proceeding
```

**Rule:** Never aggregate results if any model scores 0 on any contract without first diagnosing the cause.

---

## Audit Checklist

### Before Finalising Any Evaluation

- Manifest shows correct ground truth version
- All exceptions reviewed (CRITICAL decided, WARNING spot-checked)
- Zero-score check passed (no data issues)
- Reconciliation rate within normal bounds
- Deliverables generated and spot-checked
- No internal fields in deliverables
- Processing logs archived

### Before Updating Ground Truth

- Current evaluations archived
- Changelog entry prepared with source and rationale
- Version number incremented appropriately
- Affected evaluations identified for re-run consideration

---

## Tracked Fields Without Score Impact

The following are tracked for informational purposes but do not affect R, P, or Q scores:

| Field | Purpose |
|-------|---------|
| Classification Match | Did model classification match expected? |
| Action Match | Did model action match expected? |
| Match Type | EXACT/ADJACENT/KEYWORD/NONE (internal only, stripped from deliverables) |
| Exception Level | CRITICAL/WARNING/CLEAN (internal only, stripped from deliverables) |
| Reconciliation Flag | Was this upgraded via reconciliation? (internal only, stripped from deliverables) |

---

## Evaluation Workflow

### Phase 1: Extraction (Deterministic)

Parse model outputs exhaustively into structured format.

### Phase 2: Matching (Deterministic + Assisted)

- EXACT matches: auto-resolved
- ADJACENT/KEYWORD matches: resolved with confidence scoring

### Phase 3: Detection Scoring (Deterministic + Assisted)

- Clear Y/N cases: deterministic
- Partial (P) judgements: scored with confidence

### Phase 4: Quality Scoring

Score Q-Rat and Q-Amd for all detected issues.

### Phase 5: Additional Issue Classification

Classify each additional issue with confidence level.

### Phase 6: Exception Generation (Deterministic)

Flag items requiring human review based on:
- T1 failures
- Low confidence decisions
- Contradictory signals

### Phase 7: Human Review

Review flagged exceptions:
- Decide all CRITICAL items
- Spot-check WARNING items
- Record override decisions

### Phase 8: Finalisation (Deterministic)

- Apply overrides
- Strip internal fields
- Generate deliverables

---

## Deliverable Outputs

### Source of Truth

Evaluation JSONs are the authoritative data source. Workbooks and reports are derived views -- they contain no data not present in the evaluation JSONs.

### Standard Deliverable Structure

| Sheet | Purpose |
|-------|---------|
| **Executive Summary** | Key metrics, model rankings by R, P, Q-Rat, Q-Amd |
| **Model Leaderboard** | All models with four scores (F1 if ranking needed) |
| **Contract Comparison** | Score matrix (contract x model) |
| **T1 Analysis** | T1 detection statistics per contract per model |
| **Detection Heatmap** | All GT issues x all models with detection values |
| **Quality Scores** | Q-Rat and Q-Amd by model and contract |
| **Issue Difficulty** | Hard/Medium/Easy classification by detection rate |
| **Blind Spots** | Issues missed by multiple or all models |
| **Additional Issues** | Beyond-GT findings with classification |
| **Raw Data** | Full evaluation data |
