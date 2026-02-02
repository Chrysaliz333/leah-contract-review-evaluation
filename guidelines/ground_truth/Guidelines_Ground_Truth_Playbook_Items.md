# Guidelines Ground Truth: Playbook-Based Evaluation

**Version:** 1.0
**Date:** January 2026
**Author:** Liz
**Status:** Active

---

## Introduction

This document explains the Ground Truth (GT) for **Guidelines mode** — evaluating Leah's ability to apply playbook rules while exercising independent legal judgment. The playbook provides qualifying context on top of full Freeform analysis.

### Purpose

Guidelines evaluation tests whether Leah can:
1. Identify all risks a competent lawyer would find (Freeform baseline)
2. Apply specific playbook rules when triggers are present
3. Propose amendments aligned with playbook position hierarchy
4. Provide rationale linking risks to playbook guidance

### Key Principle: Playbook as Qualifying Context

The playbook doesn't limit what Leah should find — it provides specific instructions for handling certain issues. Leah must identify all Freeform-level risks; playbook issues receive additional scoring on amendment alignment.

| Aspect | Freeform | Guidelines |
|--------|----------|------------|
| Context document | None | Playbook |
| Risk identification | Leah's judgment | Judgment + playbook triggers |
| Amendment language | Leah generates | Playbook provides guidance |
| Position hierarchy | Leah determines | Playbook defines (GS → FB1 → FB2 → RF) |

---

## Playbook Position Hierarchy

The playbook defines acceptable positions in descending order:

| Position | Code | Meaning | Action Required |
|----------|------|---------|-----------------|
| **Gold Standard** | GS | Ideal position | None (compliant) |
| **Fallback 1** | FB1 | Acceptable compromise | FLAG for awareness |
| **Fallback 2** | FB2 | Minimum acceptable | FLAG, negotiate if possible |
| **Red Flag** | RF | **Unacceptable** | **AMEND or DELETE required** |

**Critical:** Red Flag misses trigger the gate. Missing a Red Flag means Leah failed to identify a critical issue that the playbook explicitly prohibits.

---

## Methodology

### Scoring Dimensions

| Dimension | T1 (RF) | T2 (FB) | T3 (GS/Minor) |
|-----------|---------|---------|---------------|
| Detection | 1 | 1 | 0.5 |
| Location | 1 | 1 | — |
| Action | 1 | 1 | — |
| Amendment | 2 | 1 | — |
| Rationale | 2 | 1 | — |
| **Maximum** | **7** | **5** | **0.5** |

### Dimension Criteria

| Dimension | Full Credit | Partial (Half) | Zero |
|-----------|-------------|----------------|------|
| **Detection** | Issue flagged | — | Missed |
| **Location** | Exact section reference | Correct article, wrong subsection | Wrong or not specified |
| **Action** | Correct per playbook | — | Wrong action |
| **Amendment** | Aligns with playbook guidance | Partial/missing elements | Wrong or contradicts playbook |
| **Rationale** | Cites rule + risk + trigger | Weak linkage | Wrong clause or missing |

### Actions

| Action | When to Use |
|--------|-------------|
| **AMEND** | Modify clause per playbook guidance (most common) |
| **DELETE** | Playbook prohibits clause type entirely (rare) |
| **ADD** | Missing required protection |
| **FLAG** | Escalate for commercial review |

**Note:** DELETE is reserved for absolute prohibitions only (e.g., Non-Compete, Personal Guarantee).

### Pass Criteria

| Result | Criteria |
|--------|----------|
| **PASS** | ≥70% AND all Red Flags detected |
| **MARGINAL** | 50-69% OR 1-2 Red Flag misses |
| **FAIL** | <50% OR 3+ Red Flag misses |

---

## Contract Sets

### NDA Contracts (10)

**Representing Party:** Receiving Party
**Playbook:** NDA Receiving Party Playbook

| Contract | Description |
|----------|-------------|
| NDA_TechPartners_Bilateral | Technology partnership NDA |
| NDA_Meridian_Unilateral | One-way disclosure |
| NDA_GlobalPharm_Research | Pharmaceutical research NDA |
| NDA_Vertex_Strategic | Strategic partnership NDA |
| NDA_Quantum_JointVenture | JV pre-negotiation NDA |
| NDA_Sterling_Mutual | Mutual NDA |
| NDA_Cascade_Supplier | Supplier qualification NDA |
| NDA_Nexus_Investment | Investment due diligence NDA |
| NDA_Atlas_Employment | Employment-related NDA |
| NDA_Vanguard_Technical | Technical evaluation NDA |

### Subcontract Contracts (10)

**Representing Party:** Subcontractor
**Playbook:** Subcontractor Playbook

| Contract | Description |
|----------|-------------|
| Subcontract_HVAC_Titan | HVAC installation |
| Subcontract_FireProtection_Apex | Fire protection systems |
| Subcontract_Masonry_Sterling | Masonry work |
| Subcontract_Landscaping_Omega | Landscaping services |
| Subcontract_Demolition_Prime | Demolition services |
| Subcontract_Flooring_Nexus | Flooring installation |
| Subcontract_Waterproofing_Atlas | Waterproofing systems |
| Subcontract_Curtainwall_Vector | Curtainwall installation |
| Subcontract_Sitework_Frontier | Sitework and grading |
| Subcontract_Millwork_Crest | Custom millwork |

---

## NDA Playbook Rules

### Summary Table

| Rule | Clause Type | Red Flag Trigger | Action |
|------|-------------|------------------|--------|
| 1 | CI Definition | "whether or not marked", residual knowledge, public info | AMEND |
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

### Rule Details

#### Rule 1: Confidential Information Definition

**Red Flag Triggers:**
- "whether or not marked as confidential"
- "regardless of whether publicly available"
- "including information retained in unaided memory"
- "general skills, knowledge, and experience"
- Oral disclosures without confirmation requirement

**Gold Standard:** CI must be marked "Confidential" or, if oral, confirmed in writing within 10 days.

**Expected Amendment:** Remove overbroad language; require written marking or oral confirmation.

---

#### Rule 2: Reciprocity / Mutual Obligations

