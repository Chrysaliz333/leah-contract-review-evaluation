# Freeform Mode Evaluation Prompt

---

## PROMPT START

You are evaluating Leah's contract review output for **Freeform mode** — comprehensive risk identification and remediation.

**Contract:** {CONTRACT}
**Model:** {MODEL}

---

## MANDATORY FIRST STEPS (DO NOT SKIP)

1. **Read** mode documentation: `docs/modes/freeform.md`
2. **Read** ground truth: `freeform/ground_truth/{CONTRACT}.json`
3. **Read** canonical JSON: `freeform/canonical_json/{CONTRACT}/{MODEL}.json`

---

## CRITICAL RULES

| Rule | Explanation |
|------|-------------|
| Detection values | ONLY use: `Y`, `P`, `N`, `NMI` — no symbols, no variations |
| Quality scores | Use `1`, `2`, `3`, or `null` — never `0`, never empty string |
| Evidence | Quote **verbatim** from canonical JSON — no paraphrasing |
| Independence | DO NOT read other evaluation files for "examples" |
| Completeness | Every GT item must have ALL schema fields |

---

## EVALUATION SCHEMA

Write output to: `freeform/results/{CONTRACT}/{MODEL}.json`

```json
{
  "meta": {
    "contract": "{CONTRACT}",
    "model_id": "{MODEL}",
    "evaluation_timestamp": "2026-01-27T00:00:00Z",
    "evaluator_model": "sonnet",
    "gt_version": "COPY FROM GT FILE"
  },
  "gt_evaluations": [
    {
      "gt_id": "GT-XX",
      "clause": "from GT",
      "tier": "T1|T2|T3",
      "issue": "from GT",
      "detection": "Y|P|N|NMI",
      "detection_points": number,
      "amendment_score": 1|2|3|null,
      "rationale_score": 1|2|3|null,
      "redline_quality_score": 1|2|3|null,
      "quality_points": number,
      "total_points": number,
      "matched_redline_id": "string|null",
      "evidence": {
        "proposed_revision_excerpt": "string|null (verbatim quote)",
        "effective_rationale_excerpt": "string|null (verbatim quote)",
        "judge_reasoning": "Explain scoring decision"
      }
    }
  ],
  "additional_issues": [],
  "summary": {
    "detection_counts": {"Y": 0, "P": 0, "N": 0, "NMI": 0},
    "detection_by_tier": {
      "T1": {"Y": 0, "P": 0, "N": 0, "NMI": 0},
      "T2": {"Y": 0, "P": 0, "N": 0, "NMI": 0},
      "T3": {"Y": 0, "P": 0, "N": 0, "NMI": 0}
    },
    "t1_gate_pass": false,
    "t1_count": 0,
    "t1_detected": 0,
    "total_detection_points": 0,
    "total_quality_points": 0,
    "total_points": 0
  }
}
```

---

## DETECTION VALUES (Freeform)

| Value | Meaning | Award Points? |
|-------|---------|---------------|
| **Y** | Fully detected and properly addressed | Yes (tier-based: 8/5/1) |
| **P** | Partially detected or incomplete | Yes (50% of Y: 4/2.5/0.5) |
| **N** | Missed (false negative) | No (0 points) |
| **NMI** | Not mentioned anywhere | No (0 points) |

### When to Award Each Value

**Y (Full Detection):**
- Leah's risk_table identifies the same risk
- Proposed_redlines address the GT issue
- Redline is complete and legally sound

**P (Partial Detection):**
- Risk flagged but no proposed redline exists
- Redline partially addresses issue (missing key elements)
- Semantic match at adjacent clause
- Redline partially wrong direction or incomplete

**N (Missed — False Negative):**
- Leah marks clause as Favourable/Standard when GT says it's an issue
- Leah should have flagged but didn't

**NMI (Not Mentioned):**
- Issue not mentioned anywhere in Leah output
- Only mentioned in passing without classification

---

## POINT CALCULATIONS

### Detection Points (Tier-Based)

| Tier | Y (Full) | P (Partial) | N/NMI |
|------|----------|-------------|-------|
| **T1** | 8 | 4 | 0 |
| **T2** | 5 | 2.5 | 0 |
| **T3** | 1 | 0.5 | 0 |

### Quality Points (When Detection = Y or P)

