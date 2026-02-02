# Freeform Stacking Ground Truth
## Counterparty Redline Evaluation Reference

**Version:** 1.0  
**Generated:** 2026-01-27  
**Mode:** Freeform Stacking  
**Jurisdiction:** Mixed (US/UK)

---

## Document Overview

This ground truth covers **counterparty (CP) redline evaluation** in Freeform Stacking mode. Leah reviews contracts containing adversarial CP redlines and must respond appropriately (ACCEPT/MODIFY/REJECT).

**Note:** Baseline contract issues are covered in the separate *Freeform Baseline Ground Truth* document. In Stacking mode, Leah should detect **both** the CP redline issues below **and** all baseline issues.

### Key Metrics

| Metric | Value |
|--------|-------|
| Total Contracts | 10 |
| CP Redlines | 40 (4 per contract) |
| Max Points (Part A) | 240 (6 per redline) |

### Scoring Dimensions (per CP redline)

| Dimension | Max | Weight | Description |
|-----------|-----|--------|-------------|
| Action | 2 | 40% | Correct action selected (REJECT/MODIFY/ACCEPT) |
| Revision | 2 | 40% | Proposed revision addresses key elements |
| Reasoning | 2 | 20% | Rationale addresses required points |

### Critical Failures

- REJECT-only CP redline scored as ACCEPT
- Revision contains unacceptable element
- Reasoning endorses counterparty position on adversarial redline

### Pass Threshold

≥70% score AND zero critical failures

---

## Navigation

| # | Contract | Reviewing For | CP Redlines |
|---|----------|---------------|-------------|
| 1 | [Consulting Agreement](#1-consulting-agreement) | Client | 4 |
| 2 | [Data Processing Agreement](#2-data-processing-agreement) | Controller | 4 |
| 3 | [Distribution Agreement](#3-distribution-agreement) | Distributor | 4 |
| 4 | [Joint Venture MOU](#4-joint-venture-mou) | Party B | 4 |
| 5 | [IP License Agreement](#5-ip-license-agreement) | Licensee | 4 |
| 6 | [Partnership Agreement](#6-partnership-agreement) | Partner B | 4 |
| 7 | [Reseller Agreement](#7-reseller-agreement) | Reseller | 4 |
| 8 | [Services Agreement](#8-services-agreement) | Client | 4 |
| 9 | [SaaS License Agreement](#9-saas-license-agreement) | Licensee | 4 |
| 10 | [Supply Agreement](#10-supply-agreement) | Buyer | 4 |

---

# 1. Consulting Agreement

**Contract:** Consulting
**Parties:** Beta Tech Advisors LLC (Consultant) ↔ Meridian Enterprises Inc. (Client)
**Reviewing for:** Client
**Contract ID:** `Consulting_TechAdvisors_Beta`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| CONSULTING_01 | §3.4 | Payment Terms | REJECT |
| CONSULTING_02 | §5.1 | IP Ownership | REJECT |
| CONSULTING_03 | §5.2 | Background IP | REJECT |
| CONSULTING_04 | §7.1 | Termination for Convenience | REJECT |

### CONSULTING_01 | §3.4 | [REJECT]

**Payment Terms**

**Original Contract Language:**

> Client shall pay all undisputed invoices within thirty (30) days of receipt. Late payments shall bear interest at the rate of one percent (1%) per month or the maximum rate permitted by law, whichever is less.

**Counterparty Proposed Change:**

> Client shall pay all undisputed invoices within fifteen (15) days of receipt.

**Key Elements (must preserve/restore):**

- 1) Payment terms remain at 30 days 2) Retain late payment interest provision 3) Retain Client right to dispute invoices

**Acceptable Variations:**

- Full reversion to baseline 30 days (required)
- May add invoice dispute process with timelines
- May add withholding rights for non-conforming services

**Unacceptable Responses:**

- ❌ Accepting 15-day payment terms
- ❌ Payment terms under 30 days
- ❌ Removing late payment interest
- ❌ Removing Client dispute rights

**Reasoning Must Address:**

Halving payment period strains cash flow; removes Client dispute rights; industry standard is Net 30; no justification for acceleration

**Example Revision:**

> Client shall pay all undisputed invoices within thirty (30) days of receipt. Late payments shall bear interest at the rate of one percent (1%) per month or the maximum rate permitted by law, whichever is less.

*Category: 6. General Risk & Fairness — Economic risk allocation*

---

### CONSULTING_02 | §5.1 | [REJECT]

**IP Ownership**

**Original Contract Language:**

> All deliverables created by Consultant specifically for Client pursuant to this Agreement shall be considered work-for-hire and shall be owned exclusively by Client upon full payment of all fees due hereunder.

**Counterparty Proposed Change:**

> Consultant retains all intellectual property rights in deliverables, methodologies, and work product. Client receives a non-exclusive, non-transferable license to use deliverables for its internal business purposes only.

**Key Elements (must preserve/restore):**

- 1) Work-for-hire designation for bespoke deliverables 2) Client owns deliverables created for it 3) Payment condition acceptable as protective mechanism

**Acceptable Variations:**

- Full reversion to baseline (required)
- May add explicit assignment language as backup to work-for-hire
- May clarify background IP remains with Consultant
- May add Client sublicense rights for affiliates/successors

**Unacceptable Responses:**

- ❌ Consultant retaining ownership of bespoke deliverables
- ❌ License-only model for custom work
- ❌ Non-exclusive or revocable Client rights
- ❌ Internal-use-only restrictions on Client-paid deliverables

**Reasoning Must Address:**

Client pays for custom work and must own it; license-only model creates dependency risk; work-for-hire is appropriate for bespoke consulting deliverables

**Example Revision:**

> All deliverables created by Consultant specifically for Client pursuant to this Agreement shall be considered work-for-hire and shall be owned exclusively by Client upon full payment of all fees due hereunder.

*Category: 3. Intellectual Property & Data — IP ownership*

---

### CONSULTING_03 | §5.2 | [REJECT]

**Background IP**

**Original Contract Language:**

> To the extent any Background IP is incorporated into the Deliverables, Consultant hereby grants Client a non-exclusive, perpetual, royalty-free license to use such Background IP solely as part of the Deliverables.

**Counterparty Proposed Change:**

> To the extent any Background IP is incorporated into the Deliverables, Consultant hereby grants Client a non-exclusive, royalty-free license to use such Background IP solely as part of the Deliverables for a period of three (3) years from delivery, subject to termination if Client competes with Consultant in North America.

**Key Elements (must preserve/restore):**

- 1) Perpetual license duration 2) No territorial restrictions 3) No competitive use restrictions 4) Royalty-free

**Acceptable Variations:**

- Full reversion to baseline (required)
- May expand: modification and derivative works rights
- May expand: sublicense rights for affiliates
- May expand: use independently of Deliverables for internal purposes

**Unacceptable Responses:**

- ❌ Time-limited license on deliverables Client paid for
- ❌ Revocable license
- ❌ Territorial restrictions on Client use
- ❌ Competitive use restrictions that block Client's business
- ❌ License termination provisions

**Reasoning Must Address:**

Client paid for deliverables and must use them perpetually; 3-year limit renders deliverables obsolete; competitive restriction could block Client's core business; Background IP license must enable Deliverable use

**Example Revision:**

> To the extent any Background IP is incorporated into the Deliverables, Consultant hereby grants Client a non-exclusive, perpetual, royalty-free license to use such Background IP solely as part of the Deliverables.

*Category: 3. Intellectual Property & Data — IP licensing*

---

### CONSULTING_04 | §7.1 | [REJECT]

**Termination for Convenience**

**Original Contract Language:**

> Either party may terminate this Agreement for convenience upon thirty (30) days' prior written notice to the other party.

**Counterparty Proposed Change:**

> Consultant may terminate this Agreement for convenience upon fifteen (15) days' prior written notice. Client may terminate for convenience upon ninety (90) days' prior written notice and payment of a termination fee equal to three (3) months of fees under all active Statements of Work.

**Key Elements (must preserve/restore):**

- 1) Symmetric notice periods 2) No termination fee for Client 3) Reasonable notice for both parties (30 days)

**Acceptable Variations:**

- Full reversion to baseline symmetric 30 days (required)
- May reduce to 21 days if symmetric
- May add transition assistance requirements
- May add SOW-level termination rights

**Unacceptable Responses:**

- ❌ Asymmetric notice periods favouring Consultant
- ❌ Client termination fees or penalties
- ❌ Client notice period exceeding 30 days
- ❌ Consultant notice period under 30 days

**Reasoning Must Address:**

Asymmetric terms trap Client in underperforming relationship; termination fee is penalty without justification; 90-day notice with fee eliminates Client flexibility; symmetric terms are market standard

**Example Revision:**

