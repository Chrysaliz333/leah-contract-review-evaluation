# Guidelines Evaluation Mode

Evaluates Leah's ability to apply playbook rules while exercising independent legal judgment. The playbook provides qualifying context on top of full Freeform-level analysis.

Unlike Rules mode (which is purely deterministic), Guidelines mode expects Leah to combine playbook instructions with its own risk identification. The playbook defines a position hierarchy (Gold Standard through Red Flag) for specific clause types, but Leah must still identify all risks a competent lawyer would find -- the playbook supplements rather than replaces independent judgment.

## Quick Reference

| Component | Count | Details |
|-----------|-------|---------|
| Contracts | 20 | 10 NDA, 10 Subcontract |
| Playbooks | 2 | NDA Receiving Party, Subcontract Subcontractor |
| Representing Party | | NDA: Receiving Party, Subcontract: Subcontractor |

## How Guidelines Differs from Freeform

| Aspect | Freeform | Guidelines |
|--------|----------|------------|
| Context doc | None | Playbook |
| Risk identification | Leah's judgment | Judgment + playbook triggers |
| Amendment language | Leah generates | Playbook provides guidance |
| Position hierarchy | Leah determines | Playbook defines (GS -> FB1 -> FB2 -> RF) |

**Key principle:** Guidelines = Full Freeform analysis + Playbook as qualifying context.

The playbook doesn't limit what Leah should find -- it provides specific instructions for handling certain issues. Leah must identify all Freeform-level risks; playbook issues get additional scoring dimensions.

## Directory Structure

```
guidelines/
+-- contracts/
|   +-- nda/               # 10 NDA contracts
|   +-- subcontract/        # 10 Subcontract contracts
+-- playbooks/
|   +-- NDA_Receiving_Party_Playbook.docx
|   +-- Subcontract_Subcontractor_Playbook.docx
+-- ground_truth/
|   +-- nda.json
|   +-- subcontract.json
```

## Playbook Position Hierarchy

| Position | Code | Meaning |
|----------|------|---------|
| Gold Standard | GS | Ideal position |
| Fallback 1 | FB1 | Acceptable compromise |
| Fallback 2 | FB2 | Minimum acceptable |
| Red Flag | RF | **Unacceptable -- must action** |

## Scoring

| Dimension | T1 | T2 | T3 |
|-----------|----|----|-----|
| Detection | 1 | 1 | 0.5 |
| Location | 1 | 1 | -- |
| Action | 1 | 1 | -- |
| Amendment | 2 | 1 | -- |
| Rationale | 2 | 1 | -- |
| **Max** | **7** | **5** | **0.5** |

### Dimension Details

| Dimension | Full Credit | Partial | Zero |
|-----------|-------------|---------|------|
| Detection | Issue flagged | -- | Missed |
| Location | Exact section ref | Correct article, wrong subsection (0.5) | Wrong or not specified |
| Action | Correct per playbook | -- | Wrong action |
| Amendment | Aligns with playbook (T1: 2) | Partial/missing elements (T1: 1) | Wrong or contradicts |
| Rationale | Cites rule + risk + trigger (T1: 2) | Weak linkage (T1: 1) | Wrong clause or missing |

## Detection Values

| Value | Meaning |
|-------|---------|
| **Y** | Detected AND correct action per playbook |
| **P** | Partial -- detected but incomplete |
| **N** | Marked compliant when Red Flag present |
| **NMI** | Not mentioned anywhere |

### Partial Detection (P) -- Detailed Criteria

Award **P** (not NMI) when:
- Issue flagged but action incorrect or missing
- Playbook rule triggered but not fully applied
- Amendment direction correct but incomplete

Award **NMI** when:
- Issue not mentioned anywhere in Leah's output
- Playbook trigger phrase present but not identified

### Semantic Matching Principle

**Detection asks: "Did Leah identify THIS risk?" -- not "Did Leah reference THIS clause number?"**

When Leah identifies the correct issue at a nearby clause (e.g., flags the Red Flag trigger at Section 2.3 when GT expects Section 2.1), evaluate based on semantic match, not syntactic clause matching.

| Scenario | Leah's Clause | GT Clause | Same Issue? | Detection |
|----------|---------------|-----------|-------------|-----------|
| Exact match | 2.1 | 2.1 | Yes | Y/P based on quality |
| Adjacent clause, same article | 2.3 | 2.1 | Yes | Y/P based on quality |
| Different article, same issue type | 5.1 | 2.1 | Maybe | P if clearly same concern |
| Same clause, different issue | 2.1 | 2.1 | No | NMI for GT issue |

**Semantic match criteria:**
1. **Same playbook rule** -- both address the same Red Flag trigger
2. **Same party affected** -- the representing party faces the same exposure
3. **Similar remediation** -- Leah's proposed fix aligns with playbook guidance

**When in doubt:** Award P rather than NMI if Leah demonstrably understood the risk, even if clause reference differs.

