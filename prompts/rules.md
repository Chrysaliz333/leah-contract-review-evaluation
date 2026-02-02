# Rules Mode Evaluation Prompt

---

## PROMPT START

You are evaluating Leah's contract review output for **Rules mode** — deterministic rule-based evaluation.

**Contract:** {CONTRACT}
**Model:** {MODEL}
**Contract Type:** {NDA|SUBCONTRACT}

---

## MANDATORY FIRST STEPS (DO NOT SKIP)

1. **Read** mode documentation: `docs/modes/rules.md`
2. **Read** rule file: `rules/rule_files/NDA_Rules_Deterministic.csv` or `Subcontractor_Rules_Deterministic.csv` (based on contract type)
3. **Read** ground truth: `rules/ground_truth/{nda|subcontract}.json`
4. **Read** canonical JSON: `rules/canonical_json/{CONTRACT}/{MODEL}.json`

---

## CRITICAL RULES

| Rule | Explanation |
|------|-------------|
| Detection values | ONLY use: `Y`, `P`, `N`, `NMI`, `N/A` — no symbols, no variations |
| Rule trigger | `N/A` is ONLY used when rule trigger is absent (e.g., contract has no IP clause when rule evaluates IP) |
| Quality scores | Use `0`, `1`, `2`, or `null` — never empty string |
| Evidence | Quote **verbatim** from canonical JSON or contract clauses — no paraphrasing |
| Independence | DO NOT read other evaluation files for "examples" |
| Completeness | Every rule must have ALL schema fields present |

---

## EVALUATION SCHEMA

Write output to: `rules/results/{CONTRACT}/{MODEL}.json`

```json
{
  "meta": {
    "contract": "{CONTRACT}",
    "contract_type": "NDA|SUBCONTRACT",
    "model_id": "{MODEL}",
    "evaluation_timestamp": "2026-01-27T00:00:00Z",
    "evaluator_model": "sonnet",
    "rule_version": "COPY FROM RULE FILE"
  },
  "rule_evaluations": [
    {
      "rule_id": "R-XX",
      "rule_name": "from rule file",
      "representing_party": "from rule file",
      "rule_requirement": "from rule file",
      "trigger_clause": "from rule file (may be 'N/A' if rule doesn't apply)",
      "trigger_present": true|false,
      "detection": "Y|P|N|NMI|N/A",
      "detection_score": 0|1|2,
      "compliance_score": 0|1,
      "action_score": 0|1|2,
      "language_score": 0|1|2,
      "rationale_score": 0|1|2,
      "total_points": number,
      "evidence": {
        "rule_trigger_excerpt": "string (verbatim quote from contract clause)",
        "leah_response_excerpt": "string (verbatim from canonical JSON)",
        "judge_reasoning": "Explain scoring decision and rule assessment"
      }
    }
  ],
  "additional_issues": [],
  "summary": {
    "total_rules_evaluated": number,
    "applicable_rules": number,
    "n_a_rules": number,
    "detection_counts": {"Y": 0, "P": 0, "N": 0, "NMI": 0, "N/A": 0},
    "compliance_rate": number,
    "critical_rules_passed": boolean,
    "total_points": number,
    "max_possible_points": number,
    "percentage": number,
    "pass_fail": "PASS|FAIL"
  }
}
```

---

## RULE STRUCTURE

Each rule has:

- **rule_id** — Unique identifier (R-001, R-002, etc.)
- **rule_name** — Human-readable name
- **representing_party** — Whose position is being evaluated (Receiving Party for NDA, Subcontractor for Subcontract)
- **rule_requirement** — What Leah should identify (e.g., "identify confidentiality scope limitations")
- **trigger_clause** — Where to look in contract; `N/A` if rule doesn't apply
- **trigger_present** — boolean: is the trigger clause present in this contract?

---

## DETECTION VALUES (Rules Mode)

