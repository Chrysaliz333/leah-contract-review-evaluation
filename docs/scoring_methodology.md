# Scoring Methodology

This document explains how evaluations are scored across all evaluation modes in the Leah Contract Review Evaluation Framework.

---

## Overview

All evaluation modes use a **two-component scoring system:**

1. **Detection Points** -- Did Leah identify the risk?
2. **Quality Points** -- How well did Leah address it?

**Total Score = Detection Points + Quality Points**

---

## Design Rationale

The scoring methodology reflects several deliberate design choices:

- **Tiered detection points mirror legal materiality.** A missed critical structural defect (T1) carries far more weight than a missed best-practice suggestion (T3). The 8:5:1 point ratio ensures that evaluation scores are sensitive to the issues that matter most in a real-world contract review.
- **Quality dimensions prevent detection gaming.** Identifying a risk is necessary but not sufficient. A competent review must also propose a sound remediation (amendment score), explain the legal and business impact (rationale score), and produce usable redline language (redline quality score). Scoring quality alongside detection ensures that shallow or formulaic flagging is not rewarded.
- **Semantic matching prevents false negatives from clause numbering.** Contracts vary in structure. Penalising correct legal analysis because the clause reference is off by one section would undermine the evaluation's validity. Semantic matching evaluates whether the correct risk was identified, regardless of where it is anchored.
- **Gate criteria enforce minimum competence.** A model that misses a critical T1 issue fails the entire contract, regardless of aggregate score. This reflects the professional standard: missing a structural defect is not offset by catching twenty minor items.

---

## Component 1: Detection Points

### Purpose

Measure whether Leah identified the specific risk or compliance requirement defined in the ground truth.

### Detection Values

All modes use the same four detection values:

| Value | Meaning | Example |
|-------|---------|---------|
| **Y** | Fully detected and addressed | Leah's risk table flags the issue AND proposes a redline that addresses it |
| **P** | Partially detected or incomplete | Risk is flagged but redline is missing, OR redline partially addresses the issue |
| **N** | Missed (false negative) | Leah marked the clause as Favourable/Standard when the ground truth says it is an issue |
| **NMI** | Not mentioned anywhere | Issue not mentioned in any Leah output (risk table, proposed redlines, classifications) |

### Semantic Matching Principle

**Detection evaluates: "Did Leah identify THIS RISK?" -- NOT "Did Leah reference THIS CLAUSE NUMBER?"**

Example:
- **Ground truth specifies:** Unlimited liability cap at clause 5.2
- **Leah flags:** Liability cap issue at clause 5.3 (adjacent clause, same article)
- **Detection:** Y or P (based on quality), because Leah identified the semantic risk, even though the clause reference differs

