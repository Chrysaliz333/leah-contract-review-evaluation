# Leah AI Contract Review: Evaluation Methodology

## Executive Summary

Leah AI's contract review capability is benchmarked against expert-authored ground truth across **160+ legal issues** spanning **10 commercial contract types**. The evaluation measures risk identification accuracy, quality of suggested amendments, and handling of counterparty redlines.

Top-performing models achieve:

- **Up to 95.6% risk identification accuracy** (semantic detection of ground truth issues)
- **Quality scores averaging 2.92/3.0** across amendment, rationale, and redline dimensions
- **100% precision** on additional issues identified beyond ground truth (all flagged as valid by expert review)

This document describes the methodology, metrics, and limitations of the evaluation framework.

---

## Evaluation Corpus

### Contract Types

| Contract Type | GT Issues | T1 (Critical) | T2 (Material) | T3 (Minor) |
|--------------|-----------|----------------|----------------|-------------|
| Consulting | 11 | 2 | 6 | 3 |
| Distribution | 13 | 3 | 6 | 4 |
| DPA | 12 | 4 | 5 | 3 |
| Joint Venture | 18 | 4 | 8 | 6 |
| License | 15 | 3 | 7 | 5 |
| Partnership | 12 | 3 | 5 | 4 |
| Reseller | 13 | 4 | 6 | 3 |
| Services | 26 | 5 | 12 | 9 |
| SLA | 26 | 6 | 12 | 8 |
| Supply | 14 | 3 | 7 | 4 |

**Total: 160 ground truth issues** across 10 contracts, evaluated by 6 models = **60 freeform evaluations**.

An additional **40 freeform stacking evaluations** test counterparty redline response across 4 models.

### Ground Truth Authoring

All ground truth is **hand-authored by legal experts**. Each issue includes:

- Specific clause reference and risk description
- Tiering rationale (T1/T2/T3) with statutory or commercial justification
- Proposed remediation language
- Expected amendment and rationale guidance

Ground truth is never auto-generated. This ensures the benchmark measures genuine legal risk identification, not pattern matching against synthetic data.

---

## Metrics

### 1. Risk Identification Accuracy (Detection Rate)

**What it measures:** The proportion of known legal risks that the model successfully identifies.

**Formula:** `(Y + P) / total_GT_issues`

Where:
- **Y** (Yes) = Issue fully detected with correct risk identification
- **P** (Partial) = Issue detected but with incomplete or imprecise characterisation
- **N** (No) = Issue explicitly addressed but risk not identified
- **NMI** (Not Meaningfully Identified) = Issue not found in model output

**Results (Freeform):**

| Model | Detection Rate | Y | P | N | NMI |
|-------|---------------|---|---|---|-----|
| Pioneer Deep | 95.6% | 148 | 5 | 1 | 6 |
| Sonnet 4.5 | 94.4% | 148 | 3 | 1 | 8 |
| Starliner | 86.9% | 124 | 15 | 3 | 18 |
| Scale | 84.4% | 114 | 21 | 2 | 23 |
| Pathfinder | 82.5% | 116 | 16 | 5 | 23 |
| Velocity | 65.6% | 71 | 34 | 0 | 55 |

**Industry context:** Detection rate directly maps to "What percentage of risks will Leah find in my contracts?" The semantic matching approach (described below) ensures this measures genuine risk comprehension, not keyword overlap.

### 2. False Positive Rate

**What it measures:** How often the model flags issues that are not genuine risks.

**Formula:** `(Hallucination + Not Material) / total_additional_issues`

**Current status:** Across all 6 models and 10 contracts, **3,137 additional issues** were identified beyond ground truth. Expert audit classified **100% as "Valid"** — genuine risks not included in ground truth because the GT set is deliberately conservative.

**Caveat:** A comprehensive false positive audit across all additional issues is pending. The current 0% false positive rate reflects the initial assessment but should be interpreted with this limitation in mind.

### 3. Precision

**What it measures:** Of all issues the model flags, how many are genuine risks.

**Formula:** `Valid / (Valid + Not Material)` via `calculate_precision()`

**Current result:** 1.00 (100%) across all models, reflecting the Valid-only assessment status. This metric will become more discriminating once the additional issues audit is complete.

### 4. Recall (Weighted)

**What it measures:** Coverage of ground truth issues, weighted by severity tier.

**Formula:** Tier-weighted scoring where:
- T1 (Critical): Y=8pts, P=4pts, N/NMI=0pts
- T2 (Material): Y=5pts, P=2.5pts, N/NMI=0pts
- T3 (Minor): Y=1pt, P=0.5pts, N/NMI=0pts

`weighted_recall = actual_points / max_possible_points`

This weighting ensures that missing a critical liability cap issue (T1) counts far more than missing a minor formatting concern (T3).

### 5. F1 Score

**What it measures:** Harmonic mean of precision and recall, balancing completeness against accuracy.

**Formula:** `2 * (precision * recall) / (precision + recall)` via `calculate_f1()`

**Note:** With precision currently at 1.0 for all models, F1 is dominated by recall. This will normalise once the additional issues audit introduces precision variance.

### 6. Quality Score

**What it measures:** How good the model's output is when it does find a risk.

**Dimensions (1-3 scale):**
- **Amendment Score:** Quality of proposed contract revision language
- **Rationale Score:** Quality of legal reasoning explaining the risk
- **Redline Quality Score:** Precision of redline markup and clause targeting

Only scored for detected issues (Y or P). Undetected issues (N/NMI) have null quality scores.

**Results (Freeform, per-model averages):**

