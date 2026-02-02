# Rules Stacking Evaluation Mode

Evaluates Leah's response to counterparty redlines using deterministic rules. **Redlined clauses ONLY** -- no analysis of unchanged text.

This mode combines the adversarial redline scenario from Freeform Stacking with the deterministic rule compliance from Rules mode. Leah must identify which rules apply to each counterparty redline and take the correct prescribed action, while strictly avoiding commentary on unchanged contract text.

## Quick Reference

| Component | Count | Details |
|-----------|-------|---------|
| Contracts | 10 | 5 NDA, 5 Subcontract |
| Rule Files | 2 | NDA_Rules_Deterministic.csv, Subcontractor_Rules_Deterministic.csv |
| Representing Party | | NDA: Receiving Party, Subcontract: Subcontractor |

## Critical Scope Principle

**In Rules Stacking, Leah ONLY applies rules to redlined clauses.**

| Aspect | Detail |
|--------|--------|
| Scope | **Redlined clauses ONLY** |
| Critical failure | **Commenting on unchanged text** |

This differs from Freeform Stacking (which evaluates the entire document).

## How Rules Stacking Works

1. CP makes a redline to a clause
2. Leah checks if a rule applies to that redline
3. Leah applies rule action (ACCEPT/MODIFY/REJECT)
4. Leah cites the rule

**Leah does NOT analyse unchanged text.**

## Directory Structure

```
rules_stacking/
+-- redlined_contracts/
|   +-- nda/               # 5 NDA redlined contracts
|   +-- subcontract/        # 5 Subcontract redlined contracts
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
| Action | 2 | Correct ACCEPT/MODIFY/REJECT per rules |
| Revision | 2 | Follows prescribed language |
| Reasoning | 2 | Rule citation present |
| **Total** | **6** | Per redline |

## Action Values

| Action | When |
|--------|------|
| **ACCEPT** | CP redline complies with rules |
| **MODIFY** | CP redline needs adjustment per rules |
| **REJECT** | CP redline violates rules -- revert |
| **ACCEPT WITH RISK** | No rule applies -- accept with risk note |

## Detection Values

| Value | Meaning |
|-------|---------|
| **Y** | Correctly identified and actioned per rules |
| **P** | Identified but action or revision incomplete |
| **N** | Missed rule violation or wrong action |
| **NMI** | Redline not addressed at all |

## Expected Actions by Scenario

| Scenario | Expected Action |
|----------|-----------------|
| CP INSERTED problematic text (rule says DELETE) | REJECT |
| CP INSERTED text (rule says AMEND) | MODIFY |
| CP DELETED protective text | REJECT (restore) |
| No rule applies | ACCEPT WITH RISK ANALYSIS |

## Scope Violations

A **scope violation** occurs when Leah:
- Flags an issue in unchanged text
- Proposes amendments to non-redlined clauses
- Performs general contract review outside redlines

**Scope violations = critical failure**

## Pass Criteria

| Result | Criteria |
|--------|----------|
| PASS | >=70% AND 0 scope violations |
| MARGINAL | 50-69% OR 1 scope violation |
| FAIL | <50% OR 2+ scope violations |

---

## Evaluation Schema

```json
{
  "metadata": {
    "mode": "rules_stacking",
    "contract_type": "NDA|Subcontract",
    "model_id": "string",
    "rule_file": "string",
    "gt_version": "string"
  },
  "redline_evaluations": [
    {
      "test_id": "V1",
      "contract": "NDA_Vertex_Strategic_Stacking.docx",
      "section": "Section 1.1 CI Definition",
      "original_text": "[end of standard CI definition]",
      "redline_text": ", including residual knowledge...",
      "difficulty": "SUBTLE|OBVIOUS",
      "applicable_rule": "CI Definition - Residual Knowledge Deletion",
      "expected_action": "REJECT",
      "expected_language": "[original text without the insertion]",
      "detected": "Y|P|N|NMI",
      "leah_action": "REJECT",
      "action_score": 2,
      "leah_amended_language": "...",
      "revision_score": 2,
      "leah_rationale": "...",
      "reasoning_score": 2,
      "total_score": 6
    }
  ],
  "scope_violations": [
    {
      "clause_ref": "3.1",
      "issue": "Flagged unchanged confidentiality clause",
      "severity": "CRITICAL"
    }
  ],
  "summary": {
    "total_score": "number",
    "max_points": "number",
    "percentage": "number",
    "pass_fail": "PASS|MARGINAL|FAIL",
    "redlines_evaluated": "number",
    "scope_violations": "number"
  }
}
```

## Zero Score Validation

**If any model scores 0, this is a DATA ISSUE, not model performance.**

### Zero Score Triggers

| Condition | Likely Cause |
|-----------|--------------|
| Total score = 0 | Canonical data missing/malformed |
| All NMI | Leah output not parsed, redlines not found |
| Single model = 0 | File missing or format different |
| Redlines = 0 | Redline document not loaded |

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
