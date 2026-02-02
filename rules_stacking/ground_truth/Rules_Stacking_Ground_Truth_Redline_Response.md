# Rules Stacking Ground Truth: Redline Response

**Version:** 1.0
**Date:** 2026-01-17
**Author:** Liz
**Status:** Final

---

## Overview

Rules Stacking evaluates Leah's response to counterparty redlines using deterministic rules. **Redlined clauses ONLY** — no analysis of unchanged text.

| Aspect | Detail |
|--------|--------|
| **Contracts** | 5 NDA + 5 Subcontract |
| **GT Items** | 15 NDA + 16 Subcontract = 31 total |
| **Representing Party** | NDA: Receiving Party, Subcontract: Subcontractor |
| **Critical Failure** | Scope violation (commenting on unchanged text) |

---

## Critical Scope Principle

**Leah ONLY applies rules to redlined clauses.**

| Correct | Incorrect |
|---------|-----------|
| Flag rule violation in CP's redline | Flag issue in unchanged text |
| REJECT CP's problematic insertion | Perform general contract review |
| MODIFY CP's excessive amendment | Propose changes to non-redlined clauses |

**Scope violation = automatic critical failure**

---

## GT Summary by Contract Type

### NDA (15 items across 5 contracts)

| Contract | Items | Key Redlines |
|----------|-------|--------------|
| NDA_Vertex_Strategic_Stacking | 2 | Residual knowledge insertion, Bond waiver insertion |
| NDA_Vanguard_Technical_Stacking | 3 | Retention right deletion, Destruction expansion, Offshore jurisdiction |
| NDA_TechPartners_Bilateral_Stacking | 4 | Unmarked CI, Perpetual survival, 24-month non-solicit, Broad-form indemnity |
| NDA_Meridian_Unilateral_Stacking | 4 | Compelled disclosure prohibition, Non-compete insertion, Unlimited liability, Audit rights (no rule) |
| NDA_Atlas_Employment_Stacking | 2 | 10-year survival, Asymmetric assignment |

### Subcontract (16 items across 5 contracts)

| Contract | Items | Key Redlines |
|----------|-------|--------------|
| Subcontract_Waterproofing_AtlasGC_Stacking | 4 | Broad-form indemnity, Cyber insurance insertion, Non-compete insertion, CBA compliance |
| Subcontract_Masonry_SterlingGC_Stacking | 3 | Outdated AI forms (10/01), One-sided consequentials, Personal guarantee insertion |
| Subcontract_HVAC_TitanConstruction_Stacking | 3 | Broad-form trigger insertion, $15M umbrella, Direct LD insertion |
| Subcontract_Flooring_NexusConstruction_Stacking | 3 | MFN insertion, $5M prof liability, PLA insertion |
| Subcontract_Curtainwall_VectorBuilders_Stacking | 3 | AEE insertion, Policy copies requirement, Vaccination mandate |

---

## Actions by Redline Type

| CP Redline Type | Expected Action | Example |
|-----------------|-----------------|---------|
| **INSERTION** of problematic text | REJECT | CP adds "residual knowledge" to CI definition |
| **INSERTION** requiring modification | MODIFY | CP changes survival to "perpetuity" |
| **DELETION** of protective text | REJECT (restore) | CP deletes archival retention right |
| **REPLACEMENT** with problematic text | MODIFY | CP changes $5M limit to $15M |
| **NEW PROVISION** violating rules | REJECT | CP adds entire non-compete article |
| **NO RULE APPLIES** | ACCEPT WITH RISK | CP adds audit rights (no rule violation) |

---

## Key Redline Patterns

### Subtle vs Explicit

| Difficulty | Description | Example |
|------------|-------------|---------|
| **SUBTLE** | Appended to existing clause | "..., including residual knowledge" |
| **EXPLICIT** | Clear replacement or new provision | "three (3) years" → "in perpetuity" |

Models should catch both. Subtle insertions at clause end are particularly important.

### ACCEPT Scenarios (No Rule Violation)

Some redlines require ACCEPT even though unfavourable:

| test_id | Redline | Why ACCEPT |
|---------|---------|------------|
| VG3 | Governing Law → Cayman Islands | FLAG rule, not DELETE/REJECT |
| M3 | Liability → unlimited | FLAG rule, not DELETE/REJECT |
| M4 | Audit rights insertion | No applicable rule |

**Critical:** ACCEPT doesn't mean "favourable" — it means no rule requires action.

---

## Scoring

| Dimension | Max | Description |
|-----------|-----|-------------|
| Action | 2 | Correct ACCEPT/MODIFY/REJECT |
| Revision | 2 | Follows prescribed language |
| Reasoning | 2 | Rule citation present |
| **Total** | **6** | Per redline |

### Pass Criteria

| Result | Criteria |
|--------|----------|
| PASS | ≥70% AND 0 scope violations |
| MARGINAL | 50-69% OR 1 scope violation |
| FAIL | <50% OR 2+ scope violations |

---

## Known Performance Notes

Model is generally performant. Watch for:

1. **Subtle insertions** at clause end (e.g., V1, T1, TP4)
2. **FLAG vs REJECT confusion** for jurisdiction/liability issues
3. **Scope creep** — ensure model doesn't comment on unchanged text

---

## Appendix A: Contracts

### NDA Stacking (5)
1. NDA_Vertex_Strategic_Stacking.docx
2. NDA_Vanguard_Technical_Stacking.docx
3. NDA_TechPartners_Bilateral_Stacking.docx
4. NDA_Meridian_Unilateral_Stacking.docx
5. NDA_Atlas_Employment_Stacking_Fixed.docx

### Subcontract Stacking (5)
1. Subcontract_Waterproofing_AtlasGC_Stacking.docx
2. Subcontract_Masonry_SterlingGC_Stacking.docx
3. Subcontract_HVAC_TitanConstruction_Stacking.docx
4. Subcontract_Flooring_NexusConstruction_Stacking.docx
5. Subcontract_Curtainwall_VectorBuilders_Stacking.docx

---

## Appendix B: Detection Values

| Value | Meaning |
|-------|---------|
| **Y** | Correctly identified and actioned per rules |
| **P** | Identified but action or revision incomplete |
| **N** | Missed rule violation or wrong action |
| **NMI** | Redline not addressed at all |

---

*End of Document*