**Red Flag Triggers:**
- "shall apply solely to the Receiving Party"
- "the receiving party shall [...]" (unilateral)
- Asymmetric obligations structure

**Gold Standard:** Mutual obligations — "Each party receiving CI shall..."

**Expected Amendment:** Convert to mutual structure.

---

#### Rule 3: Compelled Disclosure

**Red Flag Triggers:**
- "under no circumstances"
- "shall not disclose under any circumstances"
- "shall not make any disclosure whatsoever"

**Gold Standard:** May disclose if required by law, provided party gives prior written notice (where permitted) to enable protective order.

**Expected Amendment:** Add legal compulsion carve-out with notice requirement.

---

#### Rule 4: Term and Survival

**Red Flag Triggers:**
- "shall survive in perpetuity"
- "indefinitely following termination"
- "ten (10) years"
- "so long as the information retains its confidential character"

**Gold Standard:** Obligations survive for 3 years following termination.

**Expected Amendment:** Reduce survival to 3 years.

---

#### Rule 5: Non-Solicitation

**Red Flag Triggers:**
- Period exceeding 12 months
- "twenty-four (24) months"
- "thirty-six (36) months"
- "eighteen (18) months"

**Gold Standard:** Maximum 12 months from termination/expiration.

**Expected Amendment:** Reduce to 12 months.

---

#### Rule 6: Non-Compete

**Red Flag Triggers:**
- Any non-compete clause in an NDA
- "shall not compete"
- "shall not provide similar services to competitors"
- Competitive restrictions beyond solicitation

**Gold Standard:** No non-compete clause. Delete entirely.

**Expected Amendment:** [DELETE ENTIRE SECTION]

---

#### Rule 7: Return and Destruction

**Red Flag Triggers:**
- "destroy all copies without exception"
- "destroy all copies, notes, derivatives without retention"
- "no copies may be retained for any purpose"

**Gold Standard:** May retain archival copy for legal/compliance purposes; backups on disaster recovery systems exempt if not accessed.

**Expected Amendment:** Add retention carve-out for archival and automatic backups.

---

#### Rule 8: Injunctive Relief / Equitable Relief

**Red Flag Triggers:**
- "without the necessity of posting any bond"
- "without posting bond or security"
- "waives any requirement for bond"

**Gold Standard:** Injunctive relief available; no bond waiver.

**Expected Amendment:** Remove bond waiver language; retain injunctive relief provision.

---

#### Rule 9: Indemnification

**Red Flag Triggers:**
- "whether or not caused by the negligence"
- "regardless of the fault or negligence"
- "regardless of fault"
- "fully indemnify and hold harmless" (broad-form)

**Gold Standard:** Proportionate fault — "to the extent caused by the indemnifying party's breach or negligence"

**Expected Amendment:** Remove broad-form trigger; add proportionate fault qualifier.

---

#### Rule 10: Assignment

**Red Flag Triggers:**
- "may freely assign without consent"
- "may assign at its sole discretion"
- Asymmetric assignment rights

**Gold Standard:** Neither party may assign without prior written consent, not unreasonably withheld.

**Expected Amendment:** Make assignment restriction mutual with reasonableness standard.

---

#### Rule 11: Governing Law / Jurisdiction

**Red Flag Triggers:**
- "courts of the Cayman Islands"
- "exclusive jurisdiction of Singapore"
- "courts of Dubai, UAE"
- Offshore or distant jurisdiction with no party nexus

**Gold Standard:** Jurisdiction where a party has nexus (principal place of business).

**Expected Amendment:** Change to jurisdiction with party nexus. FLAG for commercial review.

---

#### Rule 12: Limitation of Liability

**Red Flag Triggers:**
- "unlimited liability"
- "all damages without limitation"
- "monetary damages may not provide adequate compensation" (no cap)
- "fully liable for all damages, losses, and expenses"

**Gold Standard:** Mutual liability cap (typically 1-2x fees or defined amount).

**Expected Amendment:** Add mutual liability cap.

---

## NDA Ground Truth Items (45 items)

### NDA_TechPartners_Bilateral

#### TechPartnersBilateral_01: CI Definition (T1)

**Clause:** Section 1.1 — CI Definition
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "whether or not marked as confidential"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove 'whether or not marked as confidential' and require written marking

**Key Elements:**
- Identifies overbroad CI language

**Rationale Must Include:**
- Cites specific trigger phrase from playbook rule 1

---

#### TechPartnersBilateral_02: Term and Survival (T1)

**Clause:** Section 4.1 — Term and Survival
**Playbook Rule:** 4
**Playbook Standard:** Red Flag
**Trigger Phrase:** "shall survive in perpetuity"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** three (3) years following termination

**Key Elements:**
- Identifies excessive survival period

**Rationale Must Include:**
- Cites specific duration
- References 3-year standard from rule 4

---

#### TechPartnersBilateral_03: Non-Solicitation (T1)

**Clause:** Section 7.1 — Non-Solicitation
**Playbook Rule:** 5
**Playbook Standard:** Red Flag
**Trigger Phrase:** "twenty-four (24) months"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** twelve (12) months

**Key Elements:**
- Flags period exceeding 12 months

**Rationale Must Include:**
- Cites specific duration
- References 12-month maximum

---

#### TechPartnersBilateral_04: Indemnification (T1)

**Clause:** Section 8.1 — Indemnification
**Playbook Rule:** 9
**Playbook Standard:** Red Flag
**Trigger Phrase:** "whether or not caused by the negligence"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove 'whether or not caused by the negligence' and add proportionate fault qualifier

**Key Elements:**
- Flags broad-form trigger

**Rationale Must Include:**
- Identifies negligence/fault language
- References rule 9

---

### NDA_Meridian_Unilateral

#### MeridianUnilateral_05: Reciprocity (T1)

**Clause:** Section 2.1 — Reciprocity
**Playbook Rule:** 2
**Playbook Standard:** Red Flag
**Trigger Phrase:** "shall apply solely to the Receiving Party"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Each party receiving CI shall

**Key Elements:**
- Flags unilateral obligations

