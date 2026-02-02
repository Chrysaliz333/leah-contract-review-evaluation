# Freeform Stacking Evaluation Mode

Evaluates Leah's response to counterparty (CP) redlines and whole-document risk identification. Uses the same 10 commercial contracts as Freeform, but with the addition of tracked changes from the opposing party.

This is a dual evaluation: Part A tests whether Leah correctly handles CP redlines (ACCEPT/MODIFY/REJECT), while Part B measures whether Leah still identifies whole-document risks despite the distraction of adversarial markup. The baseline delta metric tracks performance degradation compared to clean Freeform results.

## Quick Reference

| Component | Count | Description |
|-----------|-------|-------------|
| Part A: CP Redlines | 40 | Response to tracked changes |
| Part B: Whole Document | 141 | Reuses Freeform GT |
| Contracts | 10 | Same as Freeform |

## Critical Scope Principle

**Freeform Stacking reviews the ENTIRE document -- not just redlines.**

| Component | What It Tests |
|-----------|---------------|
| Part A | Negotiation competence |
| Part B | Baseline performance under distraction |
| Delta | Impact of CP redlines on overall performance |

## Directory Structure

```
freeform_stacking/
+-- redlined_contracts/   # Input contracts with CP redlines
+-- ground_truth/         # Part A GT + Part B references to freeform GT
+-- results/              # Evaluation results
+-- workbooks/            # Excel outputs
```

## Contracts and Representing Parties

**Same party as Freeform baseline:**

| Contract | Freeform | Freeform Stacking |
|----------|----------|-------------------|
| Consulting | Client | Client |
| Distribution | Distributor | Distributor |
| JV | Party B | Party B |
| License | Licensee | Licensee |
| Partnership | Partner B | Partner B |
| Reseller | Reseller | Reseller |
| Services | Client | Client |
| SLA | Licensee | Licensee |
| Supply | Buyer | Buyer |
| DPA | Controller | Controller |

**Rationale:** Same party perspective enables clean degradation measurement between Freeform baseline and Freeform Stacking. CP redlines test whether Leah properly defends client interests when reviewing adversarial counterparty proposals.

## Part A: CP Redline Scoring

| Dimension | Max | Criteria |
|-----------|-----|----------|
| Action | 2 | Matches acceptable actions |
| Revision | 2 | Key elements, no unacceptable |
| Reasoning | 2 | Required points addressed |
| **Total per redline** | **6** | |

### Actions

| Action | When |
|--------|------|
| **ACCEPT** | CP redline acceptable |
| **MODIFY** | Redline needs adjustment |
| **REJECT** | Redline unacceptable -- revert |

### Critical Failures (Part A)

| Type | Meaning |
|------|---------|
| REJECT_AS_ACCEPT | Accepted something that must be rejected |
| ACCEPT_AS_REJECT | Rejected something that should be accepted |
| UNACCEPTABLE_ELEMENT | Revision contains forbidden content |

### Pass Criteria (Part A)

| Result | Criteria |
|--------|----------|
| PASS | >=70% AND 0 critical failures |
| MARGINAL | 50-69% OR 1 critical failure |
| FAIL | <50% OR 2+ critical failures |

## Part B: Whole Document Scoring

Reuses Freeform GT (141 items) with T1/T2/T3 tiers.

| Tier | Points | Gate |
|------|--------|------|
| T1 | 8 | Hard FAIL if missed |
| T2 | 5 | Weighted |
| T3 | 1 | Weighted |

### Detection Values

| Value | Points | Meaning |
|-------|--------|---------|
| **Y** | Full | Detected AND proposed fix |
| **P** | Half | Partial (mentioned but incomplete) |
| **N** | 0 | Marked Favourable or ignored |
| **NMI** | 0 | Not mentioned anywhere |

### Detection Point Calculation

| Tier | Detection | Points |
|------|-----------|--------|
| T1 | Y | 8 |
| T1 | P | 4 |
| T1 | N/NMI | 0 |
| T2 | Y | 5 |
| T2 | P | 2.5 |
| T2 | N/NMI | 0 |
| T3 | Y | 1 |
| T3 | P | 0.5 |
| T3 | N/NMI | 0 |

### Semantic Matching Principle (Parts A and B)

**Detection asks: "Did Leah identify THIS risk?" -- not "Did Leah reference THIS clause number?"**