| Value | Meaning | Rule Trigger | When to Use |
|-------|---------|--------------|-------------|
| **Y** | Rule requirement fully detected and properly addressed | Must be present | Leah identifies the rule requirement and proposes/recommends appropriate action |
| **P** | Rule partially detected or incomplete | Must be present | Leah flags issue but misses key requirements OR action is questionable |
| **N** | False negative (marked compliant when not) | Must be present | Clause exists but Leah missed or misclassified it |
| **NMI** | Not mentioned anywhere | Must be present | Rule requirement not mentioned in Leah output |
| **N/A** | Rule doesn't apply (trigger absent) | MUST be absent | Rule evaluates specific clause/concept not present in contract |

### When to Use N/A

Use `N/A` ONLY when:
- Rule has a specific trigger (e.g., "if contract contains IP indemnity")
- That trigger is absent from the contract
- Rule cannot be evaluated for this contract

**Important:** N/A is NOT a detection failure. It means the rule is inapplicable.

### Trigger Present / Trigger Absent

```
Rule: "NDA-007: Evaluate confidentiality scope"
Trigger: "Confidentiality clause (typically clause 2-3)"

IF contract has confidentiality clause:
  trigger_present = true
  detection = Y|P|N|NMI (evaluate normally)

IF contract has NO confidentiality clause:
  trigger_present = false
  detection = N/A (rule doesn't apply)
  detection_score = 0 (N/A = 0 points)
  total_points = 0
```

---

## POINT CALCULATIONS

### Detection Score (2 points max)
- Y = 2 points
- P = 1 point
- N or NMI = 0 points
- N/A = 0 points (inapplicable rule)

### Compliance Score (1 point max)
- Compliant with rule = 1 point
- Non-compliant (Leah misses requirement) = 0 points
- N/A rules = 0 points

### Action Score (2 points max)

| Score | Criteria |
|-------|----------|
| **2** | Recommended action (DELETE/AMEND/ADD/FLAG) is clearly appropriate |
| **1** | Action is reasonable but could be debated |
| **0** | Action is questionable or missing |

### Language Score (2 points max)

| Score | Criteria |
|-------|----------|
| **2** | Clear, precise language; specific drafting guidance |
| **1** | Adequate language, minor clarity issues |
| **0** | Ambiguous, unclear, or missing guidance |

### Rationale Score (2 points max)

| Score | Criteria |
|-------|----------|
| **2** | Specific legal standard or business rationale cited |
| **1** | Rationale present but lacks specifics |
| **0** | Missing or weak rationale |

### Total Points per Rule

**Total = Detection Score + Compliance Score + Action Score + Language Score + Rationale Score**

**Max per rule: 2 + 1 + 2 + 2 + 2 = 9 points**

---

## EVALUATION PROCESS

### For Each Rule:

1. **Check trigger presence** — Is the clause/concept present in contract?
   - If NO -> detection = N/A, trigger_present = false, skip to next rule
   - If YES -> trigger_present = true, proceed

2. **Search canonical JSON** — Find Leah's response to this rule
   - Look for risk_table entries related to the rule requirement
   - Look for proposed_redlines or actions
   - Look for classifications (Unfavourable, Requires Clarification, etc.)

3. **Determine detection** — Y/P/N/NMI based on Leah's response

4. **Score each dimension:**
   - Compliance (1 pt): Does Leah's answer comply with rule?
   - Action (2 pts): Is recommended action appropriate?
   - Language (2 pts): Is language clear and specific?
   - Rationale (2 pts): Is reasoning substantive?

5. **Calculate total** — Detection + Compliance + Action + Language + Rationale

6. **Write evidence** — Verbatim excerpts + reasoning

### After All Rules:

1. Calculate summary:
   - Total points
   - Compliance rate (compliant rules / applicable rules)
   - Pass/Fail determination

2. Check critical rules gate:
   - If any critical rule is non-compliant -> FAIL
   - If overall compliance < 60% -> FAIL
   - Otherwise -> PASS

---

## RULE COMPLIANCE GATES

### Pass Criteria

**PASS requires ALL of:**
1. Overall compliance >= 60%
2. All critical rules (marked in rule file) are compliant (compliance_score = 1)

### Fail Criteria

**FAIL if ANY:**
1. Overall compliance < 60%
2. Any critical rule is non-compliant
3. Rule requirement fundamentally misunderstood

---

## SEMANTIC MATCHING FOR RULES

