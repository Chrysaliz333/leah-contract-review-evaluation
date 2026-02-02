# Rules Stacking Mode Evaluation Prompt

---

## PROMPT START

You are evaluating Leah's contract review output for **Rules Stacking mode** — evaluating responses to counterparty (CP) redlines against deterministic rules.

**Contract:** {CONTRACT}
**Model:** {MODEL}
**Contract Type:** {NDA|SUBCONTRACT}

---

## MANDATORY FIRST STEPS (DO NOT SKIP)

1. **Read** mode documentation: `docs/modes/rules_stacking.md`
2. **Read** rule file: `rules_stacking/rule_files/NDA_Rules_Deterministic.csv` or `Subcontractor_Rules_Deterministic.csv` (based on contract type)
3. **Read** ground truth: `rules_stacking/ground_truth/{nda|subcontract}.json`
4. **Read** redlined contract: `rules_stacking/redlined_contracts/{nda|subcontract}/{CONTRACT}.docx`
5. **Read** canonical JSON: `rules_stacking/canonical_json/{CONTRACT}/{MODEL}.json`

---

## CRITICAL RULES: SCOPE AND GATES

| Rule | Explanation |
|------|-------------|
| **Scope = Redlines ONLY** | Evaluate ONLY Leah's responses to CP redlines; ignore unchanged text |
| **Scope violation** | Commenting on non-redlined clauses = AUTOMATIC FAIL |
| **Action values** | ONLY: `ACCEPT`, `MODIFY`, `REJECT`, `ACCEPT WITH RISK` |
| **Detection values** | `Y`, `P`, `N`, `NMI` — no symbols, no variations |
| **Critical failures** | REJECT as ACCEPT, ACCEPT as REJECT = AUTOMATIC FAIL |
| **Evidence** | Quote **verbatim** from canonical JSON and redline excerpts — no paraphrasing |
| **Independence** | DO NOT read other evaluation files for "examples" |

---

## CRITICAL: SCOPE CONSTRAINT

**You MUST evaluate ONLY CP redlines. DO NOT comment on non-redlined text.**

### What IS in Scope:
- CP proposed redlines
- Leah's response to each redline (ACCEPT/MODIFY/REJECT/ACCEPT WITH RISK)
- Justification for Leah's response

### What IS NOT in Scope:
- Unchanged contract text
- Clauses without CP redlines
- Leah's risk identification in non-redlined sections
- Original (non-redlined) language assessment

### Scope Violation Examples

FAIL: "The confidentiality clause in clause 2 is overly broad" (no CP redline here)
OK: "CP's redline at clause 2.1 adds undefined terms; Leah's MODIFY response is justified"

FAIL: "Licence grant should include IP warranties" (general observation, not about redline)
OK: "CP redline removes IP warranty; Leah's REJECT is appropriate"

---

## EVALUATION SCHEMA