> Either party may terminate this Agreement for convenience upon thirty (30) days' prior written notice to the other party.

*Category: 4. Term, Termination & Exit — Termination rights*

---


# 2. Data Processing Agreement

**Contract:** Data Processing Agreement
**Parties:** SecureData Services Ltd. (Processor) ↔ [Unnamed Controller] (Controller)
**Reviewing for:** Controller
**Contract ID:** `DPA_DataServices`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| DPA_CP_01 | §4.1 | Sub-processor Consent | REJECT |
| DPA_CP_02 | §8.1 | Breach Notification | REJECT |
| DPA_CP_03 | §9.2 | Indemnification | REJECT |
| DPA_CP_04 | §7.2 | Audit Rights | MODIFY |

### DPA_CP_01 | §4.1 | [REJECT/MODIFY]

**Sub-processor Consent**

**Original Contract Language:**

> Controller hereby provides general written authorisation for Processor to engage Sub-processors. Processor shall notify Controller of any intended changes to Sub-processors at least thirty (30) days prior to such changes. Controller may object to such changes by providing written notice to Processor within the notice period.

**Counterparty Proposed Change:**

> Controller hereby provides general written authorisation for Processor to engage Sub-processors for the Processing of Personal Data. Processor shall maintain an up-to-date list of Sub-processors available upon Controller's request.

**Effect of CP Change:** Removes 30-day advance notice requirement; removes Controller objection right; reduces to passive list maintenance only

**Key Elements (must preserve/restore):**

- 1) Advance notice of sub-processor changes (minimum 14 days, prefer 30)
- 2) Controller objection right preserved
- 3) Consequence for objection (termination right or Processor must not proceed)

**Acceptable Variations:**

- Full reversion to baseline (preferred)
- Notice period reduced to 14-21 days acceptable
- Deemed consent if no objection within notice period
- Pre-approved sub-processor list with consent required for others

**Unacceptable Responses:**

- ❌ Accepting removal of advance notice
- ❌ Accepting removal of objection right
- ❌ Passive list maintenance only
- ❌ Notice period under 14 days

**Reasoning Must Address:**

GDPR Art 28(2) requires Controller authorisation; advance notice enables due diligence; objection right is fundamental Controller protection; passive list is inadequate

**Example Revision:**

> Controller hereby provides general written authorisation for Processor to engage Sub-processors. Processor shall notify Controller of any intended changes to Sub-processors at least thirty (30) days prior to such changes. Controller may object to such changes by providing written notice to Processor within the notice period.

*Category: 3. Intellectual Property & Data — Data protection*

---

### DPA_CP_02 | §8.1 | [REJECT/MODIFY]

**Breach Notification**

**Original Contract Language:**

> Processor shall notify Controller of any Personal Data Breach without undue delay and in any event within seventy-two (72) hours of becoming aware of such breach.

**Counterparty Proposed Change:**

> Processor shall notify Controller of any Personal Data Breach without undue delay and in any event within five (5) business days of confirming such breach. Notification shall be limited to information Processor determines is necessary.

**Effect of CP Change:** Extends notification from 72 hours to 5 business days (potentially 7+ calendar days); changes trigger from 'becoming aware' to 'confirming' (allows delay); limits information to Processor's discretion

**Key Elements (must preserve/restore):**

- 1) Maximum 72-hour notification window
- 2) Trigger is 'becoming aware' not 'confirming'
- 3) Information provided must enable Controller assessment

**Acceptable Variations:**

- Full reversion to 72 hours (preferred)
- 48-hour notification acceptable
- Initial notice within 24-48 hours, full details within 72 hours
- Specified information requirements (nature, scope, affected data subjects, remediation)

**Unacceptable Responses:**

- ❌ Accepting 5 business days
- ❌ Accepting 'confirming' as trigger (allows indefinite delay)
- ❌ Accepting Processor discretion over information provided
- ❌ Any timeline exceeding 72 hours without justification

**Reasoning Must Address:**

Controller has 72-hour regulatory notification obligation under GDPR Art 33; 'becoming aware' is the legal standard; Controller needs information to assess regulatory obligations and data subject notification requirements

**Example Revision:**

> Processor shall notify Controller of any Personal Data Breach without undue delay and in any event within seventy-two (72) hours of becoming aware of such breach.

*Category: 5. Governance & Compliance — Regulatory compliance*

---

### DPA_CP_03 | §9.2 | [REJECT/MODIFY]

**Indemnification**

**Original Contract Language:**

> Processor shall indemnify Controller against any claims, damages, or regulatory fines arising from Processor's breach of this DPA or Data Protection Laws.

**Counterparty Proposed Change:**

> Processor shall indemnify Controller against direct damages arising from Processor's gross negligence or wilful misconduct in breach of this DPA, excluding any regulatory fines, penalties, or administrative sanctions.

**Effect of CP Change:** Narrows trigger from 'breach' to 'gross negligence or wilful misconduct' (very high bar); excludes regulatory fines entirely; limits to direct damages only

**Key Elements (must preserve/restore):**

- 1) Indemnification triggered by breach (not just gross negligence)
- 2) Regulatory fines included (or capped, not excluded)
- 3) Not limited to direct damages only

**Acceptable Variations:**

- Full reversion to baseline (preferred)
- Cap on fine indemnification (e.g., 12-month fees, $500K-$2M)
- Proportionate fault allocation where both parties contributed
- Processor participation rights in regulatory proceedings
- Exclude fines for Controller-caused violations only

**Unacceptable Responses:**

- ❌ Accepting gross negligence/wilful misconduct threshold
- ❌ Accepting complete exclusion of regulatory fines
- ❌ Accepting direct damages only limitation
- ❌ No indemnification for Processor breach

**Reasoning Must Address:**

GDPR fines can reach €20M or 4% global turnover; Processor breach creates Controller regulatory exposure; gross negligence standard effectively eliminates indemnification; Controller cannot absorb Processor-caused fines

**Example Revision:**

> Processor shall indemnify Controller against any claims, damages, or regulatory fines arising from Processor's breach of this DPA or Data Protection Laws.

*Category: 2. Liability & Redress — Indemnification obligations*

---

### DPA_CP_04 | §7.2 | [REJECT/MODIFY]

**Audit Rights**

**Original Contract Language:**

> Audits shall be conducted with reasonable notice during normal business hours, no more than once per year, and at Controller's expense.

**Counterparty Proposed Change:**

> Audits shall be conducted with no less than sixty (60) days' prior written notice during normal business hours, no more than once every two (2) years, and at Controller's sole expense. Controller shall provide Processor with the audit scope and methodology for approval prior to any audit. Processor may satisfy audit requirements by providing a SOC 2 Type II report in lieu of on-site audit.

**Effect of CP Change:** Extends notice from 'reasonable' to 60 days minimum; reduces frequency from annual to biennial; requires Processor approval of audit scope (defeats independence); allows SOC 2 substitution (removes direct audit right)

**Key Elements (must preserve/restore):**

- 1) Reasonable notice period (14-30 days acceptable)
- 2) Annual audit right preserved
- 3) Controller determines audit scope (not subject to Processor approval)
- 4) SOC 2 supplements but does not replace direct audit right

**Acceptable Variations:**

- Notice period 14-30 days
- SOC 2 accepted for routine compliance, with direct audit right for cause
- Additional audit permitted following breach or complaint
- Processor bears costs if material deficiencies found

**Unacceptable Responses:**

- ❌ Accepting 60-day notice (allows evidence tampering)
- ❌ Accepting biennial audits only
- ❌ Accepting Processor approval of audit scope
- ❌ Accepting SOC 2 as complete substitute for direct audit
- ❌ Removing direct audit right entirely

**Reasoning Must Address:**

GDPR Art 28(3)(h) requires Controller audit rights; 60 days notice undermines audit effectiveness; Processor scope approval defeats audit independence; SOC 2 is point-in-time and may not cover Controller-specific concerns

**Example Revision:**

> Audits shall be conducted with reasonable notice (not less than fourteen (14) business days) during normal business hours, no more than once per year, and at Controller's expense. Processor shall provide Controller with SOC 2 Type II reports annually; such reports shall supplement but not replace Controller's direct audit rights.

*Category: 5. Governance & Compliance — Audit and inspection rights*

---


# 3. Distribution Agreement

**Contract:** Distribution
**Parties:** Global Products Manufacturing Inc. (Supplier) ↔ [Unnamed Distributor] (Distributor)
**Reviewing for:** Distributor
**Contract ID:** `Distribution_GlobalPartners`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| DISTRIBUTION_01 | §5.1 | Prices | REJECT |
| DISTRIBUTION_02 | §6.1 | Minimum Purchase | REJECT |
| DISTRIBUTION_03 | §3.1 | Non-Exclusive | REJECT |
| DISTRIBUTION_04 | §11.1 | Term | REJECT |

