# Guidelines Mode Evaluation Prompt

---

## PROMPT START

You are evaluating Leah's contract review output for **Guidelines mode** — playbook-based position guidance.

**Contract:** {CONTRACT}
**Model:** {MODEL}
**Contract Type:** {NDA|SUBCONTRACT}

---

## MANDATORY FIRST STEPS (DO NOT SKIP)

1. **Read** mode documentation: `docs/modes/guidelines.md`
2. **Read** playbook: `guidelines/playbooks/` (NDA or Subcontract playbook based on contract type)
3. **Read** ground truth: `guidelines/ground_truth/{nda|subcontract}.json`
4. **Read** canonical JSON: `guidelines/canonical_json/{CONTRACT}/{MODEL}.json`

---

## CRITICAL RULES

| Rule | Explanation |
|------|-------------|
| **Position hierarchy** | Gold Standard > Fallback 1 > Fallback 2 > Red Flag (escalating concern) |
| **Red Flag = Auto-Fail** | ANY Red Flag missed = model FAILS entire contract |
| **Detection values** | ONLY: `Y`, `P`, `N`, `NMI` — no symbols, no variations |
| **Quality scores** | Use `1`, `2`, `3`, or `null` — never `0`, never empty string |
| **Evidence** | Quote **verbatim** from canonical JSON and playbook — no paraphrasing |
| **Independence** | DO NOT read other evaluation files for "examples" |

---

## PLAYBOOK POSITION HIERARCHY

### Guidance Levels (Escalating Concern)

```
Gold Standard     (T1) [Ideal position; seek aggressively]
      |
Fallback 1        (T2) [Acceptable; reasonable compromise]
      |
Fallback 2        (T3) [Undesirable; accept only with caution]
      |
Red Flag          [UNACCEPTABLE; auto-fail if missed]
```

### What Each Level Means

| Level | Tier | Meaning | Scoring |
|-------|------|---------|---------|
| **Gold Standard** | T1 | Optimal position for our side; maximum protection/benefit | 7 pts if detected |
| **Fallback 1** | T2 | Reasonable compromise; acceptable if Gold Standard unachievable | 5 pts if detected |
| **Fallback 2** | T3 | Below ideal but tolerable under pressure; requires justification | 1 pt if detected |
| **Red Flag** | Gate | UNACCEPTABLE — must be identified and rejected | Auto-FAIL if missed |

---

## EVALUATION SCHEMA

Write output to: `guidelines/results/{CONTRACT}/{MODEL}.json`

```json
{
  "meta": {
    "contract": "{CONTRACT}",
    "contract_type": "NDA|SUBCONTRACT",
    "model_id": "{MODEL}",
    "evaluation_timestamp": "2026-01-27T00:00:00Z",
    "evaluator_model": "sonnet",
    "playbook_version": "COPY FROM PLAYBOOK"
  },
  "position_evaluations": [
    {
      "position_id": "POS-XX",
      "clause": "from playbook",
      "position_topic": "e.g., 'Liability Cap'",
      "position_tier": "T1|T2|T3",
      "position_tier_name": "Gold Standard|Fallback 1|Fallback 2",
      "gold_standard": "description from playbook",
      "fallback_1": "description from playbook",
      "fallback_2": "description from playbook",
      "red_flag": "description from playbook",
      "leah_position": "from canonical JSON",
      "detection": "Y|P|N|NMI",
      "detection_points": number,
      "amendment_score": 1|2|3|null,
      "rationale_score": 1|2|3|null,
      "action_score": 1|2|3|null,
      "quality_points": number,
      "total_points": number,
      "evidence": {
        "leah_guidance_excerpt": "string (verbatim from canonical JSON)",
        "judge_reasoning": "Explain which position level Leah achieved and scoring rationale"
      }
    }
  ],
  "red_flags_identified": [
    {
      "flag_id": "RED-FLAG-XX",
      "topic": "from playbook",
      "flag_description": "from playbook",
      "detection": "Y|NMI",
      "is_critical_failure": true|false
    }
  ],
  "additional_issues": [],
  "summary": {
    "total_positions": number,
    "t1_positions": number,
    "t2_positions": number,
    "t3_positions": number,
    "red_flags_expected": number,
    "red_flags_detected": number,
    "red_flag_gate_pass": boolean,
    "detection_counts": {"Y": 0, "P": 0, "N": 0, "NMI": 0},
    "detection_by_tier": {
      "T1": {"Y": 0, "P": 0, "N": 0, "NMI": 0},
      "T2": {"Y": 0, "P": 0, "N": 0, "NMI": 0},
      "T3": {"Y": 0, "P": 0, "N": 0, "NMI": 0}
    },
    "total_detection_points": number,
    "total_quality_points": number,
    "total_points": number,
    "pass_fail": "PASS|FAIL"
  }
}
```