Write output to: `rules_stacking/results/{CONTRACT}/{MODEL}.json`

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
  "redline_evaluations": [
    {
      "redline_id": "R-XX",
      "clause": "from rule file",
      "cp_redline_summary": "What CP is proposing to change",
      "expected_leah_action": "ACCEPT|MODIFY|REJECT|ACCEPT WITH RISK (from rule)",
      "leah_action": "ACCEPT|MODIFY|REJECT|ACCEPT WITH RISK|null (what Leah actually did)",
      "action_score": 0|1|2,
      "revision_score": 0|1|2,
      "reasoning_score": 0|1|2,
      "total_points": number,
      "critical_failure": null|"REJECT_AS_ACCEPT"|"ACCEPT_AS_REJECT"|"SCOPE_VIOLATION",
      "evidence": {
        "cp_redline_excerpt": "string (verbatim from redlined contract)",
        "leah_response_excerpt": "string (verbatim from canonical JSON)",
        "judge_reasoning": "Explain scoring decision and action assessment"
      }
    }
  ],
  "scope_violations": [
    {
      "clause_ref": "string",
      "issue": "string describing the scope violation",
      "severity": "CRITICAL"
    }
  ],
  "additional_issues": [],
  "summary": {
    "total_redlines": number,
    "redlines_evaluated": number,
    "action_correct_count": number,
    "action_score_total": number,
    "revision_score_total": number,
    "reasoning_score_total": number,
    "total_points": number,
    "max_possible_points": number,
    "percentage": number,
    "critical_failures": [],
    "scope_violations": number,
    "pass_fail": "PASS|FAIL"
  }
}
```

---

## ACTION VALUES (Rules Stacking)

| Value | Meaning | When to Use |
|-------|---------|-------------|
| **ACCEPT** | Leah agrees with CP's proposed change | CP's redline is acceptable or beneficial |
| **MODIFY** | Leah agrees with intent but proposes different language | CP's concern valid but suggested fix imperfect |
| **REJECT** | Leah disagrees with CP's proposed change | CP's redline is problematic and should not be adopted |
| **ACCEPT WITH RISK** | Leah accepts but notes risks or limitations | CP's redline acceptable but has drawbacks to monitor |

**Important:** `null` is ONLY used when Leah doesn't respond to the redline (treated as non-response).

---

## EXPECTED ACTIONS BY SCENARIO

| Scenario | Expected Action |
|----------|-----------------|
| CP INSERTED problematic text (rule says DELETE) | REJECT |
| CP INSERTED text (rule says AMEND) | MODIFY |
| CP DELETED protective text | REJECT (restore) |
| No rule applies | ACCEPT WITH RISK ANALYSIS |

---

## POINT CALCULATIONS

### Action Score (2 points max)

| Score | Criteria |
|-------|----------|
| **2** | Action matches rule expectation perfectly |
| **1** | Action is reasonable but different from rule expectation |
| **0** | Action contradicts rule or is inappropriate |

### Revision Score (2 points max)

**ONLY applicable when action = MODIFY**

| Score | Criteria |
|-------|----------|
| **2** | Proposed revision is clear, legally sound, addresses CP's concern |
| **1** | Revision is reasonable but imperfect or partially addresses concern |
| **0** | Revision is unclear, legally questionable, or doesn't address concern |
| **null** | Action is not MODIFY (no revision proposed) |

### Reasoning Score (2 points max)

| Score | Criteria |
|-------|----------|
| **2** | Specific legal basis or business justification provided |
| **1** | Rationale present but generic or incomplete |
| **0** | Missing, weak, or contradictory reasoning |

### Total Points per Redline

**Total = Action Score (2) + Revision Score (2) + Reasoning Score (2) = max 6 points**

---

## CRITICAL FAILURES (AUTOMATIC FAIL)

### REJECT as ACCEPT
Rule says: REJECT this CP redline (it's problematic)
Leah does: ACCEPT the redline
Result: AUTOMATIC FAIL — accepting unacceptable terms

### ACCEPT as REJECT
Rule says: ACCEPT this CP redline (it's standard/beneficial)
Leah does: REJECT the redline
Result: AUTOMATIC FAIL — rejecting favourable terms

### Scope Violation
Leah comments: On non-redlined text or unchanged clauses
Result: AUTOMATIC FAIL — violated evaluation scope

If ANY critical failure exists, set `pass_fail: FAIL` immediately regardless of points.

---

## EVALUATION PROCESS

### For Each Redline:

1. **Identify the redline** — Find CP's proposed change in redlined contract

2. **Find rule expectation** — What should Leah's response be?
   - Look up redline_id in rule file
   - Note expected action

3. **Find Leah's response** — Search canonical JSON
   - Find Leah's stated action (ACCEPT/MODIFY/REJECT/ACCEPT WITH RISK)
   - Find Leah's rationale and any proposed revision

4. **Check for scope violation**
   - Is Leah's response ONLY about the CP redline?
   - OR is Leah commenting on non-redlined text?
   - If comments on unchanged text -> mark as scope_violation, FAIL

5. **Check for critical failures**
   - Does action contradict rule expectation in a critical way?
   - REJECT as ACCEPT? -> critical_failure = "REJECT_AS_ACCEPT"
   - ACCEPT as REJECT? -> critical_failure = "ACCEPT_AS_REJECT"

6. **Score each dimension:**
   - Action (2 pts): Does action match rule?
   - Revision (2 pts): If MODIFY, is revision sound?
   - Reasoning (2 pts): Is rationale substantive?

7. **Calculate total** — Sum action + revision + reasoning

8. **Write evidence** — Verbatim excerpts + reasoning

### After All Redlines:

1. Calculate summary:
   - Total points
   - Check for critical failures
   - Check for scope violations
   - Determine pass/fail

2. **Pass/Fail Rule:**
   - Any critical failure -> FAIL
   - Any scope violation -> FAIL
   - Otherwise -> PASS if >=70% of total points

---

## SEMANTIC MATCHING FOR REDLINES

**Key Principle:** "Does Leah understand what the CP is proposing and why?"

| Scenario | Assessment |
|----------|-----------|
| Leah's action matches rule expectation | Correct |
| Leah's action is different but well-justified | Acceptable if reasoning is sound |
| Leah's action contradicts rule expectation | Problematic; check if it's critical |
| Leah doesn't respond to redline | NMI; score = 0 |

---

## QUALITY RUBRICS

### Action Score Rubric (2 points)

| Score | Criteria | Example |
|-------|----------|---------|
| **2** | Action matches rule expectation; appropriate and well-justified | Rule says REJECT; Leah REJECTS with sound reasoning |
| **1** | Action differs from rule but is reasonable and explained | Rule says ACCEPT; Leah MODIFIES with clear rationale |
| **0** | Action contradicts rule or is inappropriate | Rule says REJECT; Leah ACCEPTS (critical failure) |

### Revision Score Rubric (2 points) — When MODIFY

| Score | Criteria |
|-------|----------|
| **2** | Proposed revision clearly addresses CP's concern; legally sound; specific language |
| **1** | Revision attempts to address concern but is imperfect or generic |
| **0** | Revision doesn't address concern or is unclear |
| **null** | Leah's action is not MODIFY |

### Reasoning Score Rubric (2 points)

| Score | Criteria |
|-------|----------|
| **2** | Specific legal standard, contract reference, or business rationale cited |
| **1** | Rationale present but generic (e.g., "market standard") |
| **0** | Missing rationale or weak reasoning |

---

## DETECTING SCOPE VIOLATIONS

**Scope violations are NOT just bad scoring — they are automatic fails.**

### Red Flags for Scope Violation:

- [ ] Leah discusses non-redlined clause language
- [ ] Leah evaluates original contract terms (before redline)
- [ ] Leah addresses issues not in any CP redline
- [ ] Leah's comments apply to sections without redlines

### Examples of Scope Violations:

FAIL: "The confidentiality definition is too broad" (unless CP redline is about this)
FAIL: "Licence grant should include warranty" (unless CP redline addresses this)
FAIL: "Indemnity cap should be 2x fees" (unless CP redline proposes something different)

OK: "CP's redline removes the warranty; this is risky because..."
OK: "CP's proposed confidentiality definition excludes public information; market standard includes this carve-out"

---

## ADDITIONAL ISSUES (Beyond Redline Rules)

After evaluating all redlines, capture issues Leah flagged beyond redline scope:

| Assessment | Meaning |
|------------|---------|
| **Valid** | Real issue Leah correctly identified |
| **Overlaps Rule** | Relates to existing redline rule |
| **Hallucination** | Leah misread or fabricated |
| **Not Material** | Real but too minor |

Mark `gt_candidate: true` if issue is material and should be added to future rules.

---

## CRITICAL DECISION TREE

```
Is Leah's response ONLY about the CP redline?
  |-- NO  -> SCOPE VIOLATION -> FAIL
  +-- YES -> Continue