### DISTRIBUTION_01 | §5.1 | [REJECT]

**Prices**

**Original Contract Language:**

> Distributor shall purchase Products at the prices set forth in Supplier's then-current price list. Supplier may modify prices upon sixty (60) days' prior written notice.

**Counterparty Proposed Change:**

> Distributor shall purchase Products at the prices set forth in Supplier's then-current price list. Supplier may modify prices upon fifteen (15) days' prior written notice, and such changes shall apply retroactively to purchase orders placed but not yet fulfilled.

**Key Elements (must preserve/restore):**

- 1) 60-day notice period retained 2) No retroactive price changes 3) Changes apply only to future orders

**Acceptable Variations:**

- Full reversion to baseline 60 days (required)
- May extend to 90 days with price cap (CPI + 3%)
- May add termination right if price increase exceeds 10%
- May clarify: changes apply only to orders placed after effective date

**Unacceptable Responses:**

- ❌ Accepting 15-day notice
- ❌ Notice period under 60 days
- ❌ Retroactive price changes
- ❌ Price changes applying to accepted orders
- ❌ No notice requirement

**Reasoning Must Address:**

15 days insufficient for planning; retroactive changes violate pipeline protection; Distributor needs time to adjust customer pricing; 60 days is market standard

**Example Revision:**

> Distributor shall purchase Products at the prices set forth in Supplier's then-current price list. Supplier may modify prices upon sixty (60) days' prior written notice.

*Category: 6. General Risk & Fairness — Unilateral rights*

---

### DISTRIBUTION_02 | §6.1 | [REJECT]

**Minimum Purchase**

**Original Contract Language:**

> Distributor agrees to purchase a minimum of One Hundred Thousand Dollars ($100,000) of Products per calendar quarter during the Term of this Agreement. Failure to meet minimum purchase requirements for two (2) consecutive quarters shall constitute a material breach.

**Counterparty Proposed Change:**

> Distributor agrees to purchase a minimum of Two Hundred Fifty Thousand Dollars ($250,000) of Products per calendar quarter during the Term of this Agreement, with an automatic ten percent (10%) annual escalator. Failure to meet minimum purchase requirements for one (1) quarter shall constitute a material breach.

**Key Elements (must preserve/restore):**

- 1) Minimum remains at $100K/quarter 2) No automatic escalator 3) Two consecutive quarter grace period before breach

**Acceptable Variations:**

- Full reversion to baseline $100K (required)
- May accept modest increase if justified by territory ($125K-$150K)
- May add ramp-up period for new products
- May add cure period (60 days) before breach declared

**Unacceptable Responses:**

- ❌ Accepting $250K minimum (2.5x increase)
- ❌ Accepting automatic escalators
- ❌ One quarter miss = breach (no grace period)
- ❌ Minimums exceeding $150K without corresponding rights increase

**Reasoning Must Address:**

2.5x increase plus escalator creates unsustainable commitment; one-quarter breach eliminates flexibility; automatic escalators compound exposure; no justification for increase

**Example Revision:**

> Distributor agrees to purchase a minimum of One Hundred Thousand Dollars ($100,000) of Products per calendar quarter during the Term of this Agreement. Failure to meet minimum purchase requirements for two (2) consecutive quarters shall constitute a material breach.

*Category: 1. Obligations & Performance — Performance standards*

---

### DISTRIBUTION_03 | §3.1 | [REJECT]

**Non-Exclusive**

**Original Contract Language:**

> Supplier hereby appoints Distributor as a non-exclusive distributor of the Products within the Territory.

**Counterparty Proposed Change:**

> Supplier hereby appoints Distributor as a non-exclusive distributor of the Products within the Territory. Distributor agrees not to distribute, market, or sell any products that compete with the Products during the Term and for two (2) years thereafter.

**Key Elements (must preserve/restore):**

- 1) Non-exclusive appointment without non-compete 2) Distributor retains right to carry competing products 3) No post-term restrictions

**Acceptable Variations:**

- Full reversion to baseline (required)
- If adding non-compete: must convert to exclusive territory
- If adding non-compete: must be narrow (specific products only)
- May accept limited during-term non-compete if exclusive granted

**Unacceptable Responses:**

- ❌ Non-compete with non-exclusive appointment
- ❌ Post-term non-compete (2 years)
- ❌ Broad competitive product restrictions
- ❌ Non-compete without exclusive territory grant

**Reasoning Must Address:**

Non-compete with non-exclusive is one-sided; Distributor needs portfolio diversification; Supplier retains right to compete directly; post-term restriction blocks business development

**Example Revision:**

> Supplier hereby appoints Distributor as a non-exclusive distributor of the Products within the Territory.

*Category: 1. Obligations & Performance — Clarity of obligations*

---

### DISTRIBUTION_04 | §11.1 | [REJECT]

**Term**

**Original Contract Language:**

> This Agreement shall have an initial term of three (3) years from the Effective Date. Thereafter, it shall automatically renew for successive one (1) year periods unless either Party provides ninety (90) days' notice of non-renewal prior to the expiration.

**Counterparty Proposed Change:**

> This Agreement shall have an initial term of one (1) year from the Effective Date. Thereafter, it shall automatically renew for successive one (1) year periods unless either Party provides ninety (90) days' notice of non-renewal prior to the expiration. Supplier may terminate this Agreement for convenience upon sixty (60) days' written notice at any time.

**Key Elements (must preserve/restore):**

- 1) Three-year initial term 2) No unilateral Supplier termination for convenience 3) Symmetric renewal/termination rights

**Acceptable Variations:**

- Full reversion to baseline 3 years (required)
- May accept 2-year initial if market investment is lower
- May add mutual termination for convenience with notice
- May add performance-based early exit (if minimums not met)

**Unacceptable Responses:**

- ❌ Accepting 1-year initial term
- ❌ Unilateral Supplier termination for convenience
- ❌ Asymmetric termination rights favouring Supplier
- ❌ Initial term under 2 years

**Reasoning Must Address:**

1-year term insufficient to recover market investment; unilateral Supplier termination eliminates Distributor certainty; 3-year term is standard for territory development; asymmetry creates one-sided risk

**Example Revision:**

> This Agreement shall have an initial term of three (3) years from the Effective Date. Thereafter, it shall automatically renew for successive one (1) year periods unless either Party provides ninety (90) days' notice of non-renewal prior to the expiration.

*Category: 4. Term, Termination & Exit — Duration and renewal*

---


# 4. Joint Venture MOU

**Contract:** Joint Venture MOU
**Parties:** InnovateTech Solutions Corp. (Party A) ↔ Quantum Dynamics LLC (Party B)
**Reviewing for:** Party B
**Contract ID:** `JV_MOU_InnovateTech`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| JV_01 | §4.1 | Material Decisions | REJECT |
| JV_02 | §5.1 | Profit Allocation | REJECT |
| JV_03 | §6.2 | Developed IP | REJECT |
| JV_04 | §9.1 | Non-Compete | REJECT |

### JV_01 | §4.1 | [REJECT]

**Material Decisions**

**Original Contract Language:**

> All material decisions regarding the Joint Venture, including but not limited to annual budgets, capital expenditures exceeding $50,000, entry into material contracts, and changes to the business plan, shall require the unanimous written consent of both Parties.

**Counterparty Proposed Change:**

> All material decisions regarding the Joint Venture, including but not limited to annual budgets, capital expenditures exceeding $50,000, entry into material contracts, and changes to the business plan, shall be made at the sole discretion of Party A.

**Key Elements (must preserve/restore):**

- 1) Unanimous consent for material decisions 2) Both parties have veto rights 3) No unilateral decision-making authority for either party

**Acceptable Variations:**

- Full reversion to baseline unanimous consent (required)
- May add deadlock resolution mechanism
- May tier decisions (fundamental vs operational)
- May add independent chair for operational deadlocks
- May define specific reserved matters requiring unanimity

**Unacceptable Responses:**

- ❌ Party A sole discretion on material decisions
- ❌ Unilateral control by either party
- ❌ Simple majority (ineffective in 50/50 structure)
- ❌ No veto protection for Party B

**Reasoning Must Address:**

50/50 JV requires balanced governance; sole discretion eliminates Party B's control over its investment; fundamental decisions require mutual consent; unilateral control inappropriate for equal partnership

**Example Revision:**

> All material decisions regarding the Joint Venture, including but not limited to annual budgets, capital expenditures exceeding $50,000, entry into material contracts, and changes to the business plan, shall require the unanimous written consent of both Parties.

*Category: 5. Governance & Compliance — Decision-making authority*

---

### JV_02 | §5.1 | [REJECT]

**Profit Allocation**

**Original Contract Language:**