---

## DETECTION VALUES (Guidelines Mode)

| Value | Meaning | When to Use |
|-------|---------|-------------|
| **Y** | Position fully detected and properly addressed | Leah identifies the playbook position AND achieves appropriate tier level |
| **P** | Position partially detected or lower tier achieved | Leah identifies the concern but settles for lower tier than guidance suggests |
| **N** | Missed (false negative) | Clause exists but Leah misses playbook guidance |
| **NMI** | Not mentioned anywhere | Clause not addressed by Leah at all |

### Detection Point Calculation

| Tier | Y (Full) | P (Partial) | N/NMI |
|------|----------|-------------|-------|
| **T1 (Gold Standard)** | 7 | 3.5 | 0 |
| **T2 (Fallback 1)** | 5 | 2.5 | 0 |
| **T3 (Fallback 2)** | 1 | 0.5 | 0 |

---

## RED FLAG GATE RULE (CRITICAL)

### Red Flags Are Non-Negotiable

**IF ANY Red Flag has detection = NMI -> model FAILS entire contract**

Red Flags are show-stoppers. If Leah misses identifying an unacceptable position, the model fails regardless of other scores.

### Handling Red Flags

1. **Identify all Red Flags** — From playbook
2. **Check Leah's response** — Did Leah flag/reject the Red Flag?
3. **Mark detection:**
   - Y = Leah identified and rejected/flagged
   - NMI = Leah didn't mention (FAIL)
4. **Set gate:** `red_flag_gate_pass = all Red Flags have Y`

### Example Red Flag

Red Flag: "Unlimited liability indemnity for Receiving Party without cap"
Playbook says: "Must reject or cap to 2x annual fees"
Leah does: Marks as "Favourable" without comment
Result: FAIL — Red Flag missed

Leah does: "Reject unlimited indemnity; cap to 2x annual fees"
Result: PASS Red Flag gate

---

## POINT CALCULATIONS

### Detection Points (Tier-Based)

Awards points based on **position tier achieved**, not clause presence:

- **Achieves Gold Standard (T1):** Y=7, P=3.5
- **Achieves Fallback 1 (T2):** Y=5, P=2.5
- **Achieves Fallback 2 (T3):** Y=1, P=0.5
- **Missed or worse:** N/NMI=0

### Quality Points (When Detection = Y or P)

Three dimensions, max 1-3 points each:

- **Amendment Score** (1-3): Does proposed fix achieve or approach the position tier?
- **Rationale Score** (1-3): Is reasoning substantive? Cites business justification?
- **Action Score** (1-3): Is recommended action (AMEND/DELETE/ADD/FLAG) appropriate?

**Total quality = Amendment + Rationale + Action = max 9 points per position**

### Issue Total

**Total = Detection Points + Quality Points**

---

## QUALITY RUBRICS

### When Quality Scores Apply

Quality scores are awarded **only when detection = Y or P**.

If detection = N or NMI -> all quality scores = null

### Amendment Score Rubric (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Proposed language achieves or closely approaches Gold Standard position | Liability cap properly limited to 2x fees with clean drafting |
| **2** | Proposed language achieves Fallback 1 (reasonable compromise) | Indemnity capped but at 3x fees (slightly above Gold Standard) |
| **1** | Proposed language only achieves Fallback 2 or is questionable | Generic indemnity cap with unclear trigger |
| **null** | Detection = N/NMI | -- |

### Rationale Score Rubric (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Specific legal standard, business justification, market practice cited | "Indemnity caps should be 2x annual fees; market standard in SaaS" |
| **2** | Rationale present with context, missing specific details | "Indemnity should have reasonable cap; mitigates exposure" |
| **1** | Problem stated without substantive reasoning | "Unlimited indemnity is bad" |
| **null** | Detection = N/NMI | -- |

### Action Score Rubric (1-3)

| Score | Criteria | Example |
|-------|----------|---------|
| **3** | Recommended action is clearly appropriate and well-justified | AMEND to add cap; DELETE unlimited language |
| **2** | Action is reasonable but could be debated | FLAG for negotiation; modify indemnity scope |
| **1** | Action is questionable or imprecise | Suggests negotiation without clear direction |
| **null** | Detection = N/NMI | -- |

---

## EVALUATION PROCESS

### For Each Position:

1. **Identify position** — Find position topic in playbook
   - Note Gold Standard, Fallback 1, Fallback 2, Red Flag

2. **Find clause in contract** — Where does this position appear?

3. **Find Leah's response** — Search canonical JSON
   - Risk table entry?
   - Proposed redline?
   - Classification (Unfavourable, Favourable, etc.)?

4. **Determine what position Leah achieved:**
   - Did Leah seek Gold Standard? -> Y for T1
   - Did Leah achieve Fallback 1? -> Y for T2
   - Did Leah achieve Fallback 2? -> Y for T3
   - Did Leah miss the issue? -> N/NMI
   - Is Leah's approach partial? -> P for applicable tier

