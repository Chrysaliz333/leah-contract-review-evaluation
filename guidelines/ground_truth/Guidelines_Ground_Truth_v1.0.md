# Guidelines Ground Truth
## Playbook-Based Evaluation Reference

**Version:** 1.0  
**Generated:** 2026-01-27  
**Mode:** Guidelines (Playbook-Guided Review)  
**Contract Sets:** NDA (Receiving Party), Subcontract (Subcontractor)

---

## Overview

Guidelines mode evaluates Leah's ability to apply playbook rules while exercising independent legal judgment. The playbook provides qualifying context on top of full Freeform analysis.

### Key Principle

The playbook doesn't limit what Leah should find — it provides specific instructions for handling certain issues. Leah must:

1. Identify all risks a competent lawyer would find (Freeform baseline)
2. Apply specific playbook rules when triggers are present
3. Propose amendments aligned with playbook position hierarchy
4. Provide rationale linking risks to playbook guidance

### Position Hierarchy

| Position | Code | Meaning | Action Required |
|----------|------|---------|-----------------|
| **Gold Standard** | GS | Ideal position | None (compliant) |
| **Fallback 1** | FB1 | Acceptable compromise | FLAG for awareness |
| **Fallback 2** | FB2 | Minimum acceptable | FLAG, negotiate if possible |
| **Red Flag** | RF | Unacceptable | **AMEND or DELETE required** |

### Scoring Dimensions

| Dimension | T1 (RF) | T2 (FB) | T3 (GS/Minor) |
|-----------|---------|---------|---------------|
| Detection | 1 | 1 | 0.5 |
| Location | 1 | 1 | — |
| Action | 1 | 1 | — |
| Amendment | 2 | 1 | — |
| Rationale | 2 | 1 | — |
| **Maximum** | **7** | **5** | **0.5** |

### Pass Criteria

| Result | Criteria |
|--------|----------|
| **PASS** | ≥70% AND all Red Flags detected |
| **MARGINAL** | 50-69% OR 1-2 Red Flag misses |
| **FAIL** | <50% OR 3+ Red Flag misses |

---

## Summary Statistics

| Contract Type | Contracts | T1 Issues | T2 Issues | T3 Issues | Total | Max Points |
|---------------|-----------|-----------|-----------|-----------|-------|------------|
| NDA (Receiving Party) | 11 | 41 | 2 | 3 | 46 | 298.5 |
| Subcontract (Subcontractor) | 11 | 40 | 3 | 2 | 45 | 296.0 |
| **TOTAL** | **22** | **81** | **5** | **5** | **91** | **594.5** |

---

# Part 1: NDA Contracts

**Representing Party:** Receiving Party  
**Playbook:** NDA Receiving Party Playbook  
**Contracts:** 10

## NDA Playbook Rules Summary

| Rule | Clause Type | Red Flag Trigger | Action |
|------|-------------|------------------|--------|
| 1 | CI Definition | "whether or not marked", residual knowledge | AMEND |
| 2 | Reciprocity | Unilateral obligations | AMEND |
| 3 | Compelled Disclosure | "under no circumstances" | AMEND |
| 4 | Term & Survival | Perpetual, >5 years | AMEND |
| 5 | Non-Solicitation | >12 months | AMEND |
| 6 | Non-Compete | Any non-compete in NDA | DELETE |
| 7 | Return/Destruction | No retention right | AMEND |
| 8 | Injunctive Relief | Bond waiver | AMEND |
| 9 | Indemnification | Broad-form, negligence of counterparty | AMEND |
| 10 | Assignment | Asymmetric rights | AMEND |
| 11 | Governing Law | Offshore/distant jurisdiction | FLAG |
| 12 | Limitation of Liability | Unlimited, no cap | AMEND |

---


## 1. NDA_Atlas_Employment

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 1.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Section 4.2 | 4 | T1 | Red Flag | AMEND |
| 3 | Section 7.2 | 6 | T1 | Red Flag | AMEND |
| 4 | Section 8.1 | 9 | T1 | Red Flag | AMEND |

### Issue 1 | Section 1.1 | T1

**CI Definition**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> general skills, knowledge, and experience

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove 'whether or not marked as confidential' and require written marking

**Key Elements:**

- Identifies overbroad CI language

**Rationale Must Include:**

Cites specific trigger phrase from playbook rule 1

---

### Issue 2 | Section 4.2 | T1

**Term and Survival**

**Playbook Rule:** 4
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> shall remain in full force and effect for so long as the information retains its confidential character

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> three (3) years following termination

**Key Elements:**

- Identifies excessive survival period

**Rationale Must Include:**

Cites specific duration; references 3-year standard from rule 4

---

### Issue 3 | Section 7.2 | T1

**Non-Compete**

**Playbook Rule:** 6
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> shall not provide similar services to competitors

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> [DELETE ENTIRE SECTION]

**Key Elements:**

- Identifies non-compete in NDA

**Rationale Must Include:**

Notes non-compete unacceptable per rule 6

---

### Issue 4 | Section 8.1 | T1

**Indemnification**

**Playbook Rule:** 9
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> fully indemnify and hold harmless

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove broad-form trigger or add fault qualifier per Gold Standard

**Key Elements:**

- Flags broad-form trigger

**Rationale Must Include:**

Identifies negligence/fault language; references rule 9

---


## 2. NDA_Cascade_Supplier

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 1.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Section 2.1 | 2 | T1 | Red Flag | AMEND |
| 3 | Section 5.1 | 7 | T1 | Red Flag | AMEND |
| 4 | Section 9.2 | 10 | T1 | Red Flag | AMEND |

### Issue 1 | Section 1.1 | T1

**CI Definition**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Information may be disclosed in any form or medium, whether tangible or intangible, written, oral, visual, or electronic.

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Oral disclosures confirmed in writing within 10 days