> Net profits and losses of the Joint Venture shall be allocated fifty percent (50%) to Party A and fifty percent (50%) to Party B.

**Counterparty Proposed Change:**

> Net profits shall be allocated sixty percent (60%) to Party A and forty percent (40%) to Party B. Net losses shall be allocated first to Party B until Party B's capital account is exhausted, then to Party A.

**Key Elements (must preserve/restore):**

- 1) Equal 50/50 profit allocation 2) Equal 50/50 loss allocation 3) No preferential profit distribution 4) No asymmetric loss allocation

**Acceptable Variations:**

- Full reversion to baseline 50/50 (required)
- May accept unequal split if Party B contribution is proportionally less
- May add preferred return if justified by capital contribution timing
- Equal ownership requires equal profit/loss allocation

**Unacceptable Responses:**

- ❌ Accepting 60/40 profit split favouring Party A
- ❌ Party B absorbing losses first
- ❌ Asymmetric profit/loss allocation
- ❌ Waterfall favouring one party without justification

**Reasoning Must Address:**

Equal ownership requires equal economics; asymmetric allocation transfers value from Party B to Party A; loss priority creates unfair risk; no justification for preferential treatment

**Example Revision:**

> Net profits and losses of the Joint Venture shall be allocated fifty percent (50%) to Party A and fifty percent (50%) to Party B.

*Category: 6. General Risk & Fairness — Economic risk allocation*

---

### JV_03 | §6.2 | [REJECT]

**Developed IP**

**Original Contract Language:**

> All Developed IP shall be jointly owned by the Parties in equal shares. Neither Party may license or transfer Developed IP to third parties without the consent of the other Party.

**Counterparty Proposed Change:**

> All Developed IP shall be owned exclusively by Party A. Party B receives a non-exclusive, royalty-bearing license to use Developed IP for its own business purposes, subject to a royalty of five percent (5%) of Party B's gross revenues from such use.

**Key Elements (must preserve/restore):**

- 1) Joint ownership of IP developed using JV resources 2) Equal ownership shares 3) Mutual consent for third-party licensing

**Acceptable Variations:**

- Full reversion to baseline joint ownership (required)
- May add licensing framework with revenue sharing
- May add buyout rights at fair market value
- May clarify post-termination usage rights
- May add field-of-use restrictions on licensing

**Unacceptable Responses:**

- ❌ Party A exclusive ownership of jointly developed IP
- ❌ License-only for Party B on IP it helped create
- ❌ Royalty obligations on jointly funded development
- ❌ Asymmetric IP ownership in equal partnership

**Reasoning Must Address:**

Party B contributes equally to development and must own equally; license-only model expropriates Party B's contribution; royalty on jointly funded IP is double payment; joint ownership is fundamental to JV economics

**Example Revision:**

> All Developed IP shall be jointly owned by the Parties in equal shares. Neither Party may license or transfer Developed IP to third parties without the consent of the other Party.

*Category: 3. Intellectual Property & Data — IP ownership*

---

### JV_04 | §9.1 | [REJECT]

**Non-Compete**

**Original Contract Language:**

> During the Term and for a period of two (2) years thereafter, neither Party shall, directly or indirectly, engage in any business that competes with the Joint Venture's quantum AI business within the Territory without the prior written consent of the other Party.

**Counterparty Proposed Change:**

> During the Term and for a period of five (5) years thereafter, Party B shall not, directly or indirectly, engage in any business involving quantum computing, artificial intelligence, or related technologies anywhere in the world. Party A shall have no such restriction.

**Key Elements (must preserve/restore):**

- 1) Mutual non-compete (applies to both parties) 2) Reasonable duration (2 years post-term) 3) Narrow scope (specific to JV business) 4) Territorial limitation

**Acceptable Variations:**

- Full reversion to baseline mutual 2-year (required)
- May narrow scope to specific products/markets
- May shorten duration to 1 year post-term
- May add carve-outs for pre-existing businesses
- May eliminate post-term restriction entirely

**Unacceptable Responses:**

- ❌ Asymmetric restriction on Party B only
- ❌ 5-year post-term restriction
- ❌ Global scope without limitation
- ❌ Broad technology restriction (all quantum/AI)
- ❌ Party A unrestricted while Party B blocked

**Reasoning Must Address:**

Asymmetric non-compete is fundamentally unfair; 5-year global restriction blocks Party B's core business; quantum/AI is too broad; Party B cannot be permanently excluded while Party A competes freely; mutual restrictions required

**Example Revision:**

> During the Term and for a period of two (2) years thereafter, neither Party shall, directly or indirectly, engage in any business that competes with the Joint Venture's quantum AI business within the Territory without the prior written consent of the other Party.

*Category: 1. Obligations & Performance — Restrictions on business activities*

---


# 5. IP License Agreement

**Contract:** IP License
**Parties:** Innovate IP Holdings LLC (Licensor) ↔ TechPro Industries Inc. (Licensee)
**Reviewing for:** Licensee
**Contract ID:** `License_IPHoldings`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| LICENSE_01 | §3.2 | Improvements | REJECT |
| LICENSE_02 | §4.1 | Minimum Royalty | REJECT |
| LICENSE_03 | §12.2 | Liability Cap | REJECT |
| LICENSE_04 | §13.2 | Termination for Cause | REJECT |

### LICENSE_01 | §3.2 | [REJECT]

**Improvements**

**Original Contract Language:**

> Improvements to the Licensed IP developed by Licensee shall be owned by Licensor.

**Counterparty Proposed Change:**

> Improvements to the Licensed IP developed by Licensee shall be owned by Licensor. Licensee hereby grants Licensor an irrevocable, perpetual, royalty-free license to use, modify, and sublicense any Licensee Background Technology incorporated into such Improvements.

**Key Elements (must preserve/restore):**

- 1) Reject grant-back of Licensee Background Technology 2) Licensee should own improvements OR get license back 3) Licensor getting both ownership AND Licensee tech is overreach

**Acceptable Variations:**

- Reject redline entirely (required)
- Alternative: Change improvement ownership to Licensee or joint
- Alternative: Licensee owns improvements, grants license-back to Licensor
- No grant of Licensee Background Technology

**Unacceptable Responses:**

- ❌ Accepting grant-back of Licensee Background Technology
- ❌ Allowing Licensor access to Licensee's proprietary tech
- ❌ Modifications that still give Licensor rights to Licensee Background Tech

**Reasoning Must Address:**

Licensee already loses improvement ownership (baseline issue); adding grant-back of Licensee Background Technology compounds the problem; Licensor gaining rights to Licensee's proprietary technology is excessive

**Example Revision:**

> Improvements to the Licensed IP developed by Licensee shall be owned by Licensor.

*Category: 3. Intellectual Property & Data — IP ownership*

---

### LICENSE_02 | §4.1 | [REJECT]

**Minimum Royalty**

**Original Contract Language:**

> Beginning in Year 2, Licensee shall pay minimum annual royalty of $250,000, regardless of actual Net Sales. Running royalties shall be credited against this minimum.

**Counterparty Proposed Change:**

> Beginning in Year 1, Licensee shall pay minimum annual royalty of $500,000, regardless of actual Net Sales, escalating by fifteen percent (15%) annually thereafter. Running royalties shall be credited against this minimum.

**Key Elements (must preserve/restore):**

- 1) Revert to Year 2 start (not Year 1) 2) Revert to $250K amount (not $500K) 3) Remove 15% annual escalator 4) Maintain credit for running royalties

**Acceptable Variations:**

- Full reversion to baseline required
- May add: suspension for force majeure
- May add: adjustment for market conditions
- May reduce minimum amount further if negotiating

**Unacceptable Responses:**

- ❌ Accepting Year 1 start
- ❌ Accepting $500K minimum
- ❌ Accepting 15% annual escalator
- ❌ Any increase above baseline $250K

**Reasoning Must Address:**

Year 1 start eliminates ramp-up period; doubling minimum to $500K creates unsustainable fixed cost; 15% escalator compounds to 200%+ over 10 years; baseline $250K Year 2 already material commitment

**Example Revision:**

> Beginning in Year 2, Licensee shall pay minimum annual royalty of $250,000, regardless of actual Net Sales. Running royalties shall be credited against this minimum.

*Category: 6. General Risk & Fairness — Economic risk allocation*

---

### LICENSE_03 | §12.2 | [REJECT]

**Liability Cap**

**Original Contract Language:**

> LICENSOR'S TOTAL LIABILITY SHALL NOT EXCEED THE ROYALTIES PAID IN THE TWELVE MONTHS PRECEDING THE CLAIM.

**Counterparty Proposed Change:**