Three dimensions, max 1-3 points each:

- **Amendment Score** (1-3): Does the redline fix address the issue?
- **Rationale Score** (1-3): Is the reasoning substantive?
- **Redline Quality Score** (1-3): Is the language clear and well-placed?

**Total quality = Amendment + Rationale + Redline = max 9 points per issue**

### Issue Total

**Total = Detection Points + Quality Points**

**Example (T2 Issue):**
- Detection = Y -> 5 points
- Amendment Score = 3 -> 3 points
- Rationale Score = 2 -> 2 points
- Redline Quality Score = 3 -> 3 points
- **Total = 5 + 3 + 2 + 3 = 13 points**

---

## QUALITY RUBRICS

### When Quality Scores Apply

Quality scores are **only awarded when detection = Y or P**.

If detection = N or NMI -> all quality scores = **null**

### Amendment Score Rubric (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Comprehensive fix addressing ALL GT key_elements, legally sound, market-standard language | Adds all required carve-outs; strengthens position with proper references |
| **2** | Adequate fix, core issue addressed, minor gaps | Addresses main concern but misses one carve-out; generally protective |
| **1** | Weak attempt, major issues, or partially wrong direction | Generic language; doesn't fully protect; misses core concern |
| **null** | No amendment OR detection is N/NMI | — |

### Rationale Score Rubric (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Legal risk + business impact + specific values/standards cited | "Exposes client to unlimited liability; market standard is 2x annual fees; IP indemnity caps" |
| **2** | Risk identified with context, missing specific details | "This could expose client to significant liability; standard market practice prefers cap" |
| **1** | Problem stated without substance | "This clause is unfavourable" |
| **null** | Missing, wrong, or contradictory rationale OR detection is N/NMI | — |

### Redline Quality Score Rubric (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Precise language, correct placement, immediately usable | Clean tracked change; integrates seamlessly; no editing needed |
| **2** | Clear intent, minor drafting issues, needs light editing | Good concept but awkward phrasing; placed correctly but needs polish |
| **1** | Ambiguous language, placement issues, requires significant rework | Inserted in wrong location; unclear meaning; conflicts with surrounding text |
| **null** | Unusable, wrong clause structure, creates new problems OR detection is N/NMI | — |

---

## DETECTION CRITERIA — DETAILED EXAMPLES

### Y (Full Detection) — Examples

"Liability cap should be limited to 2x annual fees" (GT issue)
  Leah: Flags unlimited liability + proposes specific cap language
  **Detection = Y**

"Indemnity should exclude contractor's own negligence" (GT issue)
  Leah: Flags indemnity scope + adds carve-out for contractor negligence
  **Detection = Y**

### P (Partial Detection) — Examples

"Liability cap should be limited" (GT issue)
  Leah: Flags in risk_table but no proposed redline
  **Detection = P**

"Indemnity should exclude contractor negligence" (GT issue)
  Leah: Proposes to limit indemnity but to "gross negligence" (overly narrow)
  **Detection = P** (partial — not as protective as GT expects)

"Confidentiality scope should exclude public information" (GT at clause 2.1)
  Leah: Flags at clause 2.2 (adjacent clause, same article, same issue)
  **Detection = P or Y** (semantic match; clause offset immaterial)

### N (Missed) — Examples

"Liability cap should exist" (GT issue)
  Leah: Marks clause 5.2 as "Favourable — cap is acceptable"
  But cap is actually unlimited or too high
  **Detection = N** (false negative; Leah should have flagged)

### NMI (Not Mentioned) — Examples

"IP indemnity should exclude confidential info" (GT issue)
  Leah: No mention of IP clause or indemnity anywhere
  **Detection = NMI**

---

## SEMANTIC MATCHING PRINCIPLE

**Detection evaluates: "Did Leah identify THIS RISK?" — NOT "Did Leah reference THIS CLAUSE NUMBER?"**

### Clause Reference vs Semantic Matching

| Scenario | GT Clause | Leah Flags | Same Issue? | Detection |
|----------|-----------|-----------|-------------|-----------|
| Exact match | 5.2 | 5.2 | Yes | Y or P (based on quality) |
| Adjacent clause, same article | 5.2 | 5.3 | Yes (same section) | Y or P (semantic match) |
| Different article, same risk | 5.2 (liability) | 7.1 (indemnity scope) | Maybe (related but different) | P if clearly same concern |
| Same clause, different issue | 5.2 | 5.2 (different risk) | No | NMI for GT issue |

