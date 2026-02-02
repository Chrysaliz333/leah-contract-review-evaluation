# Rules Mode Ground Truth: Deterministic Rules

**Version:** 1.0
**Date:** 2026-01-17
**Author:** Liz
**Status:** Final

---

## Overview

Rules mode evaluates Leah's compliance with deterministic rules. Binary pass/fail: either the rule is followed or it isn't.

| Aspect | Detail |
|--------|--------|
| **Contracts** | 10 NDA + 10 Subcontract |
| **GT Items** | 38 NDA + 40 Subcontract = 78 total |
| **Representing Party** | NDA: Receiving Party, Subcontract: Subcontractor |
| **Rule Source** | CSV files (deterministic triggers) |

---

## GT Summary by Contract Type

### NDA (38 items across 10 contracts)

| Rule Category | Count | Action |
|---------------|-------|--------|
| CI Definition (Unmarked/Residual/Public) | 7 | DELETE |
| Term & Survival (Perpetual/Excessive) | 4 | AMEND |
| Non-Solicitation (>12 months) | 4 | AMEND |
| Non-Compete | 3 | DELETE |
| Compelled Disclosure | 3 | AMEND |
| Indemnification (Broad-form) | 3 | DELETE |
| Return/Destruction | 3 | AMEND |
| Injunctive Relief (Bond Waiver) | 3 | DELETE |
| Limitation of Liability | 4 | FLAG |
| Governing Law (Offshore/Distant) | 3 | FLAG |
| Assignment (Asymmetric) | 2 | AMEND |

### Subcontract (40 items across 10 contracts)

| Rule Category | Count | Action |
|---------------|-------|--------|
| Indemnity (Broad-form) | 6 | AMEND |
| Insurance Limits (Umbrella/Prof Liability) | 6 | AMEND |
| Additional Insured Forms (Outdated) | 4 | AMEND |
| Insurance Documentation | 3 | AMEND |
| Insurance (Non-standard Coverage) | 3 | DELETE |
| Liquidated Damages (Direct) | 3 | AMEND |
| Consequential Damages | 3 | AMEND |
| Personal Guarantee | 3 | DELETE |
| Non-Compete | 3 | DELETE |
| Union/PLA | 3 | DELETE |
| Vaccination | 3 | DELETE |
| Alternate Employer Endorsement | 2 | DELETE |
| MFN | 1 | DELETE |

---

## Key Rule Triggers

### NDA Rules

| # | Rule | Trigger Quote | Action |
|---|------|---------------|--------|
| 1 | CI Definition - Unmarked | "whether or not marked" | DELETE |
| 2 | CI Definition - Residual Knowledge | "residual knowledge", "unaided memory" | DELETE |
| 3 | CI Definition - Public Info | "regardless of whether publicly available" | DELETE |
| 4 | Term/Survival - Perpetual | "in perpetuity", "indefinitely", "forever" | AMEND to 3 years |
| 5 | Non-Solicitation - Excessive | >12 months | AMEND to 12 months |
| 6 | Non-Compete | Any non-compete provision | DELETE entire |
| 7 | Compelled Disclosure | Prohibition on legal disclosure | AMEND to allow |
| 8 | Indemnification - Broad-form | "negligence of Disclosing Party" | DELETE trigger |
| 9 | Return/Destruction | "without exception" | AMEND add retention right |
| 10 | Injunctive Relief | "waives any bond" | DELETE waiver |
| 11 | Limitation of Liability | "unlimited" | FLAG |
| 12 | Governing Law | Offshore/distant jurisdiction | FLAG |

### Subcontract Rules

| # | Rule | Trigger Quote | Action |
|---|------|---------------|--------|
| 1 | Indemnity - Broad-form | "whole or in part by Contractor" | AMEND to proportionate |
| 2 | Umbrella Limits | >$10M | AMEND to $5M |
| 3 | Prof Liability Limits | >$3M per claim | AMEND to $2M/$3M |
| 4 | Additional Insured Forms | 10/01 or 11/85 edition | AMEND to 04/13 |
| 5 | Insurance Documentation | "certified copies of policies" | AMEND to certificates |
| 6 | Non-standard Coverage | Pollution/Cyber/Railroad | DELETE |
| 7 | Liquidated Damages | Direct LD amount | AMEND to pass-through |
| 8 | Consequential Damages | One-sided exposure | AMEND to mutual waiver |
| 9 | Personal Guarantee | Any personal guarantee | DELETE entire |
| 10 | Non-Compete | Any non-compete | DELETE entire |
| 11 | Union/PLA | PLA, Letter of Assent | DELETE |
| 12 | Vaccination | Mandatory vaccination | DELETE |
| 13 | Alternate Employer | WC 00 03 01 endorsement | DELETE |
| 14 | MFN | "most favored nations", "pricing no less favorable" | DELETE |

---

## Scoring

| Dimension | Max | Description |
|-----------|-----|-------------|
| Detection | 2 | Rule triggered correctly |
| Compliance | 1 | Compliance status confirmed |
| Action | 2 | Correct action selected |
| Language | 2 | Prescribed language used |
| Rationale | 2 | Rule citation present |
| **Total** | **9** | Per rule |

### Pass Criteria

| Result | Criteria |
|--------|----------|
| PASS | ≥80% rule compliance rate |
| MARGINAL | 60-79% compliance |
| FAIL | <60% OR critical rule violation |

---

## Known Performance Notes

Model is generally performant across Rules mode. No systematic issues documented.

### Compound Clauses

Some items marked `[COMPOUND]` contain multiple triggers in a single clause:
- Sterling_Mutual_01: Term/Survival (120 months)
- Sterling_Mutual_03/04: Indemnity + Governing Law in same clause
- Sitework_Fr_01-04: Four issues in Article 5.1

Models should identify all triggers even when bundled.

---

## Appendix A: Contracts

### NDA (10)
1. NDA_TechPartners_Bilateral
2. NDA_Meridian_Unilateral
3. NDA_GlobalPharm_Research
4. NDA_Vertex_Strategic
5. NDA_Quantum_JointVenture
6. NDA_Sterling_Mutual
7. NDA_Cascade_Supplier
8. NDA_Nexus_Investment
9. NDA_Atlas_Employment
10. NDA_Vanguard_Technical

### Subcontract (10)
1. Subcontract_HVAC_TitanConstruction
2. Subcontract_FireProtection_ApexBuilders
3. Subcontract_Masonry_SterlingGC
4. Subcontract_Landscaping_OmegaDevelopment
5. Subcontract_Demolition_PrimeBuilders
6. Subcontract_Flooring_NexusConstruction
7. Subcontract_Waterproofing_AtlasGC
8. Subcontract_Curtainwall_VectorBuilders
9. Subcontract_Sitework_FrontierConstruction
10. Subcontract_Millwork_CrestConstruction

---

## Appendix B: Detection Values

| Value | Meaning |
|-------|---------|
| **Y** | Full compliance |
| **P** | Partial (detected but wrong action/language) |
| **N** | Non-compliance (marked compliant when trigger present) |
| **NMI** | Not mentioned (trigger not identified) |
| **N/A** | Not applicable (trigger not present in contract) |

---

*End of Document*
