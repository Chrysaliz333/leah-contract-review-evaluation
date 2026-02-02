# Leah Contract Review Evaluation Framework

A comprehensive evaluation framework for benchmarking AI-powered contract review against expert legal ground truth. Built to assess **Leah**, Leah AI's contract review system, across 10 contract types, 6 AI models, and 5 evaluation modes.

## Key Numbers

| Metric | Value |
|--------|-------|
| Ground truth issues | 160+ hand-authored |
| Contract types | 10 (SLA, DPA, Consulting, Distribution, JV, License, Partnership, Reseller, Services, Supply) |
| AI models evaluated | 6 |
| Evaluation modes | 5 (Freeform, Freeform Stacking, Rules, Rules Stacking, Guidelines) |
| Scoring dimensions | Detection + amendment quality + rationale quality + redline quality |
| Max points per contract | 787 (freeform mode) |

## Pipeline Architecture

```
Contracts (.docx)        Ground Truth (JSON)        Scoring Config (JSON)
       |                        |                          |
       v                        v                          v
+--------------+      +-------------------+      +------------------+
|  Leah AI     |      |  160+ Issues      |      |  Tier Weights    |
|  Contract    |------+  T1/T2/T3 Tiers   +------+  Quality Rubrics |
|  Review      |      |  Semantic Match   |      |  Gate Criteria   |
+--------------+      +-------------------+      +------------------+
       |                        |                          |
       v                        v                          v
+------------------------------------------------------------------+
|                    Evaluation Pipeline                            |
|  +----------+  +-----------+  +----------+  +---------------+    |
|  | Detection |->| Scoring   |->| Quality  |->| Aggregation   |   |
|  | Matching  |  | Engine    |  | Assess.  |  | & Reporting   |   |
|  +----------+  +-----------+  +----------+  +---------------+    |
+------------------------------------------------------------------+
       |
       v
+------------------------------------------------------------------+
|  Results: Per-model scores, T1 gate pass/fail, quality metrics   |
+------------------------------------------------------------------+
```

## Results: Freeform Mode (Model Comparison)

Evaluation results across 10 commercial contracts and 160+ ground truth issues:

| Model | Detection Rate | T1 Pass Rate | Avg Quality Score |
|-------|---------------|-------------|-------------------|
| Pioneer Deep | 95.0% | 6/10 | 2.89 |
| Sonnet 4.5 | 94.4% | 5/10 | 2.90 |
| Starliner | 87.5% | 3/10 | 2.54 |
| Scale | 84.4% | 7/10 | 2.56 |
| Pathfinder | 83.9% | 5/10 | 2.61 |
| Velocity | 66.2% | 2/10 | 2.17 |

**Key findings:**

- **Detection rate and T1 pass rate don't always correlate.** Scale achieves the highest T1 pass rate (7/10) despite lower overall detection, indicating it prioritises critical issues effectively.
- **Pioneer Deep and Sonnet 4.5 lead on raw detection** but miss more T1 issues, suggesting breadth of coverage doesn't guarantee depth on critical items.
- **Quality scores cluster tightly** (2.17-2.90 on a 3-point scale), making remediation quality a harder differentiator than detection capability.
- **Velocity significantly trails** on all dimensions, with a 66.2% detection rate and only 2/10 T1 passes.

## Evaluation Modes

| Mode | What It Tests | Contracts | Context Document |
|------|---------------|-----------|------------------|
| **[Freeform](docs/modes/freeform.md)** | Risk identification with no guidance | 10 | None |
| **[Freeform Stacking](docs/modes/freeform_stacking.md)** | Response to counterparty redlines + whole-doc risk | 10 | Redlined contracts |
| **[Rules](docs/modes/rules.md)** | Compliance with deterministic rules | 20 | Deterministic rule CSV |
| **[Rules Stacking](docs/modes/rules_stacking.md)** | Redline-specific rule application | 10 | Redlined contracts + Rule CSV |
| **[Guidelines](docs/modes/guidelines.md)** | Playbook-based position guidance | 20 | Playbook (GS/FB1/FB2/RF hierarchy) |