**Rationale Must Include:**
- References playbook rule 2
- Explains mutual obligation requirement

---

#### MeridianUnilateral_06: Compelled Disclosure (T1)

**Clause:** Section 3.2 — Compelled Disclosure
**Playbook Rule:** 3
**Playbook Standard:** Red Flag
**Trigger Phrase:** "under no circumstances"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** may disclose if required by law, with notice

**Key Elements:**
- Flags absolute disclosure prohibition

**Rationale Must Include:**
- Cites "under no circumstances" language
- References rule 3

---

#### MeridianUnilateral_07: Non-Compete (T1)

**Clause:** Section 7.2 — Non-Compete
**Playbook Rule:** 6
**Playbook Standard:** Red Flag
**Trigger Phrase:** "shall not compete"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE SECTION]

**Key Elements:**
- Identifies non-compete in NDA

**Rationale Must Include:**
- Notes non-compete unacceptable per rule 6

---

#### MeridianUnilateral_08: Limitation of Liability (T1)

**Clause:** Section 8.3 — Limitation of Liability
**Playbook Rule:** 12
**Playbook Standard:** Red Flag
**Trigger Phrase:** "unlimited liability"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Add mutual liability cap

**Key Elements:**
- Flags unlimited/missing liability cap

**Rationale Must Include:**
- Identifies cap issue
- Recommends mutual cap

---

### NDA_GlobalPharm_Research

#### GlobalPharmResearch_09: CI Definition (T1)

**Clause:** Section 1.1 — CI Definition
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "regardless of whether publicly available"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove 'whether or not marked as confidential' and require written marking

**Key Elements:**
- Identifies overbroad CI language

**Rationale Must Include:**
- Cites specific trigger phrase from playbook rule 1

---

#### GlobalPharmResearch_10: Return and Destruction (T1)

**Clause:** Section 5.1 — Return and Destruction
**Playbook Rule:** 7
**Playbook Standard:** Red Flag
**Trigger Phrase:** "destroy all copies without exception"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** may retain archival copy + backups

**Key Elements:**
- Flags no retention exception

**Rationale Must Include:**
- References archival copy requirement from rule 7

---

#### GlobalPharmResearch_11: Injunctive Relief (T1)

**Clause:** Section 8.2 — Injunctive Relief
**Playbook Rule:** 8
**Playbook Standard:** Red Flag
**Trigger Phrase:** "without the necessity of posting any bond"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove bond waiver language; retain injunctive relief provision

**Key Elements:**
- Identifies bond waiver

**Rationale Must Include:**
- Cites bond waiver language
- References rule 8

---

#### GlobalPharmResearch_12: Governing Law (T1)

**Clause:** Section 10.1 — Governing Law
**Playbook Rule:** 11
**Playbook Standard:** Red Flag
**Trigger Phrase:** "courts of the Cayman Islands"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Jurisdiction with party nexus

**Key Elements:**
- Flags offshore/distant jurisdiction

**Rationale Must Include:**
- Identifies jurisdiction issue
- Recommends nexus-based forum

---

### NDA_Vertex_Strategic

#### VertexStrategic_13: Reciprocity (T1)

**Clause:** Section 2.1 — Reciprocity
**Playbook Rule:** 2
**Playbook Standard:** Red Flag
**Trigger Phrase:** "shall apply solely to the Receiving Party"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Each party receiving CI shall

---

#### VertexStrategic_14: Term and Survival (T1)

**Clause:** Section 4.1 — Term and Survival
**Playbook Rule:** 4
**Playbook Standard:** Red Flag
**Trigger Phrase:** "indefinitely following termination"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** three (3) years following termination

---

#### VertexStrategic_15: Assignment (T1)

**Clause:** Section 9.2 — Assignment
**Playbook Rule:** 10
**Playbook Standard:** Red Flag
**Trigger Phrase:** "may freely assign without consent"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Neither party may assign without consent

---

#### VertexStrategic_16: Limitation of Liability (T1)

**Clause:** Section 8.3 — Limitation of Liability
**Playbook Rule:** 12
**Playbook Standard:** Red Flag
**Trigger Phrase:** "all damages without limitation"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Add mutual liability cap

---

### NDA_Quantum_JointVenture

#### QuantumJointVenture_17: CI Definition (T1)

**Clause:** Section 1.1 — CI Definition
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "including information retained in unaided memory"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove residual knowledge clause or add reasonable use limitations

---

#### QuantumJointVenture_18: Compelled Disclosure (T1)

**Clause:** Section 3.2 — Compelled Disclosure
**Playbook Rule:** 3
**Playbook Standard:** Red Flag
**Trigger Phrase:** "shall not disclose under any circumstances"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** may disclose if required by law, with notice

---

#### QuantumJointVenture_19: Non-Solicitation (T1)

**Clause:** Section 7.1 — Non-Solicitation
**Playbook Rule:** 5
**Playbook Standard:** Red Flag
**Trigger Phrase:** "thirty-six (36) months"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** twelve (12) months

---

#### QuantumJointVenture_20: Injunctive Relief (T1)

**Clause:** Section 8.2 — Injunctive Relief
**Playbook Rule:** 8
**Playbook Standard:** Red Flag
**Trigger Phrase:** "without posting bond or security"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove bond waiver language; retain injunctive relief provision

---

### NDA_Sterling_Mutual

#### SterlingMutual_21: Term and Survival (T1)

**Clause:** Section 4.1 — Term and Survival
**Playbook Rule:** 4
**Playbook Standard:** Red Flag
**Trigger Phrase:** "ten (10) years form such expiration"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** three (3) years following termination

---

#### SterlingMutual_22: Non-Compete (T1)

**Clause:** Section 7.2 — Non-Compete
**Playbook Rule:** 6
**Playbook Standard:** Red Flag
**Trigger Phrase:** "for two (2) years thereafter"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE SECTION]

---

#### SterlingMutual_23: Indemnification (T1)

**Clause:** Section 8.1 — Indemnification
**Playbook Rule:** 9
**Playbook Standard:** Red Flag
**Trigger Phrase:** "regardless of the fault or negligence"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove broad-form trigger and add proportionate fault qualifier