**Key Elements:**

- Identifies overbroad CI language

**Rationale Must Include:**

Cites specific trigger phrase from playbook rule 1

---

### Issue 2 | Section 2.1 | T1

**Reciprocity**

**Playbook Rule:** 2
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> the recieving party shall [...]

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Each party receiving CI shall

**Key Elements:**

- Flags unilateral obligations

**Rationale Must Include:**

References playbook rule 2; explains mutual obligation requirement

---

### Issue 3 | Section 5.1 | T1

**Return and Destruction**

**Playbook Rule:** 7
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> destroy all copies, notes, derivatives without retention

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> may retain archival copy + backups

**Key Elements:**

- Flags no retention exception

**Rationale Must Include:**

References archival copy requirement from rule 7

---

### Issue 4 | Section 9.2 | T1

**Assignment**

**Playbook Rule:** 10
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> may assign at its sole discretion

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Neither party may assign without consent

**Key Elements:**

- Flags asymmetric assignment

**Rationale Must Include:**

Notes unilateral assignment right; references mutual requirement

---


## 3. NDA_GlobalPharm_Research

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 1.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Section 5.1 | 7 | T1 | Red Flag | AMEND |
| 3 | Section 8.2 | 8 | T1 | Red Flag | AMEND |
| 4 | Section 10.1 | 11 | T1 | Red Flag | AMEND |

### Issue 1 | Section 1.1 | T1

**CI Definition**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> regardless of whether publicly available

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove 'whether or not marked as confidential' and require written marking

**Key Elements:**

- Identifies overbroad CI language

**Rationale Must Include:**

Cites specific trigger phrase from playbook rule 1

---

### Issue 2 | Section 5.1 | T1

**Return and Destruction**

**Playbook Rule:** 7
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> destroy all copies without exception

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> may retain archival copy + backups

**Key Elements:**

- Flags no retention exception

**Rationale Must Include:**

References archival copy requirement from rule 7

---

### Issue 3 | Section 8.2 | T1

**Injunctive Relief**

**Playbook Rule:** 8
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> without the necessity of posting any bond

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove bond waiver language; retain injunctive relief provision

**Key Elements:**

- Identifies bond waiver

**Rationale Must Include:**

Cites bond waiver language; references rule 8

---

### Issue 4 | Section 10.1 | T1

**Governing Law**

**Playbook Rule:** 11
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> courts of the Cayman Islands

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Jurisdiction with party nexus

**Key Elements:**

- Flags offshore/distant jurisdiction

**Rationale Must Include:**

Identifies jurisdiction issue; recommends nexus-based forum

---


## 4. NDA_Meridian_Unilateral

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 1.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Section 2.1 | 2 | T1 | Red Flag | AMEND |
| 3 | Section 3.2 | 3 | T1 | Red Flag | AMEND |
| 4 | Section 7.2 | 6 | T1 | Red Flag | AMEND |
| 5 | Section 8.3 | 12 | T1 | Red Flag | AMEND |

### Issue 1 | Section 1.1 | T1

**CI Definition**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> reasonably should be understood to be confidential

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Require written marking at time of disclosure, or for oral disclosures, confirmation in writing within ten (10) business days

**Key Elements:**

- Identifies overbroad CI language
- requires written confirmation for oral disclosures

**Rationale Must Include:**

Cites specific trigger phrase from playbook rule 1; explains oral disclosure risk

---

### Issue 2 | Section 2.1 | T1

**Reciprocity**

**Playbook Rule:** 2
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> shall apply solely to the Receiving Party

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Each party receiving CI shall

**Key Elements:**

- Flags unilateral obligations

**Rationale Must Include:**

References playbook rule 2; explains mutual obligation requirement

---

### Issue 3 | Section 3.2 | T1

**Compelled Disclosure**

**Playbook Rule:** 3
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> under no circumstances

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> may disclose if required by law, with notice

**Key Elements:**

- Flags absolute disclosure prohibition

**Rationale Must Include:**

Cites "under no circumstances" language; references rule 3

---

### Issue 4 | Section 7.2 | T1

**Non-Compete**

**Playbook Rule:** 6
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> shall not compete

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> [DELETE ENTIRE SECTION]

**Key Elements:**

- Identifies non-compete in NDA

**Rationale Must Include:**

Notes non-compete unacceptable per rule 6

---

### Issue 5 | Section 8.3 | T1

**Limitation of Liability**

**Playbook Rule:** 12
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> unlimited liability

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Add mutual liability cap

**Key Elements:**

- Flags unlimited/missing liability cap

**Rationale Must Include:**

Identifies cap issue; recommends mutual cap

---


## 5. NDA_Nexus_Investment

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 3.2 | 3 | T1 | Red Flag | AMEND |
| 2 | Section 7.1 | 5 | T1 | Red Flag | AMEND |
| 3 | Section 8.2 | 8 | T1 | Red Flag | AMEND |
| 4 | Section 8.3 | 12 | T1 | Red Flag | AMEND |

### Issue 1 | Section 3.2 | T1

**Compelled Disclosure**

**Playbook Rule:** 3
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> shall not make any disclosure whatsoever

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> may disclose if required by law, with notice

**Key Elements:**

- Flags absolute disclosure prohibition

**Rationale Must Include:**

Cites "under no circumstances" language; references rule 3

---

### Issue 2 | Section 7.1 | T1

**Non-Solicitation**

**Playbook Rule:** 5
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> eighteen (18) months following

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> twelve (12) months

**Key Elements:**

- Flags period exceeding 12 months

**Rationale Must Include:**

Cites specific duration; references 12-month maximum

---

### Issue 3 | Section 8.2 | T1

**Injunctive Relief**

**Playbook Rule:** 8
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> waives any requirement for bond

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove bond waiver language; retain injunctive relief provision

**Key Elements:**

- Identifies bond waiver