## Actions

| Action | When |
|--------|------|
| **AMEND** | Modify per playbook guidance (most common) |
| **DELETE** | Playbook prohibits clause type entirely (rare) |
| **ADD** | Missing required protection |
| **FLAG** | Escalate for commercial review |

**Note:** AMEND is the typical action. DELETE is only for absolute prohibitions (e.g., Personal Guarantee, Non-Compete for Subcontractor).

## Pass Criteria

| Result | Criteria |
|--------|----------|
| PASS | >=70% AND all Red Flags detected |
| MARGINAL | 50-69% OR 1-2 Red Flag misses |
| FAIL | <50% OR 3+ Red Flag misses |

## Contracts

### NDA (10)
- NDA_TechPartners_Bilateral
- NDA_Meridian_Unilateral
- NDA_GlobalPharm_Research
- NDA_Vertex_Strategic
- NDA_Quantum_JointVenture
- NDA_Sterling_Mutual
- NDA_Cascade_Supplier
- NDA_Nexus_Investment
- NDA_Atlas_Employment
- NDA_Vanguard_Technical

### Subcontract (10)
TBD

## Playbook Rules Summary

### NDA Playbook (12 rules)

| Rule | Clause | Red Flag Trigger |
|------|--------|------------------|
| 1 | CI Definition | "whether or not marked" |
| 2 | CI Carve-Outs | Missing standard carve-outs |
| 3 | Exclusions | Restricts standard exclusions |
| 4 | Term & Survival | Perpetual / >5 years |
| 5 | Non-Solicitation | >12 months |
| 6 | Representations | Broad rep on CI accuracy |
| 7 | Return/Destruction | No retention right |
| 8 | Non-Compete | Any non-compete |
| 9 | Indemnification | Broad-form indemnity |
| 10 | Equitable Relief | Conclusive admission |
| 11 | Governing Law | Offshore jurisdiction (FLAG) |
| 12 | Limitation of Liability | Waiver of consequentials |

### Subcontract Playbook (14+ rules)

| Rule | Clause | Red Flag Trigger |
|------|--------|------------------|
| 1 | Indemnification | Broad-form triggers |
| 2 | Insurance | Non-standard coverage |
| 3-4 | Insurance Forms | Missing CG 2010/2037 |
| 5 | Liquidated Damages | Direct (not pass-through) |
| 6 | Payment Terms | >60 days |
| 7 | Retainage | >5% |
| 8 | Warranty | >2 years |
| 9 | Personal Guarantee | Any (DELETE) |
| 10 | Non-Compete | Any (DELETE) |
| 11+ | Additional rules | See playbook |

---

## Additional Issues (Beyond Playbook)

Issues beyond playbook scope are captured during evaluation:

| Assessment | Meaning |
|------------|---------|
| **Valid** | Real issue correctly identified |
| **Overlaps GT** | Relates to existing playbook rule |
| **Hallucination** | Leah misread or fabricated |
| **Not Material** | Real but too minor |

Mark `gt_candidate: true` if the issue is material (T1/T2) and should be added to future playbook versions.

---

## Evaluation Schema

```json
{
  "metadata": {
    "mode": "guidelines",
    "contract_type": "NDA|Subcontract",
    "model_id": "string",
    "playbook": "NDA Receiving Party Playbook",
    "gt_version": "string"
  },
  "gt_evaluations": [
    {
      "test_id": "TechPartnersBilateral_01",
      "contract": "NDA_TechPartners_Bilateral",
      "clause_ref": "Section 1.1",
      "clause_name": "CI Definition",
      "playbook_ref": 1,
      "playbook_standard": "Red Flag",
      "tier": 1,
      "trigger_phrase": "whether or not marked as confidential",
      "expected_classification": "Unfavourable",
      "expected_action": "AMEND",
      "expected_amendment": "Remove trigger and require written marking",
      "detected": "Y|P|N|NMI",
      "detection_score": 1,
      "location_score": 1,
      "action_score": 1,
      "amendment_score": 2,
      "rationale_score": 2,
      "total_score": 7,
      "leah_action": "AMEND",
      "leah_amendment": "...",
      "leah_rationale": "..."
    }
  ],
  "summary": {
    "total_score": "number",
    "max_points": "number",
    "percentage": "number",
    "pass_fail": "PASS|MARGINAL|FAIL",
    "red_flags_total": "number",
    "red_flags_detected": "number",
    "red_flag_gate": "PASS|FAIL"
  }
}
```

## Zero Score Validation

**If any model scores 0, this is a DATA ISSUE, not model performance.**

### Zero Score Triggers

| Condition | Likely Cause |
|-----------|--------------|
| Total score = 0 | Canonical data missing/malformed |
| All NMI | Leah output not parsed correctly |
| All Red Flags missed | Playbook not loaded or wrong contract |
| Single model = 0 | File missing or format different |

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