---

#### SterlingMutual_24: Governing Law (T1)

**Clause:** Section 10.1 — Governing Law
**Playbook Rule:** 11
**Playbook Standard:** Red Flag
**Trigger Phrase:** "exclusive jurisdiction of Singapore"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Jurisdiction with party nexus

---

### NDA_Cascade_Supplier

#### CascadeSupplier_25: CI Definition (T1)

**Clause:** Section 1.1 — CI Definition
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Information may be disclosed in any form or medium, whether tangible or intangible, written, oral, visual, or electronic."

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Oral disclosures confirmed in writing within 10 days

---

#### CascadeSupplier_26: Reciprocity (T1)

**Clause:** Section 2.1 — Reciprocity
**Playbook Rule:** 2
**Playbook Standard:** Red Flag
**Trigger Phrase:** "the receiving party shall [...]"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Each party receiving CI shall

---

#### CascadeSupplier_27: Return and Destruction (T1)

**Clause:** Section 5.1 — Return and Destruction
**Playbook Rule:** 7
**Playbook Standard:** Red Flag
**Trigger Phrase:** "destroy all copies, notes, derivatives without retention"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** may retain archival copy + backups

---

#### CascadeSupplier_28: Assignment (T1)

**Clause:** Section 9.2 — Assignment
**Playbook Rule:** 10
**Playbook Standard:** Red Flag
**Trigger Phrase:** "may assign at its sole discretion"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Neither party may assign without consent

---

### NDA_Nexus_Investment

#### NexusInvestment_29: Compelled Disclosure (T1)

**Clause:** Section 3.2 — Compelled Disclosure
**Playbook Rule:** 3
**Playbook Standard:** Red Flag
**Trigger Phrase:** "shall not make any disclosure whatsoever"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** may disclose if required by law, with notice

---

#### NexusInvestment_30: Non-Solicitation (T1)

**Clause:** Section 7.1 — Non-Solicitation
**Playbook Rule:** 5
**Playbook Standard:** Red Flag
**Trigger Phrase:** "eighteen (18) months following"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** twelve (12) months

---

#### NexusInvestment_31: Injunctive Relief (T1)

**Clause:** Section 8.2 — Injunctive Relief
**Playbook Rule:** 8
**Playbook Standard:** Red Flag
**Trigger Phrase:** "waives any requirement for bond"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove bond waiver language; retain injunctive relief provision

---

#### NexusInvestment_32: Limitation of Liability (T1)

**Clause:** Section 8.3 — Limitation of Liability
**Playbook Rule:** 12
**Playbook Standard:** Red Flag
**Trigger Phrase:** "monetary damages may not provide adequate compensation"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Add mutual liability cap

---

### NDA_Atlas_Employment

#### AtlasEmployment_33: CI Definition (T1)

**Clause:** Section 1.1 — CI Definition
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "general skills, knowledge, and experience"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove 'whether or not marked as confidential' and require written marking

---

#### AtlasEmployment_34: Term and Survival (T1)

**Clause:** Section 4.2 — Term and Survival
**Playbook Rule:** 4
**Playbook Standard:** Red Flag
**Trigger Phrase:** "shall remain in full force and effect for so long as the information retains its confidential character"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** three (3) years following termination

---

#### AtlasEmployment_35: Non-Compete (T1)

**Clause:** Section 7.2 — Non-Compete
**Playbook Rule:** 6
**Playbook Standard:** Red Flag
**Trigger Phrase:** "shall not provide similar services to competitors"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE SECTION]

---

#### AtlasEmployment_36: Indemnification (T1)

**Clause:** Section 8.1 — Indemnification
**Playbook Rule:** 9
**Playbook Standard:** Red Flag
**Trigger Phrase:** "fully indemnify and hold harmless"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove broad-form trigger or add fault qualifier per Gold Standard

---

### NDA_Vanguard_Technical

#### VanguardTechnical_37: Reciprocity (T1)

**Clause:** Section 2.1 — Reciprocity
**Playbook Rule:** 2
**Playbook Standard:** Red Flag
**Trigger Phrase:** "This Agreement sets forth the obligations of the Receiving Party with respect to the Confidential Information disclosed by the Disclosing Party hereunder."

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Each party receiving CI shall

---

#### VanguardTechnical_38: Return and Destruction (T1)

**Clause:** Section 5.1 — Return and Destruction
**Playbook Rule:** 7
**Playbook Standard:** Red Flag
**Trigger Phrase:** "no copies may be retained for any purpose"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** may retain archival copy + backups

---

#### VanguardTechnical_39: Governing Law (T1)

**Clause:** Section 10.1 — Governing Law
**Playbook Rule:** 11
**Playbook Standard:** Red Flag
**Trigger Phrase:** "courts of Dubai, UAE"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Jurisdiction with party nexus

---

#### VanguardTechnical_40: Limitation of Liability (T1)

**Clause:** Section 8.3 — Limitation of Liability
**Playbook Rule:** 12
**Playbook Standard:** Red Flag
**Trigger Phrase:** "The Receiving Party shall be fully liable for all damages, losses, and expenses arising from or related to any breach of its obligations under this Agreement."

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Add mutual liability cap

---

### T2/T3 Items (NDA_TechPartners_Bilateral)

#### TechPartnersBilateral_41: Compelled Disclosure (T2)

**Clause:** Sections 3.1-3.2 — Compelled Disclosure
**Playbook Rule:** 3
**Playbook Standard:** Fallback 1
**Trigger Phrase:** "may disclose... if required by applicable law (3.1) with prompt notice (3.2) but no prior notice before disclosure"

**Expected Classification:** ⚠️
**Expected Action:** FLAG
**Expected Amendment:** Add to Section 3.1: "provided that the Receiving Party shall, where legally permitted, give prior written notice to the Disclosing Party before such disclosure"

**Key Elements:**
- Prior notice requirement where legally permitted
- Opportunity for protective order before disclosure

---

#### TechPartnersBilateral_42: Assignment (T2)