**Rationale Must Include:**

Cites bond waiver language; references rule 8

---

### Issue 4 | Section 8.3 | T1

**Limitation of Liability**

**Playbook Rule:** 12
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> monetary damages may not provide adequate compensation

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Add mutual liability cap

**Key Elements:**

- Flags unlimited/missing liability cap

**Rationale Must Include:**

Identifies cap issue; recommends mutual cap

---


## 6. NDA_Quantum_JointVenture

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 1.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Section 3.2 | 3 | T1 | Red Flag | AMEND |
| 3 | Section 7.1 | 5 | T1 | Red Flag | AMEND |
| 4 | Section 8.2 | 8 | T1 | Red Flag | AMEND |

### Issue 1 | Section 1.1 | T1

**CI Definition**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> including information retained in unaided memory

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove residual knowledge clause or add reasonable use limitations

**Key Elements:**

- Identifies overbroad CI language

**Rationale Must Include:**

Cites specific trigger phrase from playbook rule 1

---

### Issue 2 | Section 3.2 | T1

**Compelled Disclosure**

**Playbook Rule:** 3
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> shall not disclose under any circumstances

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> may disclose if required by law, with notice

**Key Elements:**

- Flags absolute disclosure prohibition

**Rationale Must Include:**

Cites "under no circumstances" language; references rule 3

---

### Issue 3 | Section 7.1 | T1

**Non-Solicitation**

**Playbook Rule:** 5
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> thirty-six (36) months

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> twelve (12) months

**Key Elements:**

- Flags period exceeding 12 months

**Rationale Must Include:**

Cites specific duration; references 12-month maximum

---

### Issue 4 | Section 8.2 | T1

**Injunctive Relief**

**Playbook Rule:** 8
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> without posting bond or security

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove bond waiver language; retain injunctive relief provision

**Key Elements:**

- Identifies bond waiver

**Rationale Must Include:**

Cites bond waiver language; references rule 8

---


## 7. NDA_Sterling_Mutual

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 4.1 | 4 | T1 | Red Flag | AMEND |
| 2 | Section 7.2 | 6 | T1 | Red Flag | AMEND |
| 3 | Section 8.1 | 9 | T1 | Red Flag | AMEND |
| 4 | Section 10.1 | 11 | T1 | Red Flag | AMEND |

### Issue 1 | Section 4.1 | T1

**Term and Survival**

**Playbook Rule:** 4
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> ten (10) years form such expiration

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> three (3) years following termination

**Key Elements:**

- Identifies excessive survival period

**Rationale Must Include:**

Cites specific duration; references 3-year standard from rule 4

---

### Issue 2 | Section 7.2 | T1

**Non-Compete**

**Playbook Rule:** 6
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> for two (2) years thereafter

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> [DELETE ENTIRE SECTION]

**Key Elements:**

- Identifies non-compete in NDA

**Rationale Must Include:**

Notes non-compete unacceptable per rule 6

---

### Issue 3 | Section 8.1 | T1

**Indemnification**

**Playbook Rule:** 9
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> regardless of the fault or negligence

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove broad-form trigger and add proportionate fault qualifier

**Key Elements:**

- Flags broad-form trigger

**Rationale Must Include:**

Identifies negligence/fault language; references rule 9

---

### Issue 4 | Section 10.1 | T1

**Governing Law**

**Playbook Rule:** 11
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> exclusive jurisdiction of Singapore

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Jurisdiction with party nexus

**Key Elements:**

- Flags offshore/distant jurisdiction

**Rationale Must Include:**

Identifies jurisdiction issue; recommends nexus-based forum

---


## 8. NDA_TechPartners_Bilateral

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 1.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Section 4.1 | 4 | T1 | Red Flag | AMEND |
| 3 | Section 7.1 | 5 | T1 | Red Flag | AMEND |
| 4 | Section 8.1 | 9 | T1 | Red Flag | AMEND |
| 5 | Sections 3.1-3.2 | 3 | T2 | Fallback 1 | FLAG |
| 6 | Section 9.2 | 10 | T2 | Fallback 1 | FLAG |
| 7 | Section 1.2 | 1 | T3 | Near Gold | FLAG |
| 8 | Section 2.1(d) | 2 | T3 | Gold Standar | FLAG |
| 9 | Section 6.1 | N/A | T3 | Gold Standar | FLAG |

### Issue 1 | Section 1.1 | T1

**CI Definition**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> whether or not marked as confidential

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove 'whether or not marked as confidential' and require written marking

**Key Elements:**

- Identifies overbroad CI language

**Rationale Must Include:**

Cites specific trigger phrase from playbook rule 1

---

### Issue 2 | Section 4.1 | T1

**Term and Survival**

**Playbook Rule:** 4
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> shall survive in perpetuity

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> three (3) years following termination

**Key Elements:**

- Identifies excessive survival period

**Rationale Must Include:**

Cites specific duration; references 3-year standard from rule 4

---

### Issue 3 | Section 7.1 | T1

**Non-Solicitation**

**Playbook Rule:** 5
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> twenty-four (24) months

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> twelve (12) months

**Key Elements:**

- Flags period exceeding 12 months

**Rationale Must Include:**

Cites specific duration; references 12-month maximum

---

### Issue 4 | Section 8.1 | T1

**Indemnification**

**Playbook Rule:** 9
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> whether or not caused by the negligence

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove 'whether or not caused by the negligence' and add proportionate fault qualifier

**Key Elements:**

- Flags broad-form trigger

**Rationale Must Include:**

Identifies negligence/fault language; references rule 9

---

### Issue 5 | Sections 3.1-3.2 | T2

**Compelled Disclosure**

**Playbook Rule:** 3
**Playbook Standard:** Fallback 1

**Trigger Phrase:**

> may disclose... if required by applicable law (3.1) with prompt notice (3.2) but no prior notice before disclosure