**Key Principle:** "Did Leah identify that this rule requirement applies?"

| Scenario | Detection |
|----------|-----------|
| Leah correctly identifies rule requirement at specified clause | Y or P (based on quality) |
| Leah flags requirement at adjacent/related clause with same issue | Y or P (semantic match) |
| Leah misses rule requirement entirely | N or NMI |
| Rule trigger not in contract | N/A |

---

## QUALITY RUBRICS

### When to Award Quality Scores

Quality scores are awarded when:
- Trigger is present (detection is not N/A)
- Leah responds to the rule (detection = Y, P, N, or NMI)

Quality scores are null when:
- Trigger is absent (detection = N/A)

### Action Score Rubric (2 points)

| Score | Criteria | Example |
|-------|----------|---------|
| **2** | Action is clearly appropriate and well-justified | DELETE for onerous indemnity; ADD for missing limitation; AMEND with specific language |
| **1** | Action is reasonable but could be debated | Action suggested but alternative approach also defensible |
| **0** | Action is questionable or poorly justified | FLAG suggested for item requiring DELETE; no clear reason for action |

### Language Quality Rubric (2 points)

| Score | Criteria |
|-------|----------|
| **2** | Clear, specific language; can be directly used; references specific legal standards |
| **1** | Adequate language but needs refinement; somewhat generic |
| **0** | Ambiguous, unclear, or missing specific guidance |

### Rationale Rubric (2 points)

| Score | Criteria |
|-------|----------|
| **2** | Specific legal standard, case law, or business justification cited |
| **1** | Rationale present but generic (e.g., "market standard") |
| **0** | Missing rationale or contradictory reasoning |

---

## ADDITIONAL ISSUES (Beyond Rules)

After evaluating all rules, capture issues flagged by Leah but not covered by rules:

| Assessment | Meaning |
|------------|---------|
| **Valid** | Real issue Leah correctly identified |
| **Overlaps Rule** | Relates to existing rule |
| **Hallucination** | Leah misread or fabricated |
| **Not Material** | Real but too minor |

Mark `gt_candidate: true` if issue is material (T1/T2) and should be added to future rules.

---

## CRITICAL: N/A vs NMI

| Situation | Value | Reasoning |
|-----------|-------|-----------|
| Rule evaluates IP indemnity; contract has NO IP indemnity clause | N/A | Rule trigger absent; rule doesn't apply |
| Rule evaluates IP indemnity; contract HAS IP indemnity; Leah doesn't mention it | NMI | Trigger present; Leah didn't detect |
| Rule evaluates IP indemnity; Leah addresses IP but not indemnity aspect | P | Partial detection; semantic match exists |

---

## EVALUATION CHECKLIST

Before finalising:

- [ ] All rules evaluated (Y/P/N/NMI/N/A for each)
- [ ] Trigger presence correctly marked for each rule
- [ ] Detection values valid only (Y, P, N, NMI, N/A)
- [ ] Quality scores only when detection is not N/A
- [ ] Total points calculated correctly per rule
- [ ] Summary totals accurate (sum of all rule points)
- [ ] Compliance rate calculated (compliant rules / applicable rules)
- [ ] Critical rules gate checked
- [ ] Pass/Fail determination correct
- [ ] Evidence includes verbatim quotes
- [ ] Judge reasoning explains each score

---

## OUTPUT VALIDATION

After writing JSON:

1. Verify JSON is valid (proper formatting)
2. Check all required fields present
3. Confirm detection_counts match individual scores
4. Verify summary totals match detailed evaluations
5. Ensure judge_reasoning exists for each rule
6. Confirm pass_fail aligns with gate criteria

---

## Common Mistakes

DO NOT: Use N/A for detection failure (should be NMI)
DO: Use N/A only when trigger is absent

DO NOT: Award quality scores when detection = N/A
DO: Quality scores = null only when detection = N/A

DO NOT: Miss that adjacent clauses can trigger semantic matches
DO: Use semantic principle: "Does Leah understand the rule requirement?"

DO NOT: Miscalculate total points
DO: Total = Detection (2) + Compliance (1) + Action (2) + Language (2) + Rationale (2) = max 9

---

## PROMPT END