**Clause:** Section 9.2 — Assignment
**Playbook Rule:** 10
**Playbook Standard:** Fallback 1
**Trigger Phrase:** "Neither party may assign... without prior written consent"

**Expected Classification:** ⚠️
**Expected Action:** FLAG
**Expected Amendment:** Add: "which consent shall not be unreasonably withheld or delayed"

**Key Elements:**
- Reasonableness standard for consent
- Prevents arbitrary refusal

---

#### TechPartnersBilateral_43: CI Carve-Out Evidence (T3)

**Clause:** Section 1.2 — CI Carve-Out Evidence
**Playbook Rule:** 1
**Playbook Standard:** Near Gold
**Trigger Phrase:** "was rightfully in possession... is rightfully obtained... is independently developed"

**Expected Classification:** ✅
**Expected Action:** FLAG
**Expected Amendment:** Consider adding "as evidenced by written records" to prior knowledge and independent development carve-outs

**Key Elements:**
- Evidence requirement clarification

---

#### TechPartnersBilateral_44: Standard of Care (T3)

**Clause:** Section 2.1(d) — Standard of Care
**Playbook Rule:** 2
**Playbook Standard:** Gold Standard
**Trigger Phrase:** "at least the same degree of care used to protect its own confidential information"

**Expected Classification:** ✅
**Expected Action:** FLAG
**Expected Amendment:** Consider adding "but in no event less than reasonable care"

**Key Elements:**
- Minimum care floor

---

#### TechPartnersBilateral_45: No Licence (T3)

**Clause:** Section 6.1 — No Licence
**Playbook Rule:** N/A
**Playbook Standard:** Gold Standard
**Trigger Phrase:** "Nothing in this Agreement grants any licence or rights to any intellectual property"

**Expected Classification:** ✅
**Expected Action:** FLAG
**Expected Amendment:** Consider adding: "All Confidential Information and any intellectual property rights therein remain the sole property of the Disclosing Party"

**Key Elements:**
- Explicit ownership confirmation

---

## Subcontract Playbook Rules

### Summary Table

| Rule | Clause Type | Red Flag Trigger | Action |
|------|-------------|------------------|--------|
| 1 | Indemnification | Broad-form (negligence of Contractor) | AMEND |
| 2 | Non-Standard Insurance | Pollution, Cyber, Railroad Protective | AMEND |
| 3 | Additional Insured Forms | Outdated forms (not CG 2010/2037 04/13) | AMEND |
| 4 | Insurance Documentation | Full policy copies required | AMEND |
| 5 | Professional Liability | >$2M/$3M | AMEND |
| 6 | Umbrella Limits | >$5M | AMEND |
| 7 | Alternate Employer | AEE endorsement required | DELETE |
| 8 | Liquidated Damages | Direct (not pass-through) | AMEND |
| 9 | Consequential Damages | One-sided exposure | AMEND |
| 10 | Personal Guarantee | Any guarantee | DELETE |
| 11 | Union/PLA | PLA or LOA required | DELETE |
| 12 | Non-Compete | Any restriction | DELETE |
| 13 | Most Favored Nations | MFN clause | DELETE |
| 14 | Vaccination | Mandatory vaccination | DELETE |

### Rule Details

#### Rule 1: Indemnification

**Red Flag Triggers:**
- "whether caused in whole or in part by negligence of Contractor"
- "regardless of the circumstances giving rise to such claims"
- "regardless of fault"
- "caused by any act or omission of Contractor"
- "including negligence of any Indemnified Party"

**Gold Standard:** "to extent caused by Subcontractor's negligence" — proportionate fault.

**Expected Amendment:** Remove broad-form language; add proportionate fault standard.

---

#### Rule 2: Non-Standard Insurance

**Red Flag Triggers:**
- Pollution liability
- Cyber liability
- Railroad Protective Liability
- Other non-standard coverage beyond CGL/Auto/WC/Umbrella

**Gold Standard:** Standard coverage only: CGL, Auto, Workers' Comp, Umbrella.

**Expected Amendment:** Remove non-standard coverage requirements.

---

#### Rule 3: Additional Insured Forms

**Red Flag Triggers:**
- CG 2010 11/85
- CG 2010 10/01
- CG 2037 10/01
- Any form earlier than 04/13 edition

**Gold Standard:** CG 2010 04/13 and CG 2037 04/13 (current editions).

**Expected Amendment:** Update to current 04/13 forms.

---

#### Rule 4: Insurance Documentation

**Red Flag Triggers:**
- "full and complete certified copies of all policies"
- "certified copies of all policies and endorsements"
- "complete certified copies of all policies"

**Gold Standard:** Certificates of Insurance and relevant endorsements only.

**Expected Amendment:** Reduce to COIs and endorsements.

---

#### Rule 5: Professional Liability Limits

**Red Flag Triggers:**
- >$2M per claim
- >$3M aggregate
- "$4,000,000 per claim / $8,000,000 aggregate"
- "$5,000,000 per claim / $10,000,000 aggregate"
- "$3,500,000 per claim / $7,000,000 aggregate"

**Gold Standard:** $2M per claim / $3M aggregate maximum.

**Expected Amendment:** Reduce to $2M/$3M.

---

#### Rule 6: Umbrella Limits

**Red Flag Triggers:**
- >$5M
- "$12,000,000"
- "$15,000,000"
- "$20,000,000"

**Gold Standard:** $5M per occurrence and aggregate.

**Expected Amendment:** Reduce to $5M.

---

#### Rule 7: Alternate Employer Endorsement

**Red Flag Triggers:**
- "Alternate Employer Endorsement (WC 00 03 01)"
- "Alternate Employer Endorsement"
- AEE requirement on Workers' Comp

**Gold Standard:** No AEE requirement.

**Expected Amendment:** [DELETE]

---

#### Rule 8: Liquidated Damages

**Red Flag Triggers:**
- Direct LD exposure to subcontractor
- "$3,000 per calendar day"
- "$2,000 per calendar day"
- "$5,000 per calendar day"
- Any daily LD rate not structured as pass-through

**Gold Standard:** Pass-through only, proportionate to fault, capped.