**Expected Classification:** ⚠️
**Expected Action:** FLAG

**Expected Amendment:**

> Add to Section 3.1: "provided that the Receiving Party shall, where legally permitted, give prior written notice to the Disclosing Party before such disclosure"

**Key Elements:**

- Prior notice requirement where legally permitted
- opportunity for protective order before disclosure

**Rationale Must Include:**

Current language permits disclosure with only post-hoc notice; Gold Standard requires prior notice to enable protective order

---

### Issue 6 | Section 9.2 | T2

**Assignment**

**Playbook Rule:** 10
**Playbook Standard:** Fallback 1

**Trigger Phrase:**

> Neither party may assign... without prior written consent

**Expected Classification:** ⚠️
**Expected Action:** FLAG

**Expected Amendment:**

> Add: "which consent shall not be unreasonably withheld or delayed"

**Key Elements:**

- Reasonableness standard for consent
- prevents arbitrary refusal

**Rationale Must Include:**

Mutual restriction is good but lacks reasonableness qualifier; could enable bad-faith refusal

---

### Issue 7 | Section 1.2 | T3

**CI Carve-Out Evidence**

**Playbook Rule:** 1
**Playbook Standard:** Near Gold

**Trigger Phrase:**

> was rightfully in possession... is rightfully obtained... is independently developed

**Expected Classification:** ✅
**Expected Action:** FLAG

**Expected Amendment:**

> Consider adding "as evidenced by written records" to prior knowledge and independent development carve-outs

**Key Elements:**

- Evidence requirement clarification

**Rationale Must Include:**

Minor drafting improvement; evidentiary standard implicit but could be explicit

---

### Issue 8 | Section 2.1(d) | T3

**Standard of Care**

**Playbook Rule:** 2
**Playbook Standard:** Gold Standard

**Trigger Phrase:**

> at least the same degree of care used to protect its own confidential information

**Expected Classification:** ✅
**Expected Action:** FLAG

**Expected Amendment:**

> Consider adding "but in no event less than reasonable care"

**Key Elements:**

- Minimum care floor

**Rationale Must Include:**

Acceptable language but adding minimum floor prevents argument that lax internal practices justify lax protection

---

### Issue 9 | Section 6.1 | T3

**No Licence**

**Playbook Rule:** N/A
**Playbook Standard:** Gold Standard

**Trigger Phrase:**

> Nothing in this Agreement grants any licence or rights to any intellectual property

**Expected Classification:** ✅
**Expected Action:** FLAG

**Expected Amendment:**

> Consider adding: "All Confidential Information and any intellectual property rights therein remain the sole property of the Disclosing Party"

**Key Elements:**

- Explicit ownership confirmation

**Rationale Must Include:**

Minor enhancement; ownership implied but explicit statement adds clarity

---


## 9. NDA_Vanguard_Technical

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 2.1 | 2 | T1 | Red Flag | AMEND |
| 2 | Section 5.1 | 7 | T1 | Red Flag | AMEND |
| 3 | Section 10.1 | 11 | T1 | Red Flag | AMEND |
| 4 | Section 8.3 | 12 | T1 | Red Flag | AMEND |

### Issue 1 | Section 2.1 | T1

**Reciprocity**

**Playbook Rule:** 2
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> This Agreement sets forth the obligations of the Receiving Party with respect to the Confidential Information disclosed by the Disclosing Party hereunder.

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Each party receiving CI shall

**Key Elements:**

- Flags unilateral obligations

**Rationale Must Include:**

References playbook rule 2; explains mutual obligation requirement

---

### Issue 2 | Section 5.1 | T1

**Return and Destruction**

**Playbook Rule:** 7
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> no copies may be retained for any purpose

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> may retain archival copy + backups

**Key Elements:**

- Flags no retention exception

**Rationale Must Include:**

References archival copy requirement from rule 7

---

### Issue 3 | Section 10.1 | T1

**Governing Law**

**Playbook Rule:** 11
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> courts of Dubai, UAE

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Jurisdiction with party nexus

**Key Elements:**

- Flags offshore/distant jurisdiction

**Rationale Must Include:**

Identifies jurisdiction issue; recommends nexus-based forum

---

### Issue 4 | Section 8.3 | T1

**Limitation of Liability**

**Playbook Rule:** 12
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> The Receiving Party shall be fully liable for all damages, losses, and expenses arising from or related to any breach of its obligations under this Agreement.

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Add mutual liability cap

**Key Elements:**

- Flags unlimited/missing liability cap

**Rationale Must Include:**

Identifies cap issue; recommends mutual cap

---


## 10. NDA_Vertex_Strategic

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Section 2.1 | 2 | T1 | Red Flag | AMEND |
| 2 | Section 4.1 | 4 | T1 | Red Flag | AMEND |
| 3 | Section 9.2 | 10 | T1 | Red Flag | AMEND |
| 4 | Section 8.3 | 12 | T1 | Red Flag | AMEND |

### Issue 1 | Section 2.1 | T1

**Reciprocity**

**Playbook Rule:** 2
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> shall apply solely to the Receiving Party

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Each party receiving CI shall

**Key Elements:**

- Flags unilateral obligations

**Rationale Must Include:**

References playbook rule 2; explains mutual obligation requirement

---

### Issue 2 | Section 4.1 | T1

**Term and Survival**

**Playbook Rule:** 4
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> indefinitely following termination

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> three (3) years following termination

**Key Elements:**

- Identifies excessive survival period

**Rationale Must Include:**

Cites specific duration; references 3-year standard from rule 4

---

### Issue 3 | Section 9.2 | T1

**Assignment**

**Playbook Rule:** 10
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> may freely assign without consent

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Neither party may assign without consent

**Key Elements:**

- Flags asymmetric assignment

**Rationale Must Include:**

Notes unilateral assignment right; references mutual requirement