**Semantic match criteria:**
1. Same risk type (e.g., both address liability exposure)
2. Same party affected (same representing party faces exposure)
3. Similar remediation (Leah's fix would address the ground truth concern)

---

## Component 2: Quality Points

### Purpose

Measure the quality of Leah's risk identification and proposed remediation.

### When Quality Points Apply

Quality points are **only awarded when detection is Y or P**.

- If detection = N or NMI, quality scores are **null**
- If detection = Y or P, evaluate all quality dimensions

### Universal Quality Dimensions

| Dimension | Applicable Modes | Scoring | Purpose |
|-----------|-----------------|---------|---------|
| **Amendment/Revision Score** | All | 1--3 or null | Does the proposed fix address the issue? Is it legally sound? |
| **Rationale Score** | All | 1--3 or null | Is the reasoning substantive? Does it cite specific legal standards or business impact? |
| **Redline/Language Quality Score** | Freeform, Stacking | 1--3 or null | Is the proposed redline well-drafted? Correct placement, clear language, usable? |
| **Action Score** | Rules, Guidelines | 1--3 or null | Is the recommended action (DELETE/AMEND/ADD/FLAG) appropriate? |

### Quality Rubric: Amendment/Revision Score (1--3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Comprehensive fix addressing ALL key elements, legally sound, market-standard language | Adds all required carve-outs with proper statutory references; strengthens position |
| **2** | Adequate fix, core issue addressed, minor gaps or imprecision | Addresses main liability concern but misses one carve-out; generally protective |
| **1** | Weak attempt, major issues, or partially wrong direction | Generic language that does not fully protect; misses core concern; or worsens position |
| **null** | No amendment proposed OR detection is N/NMI | -- |

### Quality Rubric: Rationale Score (1--3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Legal risk explained + business impact articulated + specific values/standards cited | "Exposes client to unlimited liability; market standard is 2x annual fees; IP indemnity caps at $X" |
| **2** | Risk identified with context, missing specific details | "This could expose client to significant liability; standard market practice prefers cap" |
| **1** | Problem stated without substance | "This clause is unfavourable"; "Better to change this" |
| **null** | Missing, wrong, or contradictory rationale OR detection is N/NMI | -- |

### Quality Rubric: Redline/Language Quality Score (1--3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Precise language, correct placement in document, immediately usable, integrates seamlessly | Clean tracked change, proper cross-references, no editing needed |
| **2** | Clear intent, minor drafting issues, needs light editing | Good concept but awkward phrasing; placed in right section but needs polish |
| **1** | Ambiguous language, placement issues, requires significant rework | Inserted in wrong location; unclear meaning; conflicts with surrounding text |
| **null** | Unusable, wrong clause structure, creates new problems OR detection is N/NMI | -- |

### Quality Rubric: Action Score (Rules/Guidelines, 1--3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Recommended action is clearly appropriate and well-justified | DELETE is correct for onerous indemnity; ADD is justified with regulatory reference |
| **2** | Action is reasonable but could be debated or lacks complete justification | AMEND suggested but DELETE also defensible; reasoning adequate but not comprehensive |
| **1** | Action is questionable or poorly justified | Suggests FLAG when DELETE clearly needed; action without clear reason |
| **null** | No action recommended OR detection is N/NMI | -- |

---

## Scoring Formulae

### Per-Issue Score

```
issue_total = detection_points + quality_points
```

Where:
```
detection_points = tier_weight * detection_multiplier
quality_points   = amendment_score + rationale_score + redline_quality_score
```

Detection multipliers:

| Detection | Multiplier |
|-----------|-----------|
| Y         | 1.0       |
| P         | 0.5       |
| N / NMI   | 0.0       |

### Weighted Recall

```
R = SUM(detection_points) / max_possible_points
```

Where max possible points = `(T1_count * 8) + (T2_count * 5) + (T3_count * 1)`

### Precision

```
P = valid_additional / (valid_additional + not_material)
```

### F1 Score (for ranking if required)

```
F1 = 2 * (R * P) / (R + P)
```

---

## Point Calculations by Mode

### Freeform and Freeform Stacking

**Detection Points by Tier:**

| Tier | Y (Full) | P (Partial) | N / NMI |
|------|----------|-------------|---------|
| **T1** | 8 | 4 | 0 |
| **T2** | 5 | 2.5 | 0 |
| **T3** | 1 | 0.5 | 0 |

**Quality Points (per dimension, if detection = Y or P):**

- Amendment Score: 1--3 points
- Rationale Score: 1--3 points
- Redline Quality Score: 1--3 points
- **Total quality = sum of all dimension scores (max 9 points per issue)**

**Issue Total = Detection Points + Quality Points**

**Example (T2 Issue):**
- Detection = Y --> 5 points
- Amendment Score = 3 --> 3 points
- Rationale Score = 2 --> 2 points
- Redline Quality Score = 3 --> 3 points
- **Total = 5 + 3 + 2 + 3 = 13 points**

### Rules Mode

**Max Points per Rule: 9 points**

- Detection: 2 points (Y=2, P=1, N/NMI=0)
- Compliance: 1 point (yes/no)
- Action: 2 points (correct action recommended)
- Language: 2 points (clarity and precision)
- Rationale: 2 points (substantive reasoning)

**Compliance Requirement:**
- All rules must achieve at least 60% compliance OR any critical rule violation = FAIL

### Rules Stacking Mode

**Max Points per Redline: 6 points**

- Action Score: 2 points (ACCEPT/MODIFY/REJECT/ACCEPT WITH RISK correct?)
- Revision Score: 2 points (if action = MODIFY, is the proposed revision sound?)
- Reasoning Score: 2 points (rationale substantive and specific?)

**Critical Failures (Automatic FAIL):**
- REJECT recommended as ACCEPT (accepting unacceptable element)
- ACCEPT recommended as REJECT (rejecting standard/favourable term)
- Scope violation (commenting on unchanged text)

### Guidelines Mode

**Detection Points by Tier:**

| Tier | Y (Full) | P (Partial) | N / NMI |
|------|----------|-------------|---------|
| **T1 (Gold Standard)** | 7 | 3.5 | 0 |
| **T2 (Fallback 1)** | 5 | 2.5 | 0 |
| **T3 (Fallback 2)** | 1 | 0.5 | 0 |
| **Red Flag (Auto-FAIL)** | N/A | N/A | Any miss = FAIL |

**Quality Points:** Same rubrics as Freeform (Amendment, Rationale, Action/Language)

**Red Flag Rule:**
- ANY Red Flag from the playbook not detected = automatic FAIL
- Red Flags are non-negotiable (no partial credit)

---

## Mode Comparison Table

| Aspect | Freeform | Freeform Stacking | Rules | Rules Stacking | Guidelines |
|--------|----------|-------------------|-------|----------------|------------|
| **Scoring unit** | Per issue | Per issue (Part A + Part B) | Per rule | Per redline | Per issue |
| **Max detection pts** | T1=8, T2=5, T3=1 | T1=8, T2=5, T3=1 | 2 | 2 (action) | T1=7, T2=5, T3=1 |
| **Quality dimensions** | Amendment, Rationale, Redline | Amendment, Rationale, Redline | Action, Language, Rationale | Revision, Reasoning | Amendment, Rationale, Action |
| **Max quality pts/issue** | 9 | 9 | 7 | 4 | 9 |
| **Gate criterion** | T1 miss = FAIL | T1 miss = FAIL | <60% compliance or critical rule miss = FAIL | Scope violation or action inversion = FAIL | Red Flag miss = FAIL |
| **Max pts per contract** | Varies (avg ~79) | Varies | 90 (9 x 10 rules) | 186 (6 x 31 redlines) | Varies (~70) |

---

## Gate Criteria

### Freeform and Freeform Stacking

- **Gate Rule:** ALL T1 issues must have detection = Y or P
- **Any T1 with N or NMI = model FAILS entire contract**
- Rationale: T1 issues are critical; missing them constitutes an automatic failure

### Rules Mode

- **Critical Rules Gate:** All critical rules must achieve at least 60% compliance
- **Any critical rule violation = model FAILS**

### Guidelines Mode

- **Red Flag Gate:** ANY Red Flag from the playbook must be detected (Y)
- **Any Red Flag with N or NMI = model FAILS entire contract**

---

## Additional Issues Scoring

### Purpose

Capture model value beyond ground truth scope and identify potential ground truth gaps.

### Assessment Values

Issues flagged by Leah but not in the ground truth are classified as follows:

| Assessment | Treatment | Points |
|------------|-----------|--------|
| **Valid -- Truly Additional** | Real issue beyond ground truth scope | +4.0 (T1), +2.5 (T2), +0.5 (T3) |
| **Valid -- GT Candidate** | Material issue to be added to future ground truth | Bonus (1.0--2.5 depending on tier) |
| **Valid -- Not Candidate** | Real issue, minor or niche | +1.0 |
| **Overlaps GT** | Relates to existing ground truth issue | 0 (avoid double-counting) |
| **Not Material** | Real but too minor to score | 0 |
| **Hallucination** | Leah misread or fabricated | -2.0 (penalty) |

### GT Candidate Criteria

An additional issue qualifies as a ground truth candidate if it:
- Receives a **Valid** assessment
- Is **T1 or T2 tier** (material impact)
- Is **not already covered** by any ground truth issue (even loosely)
- **Should be added** to future ground truth versions

---

## Semantic Matching in Scoring

### When to Award Detection Credit

**Award Y or P when:**
- Leah identifies the same legal risk (same risk type, same party affected, similar remediation)
- Even if clause reference differs
- Even if context is slightly different

**Example (Award Detection Credit):**
- Ground truth: "Liability cap should be limited to 2x annual fees" (clause 5.1)
- Leah flags: "Unlimited liability exposure" (clause 5.2, adjacent)
- **Detection: Y or P** -- Leah identified the semantic risk; clause offset is immaterial

**Example (Do Not Award Detection):**
- Ground truth: "Liability cap" (clause 5.1)
- Leah flags: "Indemnity scope is broad" (clause 7.2, different article, different issue)
- **Detection: NMI** -- Different issue type; no semantic match

### When in Doubt

**Rule of thumb:** When in doubt whether to award Y or P versus NMI, award P rather than NMI if Leah demonstrably understood the risk, even if execution was incomplete.

---

## Summary Statistics

### Total Possible Points

| Mode | Per Contract | Total (All Contracts) |
|------|--------------|----------------------|
| **Freeform** | 787 (160 issues) | 7,870 |
| **Freeform Stacking** | Part A + Part B (varies) | Varies |
| **Rules** | 9 x 10 rules = 90 | 900 |
| **Rules Stacking** | 6 x 31 redlines = 186 | 1,860 |
| **Guidelines** | ~700 (playbook-based) | ~7,000 |

### Passing Thresholds

| Mode | Threshold | Rationale |
|------|-----------|-----------|
| **Freeform** | No zero-score models; T1 gate pass | Detection gate is primary; additional issues bonus |
| **Rules** | At least 60% compliance on all rules | Deterministic baseline |
| **Guidelines** | No Red Flag misses; T1 gold standard | Non-negotiable red flags + tier-based scoring |

---

## Validation Before Aggregation

### Pre-Aggregation Checklist

1. **All contracts have results** -- No missing evaluation files
2. **All models present** -- All expected models accounted for
3. **No zero scores** -- If any model scores 0 on a contract, diagnose before proceeding
4. **Detection values valid** -- Only Y, P, N, NMI (no free text or symbols)
5. **Quality scores consistent** -- If detection = N/NMI, quality must be null
6. **T1/Red Flag gates checked** -- At least one T1/Red Flag detected per contract
7. **Summary counts accurate** -- Detection counts match individual evaluations

### Zero Score = Data Issue

**If any model scores 0 on any contract:**
1. **STOP** -- Do not aggregate
2. **Diagnose** -- Check input data, ground truth file, evaluation schema
3. **Fix** -- Correct the data issue
4. **Re-validate** -- Confirm fix before proceeding

---

## Common Scoring Mistakes

| Mistake | Impact | Prevention |
|---------|--------|-----------|
| Award quality points when detection = N/NMI | Inflates score | Quality scores MUST be null if detection is not Y or P |
| Miss semantic matches (over-literal clause matching) | Undercounts detection | Use semantic matching principle; risk type matters, not clause number |
| Double-count overlapping additional issues | Inflates score | Mark overlaps as "Overlaps GT" = 0 points |
| Award hallucinations as "Valid" | Corrupts data | Verify claim against source contract before marking Valid |
| Fail to explain reasoning | Unusable for review | Every detection/quality score needs supporting reasoning |
| Inconsistent detection values | Breaks aggregation | Use exact values: Y, P, N, NMI only (no variations) |