**Expected Amendment:** Convert to pass-through; add proportionate fault; add cap.

---

#### Rule 9: Consequential Damages

**Red Flag Triggers:**
- "including consequential damages, indirect damages"
- "lost profits, loss of use, loss of business opportunity"
- "special damages, punitive damages"
- One-sided consequential exposure

**Gold Standard:** Mutual waiver of consequential damages.

**Expected Amendment:** Add mutual waiver.

---

#### Rule 10: Personal Guarantee

**Red Flag Triggers:**
- Any personal guarantee requirement
- "unconditionally and irrevocably guarantee"
- "This guarantee shall remain in effect notwithstanding any modification"

**Gold Standard:** No personal guarantee.

**Expected Amendment:** [DELETE ENTIRE SECTION]

---

#### Rule 11: Union/PLA

**Red Flag Triggers:**
- "Project Labor Agreement"
- "Letter of Assent"
- PLA/LOA requirement

**Gold Standard:** No union/PLA requirement for open-shop subcontractor.

**Expected Amendment:** [DELETE]

---

#### Rule 12: Non-Compete

**Red Flag Triggers:**
- Any non-compete restriction
- "eighteen (18) months"
- "two (2) years following completion"

**Gold Standard:** No non-compete in subcontract.

**Expected Amendment:** [DELETE ENTIRE SECTION]

---

#### Rule 13: Most Favored Nations

**Red Flag Triggers:**
- "Most Favored Nations"
- MFN pricing clause

**Gold Standard:** No MFN provision.

**Expected Amendment:** [DELETE]

---

#### Rule 14: Vaccination

**Red Flag Triggers:**
- "COVID-19 vaccination"
- "annual influenza vaccination"
- "proof of vaccination"
- Mandatory vaccination requirement

**Gold Standard:** No vaccination mandate.

**Expected Amendment:** [DELETE]

---

## Subcontract Ground Truth Items (45 items)

### Subcontract_HVAC_Titan

#### HVACTitan_01: Indemnification (T1)

**Clause:** Article 5.1 — Indemnification
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "whether caused in whole or in part by negligence of Contractor"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** to extent caused by Subcontractor's negligence

---

#### HVACTitan_02: Umbrella Limits (T1)

**Clause:** Article 6.H — Umbrella Limits
**Playbook Rule:** 6
**Playbook Standard:** Red Flag
**Trigger Phrase:** "$12,000,000"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** $5,000,000 per occurrence and aggregate

---

#### HVACTitan_03: Liquidated Damages (T1)

**Clause:** Article 7.1 — Liquidated Damages
**Playbook Rule:** 8
**Playbook Standard:** Red Flag
**Trigger Phrase:** "$3,000 per calendar day"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** pass-through only, proportionate to fault

---

#### HVACTitan_04: Non-Compete (T1)

**Clause:** Article 11.1 — Non-Compete
**Playbook Rule:** 12
**Playbook Standard:** Red Flag
**Trigger Phrase:** "eighteen (18) months"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE ARTICLE 11]

---

### Subcontract_FireProtection_Apex

#### FireProtectionApex_05: Additional Insured Forms (T1)

**Clause:** Article 6.2 — Additional Insured Forms
**Playbook Rule:** 3
**Playbook Standard:** Red Flag
**Trigger Phrase:** "CG 2010 11/85 and CG 2037 10/01"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** CG 2010 04/13 and CG 2037 04/13

---

#### FireProtectionApex_06: Professional Liability (T1)

**Clause:** Article 6.G — Professional Liability
**Playbook Rule:** 5
**Playbook Standard:** Red Flag
**Trigger Phrase:** "$4,000,000 per claim / $8,000,000 aggregate"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** $2,000,000 per claim / $3,000,000 aggregate

---

#### FireProtectionApex_07: Consequential Damages (T1)

**Clause:** Article 7.2 — Consequential Damages
**Playbook Rule:** 9
**Playbook Standard:** Red Flag
**Trigger Phrase:** "including consequential damages, indirect damages"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Mutual waiver of consequential damages

---

#### FireProtectionApex_08: Vaccination (T1)

**Clause:** Article 12.1 — Vaccination
**Playbook Rule:** 14
**Playbook Standard:** Red Flag
**Trigger Phrase:** "COVID-19 vaccination"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ARTICLE 12.1]

---

### Subcontract_Masonry_Sterling

#### MasonrySterling_09: Indemnification (T1)

**Clause:** Article 5.1 — Indemnification
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "regardless of the circumstances giving rise to such claims"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** to extent caused by Subcontractor's negligence

---

#### MasonrySterling_10: Insurance Documentation (T1)

**Clause:** Article 6.3 — Insurance Documentation
**Playbook Rule:** 4
**Playbook Standard:** Red Flag
**Trigger Phrase:** "full and complete certified copies of all policies"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Certificates of Insurance and endorsements

---

#### MasonrySterling_11: Personal Guarantee (T1)

**Clause:** Article 9 — Personal Guarantee
**Playbook Rule:** 10
**Playbook Standard:** Red Flag
**Trigger Phrase:** "This guarantee shall remain in effect notwithstanding any modification, extension, or forbearance granted to Subcontractor"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE ARTICLE 9]

---

#### MasonrySterling_12: Union/PLA (T1)

**Clause:** Article 10 — Union/PLA
**Playbook Rule:** 11
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Project Labor Agreement"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE ARTICLE 10]

---

### Subcontract_Landscaping_Omega

#### LandscapingOmega_13: Non-standard Insurance (T1)

**Clause:** Article 6.D — Non-standard Insurance
**Playbook Rule:** 2
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Pollution, Cyber, Railroad Protective Liability"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove non-standard coverage requirements; retain standard CGL, Auto, Umbrella per playbook

---

#### LandscapingOmega_14: Alternate Employer (T1)

**Clause:** Article 6.4 — Alternate Employer
**Playbook Rule:** 7
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Alternate Employer Endorsement (WC 00 03 01)"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ARTICLE 6.4]

---

#### LandscapingOmega_15: Liquidated Damages (T1)