> LICENSOR'S TOTAL LIABILITY SHALL NOT EXCEED THE UPFRONT LICENSE FEE PAID UNDER SECTION 5.2. LIABILITY SHALL EXCLUDE DAMAGES FOR PRODUCT RECALLS, LOST PROFITS, OR COMMERCIAL LOSS ARISING FROM LICENSED PRODUCT DEFECTS.

**Key Elements (must preserve/restore):**

- 1) Revert cap to 12-month royalties (not upfront fee only) 2) Remove exclusion for product recall damages 3) Remove exclusion for lost profits from Licensed Product defects

**Acceptable Variations:**

- Full reversion to baseline (minimum acceptable)
- Better: increase cap to 24 months royalties
- Better: add minimum floor amount
- Better: add carve-outs for IP warranty breach

**Unacceptable Responses:**

- ❌ Cap limited to upfront fee only
- ❌ Exclusion of product recall damages
- ❌ Exclusion of commercial losses from IP defects
- ❌ Any narrowing of Licensor liability below baseline

**Reasoning Must Address:**

Upfront fee ($500K) may be exhausted in Year 1; 10-year term needs liability tied to ongoing royalties; product recall and commercial loss exclusions eliminate remedies for IP defects; baseline already limits liability (Licensee concern is cap is too LOW, not too high)

**Example Revision:**

> LICENSOR'S TOTAL LIABILITY SHALL NOT EXCEED THE ROYALTIES PAID IN THE TWELVE MONTHS PRECEDING THE CLAIM.

*Category: 2. Liability & Redress — Limitation of liability*

---

### LICENSE_04 | §13.2 | [REJECT]

**Termination for Cause**

**Original Contract Language:**

> Either party may terminate this Agreement upon written notice if the other party materially breaches this Agreement and fails to cure such breach within sixty (60) days after written notice specifying the breach.

**Counterparty Proposed Change:**

> Licensor may terminate this Agreement immediately upon written notice if Licensee materially breaches this Agreement. Licensee may terminate only if Licensor materially breaches and fails to cure within one hundred twenty (120) days after written notice.

**Key Elements (must preserve/restore):**

- 1) Symmetric termination rights (both parties equal) 2) Reasonable cure period for both (60 days) 3) Material breach standard for both 4) Written notice requirement for both

**Acceptable Variations:**

- Full reversion to baseline required
- May add: definition of material breach
- May add: immediate termination for specific severe breaches (both parties)
- May reduce cure period to 30 days if mutual

**Unacceptable Responses:**

- ❌ Immediate termination right for Licensor only
- ❌ Asymmetric cure periods (120 days for Licensee vs none for Licensor)
- ❌ Any advantage to Licensor on termination rights
- ❌ Different breach standards for parties

**Reasoning Must Address:**

Asymmetric termination creates power imbalance; Licensee has major investment (upfront fee, minimum royalties, development); 120-day cure vs immediate is grossly unfair; mutual 60-day cure is market standard

**Example Revision:**

> Either party may terminate this Agreement upon written notice if the other party materially breaches this Agreement and fails to cure such breach within sixty (60) days after written notice specifying the breach.

*Category: 4. Term, Termination & Exit — Termination rights*

---


# 6. Partnership Agreement

**Contract:** Partnership Agreement
**Parties:** Venture Alliance Capital Partners LP (Partner A) ↔ Growth Dynamics LLC (Partner B)
**Reviewing for:** Partner B
**Contract ID:** `Partnership_VentureAlliance`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| PARTNERSHIP_01 | §4.1 | Management | REJECT |
| PARTNERSHIP_02 | §6.1 | Profit Sharing | REJECT |
| PARTNERSHIP_03 | §9.1 | Confidentiality | REJECT |
| PARTNERSHIP_04 | §12.2 | Termination | REJECT |

### PARTNERSHIP_01 | §4.1 | [REJECT]

**Management**

**Original Contract Language:**

> The Partners shall jointly manage the Partnership Activities. Major decisions require unanimous consent of both Partners.

**Counterparty Proposed Change:**

> Partner A shall have sole decision-making authority for all Partnership Activities. Partner B shall be consulted but Partner A retains final authority on all major decisions.

**Key Elements (must preserve/restore):**

- 1) Revert to joint management (not Partner A sole control) 2) Maintain unanimous consent requirement 3) Equal decision-making power for both partners

**Acceptable Variations:**

- Full reversion to baseline required
- May add: escalation mechanism for deadlock
- May add: specific categories requiring unanimous consent
- May add: swing vote or mediation process

**Unacceptable Responses:**

- ❌ Partner A sole decision-making authority
- ❌ Consultative role only for Partner B
- ❌ Any asymmetric control favouring Partner A
- ❌ Removal of unanimous consent requirement

**Reasoning Must Address:**

Equal partnership means equal control; sole authority for Partner A destroys partnership balance; Partner B has equal capital at risk; 'consulted but not deciding' is unacceptable in 50/50 partnership

**Example Revision:**

> The Partners shall jointly manage the Partnership Activities. Major decisions require unanimous consent of both Partners.

*Category: 5. Governance & Compliance — Decision-making authority*

---

### PARTNERSHIP_02 | §6.1 | [REJECT]

**Profit Sharing**

**Original Contract Language:**

> All profits and losses from Co-Investments shall be allocated fifty percent (50%) to Partner A and fifty percent (50%) to Partner B, regardless of the relative capital contributions made by each Partner to any particular Co-Investment.

**Counterparty Proposed Change:**

> All profits shall be allocated sixty percent (60%) to Partner A and forty percent (40%) to Partner B. All losses shall be allocated first to Partner B until Partner B's capital account is exhausted, then to Partner A.

**Key Elements (must preserve/restore):**

- 1) Revert to 50/50 profit allocation 2) Revert to equal loss allocation 3) No preferential profit distribution to Partner A 4) No waterfall with Partner B absorbing losses first

**Acceptable Variations:**

- Full reversion to baseline required
- May add: preferred returns for larger contributor
- May add: carried interest for performance
- Pro rata allocation based on capital if contributions differ

**Unacceptable Responses:**

- ❌ 60/40 profit split favouring Partner A
- ❌ Losses allocated to Partner B first
- ❌ Any asymmetric economic allocation
- ❌ Waterfall structures favouring Partner A

**Reasoning Must Address:**

60/40 profit split gives Partner A 50% more profit than Partner B with no justification; 'losses to B first' structure is predatory; equal partnership requires equal economics unless contributions differ; baseline already has mismatch issue (50/50 regardless of capital)

**Example Revision:**

> All profits and losses from Co-Investments shall be allocated fifty percent (50%) to Partner A and fifty percent (50%) to Partner B, regardless of the relative capital contributions made by each Partner to any particular Co-Investment.

*Category: 6. General Risk & Fairness — Economic risk allocation*

---

### PARTNERSHIP_03 | §9.1 | [REJECT]

**Confidentiality**

**Original Contract Language:**

> Each Partner shall maintain in strict confidence all Confidential Information of the Partnership, including without limitation deal flow, investment terms, portfolio company information, financial projections, and the terms of this Agreement. Neither Partner shall disclose any Confidential Information to any third party without the prior written consent of the other Partner.

**Counterparty Proposed Change:**

> Partner B shall maintain in strict confidence all Confidential Information of the Partnership, including without limitation deal flow, investment terms, portfolio company information, financial projections, and the terms of this Agreement. Partner A may disclose Confidential Information to third parties as Partner A deems appropriate for Partnership business.

**Key Elements (must preserve/restore):**

- 1) Mutual confidentiality obligations (both partners bound) 2) No unilateral disclosure by Partner A 3) Consent requirement for both partners 4) Symmetric obligations

**Acceptable Variations:**

- Full reversion to baseline required
- May add: carve-outs for permitted recipients (investors, advisors) if mutual
- May add: standard legal/regulatory exceptions if mutual
- May permit disclosure with notice (not consent) if mutual

**Unacceptable Responses:**

- ❌ One-sided confidentiality (only Partner B bound)
- ❌ Partner A can disclose freely
- ❌ Unilateral determination of 'appropriate' disclosure
- ❌ Any asymmetric confidentiality obligations

**Reasoning Must Address:**

One-sided confidentiality destroys trust; Partner A could share deal flow with competitors; Partner B's proprietary information exposed; 'appropriate for Partnership business' is unlimited discretion; mutual obligations are fundamental to partnership

**Example Revision:**

> Each Partner shall maintain in strict confidence all Confidential Information of the Partnership. Neither Partner shall disclose any Confidential Information to any third party without the prior written consent of the other Partner.

*Category: 3. Intellectual Property & Data — Confidentiality scope*

---

### PARTNERSHIP_04 | §12.2 | [REJECT]

**Termination**

**Original Contract Language:**

> Either party may terminate this Agreement upon written notice if the other party materially breaches this Agreement and fails to cure such breach within sixty (60) days after written notice specifying the breach.

