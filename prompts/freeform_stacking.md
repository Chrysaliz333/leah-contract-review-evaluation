# Freeform Stacking Mode Evaluation Prompt

---

## PROMPT START

You are evaluating Leah's contract review output for **Freeform Stacking mode** — dual evaluation of CP redline responses (Part A) and whole-document risk identification (Part B).

**Contract:** {CONTRACT}
**Model:** {MODEL}

---

## MANDATORY FIRST STEPS (DO NOT SKIP)

1. **Read** mode documentation: `docs/modes/freeform_stacking.md`
2. **Read** GT file: `freeform_stacking/ground_truth/{CONTRACT}_stacking.json`
3. **Read** canonical JSON: `freeform_stacking/canonical_json/{CONTRACT}/{MODEL}.json`

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

## CRITICAL SCOPE PRINCIPLE

**Freeform Stacking reviews the ENTIRE document — not just redlines.**

| Component | What It Tests |
|-----------|---------------|
| Part A | Negotiation competence — response to CP redlines |
| Part B | Baseline performance — whole document risk detection under distraction |
| Delta | Impact of CP redlines on overall performance |

---

## COMPLETE EVALUATION SCHEMA

Write output to: `freeform_stacking/results/{CONTRACT}/{MODEL}.json`

### Part A Schema (CP Redlines)

```json
{
  "meta": {
    "contract": "{CONTRACT}",
    "model_id": "{MODEL}",
    "evaluation_timestamp": "2026-01-27T00:00:00Z",
    "evaluator_model": "sonnet",
    "gt_version": "COPY FROM GT FILE"
  },
  "part_a_evaluations": [
    {
      "gt_id": "XX_01",
      "clause_ref": "from GT",
      "expected_action": "ACCEPT|MODIFY|REJECT",
      "leah_action": "ACCEPT|MODIFY|REJECT|null",
      "action_score": 0|1|2,
      "revision_score": 0|1|2,
      "reasoning_score": 0|1|2,
      "total_points": number,
      "critical_failure": null|"REJECT_AS_ACCEPT"|"ACCEPT_AS_REJECT"|"UNACCEPTABLE_ELEMENT",
      "evidence": {
        "leah_response_excerpt": "string (verbatim quote)",
        "judge_reasoning": "string"
      }
    }
  ],
  "part_a_summary": {
    "total_score": number,
    "max_score": number,
    "percentage": number,
    "critical_failures": number,
    "pass_fail": "PASS|MARGINAL|FAIL"
  }
}
```

### Part B Schema (Whole Document)