**Clause:** Article 7.1 — Liquidated Damages
**Playbook Rule:** 8
**Playbook Standard:** Red Flag
**Trigger Phrase:** "$2,000 per calendar day"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** pass-through only, proportionate to fault

---

#### LandscapingOmega_16: Most Favored Nations (T1)

**Clause:** Article 11.1 — Most Favored Nations
**Playbook Rule:** 13
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Most Favored Nations"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE ARTICLE 11]

---

### Subcontract_Demolition_Prime

#### DemolitionPrime_17: Indemnification (T1)

**Clause:** Article 5.1 — Indemnification
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "regardless of fault"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** to extent caused by Subcontractor's negligence

---

#### DemolitionPrime_18: Additional Insured Forms (T1)

**Clause:** Article 6.2 — Additional Insured Forms
**Playbook Rule:** 3
**Playbook Standard:** Red Flag
**Trigger Phrase:** "CG 2010 10/01 and CG 2037 10/01"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** CG 2010 04/13 and CG 2037 04/13

---

#### DemolitionPrime_19: Umbrella Limits (T1)

**Clause:** Article 6.H — Umbrella Limits
**Playbook Rule:** 6
**Playbook Standard:** Red Flag
**Trigger Phrase:** "$15,000,000"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** $5,000,000 per occurrence and aggregate

---

#### DemolitionPrime_20: Consequential Damages (T1)

**Clause:** Article 7.2 — Consequential Damages
**Playbook Rule:** 9
**Playbook Standard:** Red Flag
**Trigger Phrase:** "lost profits, loss of use, loss of business opportunity"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Mutual waiver of consequential damages

---

### Subcontract_Flooring_Nexus

#### FlooringNexus_21: Insurance Documentation (T1)

**Clause:** Article 6.3 — Insurance Documentation
**Playbook Rule:** 4
**Playbook Standard:** Red Flag
**Trigger Phrase:** "certified copies of all policies and endorsements"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Certificates of Insurance and endorsements

---

#### FlooringNexus_22: Professional Liability (T1)

**Clause:** Article 6.G — Professional Liability
**Playbook Rule:** 5
**Playbook Standard:** Red Flag
**Trigger Phrase:** "$5,000,000 per claim / $10,000,000 aggregate"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** $2,000,000 per claim / $3,000,000 aggregate

---

#### FlooringNexus_23: Personal Guarantee (T1)

**Clause:** Article 9 — Personal Guarantee
**Playbook Rule:** 10
**Playbook Standard:** Red Flag
**Trigger Phrase:** "unconditionally and irrevocably guarantee"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE ARTICLE 9]

---

#### FlooringNexus_24: Vaccination (T1)

**Clause:** Article 12.1 — Vaccination
**Playbook Rule:** 14
**Playbook Standard:** Red Flag
**Trigger Phrase:** "annual influenza vaccination"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ARTICLE 12.1]

---

### Subcontract_Waterproofing_Atlas

#### WaterproofingAtlas_25: Indemnification (T1)

**Clause:** Article 5.1 — Indemnification
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "caused by any act or omission of Contractor"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** to extent caused by Subcontractor's negligence

---

#### WaterproofingAtlas_26: Non-standard Insurance (T1)

**Clause:** Article 6.D — Non-standard Insurance
**Playbook Rule:** 2
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Cyber Liability Insurance"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove non-standard coverage requirements; retain standard CGL, Auto, Umbrella per playbook

---

#### WaterproofingAtlas_27: Alternate Employer (T1)

**Clause:** Article 6.4 — Alternate Employer
**Playbook Rule:** 7
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Alternate Employer Endorsement"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ARTICLE 6.4]

---

#### WaterproofingAtlas_28: Union/PLA (T1)

**Clause:** Article 10.1 — Union/PLA
**Playbook Rule:** 11
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Letter of Assent"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ARTICLE 10]

---

### Subcontract_Curtainwall_Vector

#### CurtainwallVector_29: Additional Insured Forms (T1)

**Clause:** Article 6.2 — Additional Insured Forms
**Playbook Rule:** 3
**Playbook Standard:** Red Flag
**Trigger Phrase:** "CG 2010 11/85"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** CG 2010 04/13 and CG 2037 04/13

---

#### CurtainwallVector_30: Umbrella Limits (T1)

**Clause:** Article 6.H — Umbrella Limits
**Playbook Rule:** 6
**Playbook Standard:** Red Flag
**Trigger Phrase:** "$20,000,000"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** $5,000,000 per occurrence and aggregate

---

#### CurtainwallVector_31: Liquidated Damages (T1)

**Clause:** Article 7.1 — Liquidated Damages
**Playbook Rule:** 8
**Playbook Standard:** Red Flag
**Trigger Phrase:** "$5,000 per calendar day"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** pass-through only, proportionate to fault

---

#### CurtainwallVector_32: Non-Compete (T1)

**Clause:** Article 11.1 — Non-Compete
**Playbook Rule:** 12
**Playbook Standard:** Red Flag
**Trigger Phrase:** "two (2) years following completion"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE ARTICLE 11]

---

### Subcontract_Sitework_Frontier

#### SiteworkFrontier_33: Indemnification (T1)

**Clause:** Article 5.1 — Indemnification
**Playbook Rule:** 1
**Playbook Standard:** Red Flag
**Trigger Phrase:** "including negligence of any Indemnified Party"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** to extent caused by Subcontractor's negligence

---

#### SiteworkFrontier_34: Insurance Documentation (T1)

**Clause:** Article 6.3 — Insurance Documentation
**Playbook Rule:** 4
**Playbook Standard:** Red Flag
**Trigger Phrase:** "complete certified copies of all policies"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** Certificates of Insurance and endorsements

---

#### SiteworkFrontier_35: Consequential Damages (T1)

**Clause:** Article 7.2 — Consequential Damages
**Playbook Rule:** 9
**Playbook Standard:** Red Flag
**Trigger Phrase:** "special damages, punitive damages"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Mutual waiver of consequential damages

---

#### SiteworkFrontier_36: Personal Guarantee (T1)