**Counterparty Proposed Change:**

> Partner A may terminate this Agreement immediately upon written notice if Partner B materially breaches this Agreement. Partner B may terminate only if Partner A materially breaches and fails to cure within ninety (90) days after written notice.

**Key Elements (must preserve/restore):**

- 1) Symmetric termination rights (both partners equal) 2) Equal cure period (60 days for both) 3) Material breach standard for both 4) No immediate termination without cure opportunity

**Acceptable Variations:**

- Full reversion to baseline required
- May add: immediate termination for fraud or criminal conduct (both partners)
- May add: definition of material breach
- May reduce cure period if mutual (e.g., 30 days for both)

**Unacceptable Responses:**

- ❌ Immediate termination for Partner A, no cure period
- ❌ Asymmetric cure periods (90 days for Partner B vs none for Partner A)
- ❌ Different termination standards for partners
- ❌ Any advantage to Partner A on termination

**Reasoning Must Address:**

Asymmetric termination creates power imbalance; immediate termination without cure opportunity is harsh; 90-day cure for Partner B vs immediate for Partner A is grossly unfair; equal partnership requires equal termination rights; both partners have investments and obligations at risk

**Example Revision:**

> Either party may terminate this Agreement upon written notice if the other party materially breaches this Agreement and fails to cure such breach within sixty (60) days after written notice specifying the breach.

*Category: 4. Term, Termination & Exit — Termination rights*

---


# 7. Reseller Agreement

**Contract:** Reseller Agreement
**Parties:** CloudTech Solutions Inc. (Vendor) ↔ Pacific Tech Distributors LLC (Reseller)
**Reviewing for:** Reseller
**Contract ID:** `Reseller_TechDistributors`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| RESELLER_01 | §4.1 | Pricing | REJECT |
| RESELLER_02 | §5.1 | Payment Terms | REJECT |
| RESELLER_03 | §9.1 | Term | REJECT |
| RESELLER_04 | §12.2 | Liability Cap | REJECT |

### RESELLER_01 | §4.1 | [REJECT]

**Pricing**

**Original Contract Language:**

> Reseller shall purchase Products at the prices set forth in Exhibit B, which reflect a discount from Vendor's list prices. Vendor may modify Product prices from time to time upon thirty (30) days' prior written notice. Price changes shall apply to all orders placed after the effective date of such changes.

**Counterparty Proposed Change:**

> Reseller shall purchase Products at the prices set forth in Exhibit B, which reflect a discount from Vendor's list prices. Vendor may modify Product prices from time to time upon seven (7) days' prior written notice. Price changes shall apply retroactively to all orders not yet fulfilled.

**Key Elements (must preserve/restore):**

- 1) Revert to 30-day notice period (not 7 days) 2) Remove retroactive application 3) Price changes apply only to orders placed after effective date 4) Adequate planning time for Reseller

**Acceptable Variations:**

- Full reversion to baseline required
- May negotiate: 60-90 day notice period
- May add: price cap (CPI or fixed %)
- May add: termination right on unacceptable increase

**Unacceptable Responses:**

- ❌ 7-day notice period
- ❌ Retroactive price changes
- ❌ Application to unfulfilled orders
- ❌ Notice period under 30 days

**Reasoning Must Address:**

7 days inadequate for planning/budgeting; retroactive application to unfulfilled orders eliminates pricing certainty; Reseller may have customer quotes based on existing prices; 30-day notice is market standard minimum

**Example Revision:**

> Vendor may modify Product prices from time to time upon thirty (30) days' prior written notice. Price changes shall apply to all orders placed after the effective date of such changes.

*Category: 6. General Risk & Fairness — Economic risk allocation*

---

### RESELLER_02 | §5.1 | [REJECT]

**Payment Terms**

**Original Contract Language:**

> Reseller shall pay all invoices within thirty (30) days of invoice date. Late payments bear interest at 1.5% per month.

**Counterparty Proposed Change:**

> Reseller shall pay all invoices within fifteen (15) days of invoice date. Late payments bear interest at 2% per month. Vendor may suspend deliveries for any past-due balance.

**Key Elements (must preserve/restore):**

- 1) Revert to 30-day payment terms (not 15 days) 2) Revert to 1.5% monthly interest (not 2%) 3) Remove delivery suspension for any past-due balance 4) Maintain reasonable working capital terms

**Acceptable Variations:**

- Full reversion to baseline required
- May reduce interest to 1% per month
- May add: suspension only for material past-due (e.g., 60+ days)
- May add: dispute resolution for disputed invoices

**Unacceptable Responses:**

- ❌ 15-day payment terms
- ❌ 2% monthly interest (24% APR)
- ❌ Immediate suspension for any late payment
- ❌ Payment terms under 30 days

**Reasoning Must Address:**

15-day terms stress Reseller cash flow; 2% monthly = 24% APR is excessive; suspension for any past-due balance (even 1 day late) is draconian; 30-day terms are commercial standard; baseline 1.5% (18% APR) already high

**Example Revision:**

> Reseller shall pay all invoices within thirty (30) days of invoice date. Late payments bear interest at 1.5% per month.

*Category: 6. General Risk & Fairness — Economic risk allocation*

---

### RESELLER_03 | §9.1 | [REJECT]

**Term**

**Original Contract Language:**

> This Agreement shall commence on the Effective Date and continue for an initial term of two (2) years. Thereafter, this Agreement shall automatically renew for successive one (1) year periods unless either Party provides written notice of non-renewal at least ninety (90) days prior to the end of the then-current term. Neither Party may terminate this Agreement for convenience during the Term.

**Counterparty Proposed Change:**

> This Agreement shall commence on the Effective Date and continue for an initial term of one (1) year. Thereafter, this Agreement shall automatically renew for successive one (1) year periods unless either Party provides written notice of non-renewal at least ninety (90) days prior to the end of the then-current term. Vendor may terminate this Agreement for convenience upon thirty (30) days' prior written notice to Reseller.

**Key Elements (must preserve/restore):**

- 1) Revert to 2-year initial term (not 1 year) 2) Remove Vendor unilateral termination for convenience 3) Maintain no termination for convenience during Term 4) Adequate commitment period for Reseller investment

**Acceptable Variations:**

- Full reversion to baseline required
- May negotiate: mutual termination for convenience with 90+ day notice and transition provisions
- May add: 12-month protected period before any convenience termination
- If allowing convenience termination, must be mutual and with adequate notice

**Unacceptable Responses:**

- ❌ 1-year initial term
- ❌ Vendor-only termination for convenience
- ❌ 30-day notice for termination
- ❌ Asymmetric termination rights

**Reasoning Must Address:**

1-year term insufficient to recover Reseller investments (training, marketing, inventory); Vendor-only convenience termination creates power imbalance; 30-day notice inadequate for channel transition; 2-year term provides minimum stability; if convenience termination exists, must be mutual

**Example Revision:**

> This Agreement shall commence on the Effective Date and continue for an initial term of two (2) years. Neither Party may terminate this Agreement for convenience during the Term.

*Category: 4. Term, Termination & Exit — Termination rights*

---

### RESELLER_04 | §12.2 | [REJECT]

**Liability Cap**

**Original Contract Language:**

> VENDOR'S TOTAL LIABILITY SHALL NOT EXCEED AMOUNTS PAID BY RESELLER IN THE TWELVE MONTHS PRECEDING THE CLAIM.

**Counterparty Proposed Change:**

> VENDOR'S TOTAL LIABILITY SHALL NOT EXCEED THE LESSER OF (A) THE PRICE OF THE SPECIFIC PRODUCT GIVING RISE TO THE CLAIM OR (B) TWENTY-FIVE THOUSAND DOLLARS ($25,000).

**Key Elements (must preserve/restore):**

- 1) Revert to 12-month amounts paid (not product price or $25K) 2) Remove 'lesser of' limitation 3) Maintain meaningful liability cap tied to relationship value 4) No artificial $25K ceiling

**Acceptable Variations:**

- Full reversion to baseline (minimum acceptable)
- Better: increase to 24 months of amounts paid
- Better: add minimum floor (e.g., $100K minimum)
- Better: add carve-outs for IP infringement

**Unacceptable Responses:**

- ❌ Cap limited to product price
- ❌ $25K fixed cap
- ❌ 'Lesser of' limitation
- ❌ Any cap below baseline 12-month amount

**Reasoning Must Address:**

Product price cap is meaningless (could be $100 software license); $25K cap inadequate for software reseller relationship; 12-month purchases reflects relationship scale; baseline already limits Vendor liability (Reseller concern is cap is too LOW, not too high)

**Example Revision:**

> VENDOR'S TOTAL LIABILITY SHALL NOT EXCEED AMOUNTS PAID BY RESELLER IN THE TWELVE MONTHS PRECEDING THE CLAIM.