5. **Award detection points** — Based on tier achieved

6. **Score quality (if Y or P):**
   - Amendment: Does proposed fix align with tier?
   - Rationale: Is reasoning substantive?
   - Action: Is recommendation appropriate?

7. **Write evidence** — Verbatim excerpts + reasoning

### After All Positions:

1. **Evaluate Red Flags separately**
   - List all Red Flags from playbook
   - For each, mark Y (detected) or NMI (missed)
   - Set `red_flag_gate_pass` = all Red Flags are Y

2. **Determine Pass/Fail:**
   - If any Red Flag = NMI -> FAIL
   - Otherwise -> PASS (if points reasonable)

---

## RED FLAG vs POSITION

### Red Flags Are Separate

Red Flags are **not tiered positions**. They're binary gates:
- Detected (Y) = OK
- Missed (NMI) = FAIL

### Example Distinction

**Position (Tiered):**
- Gold: "Liability cap = 1x annual fees"
- Fallback 1: "Liability cap = 2x annual fees"
- Fallback 2: "Liability cap = 3x annual fees"
- Red Flag: "Unlimited liability — REJECT"

**If contract has unlimited liability:**
- Leah proposes 1x cap -> Y on position (achieves Gold), no Red Flag issue
- Leah proposes 2x cap -> Y on position (achieves Fallback 1)
- Leah misses unlimited clause -> Red Flag NMI = FAIL

---

## SEMANTIC MATCHING FOR GUIDELINES

**Key Principle:** "Did Leah understand what position the playbook recommends?"

| Scenario | Assessment |
|----------|-----------|
| Leah proposes exact playbook position | Y (full detection) |
| Leah proposes reasonable compromise | Y or P (depending on tier) |
| Leah misses position entirely | N or NMI |
| Leah addresses at adjacent/related clause with same concern | P (partial) |

### Semantic Match Criteria

Award Y or P when:
1. **Same playbook rule** — Both address the same Red Flag trigger
2. **Same party affected** — The representing party faces the same exposure
3. **Similar remediation** — Leah's proposed fix aligns with playbook guidance

**Rule of thumb:** When in doubt, award P rather than NMI if Leah demonstrably understood the risk.

---

## ADDITIONAL ISSUES (Beyond Playbook)

After evaluating all positions, capture issues Leah flagged beyond playbook:

| Assessment | Meaning |
|------------|---------|
| **Valid** | Real issue Leah correctly identified |
| **Overlaps Playbook** | Relates to existing playbook position |
| **Hallucination** | Leah misread or fabricated |
| **Not Material** | Real but too minor |

Mark `gt_candidate: true` if issue is material (T1/T2) and should be added to future playbook.

---

## CRITICAL DECISION TREE

```
Is this a Red Flag position?
  |-- YES -> Detection must be Y (detected)
  |         If NMI -> FAIL contract immediately
  +-- NO  -> Continue to position evaluation

What position tier did Leah achieve?
  |-- Gold Standard (T1) -> award 7 or 3.5 pts
  |-- Fallback 1 (T2)   -> award 5 or 2.5 pts
  |-- Fallback 2 (T3)   -> award 1 or 0.5 pts
  +-- Missed (N/NMI)    -> award 0 pts

Is detection Y or P?
  |-- YES -> Evaluate quality (Amendment, Rationale, Action)
  +-- NO  -> Quality scores = null
```

---

## EVALUATION CHECKLIST

Before finalising:

- [ ] All playbook positions evaluated
- [ ] All Red Flags identified and checked
- [ ] Detection values valid only (Y/P/N/NMI)
- [ ] Quality scores only when detection = Y/P
- [ ] Red Flag detection correct (Y or NMI)
- [ ] Red Flag gate pass/fail correct
- [ ] Total points calculated correctly per position
- [ ] Summary totals accurate
- [ ] Pass/Fail determination correct (including Red Flags)
- [ ] Evidence includes verbatim quotes
- [ ] Judge reasoning explains position tier achieved

---

## Common Mistakes

DO NOT: Award quality scores when detection = NMI
DO: Quality scores = null if detection is not Y/P

DO NOT: Miss Red Flag as just another position
DO: Red Flags are binary gates (Y or NMI = FAIL)

DO NOT: Award T1 points when Leah only achieves T2 tier
DO: Points match tier achieved (T2=5 or 2.5, not T1=7)

DO NOT: Fail to check Red Flags before finalising
DO: Red Flag gate is FIRST check (automatic FAIL if any NMI)

DO NOT: Confuse "position not detected" with Red Flag NMI
DO: Regular positions: N/NMI = 0 pts; Red Flags: NMI = FAIL contract

---

## PROMPT END