When Leah identifies the correct issue at a nearby clause (e.g., flags unlimited liability at 5.3 when GT expects 5.2), evaluate based on semantic match, not syntactic clause matching.

| Scenario | Leah's Clause | GT Clause | Same Issue? | Detection |
|----------|---------------|-----------|-------------|-----------|
| Exact match | 5.2 | 5.2 | Yes | Y/P based on quality |
| Adjacent clause, same article | 5.3 | 5.2 | Yes | Y/P based on quality |
| Different article, same issue type | 7.1 | 5.2 | Maybe | P if clearly same concern |
| Same clause, different issue | 5.2 | 5.2 | No | NMI for GT issue |

**Semantic match criteria:**
1. **Same risk type** -- both address the same legal concern (e.g., liability cap, indemnity scope)
2. **Same party affected** -- the representing party faces the same exposure
3. **Similar remediation** -- Leah's proposed fix would address the GT issue

**When in doubt:** Award P rather than NMI if Leah demonstrably understood the risk, even if clause reference differs.

### Partial Detection (P) -- Detailed Criteria

Award **P** (not NMI) when:
- Risk table flags the issue but no proposed redline exists
- Redline partially addresses the issue (missing key elements)
- Issue identified but fix is incomplete

Award **NMI** when:
- Issue not mentioned anywhere in Leah's output
- Only mentioned in passing without classification

### Pass Criteria (Part B)

| Result | Criteria |
|--------|----------|
| PASS | T1 Gate PASS AND >=70% |
| MARGINAL | T1 Gate PASS AND 50-69% |
| FAIL | T1 Gate FAIL OR <50% |

### Baseline Delta

```
baseline_delta = stacking_whole_doc_% - freeform_baseline_%
```

- Negative = degradation from CP redlines
- Zero/positive = no degradation

## Quality Score Rubrics (Part B Only)

Quality scores (1-3) are awarded only when detection is Y or P. **NULL for N/NMI detections.**

### Amendment Score -- Does the fix address the issue?

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Comprehensive fix addressing all GT key_elements, legally sound | Adds all required carve-outs with proper drafting |
| **2** | Adequate fix, core issue addressed, minor gaps | Addresses main risk but misses one carve-out |
| **1** | Weak attempt, major issues or partially wrong direction | Generic language that doesn't fully protect |
| **null** | No amendment or N/NMI detection | N/A for undetected issues |

### Rationale Score -- Is the reasoning sound?

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Legal risk + business impact + specific values/standards cited | "Exposes client to unlimited liability; market standard is 2x fees" |
| **2** | Risk identified with context, missing specifics | "This could expose client to significant liability" |
| **1** | States problem without substance | "This clause is unfavourable" |
| **null** | Missing, wrong, or N/NMI detection | N/A for undetected issues |

### Redline Quality Score -- Is it well-drafted?

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Precise language, correct placement, immediately usable | Clean tracked change, integrates with clause |
| **2** | Clear intent, minor drafting issues, needs light editing | Good concept but awkward phrasing |
| **1** | Ambiguous language, placement issues, requires significant rework | Inserted in wrong location or unclear meaning |
| **null** | Unusable or N/NMI detection | N/A for undetected issues |

## Quality Flags

| Flag | Threshold | Meaning |
|------|-----------|---------|
| BASELINE_DEGRADATION | delta < -10% | Significant performance drop from CP redlines |

---

## GT Files

Per-contract GT files in `ground_truth/`:

| File | Description |
|------|-------------|
| `freeform_stacking_converted.json` | Master Part A (40 items) |
| `sla_stacking.json` | SLA per-contract GT |
| `consulting_stacking.json` | Consulting per-contract GT |
| `distribution_stacking.json` | Distribution per-contract GT |
| `jv_stacking.json` | JV per-contract GT |
| `supply_stacking.json` | Supply per-contract GT |
| `services_stacking.json` | Services per-contract GT |
| `license_stacking.json` | License per-contract GT |
| `reseller_stacking.json` | Reseller per-contract GT |
| `partnership_stacking.json` | Partnership per-contract GT |
| `dpa_stacking.json` | DPA per-contract GT |

Each per-contract file contains:
- `part_a_cp_redlines`: 4 CP redline items
- `part_b_whole_document.reference`: Link to baseline Freeform GT
- `scoring_summary`: Pass criteria