*Category: 2. Liability & Redress — Limitation of liability*

---


# 8. Services Agreement

**Contract:** Services Agreement
**Parties:** Creative Digital Agency Inc. (Agency) ↔ [Unnamed Client] (Client)
**Reviewing for:** Client
**Contract ID:** `Services_DigitalAgency`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| SERVICES_01 | §2.1 | Scope | REJECT |
| SERVICES_02 | §5.2 | Agency IP | REJECT |
| SERVICES_03 | §6.1 | Review Period | REJECT |
| SERVICES_04 | §10.2 | Liability Cap | REJECT |

### SERVICES_01 | §2.1 | [REJECT]

**Scope**

**Original Contract Language:**

> Agency shall provide the creative and digital marketing services described in each Statement of Work executed by the Parties pursuant to this Agreement.

**Counterparty Proposed Change:**

> Agency shall provide services described in each Statement of Work and any related services reasonably requested by Client without requiring additional approval.

**Key Elements (must preserve/restore):**

- 1) Specific SOW scope only 2) No open-ended 'related services' 3) Agency bills for work outside SOW without approval = risk

**Acceptable Variations:**

- Full reversion to baseline (required)
- May add: expedited change order process
- May add: small change threshold (under $X or Y hours) requiring documented approval

**Unacceptable Responses:**

- ❌ Accepting 'related services' without approval
- ❌ Services outside signed SOWs
- ❌ Unilateral Client scope expansion
- ❌ No fee mechanism for additional work

**Reasoning Must Address:**

Scope creep; undefined obligation; Agency could be required to provide unbilled services

**Example Revision:**

> Revert to baseline: Services limited to those in executed SOWs. Reject any 'related services' or Client-unilateral scope expansion without defined fee mechanism.

*Category: 1. Obligations & Performance — Clarity of obligations*

---

### SERVICES_02 | §5.2 | [REJECT]

**Agency IP**

**Original Contract Language:**

> To the extent Agency IP is incorporated into any Deliverables, Agency grants Client a non-exclusive, perpetual, royalty-free license to use such Agency IP solely as part of the Deliverables.

**Counterparty Proposed Change:**

> To the extent Agency IP is incorporated into Deliverables, Agency grants Client a license to use such Agency IP in [Territory], revocable upon notice.

**Key Elements (must preserve/restore):**

- 1) Perpetual, not revocable 2) Worldwide, not territory-limited 3) Royalty-free 4) For use as part of Deliverables

**Acceptable Variations:**

- Full reversion to baseline (required)
- May add: modification rights for Client
- May add: sublicense rights to affiliates

**Unacceptable Responses:**

- ❌ Revocable license
- ❌ Territory-limited license
- ❌ Royalty-bearing license
- ❌ License narrower than baseline

**Reasoning Must Address:**

Client cannot use deliverables effectively with territory limitation or revocability; baseline already protects Agency IP ownership

**Example Revision:**

> Revert to baseline: Non-exclusive, perpetual, royalty-free license. Reject territory limitation and revocability.

*Category: 3. Intellectual Property & Data — IP ownership*

---

### SERVICES_03 | §6.1 | [REJECT]

**Review Period**

**Original Contract Language:**

> Client shall review each Deliverable and provide written acceptance or rejection within fifteen (15) business days. If rejected, Agency has opportunity to cure.

**Counterparty Proposed Change:**

> Client shall review each Deliverable and provide written acceptance or rejection within five (5) business days. If Client fails to respond, Deliverable is deemed accepted.

**Key Elements (must preserve/restore):**

- 1) Minimum 15 business days review period 2) Silence = rejection, not acceptance (baseline provision) 3) Agency has cure opportunity

**Acceptable Variations:**

- Full reversion to baseline (required)
- 15 days minimum review period
- May add: reminder process before deemed acceptance
- May clarify: cure period duration

**Unacceptable Responses:**

- ❌ 5-day deemed acceptance
- ❌ Acceptance as default for silence
- ❌ Review period under 10 business days
- ❌ No cure opportunity

**Reasoning Must Address:**

5 days insufficient for stakeholder review; silence=acceptance creates risk of accepting defective deliverables

**Example Revision:**

> Revert to baseline: 15 business days for review. Reject 5-day acceptance default.

*Category: 1. Obligations & Performance — Conditions and timeframes*

---

### SERVICES_04 | §10.2 | [REJECT]

**Liability Cap**

**Original Contract Language:**

> AGENCY'S TOTAL LIABILITY SHALL NOT EXCEED THE FEES PAID BY CLIENT UNDER THE APPLICABLE STATEMENT OF WORK.

**Counterparty Proposed Change:**

> Agency's total liability shall not exceed the lesser of SOW fees or $25,000.

**Key Elements (must preserve/restore):**

- 1) Cap tied to fees paid 2) No arbitrary low fixed cap 3) Scales with engagement size 4) Minimum floor acceptable

**Acceptable Variations:**

- Full reversion to baseline (required)
- Cap at SOW fees (no fixed ceiling)
- May add: minimum floor of $50K+
- May add: carve-outs for gross negligence, willful misconduct

**Unacceptable Responses:**

- ❌ Fixed $25K cap
- ❌ Cap below SOW fees
- ❌ Cap that does not scale with engagement
- ❌ Arbitrary low ceiling disconnected from fees

**Reasoning Must Address:**

$25K fixed cap inadequate for substantial engagements; cap should be proportional to fees paid

**Example Revision:**

> Revert to baseline: Liability cap tied to SOW fees without arbitrary fixed ceiling.

*Category: 2. Liability & Redress — Limitation of liability*

---


# 9. SaaS License Agreement

**Contract:** SaaS License
**Parties:** CloudServices Alpha Inc. (Licensor) ↔ [Unnamed Licensee] (Licensee)
**Reviewing for:** Licensee
**Contract ID:** `SLA_CloudServices_Alpha`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| SLA_01 | §9.1 | Indemnification | REJECT |
| SLA_02 | §10.2 | Liability Cap | REJECT |
| SLA_03 | §11.2 | Termination for Cause | REJECT |
| SLA_04 | §12.4 | Assignment | REJECT |

### SLA_01 | §9.1 | [REJECT]

**Indemnification**

**Original Contract Language:**

> Licensor shall indemnify, defend, and hold harmless Licensee from and against any third-party claims arising from infringement of intellectual property rights by the Software.

**Counterparty Proposed Change:**

> Each party shall indemnify, defend, and hold harmless the other party from and against any third-party claims.

**Key Elements (must preserve/restore):**

- 1) IP infringement indemnification from Licensor 2) Not watered down to generic mutual indemnity 3) Protects Licensee from Software IP claims

**Acceptable Variations:**

- Full reversion to baseline (required)
- May add: procedural requirements (notice, cooperation)
- May clarify: scope of covered IP rights
- May add: carve-outs for Licensee modifications

**Unacceptable Responses:**

- ❌ Generic mutual indemnification
- ❌ Removing IP-specific protection
- ❌ Equal obligations on both parties
- ❌ Licensee indemnifying Licensor for Software IP

**Reasoning Must Address:**

Licensor provides Software, should indemnify IP claims; mutual generic indemnity removes critical protection

**Example Revision:**

> Revert to baseline: IP-specific indemnification from Licensor. Reject generic mutual indemnification that removes IP protection.

*Category: 2. Liability & Redress — Indemnification obligations*

---

### SLA_02 | §10.2 | [REJECT]

**Liability Cap**

**Original Contract Language:**

> Licensor's total liability shall not exceed the Subscription Fees paid by Licensee in the twelve (12) months preceding the claim.

**Counterparty Proposed Change:**

> Licensor's total liability shall not exceed $50,000.

**Key Elements (must preserve/restore):**

- 1) Cap tied to 12-month fees 2) Proportional to contract value 3) No arbitrary low fixed cap

**Acceptable Variations:**

- Full reversion to baseline (required)
- May add: minimum floor of $100K+
- May add: carve-outs for IP, data breach, wilful misconduct

**Unacceptable Responses:**

- ❌ Fixed $50K cap
- ❌ Cap below 12-month fees
- ❌ Cap disconnected from contract value
- ❌ Arbitrary low ceiling

**Reasoning Must Address:**

$50K fixed cap inadequate for enterprise subscriptions; cap should scale with fees paid

**Example Revision:**

> Revert to baseline: 12-month fees cap. Reject fixed $50K cap that may be inadequate for substantial subscriptions.

*Category: 2. Liability & Redress — Limitation of liability*

---

### SLA_03 | §11.2 | [REJECT]

**Termination for Cause**

**Original Contract Language:**

> Either party may terminate upon 30 days notice if other party materially breaches and fails to cure within 30 days.

**Counterparty Proposed Change:**