---

### Issue 4 | Section 8.3 | T1

**Limitation of Liability**

**Playbook Rule:** 12
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> all damages without limitation

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Add mutual liability cap

**Key Elements:**

- Flags unlimited/missing liability cap

**Rationale Must Include:**

Identifies cap issue; recommends mutual cap

---


## 11. TOTALS

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | N/A | None | T? | N/A | None |

### Issue 1 | N/A | T?

**None**

**Playbook Rule:** None
**Playbook Standard:** Unknown

**Expected Classification:** None
**Expected Action:** None

---


# Part 2: Subcontract Contracts

**Representing Party:** Subcontractor  
**Playbook:** Subcontractor Playbook  
**Contracts:** 10

## Subcontract Playbook Rules Summary

| Rule | Clause Type | Red Flag Trigger | Action |
|------|-------------|------------------|--------|
| 1 | Indemnification | Broad-form, negligence of others | AMEND |
| 2 | Non-Standard Insurance | Unusual coverage types | AMEND |
| 3 | Insurance Limits | Excessive limits | AMEND |
| 4 | Insurance Documentation | Full policy copies | AMEND |
| 5 | Professional Liability | Excessive limits | AMEND |
| 6 | Additional Insured | Blanket AI without form | AMEND |
| 7 | Waiver of Subrogation | Excessive scope | AMEND |
| 8 | Limitation of Liability | No cap, unconscionable | AMEND |
| 9 | Consequential Damages | Not waived mutually | AMEND |
| 10 | Personal Guarantee | Any guarantee | DELETE |
| 11 | Union/PLA | Mandatory union/PLA | DELETE |
| 12 | Non-Compete | Post-completion restrictions | DELETE |
| 13 | Liquidated Damages | Excessive penalties | AMEND |
| 14 | Vaccination | Mandatory vaccination | DELETE |

---


## 1. Subcontract_Curtainwall_Vector

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 6.2 | 3 | T1 | Red Flag | AMEND |
| 2 | Article 6.H | 6 | T1 | Red Flag | AMEND |
| 3 | Article 7.1 | 8 | T1 | Red Flag | AMEND |
| 4 | Article 11.1 | 12 | T1 | Red Flag | DELETE |

### Issue 1 | Article 6.2 | T1

**Additional Insured Forms**

**Playbook Rule:** 3
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> CG 2010 11/85

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> CG 2010 04/13 and CG 2037 04/13

**Key Elements:**

- Identifies outdated endorsement forms

**Rationale Must Include:**

Cites form number; references current 04/13 requirement

---

### Issue 2 | Article 6.H | T1

**Umbrella Limits**

**Playbook Rule:** 6
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> $20,000,000

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> $5,000,000 per occurrence and aggregate

**Key Elements:**

- Flags excessive umbrella limits

**Rationale Must Include:**

Cites specific limits; references $5M standard

---

### Issue 3 | Article 7.1 | T1

**Liquidated Damages**

**Playbook Rule:** 8
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> $5,000 per calendar day

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> pass-through only, proportionate to fault

**Key Elements:**

- Flags direct LD exposure

**Rationale Must Include:**

Cites daily rate; references pass-through only standard

---

### Issue 4 | Article 11.1 | T1

**Non-Compete**

**Playbook Rule:** 12
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> two (2) years following completion

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ENTIRE ARTICLE 11]

**Key Elements:**

- Identifies non-compete in subcontract

**Rationale Must Include:**

Notes restriction; references absolute prohibition

---


## 2. Subcontract_Demolition_Prime

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 5.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Article 6.2 | 3 | T1 | Red Flag | AMEND |
| 3 | Article 6.H | 6 | T1 | Red Flag | AMEND |
| 4 | Article 7.2 | 9 | T1 | Red Flag | AMEND |

### Issue 1 | Article 5.1 | T1

**Indemnification**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> regardless of fault

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> to extent caused by Subcontractor's negligence

**Key Elements:**

- Identifies broad-form indemnification

**Rationale Must Include:**

Cites negligence trigger; references proportionate fault standard

---

### Issue 2 | Article 6.2 | T1

**Additional Insured Forms**

**Playbook Rule:** 3
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> CG 2010 10/01 and CG 2037 10/01

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> CG 2010 04/13 and CG 2037 04/13

**Key Elements:**

- Identifies outdated endorsement forms

**Rationale Must Include:**

Cites form number; references current 04/13 requirement

---

### Issue 3 | Article 6.H | T1

**Umbrella Limits**

**Playbook Rule:** 6
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> $15,000,000

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> $5,000,000 per occurrence and aggregate

**Key Elements:**

- Flags excessive umbrella limits

**Rationale Must Include:**

Cites specific limits; references $5M standard

---

### Issue 4 | Article 7.2 | T1

**Consequential Damages**

**Playbook Rule:** 9
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> lost profits, loss of use, loss of business opportunity

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Mutual waiver of consequential damages

**Key Elements:**

- Flags one-sided consequential exposure

**Rationale Must Include:**

Identifies damage types; references mutual waiver

---


## 3. Subcontract_FireProtection_Apex

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 6.2 | 3 | T1 | Red Flag | AMEND |
| 2 | Article 6.G | 5 | T1 | Red Flag | AMEND |
| 3 | Article 7.2 | 9 | T1 | Red Flag | AMEND |
| 4 | Article 12.1 | 14 | T1 | Red Flag | DELETE |

### Issue 1 | Article 6.2 | T1

**Additional Insured Forms**

**Playbook Rule:** 3
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> CG 2010 11/85 and CG 2037 10/01

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> CG 2010 04/13 and CG 2037 04/13

**Key Elements:**

- Identifies outdated endorsement forms

**Rationale Must Include:**

Cites form number; references current 04/13 requirement

---

### Issue 2 | Article 6.G | T1

**Professional Liability**