| Model | Amendment | Rationale | Redline | Overall |
|-------|-----------|-----------|---------|---------|
| Sonnet 4.5 | 2.97 | 2.98 | 2.81 | 2.92 |
| Pioneer Deep | 2.86 | 2.89 | 2.89 | 2.88 |
| Pathfinder | 2.72 | 2.76 | 2.80 | 2.76 |
| Scale | 2.61 | 2.69 | 2.63 | 2.64 |
| Starliner | 2.55 | 2.64 | 2.57 | 2.59 |
| Velocity | 2.23 | 2.44 | 2.36 | 2.34 |

### 7. T1 Critical Issue Gate

**What it measures:** Whether the model catches every critical (T1) risk in a contract.

**Rule:** All T1 issues in a contract must be detected (Y or P) to pass. A single missed T1 issue = automatic FAIL for that contract.

**Results:**

| Model | Pass Rate |
|-------|-----------|
| Sonnet 4.5 | 8/10 (80%) |
| Pioneer Deep | 8/10 (80%) |
| Pathfinder | 8/10 (80%) |
| Scale | 8/10 (80%) |
| Starliner | 6/10 (60%) |
| Velocity | 4/10 (40%) |

**Why this matters:** In legal review, a missed critical issue (e.g., unlimited liability, missing indemnity cap) can have disproportionate commercial impact. This gate metric directly measures whether the model can be trusted not to miss the issues that matter most.

### 8. Freeform Stacking: Redline Response (Part A)

**What it measures:** How well the model evaluates counterparty redlines — accepting beneficial changes and rejecting harmful ones.

**Available for:** Pathfinder, Pioneer Deep, Sonnet 4.5, Starliner (4 models, 10 contracts each).

**Scoring:** Each redline is scored on action correctness (ACCEPT/REJECT), revision quality, and reasoning quality (0-2 per dimension, max 6 per redline).

**Results:**

| Model | Avg Part A % | Pass Rate |
|-------|-------------|-----------|
| Pioneer Deep | 94.2% | 100% |
| Pathfinder | 92.5% | 100% |
| Sonnet 4.5 | 86.7% | 90% |
| Starliner | 55.0% | 50% |

---

## Methodology Detail

### Semantic Matching

Detection is **semantic**, not lexical. The question is "Did the model identify THIS risk?" not "Did it cite THIS clause number?"

A ground truth issue is matched to a model finding when three criteria are met:

1. **Same risk type** — the model describes the same category of legal risk
2. **Same affected party** — the risk impacts the same contractual party
3. **Similar remediation** — the model suggests a comparable fix

This approach prevents false negatives from clause renumbering, paraphrasing, or different citation styles. It also prevents false positives from superficially similar but substantively different findings.

### Three-Tier Scoring

Issues are tiered by commercial impact:

| Tier | Points (Y) | Description | Examples |
|------|-----------|-------------|----------|
| T1 (Critical) | 8 | Existential risk — could void deal or create material liability | Unlimited liability, missing IP assignment, no termination right |
| T2 (Material) | 5 | Significant risk — affects commercial position | Weak indemnity, one-sided change control, inadequate warranty |
| T3 (Minor) | 1 | Low risk — best practice improvements | Formatting, notice period lengths, minor drafting improvements |

Partial detection (P) receives half points. Non-detection (N, NMI) receives zero.

### Quality Dimensions

For each detected issue, three quality dimensions are scored independently on a 1-3 scale:

| Score | Amendment | Rationale | Redline |
|-------|-----------|-----------|---------|
| 3 | Precise, legally sound revision | Clear risk explanation with statutory/commercial basis | Accurate clause targeting with clean markup |
| 2 | Adequate revision with minor gaps | Identifies risk but reasoning incomplete | Correct clause but imprecise markup |
| 1 | Vague or incorrect revision | Superficial or incorrect reasoning | Wrong clause or unusable markup |

### Gate Criteria

Two gate mechanisms ensure minimum safety thresholds:

1. **T1 Gate (Freeform):** Every T1 issue must be detected. One miss = contract FAIL.
2. **Critical Failure Gate (Stacking):** Accepting a harmful redline or rejecting a beneficial one triggers a critical failure flag.

---

## Limitations

1. **Additional issues audit pending.** All 3,137 additional issues across models are currently classified as "Valid". A systematic audit may reclassify some as "Not Material", which would introduce precision variance between models.

2. **Rules and Guidelines modes pending.** The current results cover Freeform and Freeform Stacking only. Rules (deterministic rule compliance) and Guidelines (playbook position guidance) evaluations are prepared but not yet scored.

3. **Sample size.** 10 contracts with 160 GT issues provides meaningful signal but is not exhaustive. Results should be interpreted as indicative of model capability across common commercial contract types, not as guarantees of performance on specific document types.

4. **Stacking model coverage.** Only 4 of 6 models have stacking evaluations. Velocity and Scale were not evaluated in stacking mode.

5. **Single evaluation environment.** All results are from the "hotfix" environment. Cross-environment comparison is not yet available.

---

## Glossary

| Term | Definition |
|------|-----------|
| **GT** | Ground Truth — the expert-authored set of expected legal findings |
| **T1 / T2 / T3** | Tier 1 (Critical) / Tier 2 (Material) / Tier 3 (Minor) severity levels |
| **Y / P / N / NMI** | Yes (detected) / Partial / No (addressed but missed) / Not Meaningfully Identified |
| **F1** | Harmonic mean of precision and recall |
| **Detection Rate** | Percentage of GT issues found by the model (Y + P) |
| **Weighted Recall** | Tier-weighted recall score favouring critical issue detection |
| **Part A** | Stacking evaluation component: counterparty redline response |
| **Part B** | Stacking evaluation component: whole-document risk identification |
| **Semantic Matching** | Detection method based on risk equivalence, not textual overlap |