Each mode tests a different aspect of contract review capability. Freeform measures pure legal judgment; Rules measures deterministic compliance; Guidelines measures the ability to apply structured negotiation playbooks.

## Ground Truth: What Expert Analysis Looks Like

Each ground truth issue is hand-authored with specific legal analysis, statutory references, and remediation guidance. Example from the Consulting contract:

```json
{
  "gt_id": "GT-01",
  "clause": "5.1",
  "tier": "T1",
  "issue": "Work-for-hire designation likely ineffective - IP ownership at risk",
  "key_elements": [
    "Clause relies on work-for-hire doctrine which has LIMITED APPLICATION to independent contractors",
    "Under 17 U.S.C. Section 101, work-for-hire only applies to: (1) employees, or (2) specially commissioned works in 9 enumerated categories WITH a signed writing",
    "Software, reports, and most consulting deliverables do NOT fall within the 9 categories",
    "Without valid work-for-hire, copyright vests in Consultant by default",
    "Should add explicit IP assignment as fallback"
  ],
  "expected_action": "AMEND",
  "contract_text": "All deliverables created by Consultant specifically for Client pursuant to this Agreement shall be considered work-for-hire..."
}
```

This T1 (critical) issue identifies that a standard work-for-hire clause is structurally defective for independent contractor engagements under US copyright law, specifying the exact statutory basis (17 U.S.C. Section 101) and remediation path (explicit IP assignment).

## Scoring Methodology

### Three-Tier System

| Tier | Points | Criteria | Gate |
|------|--------|----------|------|
| **T1** (Critical) | 8 | Structural defects, unlimited exposure, missing protections | Miss = automatic FAIL |
| **T2** (Material) | 5 | Significant negotiation points, allocation gaps | Weighted |
| **T3** (Minor) | 1 | Best practice improvements, drafting suggestions | Weighted |

### Detection + Quality

Each issue is scored on **detection** (did the model find it?) and **quality** (how good was the fix?):

- **Detection**: Y (full), P (partial), N (missed), NMI (not mentioned)
- **Amendment Quality** (1-3): Does the proposed fix address all key elements?
- **Rationale Quality** (1-3): Is the legal reasoning substantive and specific?
- **Redline Quality** (1-3): Is the proposed language precise, well-placed, and usable?

### Semantic Matching

Detection is semantic, not syntactic: *"Did the model identify THIS risk?"* rather than *"Did it reference THIS clause number?"* A model that flags unlimited liability at clause 5.3 when the GT expects 5.2 still receives credit if the risk analysis is correct.

Three criteria determine a semantic match:
1. **Same risk type** - both address the same legal concern
2. **Same party affected** - the representing party faces the same exposure
3. **Similar remediation** - the proposed fix addresses the GT concern

See [docs/scoring_methodology.md](docs/scoring_methodology.md) for the complete methodology.

## How It Was Built

This framework was designed and built through four integrated workstreams:

**Legal Analysis** - Hand-authored 160+ ground truth issues across 10 contract types, each with specific legal reasoning, statutory references where applicable, and remediation guidance. The ground truth establishes what a competent lawyer should identify when reviewing each contract from the representing party's perspective.

**Framework Design** - Designed the multi-tier scoring methodology with weighted detection points, quality rubrics, hard gates (T1 miss = automatic fail), and semantic matching principles. Each of the 5 evaluation modes has a distinct scoring approach calibrated to what it tests.

**Pipeline Engineering** - Built the Python scoring engine as pure functions (no global state, no file I/O, no external API calls), along with ground truth loaders, schema validators, workbook generators, and aggregation scripts. The framework processes evaluations into structured results with full traceability.

**AI Orchestration** - Designed the evaluation agent prompts (see [`prompts/`](prompts/)) that specify detection criteria, quality rubrics, scoring rules, semantic matching principles, and decision trees. These prompts directed AI agents to execute evaluations at scale across all models and contracts.

## Getting Started

```bash
# Clone the repository
git clone <repo-url>
cd leah-contract-review-evaluation

# Install dependencies
pip install -r requirements.txt

# Run the evaluation pipeline notebook
jupyter notebook notebooks/01_evaluation_pipeline.ipynb

# Run scoring tests
pytest tests/
```

