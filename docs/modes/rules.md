# Rules Evaluation Mode

Evaluates Leah's compliance with deterministic rules provided via CSV configuration files. This is a binary pass/fail assessment: either the rule is followed or it isn't.

Unlike Freeform (which relies on Leah's independent judgment), Rules mode provides explicit trigger-action pairs. When a trigger phrase is detected in the contract, Leah must apply the prescribed action with the exact language specified by the rule.

## Quick Reference

| Component | Count | Details |
|-----------|-------|---------|
| Contracts | 20 | 10 NDA, 10 Subcontract |
| Rules | 22 NDA, 14 Subcontract | See CSV files |
| Representing Party | | NDA: Receiving Party, Subcontract: Subcontractor |

## How Rules Mode Works

```
IF trigger phrase detected in contract
THEN apply prescribed action with exact language
```

No interpretive flexibility. Either the rule is followed or it isn't.

## Directory Structure

```
rules/
+-- contracts/
|   +-- nda/               # 10 NDA contracts
|   +-- subcontract/        # 10 Subcontract contracts
+-- rule_files/
|   +-- NDA_Rules_Deterministic.csv
|   +-- Subcontractor_Rules_Deterministic.csv
+-- ground_truth/
|   +-- nda.json
|   +-- subcontract.json
```

## Scoring

| Dimension | Max | Description |
|-----------|-----|-------------|
| Detection | 2 | Rule triggered correctly |
| Compliance | 1 | Compliance status confirmed |
| Action | 2 | Correct action selected |
| Language | 2 | Prescribed language used |
| Rationale | 2 | Rule citation present |
| **Total** | **9** | Per rule |

## Detection Values

| Value | Meaning |
|-------|---------|
| **Y** | Full compliance -- trigger detected, correct action, prescribed language |
| **P** | Partial -- trigger detected but wrong action OR wrong language |
| **N** | Non-compliance -- marked compliant when trigger present |
| **NMI** | Not mentioned -- trigger not identified |
| **N/A** | Not applicable -- trigger not present in contract |

### Partial (P) vs NMI -- Detailed Criteria

Award **P** when:
- Trigger phrase detected but action is wrong
- Correct action but prescribed language not used
- Rule citation missing but fix is correct

Award **NMI** when:
- Trigger phrase present but not identified at all
- Issue not mentioned in Leah's output

## Actions

| Action | When |
|--------|------|
| **DELETE** | Remove phrase/clause entirely |
| **AMEND** | Replace with prescribed language |
| **ADD** | Insert missing protective language |
| **FLAG** | Escalate for commercial review |

## Key NDA Rules

| Category | Action | Trigger |
|----------|--------|---------|
| CI Definition | DELETE | "whether or not marked" |
| CI Carve-Outs | ADD | Missing standard carve-outs |
| Term & Survival | AMEND | Perpetual / >5 years |
| Non-Compete | DELETE | Any non-compete provision |
| Governing Law | FLAG | Offshore jurisdiction |

## Key Subcontract Rules

| Category | Action | Trigger |
|----------|--------|---------|
| Indemnity | AMEND | Broad-form triggers |
| Insurance | DELETE | Non-standard coverage |
| Liquidated Damages | AMEND | Direct (not pass-through) |
| Personal Guarantee | DELETE | Any personal guarantee |
| Non-Compete | DELETE | Any non-compete |

## Pass Criteria

| Result | Criteria |
|--------|----------|
| PASS | >=80% rule compliance rate |
| MARGINAL | 60-79% compliance |
| FAIL | <60% OR critical rule violation |

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

---

## Evaluation Schema

```json
{
  "metadata": {
    "mode": "rules",
    "contract_type": "NDA|Subcontract",
    "model_id": "string",
    "rule_file": "NDA_Rules_Deterministic.csv",
    "gt_version": "string"
  },
  "rule_evaluations": [
    {
      "test_id": "TechPartners_Bi_01",
      "contract": "NDA_TechPartners_Bilateral",
      "clause_ref": "1.1",
      "rule_name": "CI Definition - Unmarked Information Deletion",
      "expected_action": "DELETE",
      "detected": "Y|P|N|NMI|N/A",
      "detection_score": 2,
      "compliance_score": 1,
      "action_score": 2,
      "language_score": 2,
      "rationale_score": 2,
      "total_score": 9,
      "leah_action": "DELETE",
      "leah_language": "...",
      "leah_rationale": "..."
    }
  ],
  "summary": {
    "total_score": "number",
    "max_points": "number",
    "percentage": "number",
    "pass_fail": "PASS|MARGINAL|FAIL",
    "rules_triggered": "number",
    "rules_complied": "number",
    "compliance_rate": "number",
    "critical_rules_missed": []
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
| All N/A | Rule triggers not found in contract |
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