**Playbook Rule:** 5
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> $4,000,000 per claim / $8,000,000 aggregate

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> $2,000,000 per claim / $3,000,000 aggregate

**Key Elements:**

- Flags excessive PL limits

**Rationale Must Include:**

Cites specific limits; references $2M/$3M maximum

---

### Issue 3 | Article 7.2 | T1

**Consequential Damages**

**Playbook Rule:** 9
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> including consequential damages, indirect damages

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Mutual waiver of consequential damages

**Key Elements:**

- Flags one-sided consequential exposure

**Rationale Must Include:**

Identifies damage types; references mutual waiver

---

### Issue 4 | Article 12.1 | T1

**Vaccination**

**Playbook Rule:** 14
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> COVID-19 vaccination

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ARTICLE 12.1]

**Key Elements:**

- Flags mandatory vaccination

**Rationale Must Include:**

Identifies vaccination requirement; references rule 14

---


## 4. Subcontract_Flooring_Nexus

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 6.3 | 4 | T1 | Red Flag | AMEND |
| 2 | Article 6.G | 5 | T1 | Red Flag | AMEND |
| 3 | Article 9 | 10 | T1 | Red Flag | DELETE |
| 4 | Article 12.1 | 14 | T1 | Red Flag | DELETE |

### Issue 1 | Article 6.3 | T1

**Insurance Documentation**

**Playbook Rule:** 4
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> certified copies of all policies and endorsements

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Certificates of Insurance and endorsements

**Key Elements:**

- Flags excessive documentation requirement

**Rationale Must Include:**

Notes policy copy requirement; references certificate standard

---

### Issue 2 | Article 6.G | T1

**Professional Liability**

**Playbook Rule:** 5
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> $5,000,000 per claim / $10,000,000 aggregate

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> $2,000,000 per claim / $3,000,000 aggregate

**Key Elements:**

- Flags excessive PL limits

**Rationale Must Include:**

Cites specific limits; references $2M/$3M maximum

---

### Issue 3 | Article 9 | T1

**Personal Guarantee**

**Playbook Rule:** 10
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> unconditionally and irrevocably guarantee

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ENTIRE ARTICLE 9]

**Key Elements:**

- Identifies personal guarantee

**Rationale Must Include:**

Notes guarantee language; references absolute prohibition

---

### Issue 4 | Article 12.1 | T1

**Vaccination**

**Playbook Rule:** 14
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> annual influenza vaccination

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ARTICLE 12.1]

**Key Elements:**

- Flags mandatory vaccination

**Rationale Must Include:**

Identifies vaccination requirement; references rule 14

---


## 5. Subcontract_HVAC_Titan

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 5.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Article 6.H | 6 | T1 | Red Flag | AMEND |
| 3 | Article 7.1 | 8 | T1 | Red Flag | AMEND |
| 4 | Article 11.1 | 12 | T1 | Red Flag | DELETE |
| 5 | Article 3.2 | N/A | T2 | Fallback 2 | FLAG |
| 6 | Article 3.2 | N/A | T2 | Fallback 1 | FLAG |
| 7 | Article 13.3 | N/A | T2 | Fallback 2 | FLAG |
| 8 | Article 6.D/E/F | 2 | T3 | Gold Standar | FLAG |
| 9 | Article 12.1 | N/A | T3 | Gold Standar | FLAG |

### Issue 1 | Article 5.1 | T1

**Indemnification**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> whether caused in whole or in part by negligence of Contractor

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> to extent caused by Subcontractor's negligence

**Key Elements:**

- Identifies broad-form indemnification

**Rationale Must Include:**

Cites negligence trigger; references proportionate fault standard

---

### Issue 2 | Article 6.H | T1

**Umbrella Limits**

**Playbook Rule:** 6
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> $12,000,000

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> $5,000,000 per occurrence and aggregate

**Key Elements:**

- Flags excessive umbrella limits

**Rationale Must Include:**

Cites specific limits; references $5M standard

---

### Issue 3 | Article 7.1 | T1

**Liquidated Damages**

**Playbook Rule:** 8
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> $3,000 per calendar day

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> pass-through only, proportionate to fault

**Key Elements:**

- Flags direct LD exposure

**Rationale Must Include:**

Cites daily rate; references pass-through only standard

---

### Issue 4 | Article 11.1 | T1

**Non-Compete**

**Playbook Rule:** 12
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> eighteen (18) months

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ENTIRE ARTICLE 11]

**Key Elements:**

- Identifies non-compete in subcontract

**Rationale Must Include:**

Notes restriction; references absolute prohibition

---

### Issue 5 | Article 3.2 | T2

**Payment Terms**

**Playbook Rule:** N/A
**Playbook Standard:** Fallback 2

**Trigger Phrase:**

> within forty-five (45) days after receipt

**Expected Classification:** ⚠️
**Expected Action:** FLAG

**Expected Amendment:**

> Negotiate to "within thirty (30) days after receipt of a proper application"

**Key Elements:**

- 30-day payment term
- industry standard timing

**Rationale Must Include:**

45-day payment terms extend cash flow burden; 30 days is industry standard for subcontractors

---

### Issue 6 | Article 3.2 | T2

**Retainage**

**Playbook Rule:** N/A
**Playbook Standard:** Fallback 1

**Trigger Phrase:**

> less retainage of ten percent (10%)

**Expected Classification:** ⚠️
**Expected Action:** FLAG

**Expected Amendment:**

> Negotiate to "less retainage of five percent (5%)" or add retainage reduction at 50% completion

**Key Elements:**

- Reduced retainage percentage
- or retainage release schedule

**Rationale Must Include:**

10% retainage significantly impacts cash flow; 5% or graduated release is more balanced

---

### Issue 7 | Article 13.3 | T2

**Assignment**

**Playbook Rule:** N/A
**Playbook Standard:** Fallback 2