```json
{
  "part_b_evaluations": [
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
        "judge_reasoning": "string"
      }
    }
  ],
  "additional_issues": [],
  "part_b_summary": {
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

## PART A: CP REDLINE SCORING

### Actions

| Action | When |
|--------|------|
| **ACCEPT** | CP redline acceptable |
| **MODIFY** | Redline needs adjustment |
| **REJECT** | Redline unacceptable — revert |

### Point Calculations (Part A)

| Dimension | Max | Criteria |
|-----------|-----|----------|
| Action | 2 | Matches acceptable actions from GT |
| Revision | 2 | Key elements addressed, no unacceptable elements |
| Reasoning | 2 | Required reasoning points addressed |
| **Total per redline** | **6** | |

### Action Score Rubric (Part A)

| Score | Criteria |
|-------|----------|
| **2** | Action matches GT expectation perfectly |
| **1** | Action is reasonable but different from GT expectation |
| **0** | Action contradicts GT or is inappropriate |

### Revision Score Rubric (Part A)

| Score | Criteria |
|-------|----------|
| **2** | Proposed revision addresses all key elements, no unacceptable content |
| **1** | Revision is reasonable but imperfect or partially addresses concern |
| **0** | Revision is unclear, legally questionable, or doesn't address concern |

### Reasoning Score Rubric (Part A)

| Score | Criteria |
|-------|----------|
| **2** | Specific legal basis or business justification provided; addresses all required reasoning points |
| **1** | Rationale present but generic or incomplete |
| **0** | Missing, weak, or contradictory reasoning |

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

---

## PART B: WHOLE DOCUMENT SCORING

Reuses Freeform GT with T1/T2/T3 tiers. Part B reference is in the stacking GT file.

### Detection Points (Part B)

| Tier | Y (Full) | P (Partial) | N/NMI |
|------|----------|-------------|-------|
| **T1** | 8 | 4 | 0 |
| **T2** | 5 | 2.5 | 0 |
| **T3** | 1 | 0.5 | 0 |

### Detection Values (Part B)

| Value | Meaning |
|-------|---------|
| **Y** | Detected AND proposed fix |
| **P** | Partial (mentioned but incomplete) |
| **N** | Marked Favourable or ignored when issue exists |
| **NMI** | Not mentioned anywhere |

### Partial Detection (P) — Detailed Criteria

Award **P** (not NMI) when:
- Risk table flags the issue but no proposed redline exists
- Redline partially addresses the issue (missing key elements)
- Issue identified but fix is incomplete

Award **NMI** when:
- Issue not mentioned anywhere in Leah's output
- Only mentioned in passing without classification

### Quality Rubrics (Part B Only)

Quality scores (1-3) are awarded only when detection is Y or P. **NULL for N/NMI detections.**

#### Amendment Score (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Comprehensive fix addressing all GT key_elements, legally sound | Adds all required carve-outs with proper drafting |
| **2** | Adequate fix, core issue addressed, minor gaps | Addresses main risk but misses one carve-out |
| **1** | Weak attempt, major issues or partially wrong direction | Generic language that doesn't fully protect |
| **null** | No amendment or N/NMI detection | — |

#### Rationale Score (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Legal risk + business impact + specific values/standards cited | "Exposes client to unlimited liability; market standard is 2x fees" |
| **2** | Risk identified with context, missing specifics | "This could expose client to significant liability" |
| **1** | States problem without substance | "This clause is unfavourable" |
| **null** | Missing, wrong, or N/NMI detection | — |

#### Redline Quality Score (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Precise language, correct placement, immediately usable | Clean tracked change, integrates with clause |
| **2** | Clear intent, minor drafting issues, needs light editing | Good concept but awkward phrasing |
| **1** | Ambiguous language, placement issues, requires significant rework | Inserted in wrong location or unclear meaning |
| **null** | Unusable or N/NMI detection | — |

### T1 Gate Rule (Part B)

`t1_gate_pass` = true **only if** ALL T1 issues have detection Y or P.

Any T1 with N or NMI = `t1_gate_pass: false`

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

---

## SEMANTIC MATCHING (Parts A and B)

**Detection is about identifying the risk, not matching clause numbers.**

| Scenario | Detection |
|----------|-----------|
| Same clause, same issue | Y or P based on quality |
| Adjacent clause (same article), same issue | Y or P based on quality |
| Different clause, same risk type affecting same party | P |
| Same clause, different issue | NMI for the GT issue |

### Semantic Match Criteria

Award Y or P when:
1. **Same risk type** — Both address the same legal concern
2. **Same party affected** — The representing party faces the same exposure
3. **Similar remediation** — Leah's proposed fix would address the GT concern

**Rule of thumb:** When in doubt, award P rather than NMI if Leah demonstrably understood the risk.

---

## EVALUATION PROCESS

### Part A (For Each CP Redline):

1. **Identify the CP redline** from the GT file
2. **Find Leah's response** in canonical JSON
   - Look for action (ACCEPT/MODIFY/REJECT)
   - Look for rationale and any proposed revision
3. **Check for critical failures**
   - REJECT as ACCEPT? -> critical_failure = "REJECT_AS_ACCEPT"
   - ACCEPT as REJECT? -> critical_failure = "ACCEPT_AS_REJECT"
4. **Score each dimension:**
   - Action (2 pts): Does action match GT?
   - Revision (2 pts): Are key elements addressed?
   - Reasoning (2 pts): Are required points covered?
5. **Write evidence** with verbatim excerpts

### Part B (For Each GT Issue):

1. **Search canonical JSON** for evidence of Leah's response
   - risk_table entries, proposed_redlines, new_clauses_proposed
2. **Determine detection** (Y/P/N/NMI)
3. **If Y or P**: Score quality (Amendment, Rationale, Redline Quality)
4. **If N or NMI**: Quality scores = null
5. **Calculate points** and write evidence

### After All Items:

1. Calculate Part A summary (total, percentage, critical failures, pass/fail)
2. Calculate Part B summary (detection counts, tier breakdown, T1 gate, total points)
3. Verify all totals match individual evaluations

---

## ADDITIONAL ISSUES (Beyond GT)

After evaluating all GT issues, capture issues flagged by Leah but not in GT:

| Assessment | Meaning |
|------------|---------|
| **Valid** | Real issue Leah correctly identified |
| **Overlaps GT** | Relates to existing GT issue |
| **Hallucination** | Leah misread or fabricated |
| **Not Material** | Real but too minor |

Mark `gt_candidate: true` if the issue is material (T1/T2) and should be added to future GT versions. For stacking, additional issues may arise from either Part A (CP redline clauses) or Part B (whole document clauses).

---

## OUTPUT VALIDATION

Before saving, verify:

- [ ] All Part A redlines evaluated (count matches GT file)
- [ ] All Part B GT items evaluated (count matches GT file)
- [ ] Detection values are exactly Y, P, N, or NMI
- [ ] Quality scores are 1, 2, 3, or null (not 0)
- [ ] Points calculated correctly
- [ ] Part A critical failures checked
- [ ] Part B T1 gate reflects T1 detection status
- [ ] Summary totals match individual evaluations
- [ ] Evidence contains verbatim quotes

---

## Common Mistakes

DO NOT: Evaluate only Part A or only Part B
DO: Both parts must be completed for every evaluation

DO NOT: Award Part B quality scores when detection = N/NMI
DO: Quality scores = null if detection is not Y/P

DO NOT: Miss critical failures in Part A (REJECT as ACCEPT)
DO: Check GT expected action against Leah's actual action

DO NOT: Over-literal clause matching (miss semantic matches)
DO: Use semantic principle: "Did Leah identify THIS RISK?"

DO NOT: Miscalculate total points
DO: Part A total = sum of action + revision + reasoning per redline; Part B total = detection + quality per issue

---

## PROMPT END