Does Leah's action match rule expectation?
  |-- YES perfectly  -> Action Score = 2
  |-- YES, justified -> Action Score = 1-2 (depends on reasoning)
  |-- NO, critical mismatch -> CRITICAL FAILURE -> FAIL
  +-- NO, but explained -> Action Score = 0-1

Is action = MODIFY?
  |-- YES -> Score revision quality (0-2)
  +-- NO  -> Revision Score = null

Is reasoning substantive?
  |-- YES, specific -> Reasoning Score = 2
  |-- PARTIAL -> Reasoning Score = 1
  +-- MISSING/WEAK -> Reasoning Score = 0
```

---

## EVALUATION CHECKLIST

Before finalising:

- [ ] All redlines evaluated
- [ ] Scope violations identified and flagged
- [ ] Critical failures checked (REJECT as ACCEPT, ACCEPT as REJECT)
- [ ] Action values valid only (ACCEPT/MODIFY/REJECT/ACCEPT WITH RISK)
- [ ] Revision scores only when action = MODIFY
- [ ] Total points calculated correctly per redline
- [ ] Summary totals accurate
- [ ] Pass/Fail determination correct (considering critical failures)
- [ ] Evidence includes verbatim quotes
- [ ] Judge reasoning explains each decision

---

## Common Mistakes

DO NOT: Award revision score when action is not MODIFY
DO: Revision Score = null if action is not MODIFY

DO NOT: Comment on non-redlined text
DO: Scope = CP redlines ONLY

DO NOT: Miss critical failures (REJECT as ACCEPT)
DO: Check rule expectation against Leah's action

DO NOT: Award points despite scope violation
DO: Scope violation = automatic FAIL regardless of points

---

## PROMPT END