> Licensor may terminate immediately upon material breach. Licensee may terminate if Licensor fails to cure breach within 60 days notice.

**Key Elements (must preserve/restore):**

- 1) Equal cure periods 2) Minimum 30 days for both parties 3) No immediate termination without cure opportunity

**Acceptable Variations:**

- Full reversion to baseline (required)
- May differentiate: immediate for security breaches, 30 days for others
- May add: suspension before termination

**Unacceptable Responses:**

- ❌ Asymmetric cure periods
- ❌ Licensor immediate termination rights
- ❌ Licensee 60 days while Licensor immediate
- ❌ No cure opportunity for Licensee breaches

**Reasoning Must Address:**

Asymmetry unfairly favours Licensor; both parties need reasonable cure opportunity

**Example Revision:**

> Revert to baseline: Symmetric 30-day cure period for both parties. Reject asymmetric provision favouring Licensor.

*Category: 4. Term, Termination & Exit — Termination rights*

---

### SLA_04 | §12.4 | [REJECT]

**Assignment**

**Original Contract Language:**

> Neither party may assign this Agreement without the other party's prior written consent, except Licensee may assign to affiliates or in connection with merger or acquisition.

**Counterparty Proposed Change:**

> Licensee may not assign this Agreement in connection with change of control without Licensor consent. Violation of this Section shall constitute material breach.

**Key Elements (must preserve/restore):**

- 1) Licensee M&A assignment rights preserved 2) No consent required for change of control 3) Not a material breach

**Acceptable Variations:**

- Full reversion to baseline (required)
- May add: notice requirement for M&A (not consent)
- May add: successor assumes obligations

**Unacceptable Responses:**

- ❌ Blocking M&A assignments
- ❌ Requiring Licensor consent for change of control
- ❌ Material breach for M&A assignment
- ❌ No M&A carve-out

**Reasoning Must Address:**

M&A restrictions block business transactions; Licensee must have change-of-control flexibility

**Example Revision:**

> Revert to baseline: Licensee may assign to affiliates or in M&A transactions. Reject restriction on M&A assignments.

*Category: 6. General Risk & Fairness — Unilateral rights*

---


# 10. Supply Agreement

**Contract:** Supply Agreement
**Parties:** Precision Manufacturing Co. (Supplier) ↔ Apex Automotive Inc. (Buyer)
**Reviewing for:** Buyer
**Contract ID:** `Supply_ManufacturingCo`

## CP Redline Summary

| Test ID | Section | Issue | Primary Action |
|---------|---------|-------|----------------|
| SUPPLY_01 | §4.2 | Payment Terms | REJECT |
| SUPPLY_02 | §5.1 | Product Warranty | REJECT |
| SUPPLY_03 | §11.2 | Liability Cap | REJECT |
| SUPPLY_04 | §14.3 | Termination | REJECT |

### SUPPLY_01 | §4.2 | [REJECT]

**Payment Terms**

**Original Contract Language:**

> Buyer shall pay all invoices within thirty (30) days of invoice date. Late payments bear interest at 1% per month.

**Counterparty Proposed Change:**

> Buyer shall pay all invoices within fifteen (15) days of invoice date. Supplier may suspend deliveries if payment is late.

**Key Elements (must preserve/restore):**

- 1) Minimum 30-day payment terms 2) Suspension requires cure period and notice 3) Standard commercial terms

**Acceptable Variations:**

- Full reversion to baseline (required)
- May add: 2% early payment discount for 10 days
- May clarify: suspension requires 15 days notice and cure opportunity
- May add: late payment protections for Supplier

**Unacceptable Responses:**

- ❌ 15-day payment terms
- ❌ Net under 30 days
- ❌ Immediate suspension without notice
- ❌ Suspension without cure opportunity

**Reasoning Must Address:**

15 days insufficient for AP cycles; suspension needs due process; industry standard is Net 30

**Example Revision:**

> Revert to baseline: Net 30 payment terms. Reject 15-day requirement and unilateral suspension rights.

*Category: 1. Obligations & Performance — Conditions and timeframes*

---

### SUPPLY_02 | §5.1 | [REJECT]

**Product Warranty**

**Original Contract Language:**

> Supplier warrants Products shall be free from defects in materials and workmanship for one (1) year from delivery.

**Counterparty Proposed Change:**

> Supplier warrants Products free from defects for sixty (60) days from delivery, excluding normal wear, improper use, unauthorised modifications, environmental damage, and third-party components.

**Key Elements (must preserve/restore):**

- 1) Minimum 12 months warranty 2) From delivery date 3) Reasonable exclusions only

**Acceptable Variations:**

- Full reversion to baseline (required)
- May add: reasonable exclusions (misuse, unauthorised modification)
- 12 months minimum required
- May clarify: manufacturing defects covered

**Unacceptable Responses:**

- ❌ 60-day warranty
- ❌ Warranty under 12 months
- ❌ Excessive exclusions
- ❌ Normal wear excluded (reasonable but needs definition)

**Reasoning Must Address:**

60 days grossly inadequate; automotive industry standard 12-24 months; many defects manifest beyond 60 days

**Example Revision:**

> Revert to baseline: One (1) year warranty from delivery. Reject 60-day reduction and extensive exclusions.

*Category: 2. Liability & Redress — Warranties and representations*

---

### SUPPLY_03 | §11.2 | [REJECT]

**Liability Cap**

**Original Contract Language:**

> Supplier's total liability shall not exceed amounts paid by Buyer for Products in the twelve (12) months preceding the claim.

**Counterparty Proposed Change:**

> Supplier's total liability shall not exceed the lesser of product price or $50,000.

**Key Elements (must preserve/restore):**

- 1) Cap tied to 12-month product payments 2) Proportional to relationship value 3) No arbitrary low fixed cap

**Acceptable Variations:**

- Full reversion to baseline (required)
- May add: minimum floor of $100K+
- May add: carve-outs for IP, gross negligence, willful misconduct
- May increase to 24-month fees

**Unacceptable Responses:**

- ❌ Fixed $50K cap
- ❌ Lesser of product price or fixed amount
- ❌ Cap below 12-month payments
- ❌ Arbitrary low ceiling

**Reasoning Must Address:**

$50K inadequate for automotive supply relationship; cap should scale with purchase volume

**Example Revision:**

> Revert to baseline: 12-month product payments cap. Reject fixed $50K ceiling.

*Category: 2. Liability & Redress — Limitation of liability*

---

### SUPPLY_04 | §14.3 | [REJECT]

**Termination**

**Original Contract Language:**

> Either party may terminate this Agreement upon 180 days written notice.

**Counterparty Proposed Change:**

> Supplier may terminate upon 30 days notice. Buyer may not terminate for convenience.

**Key Elements (must preserve/restore):**

- 1) Symmetric termination rights 2) Reasonable notice period (90-180 days) 3) Both parties can terminate for convenience

**Acceptable Variations:**

- Full reversion to baseline (required)
- 180 days notice for both parties
- May compromise: 90 days notice for both
- May add: payment for work in progress

**Unacceptable Responses:**

- ❌ Asymmetric termination rights
- ❌ Supplier 30 days while Buyer cannot terminate
- ❌ Removing Buyer termination for convenience
- ❌ Notice period under 90 days

**Reasoning Must Address:**

Buyer needs termination flexibility for supply strategy changes; asymmetric provision creates vendor lock-in

**Example Revision:**

> Revert to baseline: Either party may terminate on 180 days notice. Reject asymmetric provision.

*Category: 4. Term, Termination & Exit — Termination rights*

---


# Appendix: Summary Statistics

## CP Redlines by Contract

| Contract | CP Redlines | Max Points |
|----------|-------------|------------|
| Consulting Agreement | 4 | 24 |
| Data Processing Agreement | 4 | 24 |
| Distribution Agreement | 4 | 24 |
| Joint Venture MOU | 4 | 24 |
| IP License Agreement | 4 | 24 |
| Partnership Agreement | 4 | 24 |
| Reseller Agreement | 4 | 24 |
| Services Agreement | 4 | 24 |
| SaaS License Agreement | 4 | 24 |
| Supply Agreement | 4 | 24 |
| **TOTAL** | **40** | **240** |

## CP Redlines by Category

| Category | Count |
|----------|-------|
| 1. Obligations & Performance | 6 |
| 2. Liability & Redress | 8 |
| 3. Intellectual Property & Data | 7 |
| 4. Term, Termination & Exit | 7 |
| 5. Governance & Compliance | 4 |
| 6. General Risk & Fairness | 8 |

## CP Redlines by Primary Action

| Action | Count | % |
|--------|-------|---|
| MODIFY | 1 | 2% |
| REJECT | 39 | 98% |

---

*Ground Truth Version 1.0 | Generated 2026-01-27*