**Trigger Phrase:**

> Subcontractor shall not assign... without prior written consent

**Expected Classification:** ⚠️
**Expected Action:** FLAG

**Expected Amendment:**

> Add mutual restriction: "Neither party may assign this Subcontract without prior written consent, which shall not be unreasonably withheld"

**Key Elements:**

- Mutual assignment restriction
- reasonableness standard

**Rationale Must Include:**

One-sided restriction; Contractor can assign freely while Subcontractor is restricted

---

### Issue 8 | Article 6.D/E/F | T3

**Reserved Insurance Sections**

**Playbook Rule:** 2
**Playbook Standard:** Gold Standard

**Trigger Phrase:**

> D. Reserved. E. Reserved. F. Reserved.

**Expected Classification:** ✅
**Expected Action:** FLAG

**Expected Amendment:**

> Request clarification: confirm reserved sections will not be populated with additional requirements

**Key Elements:**

- Confirmation no additional coverage will be required

**Rationale Must Include:**

Reserved sections may indicate future additions; confirm scope is final

---

### Issue 9 | Article 12.1 | T3

**Safety Plan Submission**

**Playbook Rule:** N/A
**Playbook Standard:** Gold Standard

**Trigger Phrase:**

> Subcontractor shall comply with all applicable OSHA regulations... implement and maintain a comprehensive safety programme

**Expected Classification:** ✅
**Expected Action:** FLAG

**Expected Amendment:**

> Consider adding timeline: "Subcontractor shall submit its site-specific safety plan for Contractor review within 10 days of Notice to Proceed"

**Key Elements:**

- Safety plan submission timeline
- review process

**Rationale Must Include:**

Minor enhancement; formalises safety plan approval process

---


## 6. Subcontract_Landscaping_Omega

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 6.D | 2 | T1 | Red Flag | AMEND |
| 2 | Article 6.4 | 7 | T1 | Red Flag | DELETE |
| 3 | Article 7.1 | 8 | T1 | Red Flag | AMEND |
| 4 | Article 11.1 | 13 | T1 | Red Flag | DELETE |

### Issue 1 | Article 6.D | T1

**Non-standard Insurance**

**Playbook Rule:** 2
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Pollution, Cyber, Railroad Protective Liability

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove non-standard coverage requirements; retain standard CGL, Auto, Umbrella per playbook

**Key Elements:**

- Flags non-standard coverage requirement

**Rationale Must Include:**

Identifies specific coverage type; references rule 2

---

### Issue 2 | Article 6.4 | T1

**Alternate Employer**

**Playbook Rule:** 7
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Alternate Employer Endorsement (WC 00 03 01)

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ARTICLE 6.4]

**Key Elements:**

- Identifies AEE requirement

**Rationale Must Include:**

Notes WC endorsement requirement; references rule 7 prohibition

---

### Issue 3 | Article 7.1 | T1

**Liquidated Damages**

**Playbook Rule:** 8
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> $2,000 per calendar day

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> pass-through only, proportionate to fault

**Key Elements:**

- Flags direct LD exposure

**Rationale Must Include:**

Cites daily rate; references pass-through only standard

---

### Issue 4 | Article 11.1 | T1

**Most Favored Nations**

**Playbook Rule:** 13
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Most Favored Nations

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ENTIRE ARTICLE 11]

**Key Elements:**

- Flags MFN provision

**Rationale Must Include:**

Identifies MFN language; references rule 13

---


## 7. Subcontract_Masonry_Sterling

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 5.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Article 6.3 | 4 | T1 | Red Flag | AMEND |
| 3 | Article 9 | 10 | T1 | Red Flag | DELETE |
| 4 | Article 10 | 11 | T1 | Red Flag | DELETE |

### Issue 1 | Article 5.1 | T1

**Indemnification**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> regardless of the circumstances giving rise to such claims

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> to extent caused by Subcontractor's negligence

**Key Elements:**

- Identifies broad-form indemnification

**Rationale Must Include:**

Cites negligence trigger; references proportionate fault standard

---

### Issue 2 | Article 6.3 | T1

**Insurance Documentation**

**Playbook Rule:** 4
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> full and complete certified copies of all policies

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Certificates of Insurance and endorsements

**Key Elements:**

- Flags excessive documentation requirement

**Rationale Must Include:**

Notes policy copy requirement; references certificate standard

---

### Issue 3 | Article 9 | T1

**Personal Guarantee**

**Playbook Rule:** 10
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> This guarantee shall remain in effect notwithstanding any modification, extension, or forbearance granted to Subcontractor

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ENTIRE ARTICLE 9]

**Key Elements:**

- Identifies personal guarantee

**Rationale Must Include:**

Notes guarantee language; references absolute prohibition

---

### Issue 4 | Article 10 | T1

**Union/PLA**

**Playbook Rule:** 11
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Project Labor Agreement

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ENTIRE ARTICLE 10]

**Key Elements:**

- Flags union/PLA requirement

**Rationale Must Include:**

Identifies PLA/LOA requirement; references rule 11

---


## 8. Subcontract_Millwork_Crest

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 6.D | 2 | T1 | Red Flag | AMEND |
| 2 | Article 6.G | 5 | T1 | Red Flag | AMEND |
| 3 | Article 9.1 | 11 | T1 | Red Flag | DELETE |
| 4 | Article 10.1 | 14 | T1 | Red Flag | DELETE |

### Issue 1 | Article 6.D | T1

**Non-standard Insurance**

**Playbook Rule:** 2
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Railroad Protective Liability

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove non-standard coverage requirements; retain standard CGL, Auto, Umbrella per playbook

**Key Elements:**

- Flags non-standard coverage requirement

**Rationale Must Include:**

Identifies specific coverage type; references rule 2

---

### Issue 2 | Article 6.G | T1

**Professional Liability**

