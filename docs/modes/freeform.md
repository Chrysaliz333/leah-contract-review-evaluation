# Freeform Evaluation Mode

Base Leah evaluation with no additional configuration. Evaluates risk identification and remediation from the buyer's/client's perspective across 10 commercial contract types.

This is the foundational evaluation mode: Leah receives a clean contract with no playbook, rules, or counterparty redlines, and must identify risks and propose amendments using only its own legal judgment.

## Quick Reference

| Component | Count | Details |
|-----------|-------|---------|
| Contracts | 10 | SLA, DPA, Consulting, Distribution, JV, License, Partnership, Reseller, Services, Supply |
| GT Issues | 160 | 45 T1, 78 T2, 37 T3 |
| Max Points | 787 | T1=8pts, T2=5pts, T3=1pt + quality |

## Directory Structure

```
freeform/
+-- contracts/           # Source contract files
+-- ground_truth/        # GT JSONs (T1/T2/T3 tiers)
+-- results/             # Evaluation results
+-- workbooks/           # Excel outputs
```

## Contracts and Representing Parties

| Contract | Representing Party |
|----------|-------------------|
| Consulting | Meridian Enterprises Inc. (Client) |
| DPA | Controller |
| Distribution | Distributor |
| JV | Quantum Dynamics LLC (Party B) |
| License | TechPro Industries Corp. (Licensee) |
| Partnership | Growth Dynamics Partners LP (Partner B) |
| Reseller | Pacific Tech Distributors LLC (Reseller) |
| Services | Client |
| SLA | Licensee |
| Supply | Apex Automotive Systems Inc. (Buyer) |

## Scoring

| Tier | Detection Points | Quality Points | Gate |
|------|------------------|----------------|------|
| T1 | 8 (Y), 4 (P), 0 (N/NMI) | 0-3 | **Miss = FAIL** |
| T2 | 5 (Y), 2.5 (P), 0 (N/NMI) | 0-3 | Weighted |
| T3 | 1 (Y), 0.5 (P), 0 (N/NMI) | 0-3 | Weighted |

## Detection Values

| Value | Meaning | Criteria |
|-------|---------|----------|
| **Y** | Detected | proposed_redline addresses the GT issue |
| **P** | Partial | risk_table flags issue OR redline partially addresses |
| **N** | Missed | Marked Favorable/Standard when issue exists |
| **NMI** | Not mentioned | Issue not flagged anywhere |

### Partial Detection (P) -- Detailed Criteria

Award **P** (not NMI) when:
- Risk table flags the issue but no proposed redline exists
- Redline partially addresses the issue (missing key elements from GT)
- Redline addresses a related clause with the same issue type
- Issue identified but fix is incomplete or wrong direction

Award **NMI** when:
- Issue not mentioned anywhere in Leah's output
- Only mentioned in passing without classification or recommended action
- Completely different issue flagged at the same clause

### Semantic Matching Principle

**Detection asks: "Did Leah identify THIS risk?" -- not "Did Leah reference THIS clause number?"**

When Leah identifies the correct issue at a nearby clause (e.g., flags unlimited liability at 5.3 when GT expects it at 5.2), evaluate based on semantic match, not syntactic clause matching.

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

## Quality Score Rubrics

Quality scores (1-3) are awarded only when detection is Y or P.

### Amendment Score -- Does the fix address the issue?

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Comprehensive fix addressing all GT key_elements, legally sound | Adds all required carve-outs with proper drafting |
| **2** | Adequate fix, core issue addressed, minor gaps | Addresses main risk but misses one carve-out |
| **1** | Weak attempt, major issues or partially wrong direction | Generic language that doesn't fully protect |
| **0/null** | No amendment or makes position worse | N/A for undetected issues |

### Rationale Score -- Is the reasoning sound?

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Legal risk + business impact + specific values/standards cited | "Exposes client to unlimited liability; market standard is 2x fees" |
| **2** | Risk identified with context, missing specifics | "This could expose client to significant liability" |
| **1** | States problem without substance | "This clause is unfavourable" |
| **0/null** | Missing, wrong, or contradictory rationale | N/A for undetected issues |

### Redline Quality Score -- Is it well-drafted?

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Precise language, correct placement, immediately usable | Clean tracked change, integrates with clause |
| **2** | Clear intent, minor drafting issues, needs light editing | Good concept but awkward phrasing |
| **1** | Ambiguous language, placement issues, requires significant rework | Inserted in wrong location or unclear meaning |
| **0/null** | Unusable, wrong clause structure, creates new problems | N/A for undetected issues |

---

## Additional Issues (Beyond GT)

After evaluating all GT issues, Leah's output is scanned for flags NOT covered by GT. This captures model value beyond predefined issues and identifies potential GT gaps.

### What to Capture

Look for risk_table entries or proposed_redlines at clauses not in the GT where Leah classified as:
- Unfavourable
- Requires Clarification
- Any non-Favourable/Standard classification

### Assessment Values

| Assessment | Meaning | Example |
|------------|---------|---------|
| **Valid** | Real issue Leah correctly identified beyond GT scope | Missing force majeure clause (not in GT) |
| **Overlaps GT** | Relates to existing GT issue at different clause | Same liability concern, different section |
| **Hallucination** | Leah misread contract or flagged non-existent issue | Clause doesn't say what Leah claims |
| **Not Material** | Real but too minor to matter | Stylistic preference, no legal risk |

### GT Candidate

Mark `gt_candidate: true` if the issue is:
- Valid assessment
- T1 or T2 tier (material impact)
- Should be added to future GT versions

### Additional Issues Scoring

Models earn or lose points based on additional issues found beyond GT:

| Assessment | GT Candidate | Proposed Tier | Points |
|------------|--------------|---------------|--------|
| Valid | Yes | T1 | +4.0 |
| Valid | Yes | T2 | +2.5 |
| Valid | Yes | T3 | +0.5 |
| Valid | Yes | (none) | +2.5 |
| Valid | No | - | +1.0 |
| Overlaps GT | - | - | 0 |
| Not Material | - | - | 0 |
| Hallucination | - | - | -2.0 |

**Rationale:**
- GT candidates demonstrate valuable risk identification beyond predefined issues
- Valid non-candidate issues show thoroughness (+1 each)
- Hallucinations indicate model quality issues and incur a penalty
- Overlaps GT issues are reconciled separately (not double-counted)

---

## Evaluation Schema

```json
{
  "meta": {
    "contract": "string",
    "model_id": "string",
    "gt_version": "string",
    "evaluation_timestamp": "ISO8601"
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
  "additional_issues": [
    {
      "clause": "string",
      "issue_summary": "string",
      "leah_classification": "Unfavorable|Requires Clarification|etc",
      "leah_action": "AMEND|DELETE|ADD|FLAG",
      "assessment": "Valid|Overlaps GT|Hallucination|Not Material",
      "proposed_tier": "T1|T2|T3|null",
      "gt_candidate": "boolean",
      "notes": "string"
    }
  ],
  "summary": {
    "detection_counts": {"Y": "n", "P": "n", "N": "n", "NMI": "n"},
    "detection_by_tier": {},
    "t1_all_detected": "boolean",
    "total_detection_points": "number",
    "total_quality_points": "number",
    "total_points": "number",
    "additional_issues_count": "number"
  }
}
```

## Zero Score Validation

**If any model scores 0, this is a DATA ISSUE, not model performance.**

| Condition | Likely Cause |
|-----------|--------------|
| All models = 0 same item | GT issue (wrong clause ref) or missing data |
| Single model = 0 | File missing or format different |
| Total_points = 0 | Leah output not parsed correctly |

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