**Clause:** Article 9.1 — Personal Guarantee
**Playbook Rule:** 10
**Playbook Standard:** Red Flag
**Trigger Phrase:** "unconditionally and irrevocably guarantee"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ENTIRE ARTICLE 9]

---

### Subcontract_Millwork_Crest

#### MillworkCrest_37: Non-standard Insurance (T1)

**Clause:** Article 6.D — Non-standard Insurance
**Playbook Rule:** 2
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Railroad Protective Liability"

**Expected Classification:** ❌
**Expected Action:** AMEND
**Expected Amendment:** Remove non-standard coverage requirements; retain standard CGL, Auto, Umbrella per playbook

---

#### MillworkCrest_38: Professional Liability (T1)

**Clause:** Article 6.G — Professional Liability
**Playbook Rule:** 5
**Playbook Standard:** Red Flag
**Trigger Phrase:** "$3,500,000 per claim / $7,000,000 aggregate"

**Expected Classification:** ⚠️
**Expected Action:** AMEND
**Expected Amendment:** $2,000,000 per claim / $3,000,000 aggregate

---

#### MillworkCrest_39: Union/PLA (T1)

**Clause:** Article 9.1 — Union/PLA
**Playbook Rule:** 11
**Playbook Standard:** Red Flag
**Trigger Phrase:** "Project Labor Agreement and Letter of Assent"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ARTICLE 10]

---

#### MillworkCrest_40: Vaccination (T1)

**Clause:** Article 10.1 — Vaccination
**Playbook Rule:** 14
**Playbook Standard:** Red Flag
**Trigger Phrase:** "proof of vaccination against COVID-19"

**Expected Classification:** ❌
**Expected Action:** DELETE
**Expected Amendment:** [DELETE ARTICLE 12.1]

---

### T2/T3 Items (Subcontract_HVAC_Titan)

#### HVACTitan_41: Payment Terms (T2)

**Clause:** Article 3.2 — Payment Terms
**Playbook Rule:** N/A
**Playbook Standard:** Fallback 2
**Trigger Phrase:** "within forty-five (45) days after receipt"

**Expected Classification:** ⚠️
**Expected Action:** FLAG
**Expected Amendment:** Negotiate to "within thirty (30) days after receipt of a proper application"

**Key Elements:**
- 30-day payment term
- Industry standard timing

---

#### HVACTitan_42: Retainage (T2)

**Clause:** Article 3.2 — Retainage
**Playbook Rule:** N/A
**Playbook Standard:** Fallback 1
**Trigger Phrase:** "less retainage of ten percent (10%)"

**Expected Classification:** ⚠️
**Expected Action:** FLAG
**Expected Amendment:** Negotiate to "less retainage of five percent (5%)" or add retainage reduction at 50% completion

**Key Elements:**
- Reduced retainage percentage
- Or retainage release schedule

---

#### HVACTitan_43: Assignment (T2)

**Clause:** Article 13.3 — Assignment
**Playbook Rule:** N/A
**Playbook Standard:** Fallback 2
**Trigger Phrase:** "Subcontractor shall not assign... without prior written consent"

**Expected Classification:** ⚠️
**Expected Action:** FLAG
**Expected Amendment:** Add mutual restriction: "Neither party may assign this Subcontract without prior written consent, which shall not be unreasonably withheld"

**Key Elements:**
- Mutual assignment restriction
- Reasonableness standard

---

#### HVACTitan_44: Reserved Insurance Sections (T3)

**Clause:** Article 6.D/E/F — Reserved Insurance Sections
**Playbook Rule:** 2
**Playbook Standard:** Gold Standard
**Trigger Phrase:** "D. Reserved. E. Reserved. F. Reserved."

**Expected Classification:** ✅
**Expected Action:** FLAG
**Expected Amendment:** Request clarification: confirm reserved sections will not be populated with additional requirements

**Key Elements:**
- Confirmation no additional coverage will be required

---

#### HVACTitan_45: Safety Plan Submission (T3)

**Clause:** Article 12.1 — Safety Plan Submission
**Playbook Rule:** N/A
**Playbook Standard:** Gold Standard
**Trigger Phrase:** "Subcontractor shall comply with all applicable OSHA regulations... implement and maintain a comprehensive safety programme"

**Expected Classification:** ✅
**Expected Action:** FLAG
**Expected Amendment:** Consider adding timeline: "Subcontractor shall submit its site-specific safety plan for Contractor review within 10 days of Notice to Proceed"

**Key Elements:**
- Safety plan submission timeline
- Review process

---

## Appendix A: GT Summary

### NDA GT Summary

| Tier | Count | Max Points | Description |
|------|-------|------------|-------------|
| T1 (Red Flag) | 40 | 280 | Critical playbook violations |
| T2 (Fallback) | 2 | 10 | Minor deviations |
| T3 (Gold/Minor) | 3 | 1.5 | Near-compliant improvements |
| **Total** | **45** | **291.5** | |

### Subcontract GT Summary

| Tier | Count | Max Points | Description |
|------|-------|------------|-------------|
| T1 (Red Flag) | 40 | 280 | Critical playbook violations |
| T2 (Fallback) | 3 | 15 | Minor deviations |
| T3 (Gold/Minor) | 2 | 1 | Near-compliant improvements |
| **Total** | **45** | **296** | |

---

## Appendix B: Red Flag Gate

The Red Flag Gate ensures that critical issues are never missed. A model that scores well overall but misses Red Flags has failed the fundamental purpose of playbook-guided review.

| Red Flags Missed | Result |
|------------------|--------|
| 0 | Gate PASS |
| 1-2 | Gate MARGINAL (capped at MARGINAL overall) |
| 3+ | Gate FAIL (automatic FAIL) |

---

## Appendix C: Position Hierarchy Quick Reference

| Contract Position | Playbook Position | Action Required |
|-------------------|-------------------|-----------------|
| Matches Gold Standard | GS | None |
| Matches Fallback 1 | FB1 | FLAG |
| Matches Fallback 2 | FB2 | FLAG |
| Matches Red Flag | RF | AMEND or DELETE |
| Worse than Red Flag | Beyond RF | AMEND or DELETE + escalate |

---

*End of Document*