---

## Evaluation Schemas

### Part A Evaluation Schema (CP Redlines)

```json
{
  "meta": {
    "contract": "string",
    "model_id": "string",
    "evaluation_timestamp": "ISO8601",
    "gt_version": "string"
  },
  "part_a_evaluations": [
    {
      "gt_id": "CP-XX",
      "clause": "string",
      "cp_redline_description": "string",
      "expected_action": "ACCEPT|MODIFY|REJECT",
      "leah_action": "ACCEPT|MODIFY|REJECT|null",
      "action_score": "0|1|2",
      "revision_score": "0|1|2",
      "reasoning_score": "0|1|2",
      "total_points": "number",
      "critical_failure": "null|REJECT_AS_ACCEPT|ACCEPT_AS_REJECT|UNACCEPTABLE_ELEMENT",
      "evidence": {
        "leah_response_excerpt": "string (verbatim quote)",
        "judge_reasoning": "string"
      }
    }
  ],
  "part_a_summary": {
    "total_score": "number",
    "max_score": "number",
    "percentage": "number",
    "critical_failures": "number",
    "pass_fail": "PASS|MARGINAL|FAIL"
  }
}
```

### Part B Evaluation Schema (Whole Document)

```json
{
  "meta": {
    "contract": "string",
    "model_id": "string",
    "evaluation_timestamp": "ISO8601",
    "gt_version": "string"
  },
  "gt_evaluations": [
    {
      "gt_id": "GT-XX",
      "clause": "string",
      "tier": "T1|T2|T3",
      "issue": "string",
      "detection": "Y|P|N|NMI",
      "detection_points": "number",
      "amendment_score": "1|2|3|null",
      "rationale_score": "1|2|3|null",
      "redline_quality_score": "1|2|3|null",
      "quality_points": "number",
      "total_points": "number",
      "matched_redline_id": "string|null",
      "evidence": {
        "proposed_revision_excerpt": "string|null",
        "effective_rationale_excerpt": "string|null",
        "judge_reasoning": "string"
      }
    }
  ],
  "additional_issues": [],
  "summary": {
    "detection_counts": {"Y": "n", "P": "n", "N": "n", "NMI": "n"},
    "detection_by_tier": {
      "T1": {"Y": "n", "P": "n", "N": "n", "NMI": "n"},
      "T2": {"Y": "n", "P": "n", "N": "n", "NMI": "n"},
      "T3": {"Y": "n", "P": "n", "N": "n", "NMI": "n"}
    },
    "t1_gate_pass": "boolean",
    "t1_count": "number",
    "t1_detected": "number",
    "total_detection_points": "number",
    "total_quality_points": "number",
    "total_points": "number"
  }
}
```

### Combined Summary Schema

```json
{
  "summary": {
    "part_a": {
      "percentage": 83.3,
      "critical_failures": 0,
      "pass_fail": "PASS"
    },
    "part_b": {
      "percentage": 70.8,
      "t1_gate": "PASS",
      "baseline_delta": -2.1,
      "pass_fail": "PASS"
    },
    "combined": { "pass": true }
  }
}
```

## Additional Issues

Issues beyond GT scope are captured during evaluation:

| Assessment | Meaning |
|------------|---------|
| **Valid** | Real issue correctly identified |
| **Overlaps GT** | Relates to existing GT issue |
| **Hallucination** | Leah misread or fabricated |
| **Not Material** | Real but too minor |

Mark `gt_candidate: true` if the issue is material (T1/T2) and should be added to future GT versions.

For stacking, additional issues may arise from either CP redline clauses (Part A) or whole document clauses (Part B).

## Zero Score Validation

**If any model scores 0, this is a DATA ISSUE, not model performance.**

### Zero Score Triggers

| Condition | Likely Cause |
|-----------|--------------|
| Part A = 0 | Leah output not parsed, CP redlines not found |
| Part B = 0 | Canonical data missing/malformed |
| All NMI | Leah output format changed or file missing |

Zero scores must be diagnosed and resolved before aggregation proceeds.

---

## Models

| Display Name | model_id |
|--------------|----------|
| Sonnet 4.5 | sonnet45 |
| Pathfinder | pathfinder |
| Starliner | starliner |
| Velocity | velocity |
| Scale | scale |
| Pioneer Deep | pioneer_deep |