**Playbook Rule:** 5
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> $3,500,000 per claim / $7,000,000 aggregate

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> $2,000,000 per claim / $3,000,000 aggregate

**Key Elements:**

- Flags excessive PL limits

**Rationale Must Include:**

Cites specific limits; references $2M/$3M maximum

---

### Issue 3 | Article 9.1 | T1

**Union/PLA**

**Playbook Rule:** 11
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Project Labor Agreement and Letter of Assent

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ARTICLE 10]

**Key Elements:**

- Flags union/PLA requirement

**Rationale Must Include:**

Identifies PLA/LOA requirement; references rule 11

---

### Issue 4 | Article 10.1 | T1

**Vaccination**

**Playbook Rule:** 14
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> proof of vaccination against COVID-19

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ARTICLE 12.1]

**Key Elements:**

- Flags mandatory vaccination

**Rationale Must Include:**

Identifies vaccination requirement; references rule 14

---


## 9. Subcontract_Sitework_Frontier

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 5.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Article 6.3 | 4 | T1 | Red Flag | AMEND |
| 3 | Article 7.2 | 9 | T1 | Red Flag | AMEND |
| 4 | Article 9.1 | 10 | T1 | Red Flag | DELETE |

### Issue 1 | Article 5.1 | T1

**Indemnification**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> including negligence of any Indemnified Party

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> to extent caused by Subcontractor's negligence

**Key Elements:**

- Identifies broad-form indemnification

**Rationale Must Include:**

Cites negligence trigger; references proportionate fault standard

---

### Issue 2 | Article 6.3 | T1

**Insurance Documentation**

**Playbook Rule:** 4
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> complete certified copies of all policies

**Expected Classification:** ⚠️
**Expected Action:** AMEND

**Expected Amendment:**

> Certificates of Insurance and endorsements

**Key Elements:**

- Flags excessive documentation requirement

**Rationale Must Include:**

Notes policy copy requirement; references certificate standard

---

### Issue 3 | Article 7.2 | T1

**Consequential Damages**

**Playbook Rule:** 9
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> special damages, punitive damages

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Mutual waiver of consequential damages

**Key Elements:**

- Flags one-sided consequential exposure

**Rationale Must Include:**

Identifies damage types; references mutual waiver

---

### Issue 4 | Article 9.1 | T1

**Personal Guarantee**

**Playbook Rule:** 10
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> unconditionally and irrevocably guarantee

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ENTIRE ARTICLE 9]

**Key Elements:**

- Identifies personal guarantee

**Rationale Must Include:**

Notes guarantee language; references absolute prohibition

---


## 10. Subcontract_Waterproofing_Atlas

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | Article 5.1 | 1 | T1 | Red Flag | AMEND |
| 2 | Article 6.D | 2 | T1 | Red Flag | AMEND |
| 3 | Article 6.4 | 7 | T1 | Red Flag | DELETE |
| 4 | Article 10.1 | 11 | T1 | Red Flag | DELETE |

### Issue 1 | Article 5.1 | T1

**Indemnification**

**Playbook Rule:** 1
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> caused by any act or omission of Contractor

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> to extent caused by Subcontractor's negligence

**Key Elements:**

- Identifies broad-form indemnification

**Rationale Must Include:**

Cites negligence trigger; references proportionate fault standard

---

### Issue 2 | Article 6.D | T1

**Non-standard Insurance**

**Playbook Rule:** 2
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Cyber Liability Insurance

**Expected Classification:** ❌
**Expected Action:** AMEND

**Expected Amendment:**

> Remove non-standard coverage requirements; retain standard CGL, Auto, Umbrella per playbook

**Key Elements:**

- Flags non-standard coverage requirement

**Rationale Must Include:**

Identifies specific coverage type; references rule 2

---

### Issue 3 | Article 6.4 | T1

**Alternate Employer**

**Playbook Rule:** 7
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Alternate Employer Endorsement

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ARTICLE 6.4]

**Key Elements:**

- Identifies AEE requirement

**Rationale Must Include:**

Notes WC endorsement requirement; references rule 7 prohibition

---

### Issue 4 | Article 10.1 | T1

**Union/PLA**

**Playbook Rule:** 11
**Playbook Standard:** Red Flag

**Trigger Phrase:**

> Letter of Assent

**Expected Classification:** ❌
**Expected Action:** DELETE

**Expected Amendment:**

> [DELETE ARTICLE 10]

**Key Elements:**

- Flags union/PLA requirement

**Rationale Must Include:**

Identifies PLA/LOA requirement; references rule 11

---


## 11. TOTALS

| ID | Location | Rule | Tier | Standard | Action |
|----| ---------|------|------|----------|--------|
| 1 | N/A | None | T? | N/A | None |

### Issue 1 | N/A | T?

**None**

**Playbook Rule:** None
**Playbook Standard:** Unknown

**Expected Classification:** None
**Expected Action:** None

---


# Appendix: Action Reference

## AMEND vs DELETE

| Action | When to Use | Examples |
|--------|-------------|----------|
| **AMEND** | Modify clause per playbook guidance (most common) | CI definition, indemnification, insurance limits |
| **DELETE** | Playbook prohibits clause type entirely (rare) | Non-Compete, Personal Guarantee, Union/PLA |
| **ADD** | Missing required protection | Missing carve-out, missing cap |
| **FLAG** | Escalate for commercial review | Jurisdiction issues |

**Note:** DELETE is reserved for absolute prohibitions only. Most issues require AMEND — removing the trigger phrase and proposing compliant language.

---

## Red Flag Gate

The Red Flag Gate ensures critical issues are never missed.

| Red Flags Missed | Result |
|------------------|--------|
| 0 | Gate PASS |
| 1-2 | Gate MARGINAL |
| 3+ | Gate FAIL (automatic) |

---

*Ground Truth Version 1.0 | Generated 2026-01-27*