### Semantic Match Criteria

Award Y or P when:
1. **Same risk type** — Both address the same legal concern (e.g., liability, indemnity, IP)
2. **Same party affected** — The representing party faces the same exposure
3. **Similar remediation** — Leah's proposed fix would address the GT concern

**Rule of thumb:** When in doubt, award P rather than NMI if Leah demonstrably understood the risk.

---

## T1 GATE RULE

**`t1_gate_pass` = true ONLY if ALL T1 issues have detection Y or P**

Any T1 with N or NMI -> `t1_gate_pass: false` (model FAILS contract)

T1 issues are critical. Missing even one is an automatic failure.

---

## EVALUATION PROCESS

### For Each GT Issue:

1. **Search canonical JSON** — Find evidence of Leah's response
   - Look for risk_table entries related to the clause/issue
   - Look for proposed_redlines
   - Look for classifications (Unfavourable, etc.)

2. **Determine detection** — Y/P/N/NMI
   - Did Leah identify the same risk?
   - Is there a proposed fix?
   - Is the fix complete or partial?

3. **Award detection points** — Based on tier and detection value

4. **Score quality (if Y or P only):**
   - Amendment: Does fix address issue? (1-3)
   - Rationale: Is reasoning substantive? (1-3)
   - Redline Quality: Is language clear? (1-3)

5. **Calculate total** — Detection + Quality

6. **Write evidence** — Verbatim excerpts + reasoning

### After All GT Issues:

1. Calculate summary:
   - detection_counts (Y, P, N, NMI)
   - detection_by_tier
   - t1_gate_pass (all T1 detected?)
   - Total points

2. Verify:
   - T1 gate is correct
   - Summary counts match individual scores
   - All required fields present

---

## ADDITIONAL ISSUES (Beyond GT)

After evaluating all GT issues, capture issues flagged by Leah but not in GT:

| Assessment | Meaning |
|------------|---------|
| **Valid** | Real issue Leah correctly identified |
| **Overlaps GT** | Relates to existing GT issue |
| **Hallucination** | Leah misread or fabricated |
| **Not Material** | Real but too minor |

Mark `gt_candidate: true` if the issue is material (T1/T2) and should be added to future GT versions.

---

## CRITICAL DECISION TREE

```
Did Leah identify the GT risk?
  |-- YES, fully (redline addresses) -> Detection = Y
  |-- YES, partially (flag but no redline / incomplete) -> Detection = P
  |-- NO, false negative (marked compliant) -> Detection = N
  +-- NO, not mentioned -> Detection = NMI

Is detection Y or P?
  |-- YES -> Evaluate quality (Amendment, Rationale, Redline)
  +-- NO  -> Quality scores = null

Award points:
  - Detection: tier-based (T1=8/4, T2=5/2.5, T3=1/0.5)
  - Quality: 1-3 per dimension (max 9)
  - Total: Detection + Quality
```

---

## EVALUATION CHECKLIST

Before finalising:

- [ ] All GT issues evaluated
- [ ] Detection values valid only (Y/P/N/NMI)
- [ ] Quality scores only when detection = Y/P
- [ ] Quality scores null when detection = N/NMI
- [ ] Total points calculated correctly per issue
- [ ] Summary totals accurate (sum of all issue points)
- [ ] T1 gate pass/fail correct
- [ ] Evidence includes verbatim quotes
- [ ] Judge reasoning explains each score

---

## Common Mistakes

DO NOT: Award quality scores when detection = N/NMI
DO: Quality scores = null if detection is not Y/P

DO NOT: Over-literal clause matching (miss semantic matches)
DO: Use semantic principle: "Did Leah identify THIS RISK?" (not clause number)

DO NOT: Award Y for issue at clause 5.3 when GT expects 5.2 and issue is different
DO: Evaluate semantic match; same issue type = same article = Y/P eligible

DO NOT: Miscalculate total points
DO: Total = Detection Points + Quality Points

DO NOT: Miss quality scores in summary totals
DO: Verify summary sums all issue totals correctly

---

## PROMPT END