The notebook walks through the complete pipeline: loading ground truth, scoring evaluations, visualising model comparisons, and exploring the T1 gate heatmap.

## Repository Structure

```
leah-contract-review-evaluation/
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── notebooks/
│   └── 01_evaluation_pipeline.ipynb       # Interactive pipeline walkthrough
│
├── docs/
│   ├── scoring_methodology.md             # Tier system, quality rubrics, gates
│   ├── ground_truth_principles.md         # GT authoring standards and tiering
│   ├── evaluation_integrity.md            # Data governance and versioning
│   └── modes/                             # Per-mode documentation
│       ├── freeform.md
│       ├── freeform_stacking.md
│       ├── rules.md
│       ├── rules_stacking.md
│       └── guidelines.md
│
├── prompts/                               # Evaluation agent specifications
│   ├── freeform.md
│   ├── freeform_stacking.md
│   ├── rules.md
│   ├── rules_stacking.md
│   └── guidelines.md
│
├── framework/                             # Scoring engine and pipeline tools
│   ├── config/                            # Mode-specific scoring configurations
│   ├── scoring/                           # Pure scoring functions
│   ├── scripts/                           # GT loaders, validators, generators
│   ├── validators/                        # Schema and data validators
│   └── schemas/                           # JSON schemas
│
├── tests/                                 # Scoring module tests
│
├── freeform/                              # Complete: contracts + GT + results
│   ├── contracts/                         # 10 commercial contracts (.docx)
│   ├── ground_truth/                      # 160+ issues (T1/T2/T3)
│   ├── results/                           # Aggregated evaluations (6 models)
│   └── workbooks/                         # Excel deliverables
│
├── freeform_stacking/                     # Complete: redlined contracts + GT + results
│   ├── redlined_contracts/                # 10 contracts with CP redlines
│   ├── ground_truth/                      # Dual GT (Part A: redlines, Part B: whole doc)
│   ├── results/                           # Aggregated evaluations
│   └── workbooks/                         # Stacking workbooks
│
├── rules/                                 # GT + inputs (evaluation pending)
│   ├── contracts/                         # 10 NDA + 10 Subcontract
│   ├── rule_files/                        # Deterministic rule CSVs
│   └── ground_truth/                      # Rule-based GT
│
├── rules_stacking/                        # GT + inputs (evaluation pending)
│   ├── redlined_contracts/                # 5 NDA + 5 Subcontract (redlined)
│   ├── rule_files/                        # Deterministic rule CSVs
│   └── ground_truth/                      # Redline-specific GT
│
└── guidelines/                            # GT + inputs (evaluation pending)
    ├── contracts/                          # 10 NDA + 10 Subcontract
    ├── playbooks/                          # NDA + Subcontract playbooks
    └── ground_truth/                       # Playbook-based GT
```

## Documentation

| Document | Description |
|----------|-------------|
| [Scoring Methodology](docs/scoring_methodology.md) | Tier definitions, detection values, quality rubrics, gate criteria, formulae |
| [Ground Truth Principles](docs/ground_truth_principles.md) | How GT issues are authored, tiered, and validated |
| [Evaluation Integrity](docs/evaluation_integrity.md) | Data governance, versioning scheme, audit trail |
| [Freeform Mode](docs/modes/freeform.md) | Comprehensive risk identification (no context) |
| [Freeform Stacking](docs/modes/freeform_stacking.md) | Counterparty redline response + whole-doc risk |
| [Rules Mode](docs/modes/rules.md) | Deterministic rule compliance |
| [Rules Stacking](docs/modes/rules_stacking.md) | Redline-specific rule application |
| [Guidelines Mode](docs/modes/guidelines.md) | Playbook position guidance with hierarchy |

## Models Evaluated

| Display Name | Model ID |
|--------------|----------|
| Sonnet 4.5 | sonnet45 |
| Pathfinder | pathfinder |
| Starliner | starliner |
| Velocity | velocity |
| Scale | scale |
| Pioneer Deep | pioneer_deep |
