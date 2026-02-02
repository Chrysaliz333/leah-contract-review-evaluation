# Contract Review Ground Truth
## Freeform Analysis Mode

**Version:** 1.0_LOCKED
**Generated:** 2026-01-27
**Jurisdiction:** US Commercial
**Mode:** Freeform contract analysis

---

## Contract Navigation

| # | Contract | Issues | T1 | T2 | T3 | Max Pts |
|---|----------|--------|----|----|----|----|
| 1 | [Consulting Agreement](#1-consulting-agreement) | 11 | 1 | 8 | 2 | 50 |
| 2 | [Data Processing Agreement](#2-data-processing-agreement) | 12 | 3 | 6 | 3 | 57 |
| 3 | [Distribution Agreement](#3-distribution-agreement) | 13 | 6 | 5 | 2 | 75 |
| 4 | [Joint Venture MOU](#4-joint-venture-mou) | 18 | 5 | 10 | 3 | 93 |
| 5 | [IP License Agreement](#5-ip-license-agreement) | 15 | 4 | 7 | 4 | 71 |
| 6 | [Partnership Agreement](#6-partnership-agreement) | 12 | 6 | 4 | 2 | 70 |
| 7 | [Reseller Agreement](#7-reseller-agreement) | 13 | 4 | 7 | 2 | 69 |
| 8 | [Services Agreement](#8-services-agreement) | 26 | 4 | 11 | 11 | 98 |
| 9 | [SaaS License Agreement](#9-saas-license-agreement) | 26 | 8 | 12 | 6 | 130 |
| 10 | [Supply Agreement](#10-supply-agreement) | 14 | 4 | 8 | 2 | 74 |

**Total Issues:** 160 | **Total Points:** 787

---

# 1. Consulting Agreement

**Contract:** Consulting
**Parties:** Beta Tech Advisors LLC (Consultant) ↔ Meridian Enterprises Inc. (Client)
**Reviewing for:** Meridian Enterprises Inc. (Client)
**Contract ID:** `Consulting_TechAdvisors_Beta`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 1 | GT-01 |
| T2 Material | 8 | GT-02, GT-03, GT-04, GT-05, GT-06, GT-07, GT-08, GT-09 |
| T3 Minor | 2 | GT-10, GT-11 |

**Weighted Max Points:** 50

## T1: Critical Issues

### GT-01 | Clause 5.1 | [X] AMEND

**Work-for-hire designation likely ineffective - IP ownership at risk**

**Contract Language:**

> All deliverables created by Consultant specifically for Client pursuant to this Agreement shall be considered work-for-hire and shall be owned exclusively by Client upon full payment of all fees due hereunder.

**Analysis:**

- Clause relies on work-for-hire doctrine which has LIMITED APPLICATION to independent contractors
- Under 17 U.S.C. Section 101, work-for-hire only applies to: (1) employees, or (2) specially commissioned works in 9 enumerated categories WITH a signed writing
- Software, reports, and most consulting deliverables do NOT fall within the 9 categories
- Without valid work-for-hire, copyright vests in Consultant by default - Client may not own what it paid for
- ❌ No express assignment as fallback if work-for-hire fails
- Should add explicit IP assignment: 'Consultant hereby assigns all right, title, and interest...'
- Should add present-tense assignment language operative upon creation
- Payment condition is secondary concern - standard protective mechanism

**Recommended Actions:**

1. Should add explicit IP assignment: 'Consultant hereby assigns all right, title, and interest...'
2. Should add present-tense assignment language operative upon creation

---

## T2: Material Issues

### GT-02 | Clause 9.2 | [!] AMEND

**Liability cap lacks critical carve-outs**

**Contract Language:**

> EXCEPT FOR BREACHES OF CONFIDENTIALITY OBLIGATIONS OR INDEMNIFICATION OBLIGATIONS, NEITHER PARTY'S TOTAL LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT SHALL EXCEED THE TOTAL FEES PAID OR PAYABLE BY CLIENT TO CONSULTANT UNDER THE APPLICABLE STATEMENT OF WORK GIVING RISE TO THE CLAIM.

**Analysis:**

- Cap structure is standard (fees under applicable SOW)
- Carve-outs exist for confidentiality and indemnification - good
- ❌ MISSING carve-out for IP infringement claims
- ❌ MISSING carve-out for data breach / security incidents
- ❌ MISSING carve-out for gross negligence / willful misconduct
- Should add explicit carve-outs for: IP infringement, data breach, gross negligence
- Cap quantum is commercial judgment - negotiate based on deal economics

**Recommended Actions:**

1. Should add explicit carve-outs for: IP infringement, data breach, gross negligence

---

### GT-03 | Clause 9.1 | [!] AMEND

**Consequential damages exclusion lacks carve-outs**

**Contract Language:**

> IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER PARTY FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING WITHOUT LIMITATION LOSS OF PROFITS, LOSS OF DATA, OR LOSS OF BUSINESS OPPORTUNITY, ARISING OUT OF OR RELATED TO THIS AGREEMENT.

**Analysis:**

- Mutual exclusion of indirect/consequential/punitive damages - standard structure
- Includes loss of profits, data, business opportunity
- May prevent Client recovering significant losses from Consultant failures
- Should add carve-outs for confidentiality breach, IP infringement, data loss
- Carve-outs should align with indemnification obligations

**Recommended Actions:**

1. Should add carve-outs for confidentiality breach, IP infringement, data loss

---

### GT-04 | Clause 7.1 | [!] AMEND

**Termination for convenience terms inadequate for Client flexibility**

**Contract Language:**

> Either party may terminate this Agreement for convenience upon thirty (30) days' prior written notice to the other party.

**Analysis:**

- TfC exists but requires 30 days notice
- Client may need shorter notice period for agility
- ❌ No explicit right to terminate individual SOWs for convenience
- ❌ No clear wind-down or transition assistance provisions
- Effect of termination (7.4) only requires delivery of paid-for work
- Should add SOW-level TfC right
- Should add transition assistance obligation

**Recommended Actions:**

1. Should add SOW-level TfC right
2. Should add transition assistance obligation

---

### GT-05 | Clause 5.2 | [!] AMEND

**Background IP license scope too narrow**

**Contract Language:**

> To the extent any Background IP is incorporated into the Deliverables, Consultant hereby grants Client a non-exclusive, perpetual, royalty-free license to use such Background IP solely as part of the Deliverables.

**Analysis:**

- License limited to use 'solely as part of the Deliverables'
- ❌ No right to modify, adapt, or use Background IP independently
- May restrict Client's ability to maintain, enhance, or integrate deliverables
- Should expand to include modification, internal use, derivative works
- Consider sublicensing rights for affiliates/successors

**Recommended Actions:**

1. Should expand to include modification, internal use, derivative works
2. Consider sublicensing rights for affiliates/successors

---

### GT-06 | Clause 6.4 / Clause 13.10 | [!] AMEND

**Confidentiality survival period and trade secret treatment unclear**

**Contract Language:**

> Upon termination of this Agreement or upon request by the disclosing Party, the receiving Party shall promptly return or destroy all Confidential Information of the disclosing Party in its possession, except as required for legal or regulatory compliance.

**Analysis:**

- Article 6 survives per 13.10, but no explicit duration specified
- Trade secrets should survive indefinitely
- Standard confidential information typically survives 3-5 years
- ❌ No compelled disclosure process defined
- Return/destruction provision exists (6.4) but lacks certification requirement
- Should add explicit survival period with trade secret carve-out

**Recommended Actions:**

1. Should add explicit survival period with trade secret carve-out

---

### GT-07 | Clause N/A | [X] ADD

**Data protection / privacy clause missing entirely**

**STATUS: CLAUSE MISSING — Addition required**

**Analysis:**

- ❌ No data protection clause exists in contract
- If Consultant handles personal/sensitive data, Client faces compliance risk
- Should add GDPR/CCPA compliance requirements
- Define security measures and breach notification
- Clarify controller/processor roles
- Address subprocessors and audit rights

**Recommended Actions:**

1. Should add GDPR/CCPA compliance requirements

---

### GT-08 | Clause 10.1 | [!] AMEND

**Consultant indemnification limited to gross negligence/willful misconduct**

**Contract Language:**

> Consultant shall indemnify, defend, and hold harmless Client from and against any third-party claims arising from: (a) Consultant's gross negligence or wilful misconduct; or (b) any claim that the Deliverables infringe any third-party intellectual property rights.

**Analysis:**

- Indemnification only covers gross negligence or willful misconduct
- Does NOT cover ordinary negligence - high bar to prove
- IP infringement coverage exists but narrow
- ❌ No coverage for warranty breaches
- ❌ No coverage for confidentiality breaches
- Should expand to include ordinary negligence
- Should add indemnification for warranty and confidentiality breaches

**Recommended Actions:**

1. Should expand to include ordinary negligence
2. Should add indemnification for warranty and confidentiality breaches

---

### GT-09 | Clause N/A | [!] ADD

**No cyber insurance requirement**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - Cyber insurance not specified. Article 11.1 requires CGL ($1M) and E&O ($2M) but no cyber coverage.

**Analysis:**

- Article 11 requires CGL and E&O insurance - good
- ❌ No cyber liability insurance requirement
- Consultant may handle sensitive Client data/systems
- Should require cyber insurance if handling data
- Should require Client named as additional insured

**Recommended Actions:**

1. Should require cyber insurance if handling data
2. Should require Client named as additional insured

---

## T3: Minor Issues

### GT-10 | Clause 3.4 | [!] ADD

**Payment terms lack formal invoice dispute mechanism**

**Contract Language:**

> Client shall pay all undisputed invoices within thirty (30) days of receipt. Late payments shall bear interest at the rate of one percent (1%) per month or the maximum rate permitted by law, whichever is less.

**Analysis:**

- Late payment interest IS specified (1% per month) - reasonable rate
- 'Undisputed invoices' language implies dispute right exists
- ❌ No formal mechanism for Client to dispute invoices
- ❌ No explicit right to withhold payment for non-conforming services
- Consider adding dispute window and good faith resolution process

**Recommended Actions:**

1. Consider adding dispute window and good faith resolution process

---

### GT-11 | Clause 13.1 / Clause 13.2 | [!] AMEND

**Governing law and dispute forum favour Consultant location**

**Contract Language:**

> This Agreement shall be governed by and construed in accordance with the laws of the State of Texas, without regard to its conflicts of law principles.

**Analysis:**

- Texas law governs - Consultant is Texas-based, so predictable choice
- Travis County, Texas forum - Consultant's home jurisdiction
- Increases litigation cost for Nevada-based Client
- Standard for drafter to choose home jurisdiction
- Consider negotiating neutral venue or arbitration if material concern

**Recommended Actions:**

1. Consider negotiating neutral venue or arbitration if material concern

---


# 2. Data Processing Agreement

**Contract:** DPA
**Parties:** SecureData Services Ltd. (Processor) ↔ [Unnamed Controller] (Controller)
**Reviewing for:** Controller
**Contract ID:** `DPA_DataServices`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 3 | GT-01, GT-02, GT-03 |
| T2 Material | 6 | GT-04, GT-05, GT-06, GT-07, GT-08, GT-09 |
| T3 Minor | 3 | GT-10, GT-11, GT-12 |

**Weighted Max Points:** 57

## T1: Critical Issues

### GT-01 | Clause 4.1 | [!] AMEND

**General Sub-processor Authorization with Ineffective Objection**

**Contract Language:**

> Controller hereby provides general written authorisation for Processor to engage Sub-processors. Processor shall notify Controller of any intended changes to Sub-processors at least thirty (30) days prior to such changes. Controller may object to such changes by providing written notice to Processor within the notice period.

**Analysis:**

- Controller gives GENERAL (not specific) authorization
- 30-day notice for sub-processor changes
- Controller can object BUT no consequence stated
- What happens if Controller objects? Contract silent
- Should require specific consent for new sub-processors
- Or add termination right if objection not resolved

**Recommended Actions:**

1. Should require specific consent for new sub-processors

---

### GT-02 | Clause 5.1 | [!] AMEND

**Vague Security Measures**

**Contract Language:**

> Processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk, including encryption, pseudonymisation, access controls, and regular security testing.

**Analysis:**

- 'Appropriate' measures is subjective standard
- Examples given (encryption, pseudonymisation, access controls) but not required
- 5.2 requires ISO 27001 'or equivalent' - still flexible
- Should specify mandatory minimum controls
- Should require annual pen testing

**Recommended Actions:**

1. Should specify mandatory minimum controls
2. Should require annual pen testing

---

### GT-03 | Clause N/A | [!] ADD

**No Limitation of Liability in DPA**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No limitation of liability clause exists in DPA. Article 11.2 states: 'In the event of conflict between this DPA and the Principal Agreement, the provisions of this DPA shall prevail with respect to data protection matters.' - but liability not addressed

**Analysis:**

- DPA has no liability cap or exclusion clause
- Principal Agreement caps likely apply by reference
- But unclear how data breach damages are treated
- Should explicitly address liability for data breaches
- Should carve regulatory fines out of any caps

**Recommended Actions:**

1. Should explicitly address liability for data breaches
2. Should carve regulatory fines out of any caps

---

## T2: Material Issues

### GT-04 | Clause 9.1 / Clause 9.2 | [!] AMEND

**Indemnification May Be Subject to Hidden Caps**

**Contract Language:**

> 9.1: Each Party shall be liable for damages caused by Processing that infringes Data Protection Laws, in accordance with applicable law. 9.2: Processor shall indemnify Controller against any claims, damages, or regulatory fines arising from Processor's breach of this DPA or Data Protection Laws.

**Analysis:**

- 9.2 provides indemnification for Processor breach
- BUT 9.1 references 'in accordance with applicable law'
- Principal Agreement may have liability caps that apply
- Indemnification could be capped without Controller knowing
- Should explicitly state indemnification is unlimited
- Or carve indemnification out of any caps

**Recommended Actions:**

1. Should explicitly state indemnification is unlimited

---

### GT-05 | Clause 3.4 | [!] AMEND

**Deletion Timeline Unspecified**

**Contract Language:**

> Upon termination of the Principal Agreement, Processor shall delete or return all Personal Data to Controller, at Controller's option, unless retention is required by law.

**Analysis:**

- Must delete or return data on termination
- ❌ No specific timeline stated
- Could retain data indefinitely
- Should add 30-60 day deletion requirement
- Should require deletion certificate

**Recommended Actions:**

1. Should add 30-60 day deletion requirement
2. Should require deletion certificate

---

### GT-06 | Exhibit A / 2.2 | [X] AMEND

**Processing details Exhibit A is blank - GDPR Art 28 non-compliance**

**Contract Language:**

> 2.2 Processing Details. The subject matter, duration, nature, and purpose of Processing, the types of Personal Data, and categories of Data Subjects are described in Exhibit A. [...] EXHIBIT A - PROCESSING DETAILS Subject Matter of Processing: [blank]

**Analysis:**

- Exhibit A is blank - states 'Subject Matter of Processing:' with no content
- Clause 2.2 references Exhibit A for processing scope
- GDPR Art 28(3) requires documented subject matter, duration, nature, purpose
- Controller cannot demonstrate lawful basis without defined scope
- Creates regulatory exposure and audit failure risk
- Must require populated exhibit before execution

---

### GT-07 | Exhibit B / 5.1 | [X] AMEND

**Security measures Exhibit B is blank - cannot verify GDPR Art 32 compliance**

**Contract Language:**

> 5.1 Processor shall implement appropriate technical and organisational measures... [...] EXHIBIT B - TECHNICAL AND ORGANISATIONAL MEASURES [Description of security measures to be attached]

**Analysis:**

- Exhibit B is blank - states '[Description of security measures to be attached]'
- Clause 5.1 requires 'appropriate technical and organisational measures'
- Without schedule, Controller cannot verify security posture
- GDPR Art 32 requires documented security measures
- Creates due diligence and audit failure risk
- Must require populated exhibit before execution

---

### GT-08 | Exhibit C / 4.1 | [X] AMEND

**Approved sub-processors Exhibit C is blank - cannot exercise objection rights**

**Contract Language:**

> 4.1 Controller hereby provides general written authorisation for Processor to engage Sub-processors. [...] EXHIBIT C - APPROVED SUB-PROCESSORS [List of approved sub-processors to be attached]

**Analysis:**

- Exhibit C is blank - states '[List of approved sub-processors to be attached]'
- Clause 4.1 provides objection right for sub-processor changes
- Without baseline list, objection right is meaningless
- Controller cannot perform due diligence on existing sub-processors
- GDPR Art 28(2) requires Controller authorization of sub-processors
- Must require populated exhibit before execution

---

### GT-09 | Clause N/A | [!] ADD

**No Cyber Insurance Requirement**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No insurance requirement exists in DPA

**Analysis:**

- ❌ No requirement for Processor to maintain cyber insurance
- DPA involves processing personal data with breach risk
- Data breach could result in significant Controller liability
- Processor financial ability to honour indemnity is uncertain
- Should require minimum cyber/E&O insurance coverage
- Should require Controller named as additional insured

**Recommended Actions:**

1. Should require minimum cyber/E&O insurance coverage
2. Should require Controller named as additional insured

---

## T3: Minor Issues

### GT-10 | Clause 8.1 | [!] AMEND

**72-Hour Breach Notification May Be Slow**

**Contract Language:**

> Processor shall notify Controller of any Personal Data Breach without undue delay and in any event within seventy-two (72) hours of becoming aware of such breach.

**Analysis:**

- 72 hours meets GDPR minimum but is the maximum allowed
- May be too slow for high-risk breaches (financial data, health data)
- 'Without undue delay' qualifier is good but 72hr is backstop
- Should add 24-hour notification for high-severity breaches
- Should add interim notification for ongoing incidents

**Recommended Actions:**

1. Should add 24-hour notification for high-severity breaches
2. Should add interim notification for ongoing incidents

---

### GT-11 | Clause 7.2 | [!] AMEND

**All Audit Costs on Controller**

**Contract Language:**

> Audits shall be conducted with reasonable notice during normal business hours, no more than once per year, and at Controller's expense.

**Analysis:**

- Controller bears all audit expenses
- May discourage necessary oversight
- ❌ No obligation if issues found
- Should shift costs to Processor if deficiencies found
- Should add SOC 2 report option as alternative

**Recommended Actions:**

1. Should shift costs to Processor if deficiencies found
2. Should add SOC 2 report option as alternative

---

### GT-12 | Clause 10.1 | [!] AMEND

**Indefinite Duration**

**Contract Language:**

> This DPA shall remain in effect for the duration of the Principal Agreement and for as long as Processor processes Personal Data on behalf of Controller.

**Analysis:**

- DPA continues while processing occurs
- Appropriate structure but potentially indefinite
- Should clarify maximum retention periods
- Should add periodic review requirement

**Recommended Actions:**

1. Should clarify maximum retention periods
2. Should add periodic review requirement

---


# 3. Distribution Agreement

**Contract:** Distribution
**Parties:** Global Products Manufacturing Inc. (Supplier) ↔ [Unnamed Distributor] (Distributor)
**Reviewing for:** Distributor
**Contract ID:** `Distribution_GlobalPartners`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 6 | GT-01, GT-02, GT-03, GT-04, GT-05, GT-06 |
| T2 Material | 5 | GT-07, GT-08, GT-09, GT-10, GT-11 |
| T3 Minor | 2 | GT-12, GT-13 |

**Weighted Max Points:** 75

## T1: Critical Issues

### GT-01 | Clause 3.1 / Clause 3.2 | [X] AMEND

**Non-exclusive appointment with Supplier competition rights**

**Contract Language:**

> Supplier hereby appoints Distributor as a non-exclusive distributor of the Products within the Territory... Supplier reserves the right to: (a) sell Products directly to customers within the Territory; (b) appoint other distributors within the Territory; and (c) sell Products to customers outside the Territory who may resell such Products within the Territory.

**Analysis:**

- Non-exclusive distributor status
- Supplier can sell directly within Territory
- Supplier can appoint other distributors
- Cross-territory sales permitted (customers outside Territory can resell within)
- Distributor's investment in territory development unprotected
- Should negotiate exclusive territory OR exclusive product lines
- Limit or prohibit direct Supplier competition on Distributor-sourced leads

**Recommended Actions:**

1. Should negotiate exclusive territory OR exclusive product lines

---

### GT-02 | Clause 5.1 | [X] AMEND

**Unilateral price changes with no cap**

**Contract Language:**

> Distributor shall purchase Products at the prices set forth in Supplier's then-current price list. Supplier may modify prices upon sixty (60) days' prior written notice.

**Analysis:**

- Supplier can modify prices with only 60 days notice
- ❌ No cap on price increases
- ❌ No right to terminate if price unacceptable
- Distributor locked into minimum purchases at unknown future prices
- Should add price cap (CPI or 5% annual max)
- Longer notice period (90+ days)
- Right to terminate on material price increase (>10%)

**Recommended Actions:**

1. Should add price cap (CPI or 5% annual max)

---

### GT-03 | Clause 6.1 | [X] AMEND

**Mandatory minimum purchase with automatic breach trigger**

**Contract Language:**

> Distributor agrees to purchase a minimum of One Hundred Thousand Dollars ($100,000) of Products per calendar quarter during the Term of this Agreement. Failure to meet minimum purchase requirements for two (2) consecutive quarters shall constitute a material breach.

**Analysis:**

- $100K per quarter minimum ($400K/year)
- 2 consecutive misses = automatic material breach
- ❌ No cure period before breach declaration
- ❌ No good faith negotiation on shortfall
- ❌ No adjustment for market conditions or force majeure
- Should reduce minimum or make adjustable based on territory performance
- Add cure period (e.g., 60 days to make up shortfall)
- Add negotiation rights before breach declared

**Recommended Actions:**

1. Should reduce minimum or make adjustable based on territory performance
2. Add cure period (e.g., 60 days to make up shortfall)
3. Add negotiation rights before breach declared

---

### GT-04 | Clause 13.3 | [X] AMEND

**Asymmetric assignment rights**

**Contract Language:**

> Distributor may not assign this Agreement without Supplier's prior written consent.

**Analysis:**

- Distributor cannot assign without Supplier consent
- ❌ No restriction stated on Supplier assignment
- Supplier could assign to competitor or unfavorable party
- Blocks Distributor M&A or business sale
- Should have mutual assignment provisions
- Add M&A/affiliate exception for Distributor
- Add consent not to be unreasonably withheld

**Recommended Actions:**

1. Should have mutual assignment provisions
2. Add M&A/affiliate exception for Distributor
3. Add consent not to be unreasonably withheld

---

### GT-05 | Clause N/A | [X] ADD

**No indemnification clause - Distributor exposed to product claims**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No indemnification clause exists in contract. Articles 1-13 contain no indemnification provisions.

**Analysis:**

- ❌ No product liability indemnification from Supplier
- ❌ No IP infringement protection
- Distributor exposed to third-party claims for product defects
- Distributor has no control over product design or manufacturing
- Critical for physical goods distribution
- Should add Supplier indemnification for product defects, recalls
- Should add IP infringement indemnification
- Should cover defense costs and settlements

**Recommended Actions:**

1. Should add Supplier indemnification for product defects, recalls
2. Should add IP infringement indemnification
3. Should cover defense costs and settlements

---

### GT-06 | Clause 4.1 | [!] AMEND

**Supplier can reject purchase orders - no supply obligation**

**Contract Language:**

> Distributor shall submit purchase orders to Supplier in writing. Supplier shall accept or reject each purchase order within five (5) business days of receipt.

**Analysis:**

- Supplier can accept OR reject each purchase order
- Only 5 business days to respond
- ❌ No obligation to accept orders even within forecast
- Distributor commits to minimums but Supplier doesn't commit to supply
- Creates supply uncertainty
- Should require acceptance of orders within agreed capacity/forecast
- Add deemed acceptance if no rejection within period
- Add supply assurance for forecasted quantities

**Recommended Actions:**

1. Should require acceptance of orders within agreed capacity/forecast
2. Add deemed acceptance if no rejection within period
3. Add supply assurance for forecasted quantities

---

## T2: Material Issues

### GT-07 | Clause 10.2 | [!] AMEND

**Low liability cap for both parties**

**Contract Language:**

> NEITHER PARTY'S TOTAL LIABILITY SHALL EXCEED THE AMOUNT PAID BY DISTRIBUTOR TO SUPPLIER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.

**Analysis:**

- Cap at 12 months payments applies to BOTH parties
- May be insufficient for product liability or recalls
- ❌ No carve-outs for IP, willful misconduct, gross negligence
- ❌ No carve-outs for indemnification obligations
- Increase to 24+ months
- Add carve-outs for critical claims
- Consider higher cap for Supplier (product manufacturer)

**Recommended Actions:**

1. Increase to 24+ months
2. Add carve-outs for critical claims
3. Consider higher cap for Supplier (product manufacturer)

---

### GT-08 | Clause 4.2 | [!] AMEND

**FOB shipping terms shift all transit risk to Distributor**

**Contract Language:**

> Unless otherwise agreed in writing, all Products shall be delivered FOB Supplier's facility. Title and risk of loss shall pass to Distributor upon delivery to the carrier.

**Analysis:**

- Risk passes at Supplier facility
- Distributor bears all transit risk including damage, loss, delay
- Distributor pays shipping, freight, insurance, handling (4.3)
- Should negotiate DDP or CIF terms
- Require Supplier-arranged transit insurance
- Risk to pass at Distributor facility

**Recommended Actions:**

1. Should negotiate DDP or CIF terms
2. Require Supplier-arranged transit insurance

---

### GT-09 | Clause 7.2 | [!] AMEND

**Marketing approval required for all materials**

**Contract Language:**

> All advertising and promotional materials prepared by Distributor shall be submitted to Supplier for approval prior to use.

**Analysis:**

- ALL advertising must be submitted for approval
- ❌ No timeline for approval/rejection
- ❌ No deemed approval mechanism
- Could delay time-sensitive marketing
- Add deemed approval if no response within 10 business days
- Limit approval requirement to major campaigns only
- Pre-approve standard templates

**Recommended Actions:**

1. Add deemed approval if no response within 10 business days

---

### GT-10 | Clause 11.3 | [!] ADD

**Termination effects lack buyback and transition**

**Contract Language:**

> Upon termination: (a) all rights granted to Distributor shall terminate; (b) Distributor shall cease use of the Trademarks; (c) Distributor may sell remaining inventory for ninety (90) days.

**Analysis:**

- 90-day sell-off period (better than Reseller which has none)
- ❌ No inventory buyback right - stuck with unsold inventory after 90 days
- ❌ No transition assistance from Supplier
- ❌ No refund of prepaid amounts
- Rights terminate immediately except sell-off
- Should add Supplier buyback at cost for remaining inventory
- Add transition period for customer handover
- Add refund of prepaid but undelivered orders

**Recommended Actions:**

1. Should add Supplier buyback at cost for remaining inventory
2. Add transition period for customer handover
3. Add refund of prepaid but undelivered orders

---

### GT-11 | Clause 10.1 | [!] ADD

**Consequential Damages Exclusion Missing Critical Carve-Outs**

**Contract Language:**

> 10.1 NEITHER PARTY SHALL BE LIABLE TO THE OTHER FOR ANY INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES, INCLUDING WITHOUT LIMITATION LOST PROFITS OR LOST BUSINESS OPPORTUNITIES.

**Analysis:**

- Mutual exclusion of indirect/consequential damages
- Blocks recovery for lost profits from product defects or supply failures
- ❌ No carve-out for indemnification obligations
- ❌ No carve-out for breach of confidentiality
- ❌ No carve-out for willful misconduct or gross negligence
- ❌ No carve-out for IP infringement claims
- Distribution relationship involves significant opportunity costs
- Should add carve-outs for: confidentiality breach, IP infringement, willful misconduct, indemnification obligations

**Recommended Actions:**

1. Should add carve-outs for: confidentiality breach, IP infringement, willful misconduct, indemnification obligations

---

## T3: Minor Issues

### GT-12 | Clause 5.3 | [!] AMEND

**High late payment interest rate**

**Contract Language:**

> Any amounts not paid when due shall bear interest at the rate of one and one-half percent (1.5%) per month.

**Analysis:**

- 1.5% per month = 18% APR
- Above typical commercial rates (prime + 2-3%)
- ❌ No exclusion for disputed amounts
- Should reduce to 1% or prime + margin
- Exclude disputed amounts from interest
- Add grace period before interest accrues

**Recommended Actions:**

1. Should reduce to 1% or prime + margin
2. Add grace period before interest accrues

---

### GT-13 | Clause 3.3 | [!] AMEND

**Territory restriction on outside sales**

**Contract Language:**

> Distributor shall not actively solicit sales or establish any branch, warehouse, or distribution centre outside the Territory without Supplier's prior written consent.

**Analysis:**

- Cannot actively solicit outside Territory
- Cannot establish operations outside Territory without consent
- Standard distribution restriction
- May limit growth opportunities
- Passive sales outside Territory should be permitted

---


# 4. Joint Venture MOU

**Contract:** JV
**Parties:** InnovateTech Solutions Corp. (Party A) ↔ Quantum Dynamics LLC (Party B)
**Reviewing for:** Quantum Dynamics LLC (Party B)
**Contract ID:** `JV_MOU_InnovateTech`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 5 | GT-01, GT-02, GT-03, GT-04, GT-05 |
| T2 Material | 10 | GT-06, GT-07, GT-08, GT-09, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15 |
| T3 Minor | 3 | GT-16, GT-17, GT-18 |

**Weighted Max Points:** 93

## T1: Critical Issues

### GT-01 | Clause 8.1 | [X] ADD

**No Deadlock Resolution - Article 8 [Reserved]**

**Contract Language:**

> 8.1 [Reserved]

**Analysis:**

- Article 8 Deadlock is entirely [Reserved]
- ❌ No mechanism to break 50/50 deadlock on Steering Committee
- Combined with 4.1 unanimous consent creates trap
- Parties can be indefinitely stuck
- Should add escalation: mediation → swing vote → buyout
- Consider buy-sell (shotgun) provision

**Recommended Actions:**

1. Should add escalation: mediation → swing vote → buyout
2. Consider buy-sell (shotgun) provision

---

### GT-02 | Clause N/A | [X] ADD

**No Exit/Buyout Rights**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No exit or buyout provisions exist in contract

**Analysis:**

- ❌ No put/call options
- ❌ No buyout mechanism at fair market value
- ❌ No exit path defined
- 5-year term with no early exit
- Should add put right after Year 3
- Should add call right on change of control

**Recommended Actions:**

1. Should add put right after Year 3
2. Should add call right on change of control

---

### GT-03 | Clause 4.1 | [!] AMEND

**Unanimous Consent + No Tiebreaker**

**Contract Language:**

> All material decisions regarding the Joint Venture, including but not limited to annual budgets, capital expenditures exceeding $50,000, entry into material contracts, and changes to the business plan, shall require the unanimous written consent of both Parties.

**Analysis:**

- All material decisions require unanimous consent
- 50/50 structure makes deadlock inevitable
- Includes budgets, contracts, business plan changes
- Combined with [Reserved] deadlock = paralysis risk
- Should add tiered decision rights
- Consider supermajority for some decisions

**Recommended Actions:**

1. Should add tiered decision rights
2. Consider supermajority for some decisions

---

### GT-04 | Clause 6.2 | [!] AMEND

**Developed IP Consent Lock-Up**

**Contract Language:**

> All Developed IP shall be jointly owned by the Parties in equal shares. Neither Party may license or transfer Developed IP to third parties without the consent of the other Party.

**Analysis:**

- Neither party can license/transfer Developed IP without consent
- Creates commercialization veto
- Blocks market opportunities if parties disagree
- Combined with deadlock [Reserved] = IP stuck
- Should add licensing rights with revenue share
- Should add buyout right for IP

**Recommended Actions:**

1. Should add licensing rights with revenue share
2. Should add buyout right for IP

---

### GT-05 | Clause N/A | [X] ADD

**No Limitation of Liability**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No limitation of liability clause exists in contract Articles 1-12

**Analysis:**

- ❌ No cap on damages between parties
- Exposes parties to unlimited liability
- ❌ Fundamental risk allocation missing
- Should add mutual liability cap
- Should add consequential damages exclusion
- Should add carve-outs for IP, fraud

**Recommended Actions:**

1. Should add mutual liability cap
2. Should add consequential damages exclusion
3. Should add carve-outs for IP, fraud

---

## T2: Material Issues

### GT-06 | Clause 9.1 | [!] DELETE

**Broad Post-Term Non-Compete**

**Contract Language:**

> During the Term and for a period of two (2) years thereafter, neither Party shall, directly or indirectly, engage in any business that competes with the Joint Venture's quantum AI business within the Territory without the prior written consent of the other Party.

**Analysis:**

- 2-year post-term non-compete in quantum AI
- Applies even if terminated for cause by other party
- Broad geographic scope ('Territory' undefined in contract)
- Could block core business for Party B (quantum computing)
- Should narrow scope to specific products/markets
- Should exclude wrongful termination scenarios

**Recommended Actions:**

1. Should narrow scope to specific products/markets
2. Should exclude wrongful termination scenarios

---

### GT-07 | Clause 3.4 | [!] AMEND

**Capital Call Dilution Risk**

**Contract Language:**

> Additional capital contributions may be required upon approval of both Parties. Any Party failing to make a required capital contribution shall have its ownership interest diluted proportionately.

**Analysis:**

- Failure to fund capital call = proportionate dilution
- ❌ No dispute mechanism before dilution
- ❌ No cure period
- Could be used strategically to dilute partner
- Should add cure period (30-60 days)
- Should add arbitration before dilution

**Recommended Actions:**

1. Should add cure period (30-60 days)
2. Should add arbitration before dilution

---

### GT-08 | Clause 6.3 | [!] AMEND

**Improvement Ownership Unclear on Termination**

**Contract Language:**

> Any improvements to a Party's Contributed IP that are developed using Joint Venture resources shall be owned by the contributing Party, subject to a perpetual license to the Joint Venture.

**Analysis:**

- Improvements to Contributed IP owned by contributor
- JV gets perpetual license during Term
- What happens to license on termination unclear
- 10.4 silent on improvement licenses
- Should clarify post-termination license scope

**Recommended Actions:**

1. Should clarify post-termination license scope

---

### GT-09 | Clause 4.3 | [!] AMEND

**General Manager Authority Unbounded**

**Contract Language:**

> The Parties shall jointly appoint a General Manager to oversee the day-to-day operations of the Joint Venture. The General Manager shall have authority to make operational decisions within approved budgets and policies.

**Analysis:**

- GM has operational authority within approved budgets
- ❌ No reporting requirements specified
- ❌ No removal process defined
- ❌ No oversight mechanism
- Should add quarterly reporting
- Should add removal process

**Recommended Actions:**

1. Should add quarterly reporting
2. Should add removal process

---

### GT-10 | Clause 6.1 | [!] AMEND

**Contributed IP License Gaps**

**Contract Language:**

> Each Party hereby grants to the Joint Venture a non-exclusive, royalty-free license to use its Contributed IP for the Purpose during the Term.

**Analysis:**

- Non-exclusive, royalty-free license for the Purpose during the Term
- License scope limited to 'the Purpose'
- ❌ No wind-down period post-termination
- ❌ No sublicensing restrictions to third parties
- Should add transition period
- Should clarify sublicensing rules

**Recommended Actions:**

1. Should add transition period
2. Should clarify sublicensing rules

---

### GT-11 | Clause 10.4 | [!] AMEND

**Termination IP Allocation Undefined**

**Contract Language:**

> Upon termination: ... (b) Developed IP shall be divided or licensed as agreed...

**Analysis:**

- Developed IP divided 'as agreed' - no fallback
- If parties can't agree, IP stuck
- Combined with deadlock [Reserved] = no resolution
- Should add default allocation (50/50 license-back)
- Should add buyout at FMV

**Recommended Actions:**

1. Should add default allocation (50/50 license-back)
2. Should add buyout at FMV

---

### GT-12 | Clause N/A | [!] ADD

**No Indemnification Regime**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No indemnification provisions exist in contract

**Analysis:**

- ❌ No mutual indemnity for breach
- ❌ No IP infringement indemnity
- ❌ No third-party claims coverage
- Should add mutual indemnification
- Should add IP warranties and indemnity

**Recommended Actions:**

1. Should add mutual indemnification
2. Should add IP warranties and indemnity

---

### GT-13 | Clause N/A | [!] ADD

**No Change of Control Provision**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No change of control provision exists in contract

**Analysis:**

- Party A could be acquired by competitor
- ❌ No notice requirement on change of control
- ❌ No termination rights
- ❌ No buyout option at FMV
- Should add CoC notice and consent
- Should add termination/buyout rights

**Recommended Actions:**

1. Should add CoC notice and consent
2. Should add termination/buyout rights

---

### GT-14 | Clause N/A | [!] ADD

**No Data Protection / Privacy Clause**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No data protection or privacy provisions exist in contract

**Analysis:**

- JV involves quantum AI technology development
- May process personal data (employee, researcher, customer data)
- ❌ No GDPR/CCPA compliance requirements stated
- ❌ No data security obligations between parties
- Should add data protection clause if personal data processed
- Should clarify controller/processor roles

**Recommended Actions:**

1. Should add data protection clause if personal data processed
2. Should clarify controller/processor roles

---

### GT-15 | Clause 7.2 | [!] AMEND

**Confidentiality Survival Inadequate for Trade Secrets**

**Contract Language:**

> 7.2 Survival. The confidentiality obligations shall survive termination of this MOU for a period of five (5) years.

**Analysis:**

- 5-year survival period for confidentiality
- Quantum technology trade secrets have indefinite commercial value
- 5 years insufficient to protect core IP
- Should add perpetual protection for trade secrets
- Should differentiate trade secrets from general confidential info

**Recommended Actions:**

1. Should add perpetual protection for trade secrets
2. Should differentiate trade secrets from general confidential info

---

## T3: Minor Issues

### GT-16 | Clause 5.2 | [!] AMEND

**Vague Reserve Rights**

**Contract Language:**

> Distributions shall be made quarterly, subject to the retention of reasonable reserves for working capital and anticipated expenses as determined by the Steering Committee.

**Analysis:**

- 'Reasonable reserves' determined by Steering Committee
- Could delay distributions indefinitely
- Subject to deadlock risk
- Should add cap on reserves (% of profits)

**Recommended Actions:**

1. Should add cap on reserves (% of profits)

---

### GT-17 | Clause 11.1-11.3 | [!] AMEND

**Multi-Step Dispute Resolution**

**Contract Language:**

> 11.1: The Parties shall attempt to resolve any dispute through good faith negotiations... 11.2: If negotiation fails within thirty (30) days, the Parties shall submit the dispute to mediation. 11.3: If mediation fails, disputes shall be resolved by binding arbitration in San Francisco, California.

**Analysis:**

- Negotiation (no timeline) → Mediation (30 days) → Arbitration
- Could delay urgent resolution
- San Francisco venue
- Consider adding emergency arbitration option

**Recommended Actions:**

1. Consider adding emergency arbitration option

---

### GT-18 | Clause 1.4 | [!] AMEND

**No Conditions Precedent for JV Entity**

**Contract Language:**

> "JV Entity" means the legal entity to be formed by the Parties to conduct the business of the Joint Venture, if the Parties elect to form such entity.

**Analysis:**

- JV Entity formation is optional ('if the Parties elect')
- ❌ No timeline for entity formation decision
- Capital and IP could flow before entity formed
- Should add formation timeline
- Should add conditions precedent

**Recommended Actions:**

1. Should add formation timeline
2. Should add conditions precedent

---


# 5. IP License Agreement

**Contract:** IP License
**Parties:** Innovate IP Holdings Ltd. (Licensor) ↔ TechPro Industries Corp. (Licensee)
**Reviewing for:** TechPro Industries Corp. (Licensee)
**Contract ID:** `License_IPHoldings`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 4 | GT-01, GT-02, GT-03, GT-04 |
| T2 Material | 7 | GT-05, GT-06, GT-07, GT-08, GT-09, GT-10, GT-11 |
| T3 Minor | 4 | GT-12, GT-13, GT-14, GT-15 |

**Weighted Max Points:** 71

## T1: Critical Issues

### GT-01 | Clause 3.2 | [X] AMEND

**Improvements owned by Licensor - loses R&D investment**

**Contract Language:**

> Improvements to the Licensed IP developed by Licensee shall be owned by Licensor.

**Analysis:**

- All improvements to Licensed IP developed by Licensee become Licensor property
- Licensee loses R&D investment entirely
- Creates disincentive to innovate
- Should negotiate Licensee ownership of improvements
- Alternative: Joint ownership with license-back
- Licensor should pay for Licensee-developed improvements

**Recommended Actions:**

1. Should negotiate Licensee ownership of improvements

---

### GT-02 | Clause 9.2 | [!] AMEND

**AS-IS disclaimer with limited warranties**

**Contract Language:**

> Licensor represents it has the right to grant the license and, to its knowledge, the Licensed IP does not infringe third-party rights. EXCEPT AS EXPRESSLY SET FORTH HEREIN, THE LICENSED IP IS PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND.

**Analysis:**

- Licensed IP provided AS-IS
- Only warranty is 9.1 (right to grant + non-infringement 'to knowledge')
- 'To knowledge' qualifier weakens non-infringement warranty
- ❌ No express warranty of functionality or commercial viability
- ❌ No warranty of fitness for Field of Use
- Should strengthen to unconditional non-infringement
- Add functionality warranty for patent claims

**Recommended Actions:**

1. Should strengthen to unconditional non-infringement
2. Add functionality warranty for patent claims

---

### GT-03 | Clause N/A | [X] ADD

**No IP infringement indemnification from Licensor**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No indemnification provision exists. Contract contains only 9.1 warranty ('to its knowledge, the Licensed IP does not infringe') but no indemnification for breach.

**Analysis:**

- ❌ No indemnification clause exists in the agreement
- Licensee exposed to third-party infringement claims
- If Licensed IP infringes, Licensee bears defense costs and damages
- Standard provision in commercial IP licenses
- Should add Licensor indemnity for IP infringement claims
- Include defense obligation, settlement control, and hold-harmless

**Recommended Actions:**

1. Should add Licensor indemnity for IP infringement claims

---

### GT-04 | Clause 9.1 | [X] AMEND

**Non-infringement warranty qualified 'to knowledge' - inadequate for IP license**

**Contract Language:**

> 9.1 Licensor represents it has the right to grant the license and, to its knowledge, the Licensed IP does not infringe third-party rights.

**Analysis:**

- 9.1 only warrants non-infringement 'to Licensor's knowledge'
- Knowledge qualifier shifts due diligence burden to Licensee
- Licensor should know their own IP portfolio and freedom to operate
- If Licensee faces infringement claim, 'knowledge' defense is worthless
- Should be unconditional non-infringement warranty
- Or require Licensor to have conducted clearance search
- Critical for commercial IP license - T1 issue

**Recommended Actions:**

1. Should be unconditional non-infringement warranty

---

## T2: Material Issues

### GT-05 | Clause 12.2 | [!] AMEND

**Licensor liability cap too low**

**Contract Language:**

> LICENSOR'S TOTAL LIABILITY SHALL NOT EXCEED THE ROYALTIES PAID IN THE TWELVE MONTHS PRECEDING THE CLAIM.

**Analysis:**

- Licensor liability capped at 12 months royalties only
- Royalties may be low in early years (Year 1 = $0 running royalty possible)
- ❌ No carve-outs for IP title failure
- ❌ No carve-outs for willful misconduct
- Increase to 24+ months or fixed minimum floor
- Add carve-outs for IP warranty breach

**Recommended Actions:**

1. Increase to 24+ months or fixed minimum floor
2. Add carve-outs for IP warranty breach

---

### GT-06 | Clause 4.1 | [!] AMEND

**Mandatory minimum royalty regardless of sales**

**Contract Language:**

> Beginning in Year 2, Licensee shall pay minimum annual royalty of $250,000, regardless of actual Net Sales. Running royalties shall be credited against this minimum.

**Analysis:**

- $250K minimum royalty from Year 2
- Payable regardless of actual Net Sales
- Running royalties credited against minimum
- Creates significant fixed cost even if IP proves uncommercial
- Should reduce minimum amount or phase in gradually
- Add adjustment for market conditions or force majeure
- Allow credit for marketing/development expenses

**Recommended Actions:**

1. Should reduce minimum amount or phase in gradually
2. Add adjustment for market conditions or force majeure

---

### GT-07 | Clause 12.1 | [!] AMEND

**Consequential damages exclusion**

**Contract Language:**

> NEITHER PARTY SHALL BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES.

**Analysis:**

- Neither party liable for indirect/consequential damages
- Blocks recovery for lost profits if IP fails or is invalid
- Should add carve-outs for IP title failure
- Carve-outs for willful misconduct
- Carve-outs for breach of exclusivity

**Recommended Actions:**

1. Should add carve-outs for IP title failure

---

### GT-08 | Clause N/A | [!] ADD

**No termination for convenience - 10-year lock-in**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> This Agreement shall continue for ten (10) years from the Effective Date, unless earlier terminated. [No termination for convenience provision exists]

**Analysis:**

- 10-year term with no TfC right
- Only exit is termination for cause (60-day cure)
- Locked in even if IP proves commercially unviable
- Should add TfC with 12-month notice after Year 3
- Consider annual opt-out after initial commitment period
- Allow exit if minimum royalties become unsustainable

**Recommended Actions:**

1. Should add TfC with 12-month notice after Year 3
2. Consider annual opt-out after initial commitment period

---

### GT-09 | Exhibit A | [X] AMEND

**Licensed IP schedule (Exhibit A) not attached - undefined scope**

**Contract Language:**

> 1.2 'Licensed IP' means the patents, trademarks, trade secrets, and proprietary technology described in Exhibit A. [...] EXHIBIT A - LICENSED INTELLECTUAL PROPERTY [Patent and trademark schedule to be attached]

**Analysis:**

- Exhibit A is blank - states '[Patent and trademark schedule to be attached]'
- Licensed IP definition (1.2) references Exhibit A for scope
- Client cannot know what IP they are licensing
- Value of exclusivity cannot be assessed
- Creates fundamental uncertainty about contract scope
- Must require populated schedule before execution

---

### GT-10 | Exhibit B | [X] AMEND

**Territory definition (Exhibit B) not attached - exclusivity meaningless**

**Contract Language:**

> 2.1 Grant. Licensor grants Licensee an exclusive license to use the Licensed IP within the Field of Use and Territory during the Term. [...] EXHIBIT B - TERRITORY [Territory definition to be attached]

**Analysis:**

- Exhibit B is blank - states '[Territory definition to be attached]'
- License grant (2.1) is exclusive within 'Territory'
- Exclusivity has no meaning without defined geographic scope
- Cannot assess market value or competitive protection
- Must require populated schedule before execution

---

### GT-11 | Clause 8.1 | [!] AMEND

**Confidentiality Survival Inadequate for Trade Secrets**

**Contract Language:**

> 8.1 Confidentiality. Each Party shall maintain the confidentiality of all Confidential Information. This obligation survives termination for five (5) years.

**Analysis:**

- 5-year survival period for confidentiality
- IP license involves trade secrets, manufacturing know-how, proprietary technology
- Trade secrets have indefinite commercial value
- 5 years insufficient for competitive protection post-termination
- Should add perpetual protection for trade secrets
- Should differentiate trade secrets from general confidential info

**Recommended Actions:**

1. Should add perpetual protection for trade secrets
2. Should differentiate trade secrets from general confidential info

---

## T3: Minor Issues

### GT-12 | Clause 5.1 | [!] AMEND

**High royalty rate**

**Contract Language:**

> Licensee shall pay Licensor a royalty equal to ten percent (10%) of Net Sales of Licensed Products, payable quarterly within thirty (30) days following the end of each calendar quarter.

**Analysis:**

- 10% of Net Sales is above typical rates for consumer electronics (usually 2-5%)
- May compress Licensee margins significantly
- Should negotiate lower rate or tiered structure
- Consider volume discounts at higher sales levels
- Review industry benchmarks for comparable IP

**Recommended Actions:**

1. Should negotiate lower rate or tiered structure
2. Consider volume discounts at higher sales levels

---

### GT-13 | Clause 2.2 | [!] AMEND

**Sublicensing requires Licensor consent**

**Contract Language:**

> Licensee may grant sublicenses with Licensor's prior written consent.

**Analysis:**

- Prior written consent required for any sublicenses
- Could limit business model flexibility
- May restrict contract manufacturing arrangements
- Should add automatic affiliate sublicensing right
- Consent not to be unreasonably withheld or delayed
- Pre-approved sublicensee categories for manufacturing

**Recommended Actions:**

1. Should add automatic affiliate sublicensing right

---

### GT-14 | Clause 5.2 | [!] AMEND

**Non-refundable upfront fee**

**Contract Language:**

> Upon execution, Licensee shall pay a non-refundable upfront license fee of $500,000.

**Analysis:**

- $500K upfront license fee is non-refundable
- Significant sunk cost if IP proves unusable
- Standard for exclusive IP licenses but still a risk
- Could negotiate partial refund if IP fails validity challenge
- Consider escrow until first commercial use

**Recommended Actions:**

1. Consider escrow until first commercial use

---

### GT-15 | Clause 7.1 | [!] AMEND

**Audit cost-shifting threshold favors Licensor**

**Contract Language:**

> Licensor may audit Licensee's books and records once per year upon reasonable notice. Licensor bears audit costs unless underpayment exceeds 5%, in which case Licensee bears costs.

**Analysis:**

- Licensor can audit annually
- Licensee bears audit costs if underpayment exceeds 5%
- 5% threshold is relatively low
- Should increase threshold to 10%
- Add cap on audit frequency
- Require reasonable advance notice

**Recommended Actions:**

1. Should increase threshold to 10%
2. Add cap on audit frequency
3. Require reasonable advance notice

---


# 6. Partnership Agreement

**Contract:** Partnership
**Parties:** Venture Alliance Capital LLC (Partner A) ↔ Growth Dynamics Partners LP (Partner B)
**Reviewing for:** Growth Dynamics Partners LP (Partner B)
**Contract ID:** `Partnership_VentureAlliance`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 6 | GT-01, GT-02, GT-03, GT-04, GT-05, GT-06 |
| T2 Material | 4 | GT-07, GT-08, GT-09, GT-10 |
| T3 Minor | 2 | GT-11, GT-12 |

**Weighted Max Points:** 70

## T1: Critical Issues

### GT-01 | Clause 10.1 | [X] ADD

**No Exit/Buyout Mechanism - Article 10.1 [Reserved]**

**Contract Language:**

> 10.1 [Reserved]

**Analysis:**

- Section 10.1 is [Reserved]
- ❌ No exit rights defined
- ❌ No buyout provisions
- ❌ No liquidity mechanism
- 5-year term with no early exit path
- Should add put/call rights
- Should add buyout at FMV

**Recommended Actions:**

1. Should add put/call rights
2. Should add buyout at FMV

---

### GT-02 | Clause 4.1 | [!] AMEND

**Unanimous Consent Creates Deadlock Risk**

**Contract Language:**

> The Partners shall jointly manage the Partnership Activities. Major decisions require unanimous consent of both Partners.

**Analysis:**

- All major decisions require unanimous consent
- Creates veto power for either partner
- ❌ No tie-breaker or escalation mechanism
- Combined with [Reserved] exit = trapped
- Should add escalation path
- Should add swing vote mechanism

**Recommended Actions:**

1. Should add escalation path
2. Should add swing vote mechanism

---

### GT-03 | Clause 3.3 | [X] AMEND

**Default Provisions Cross-Reference Error**

**Contract Language:**

> A Partner that fails to fund a capital call shall be subject to the default provisions in Section 10.3. [But Section 10.3 is Effect of Termination]

**Analysis:**

- References 'default provisions in Section 10.3'
- But 10.3 is Effect of Termination, not default provisions
- ❌ No actual default consequences defined
- Could fail to fund without consequence
- Should add actual default provisions
- Should fix cross-reference

**Recommended Actions:**

1. Should add actual default provisions
2. Should fix cross-reference

---

### GT-04 | Clause 6.1 | [!] AMEND

**Fixed 50/50 Split Regardless of Capital**

**Contract Language:**

> All profits and losses from Co-Investments shall be allocated fifty percent (50%) to Partner A and fifty percent (50%) to Partner B, regardless of the relative capital contributions made by each Partner to any particular Co-Investment.

**Analysis:**

- Equal profit/loss split regardless of contributions
- Partner contributing more capital gets same return
- Economic misalignment with capital at risk
- Should allocate returns pro rata to capital
- Or add preferred return to larger contributor

**Recommended Actions:**

1. Should allocate returns pro rata to capital

---

### GT-05 | Clause N/A | [X] ADD

**No Limitation of Liability**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No limitation of liability clause exists in contract Articles 1-14

**Analysis:**

- ❌ No cap on damages between partners
- Unlimited liability exposure
- ❌ Fundamental risk allocation missing
- Should add mutual liability cap
- Should add consequential damages exclusion

**Recommended Actions:**

1. Should add mutual liability cap
2. Should add consequential damages exclusion

---

### GT-06 | Clause N/A | [X] ADD

**No Indemnification Provisions**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No indemnification provisions exist in contract

**Analysis:**

- ❌ No mutual indemnification for breach
- ❌ No coverage for third-party claims
- ❌ No protection for regulatory issues
- Should add mutual indemnification
- Should add third-party claim procedures

**Recommended Actions:**

1. Should add mutual indemnification
2. Should add third-party claim procedures

---

## T2: Material Issues

### GT-07 | Clause 12.3 | [!] AMEND

**Continuation Post-Termination Indefinite**

**Contract Language:**

> Upon termination, the Partners shall continue to manage existing Co-Investments until liquidation or transfer, sharing profits and losses per Section 6.1.

**Analysis:**

- Must continue managing existing investments until liquidation
- Could be years before all investments exit
- Forced continued relationship after termination
- Should add maximum wind-down period
- Should add buyout right for portfolio interests

**Recommended Actions:**

1. Should add maximum wind-down period
2. Should add buyout right for portfolio interests

---

### GT-08 | Clause N/A | [!] ADD

**No Information Rights or Reporting**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> The Investment Committee shall meet at least monthly to review deal pipeline and portfolio performance. [No formal reporting provisions exist]

**Analysis:**

- 4.3 requires monthly Investment Committee meetings
- But no formal reporting requirements
- ❌ No portfolio financial statements requirement
- ❌ No material event notices
- ❌ No inspection rights
- Should add quarterly portfolio reports
- Should add material event notification

**Recommended Actions:**

1. Should add quarterly portfolio reports
2. Should add material event notification

---

### GT-09 | Clause 9.1 | [!] AMEND

**Confidentiality Survival Inadequate for Trade Secrets**

**Contract Language:**

> 9.1 Confidentiality Obligations. Each Partner shall maintain strict confidentiality regarding deal flow, investment terms, portfolio company information, and the terms of this Agreement. This obligation survives termination for five (5) years.

**Analysis:**

- 5-year survival period for confidentiality
- Investment partnership involves proprietary deal flow and strategies
- Trade secrets (investment thesis, portfolio analysis) have indefinite value
- 5 years may be insufficient for competitive protection
- Should add perpetual protection for trade secrets
- Should differentiate trade secrets from general confidential info

**Recommended Actions:**

1. Should add perpetual protection for trade secrets
2. Should differentiate trade secrets from general confidential info

---

### GT-10 | Clause 10.2 | [!] AMEND

**Non-Renewal Notice Period Too Short for Partnership Wind-Down**

**Contract Language:**

> This Agreement shall automatically renew for successive one (1) year periods unless either Partner provides written notice of non-renewal at least ninety (90) days prior to the end of the then-current term.

**Analysis:**

- 90-day notice required for non-renewal
- Partnership has complex wind-down requirements (existing investments)
- 90 days insufficient to prepare for orderly transition
- Combined with indefinite post-termination continuation (12.3) creates planning uncertainty
- Should extend to 180 days minimum for investment partnership
- Should add transition planning requirements
- Should specify wind-down procedures in notice period

**Recommended Actions:**

1. Should extend to 180 days minimum for investment partnership
2. Should add transition planning requirements
3. Should specify wind-down procedures in notice period

---

## T3: Minor Issues

### GT-11 | Clause 5.3 | [!] AMEND

**60-Day Exclusivity Period May Be Insufficient**

**Contract Language:**

> Once a Target Company is presented to the Investment Committee, neither Partner may pursue an independent investment in such company for sixty (60) days.

**Analysis:**

- 60 days may be too short for complex due diligence
- ❌ No consequences for breach of exclusivity
- ❌ No post-period disclosure requirements
- Should extend to 90-120 days
- Should add penalty for breach

**Recommended Actions:**

1. Should extend to 90-120 days
2. Should add penalty for breach

---

### GT-12 | Clause 11.2 | [!] AMEND

**Non-Solicitation Standard Term**

**Contract Language:**

> Neither Partner shall solicit or hire employees of the other Partner during the Term and for one (1) year thereafter.

**Analysis:**

- 1-year post-term restriction on hiring partner employees
- Mutual and limited scope
- Standard provision
- Consider whether needed at all

**Recommended Actions:**

1. Consider whether needed at all

---


# 7. Reseller Agreement

**Contract:** Reseller
**Parties:** CloudTech Solutions Inc. (Vendor) ↔ Pacific Tech Distributors LLC (Reseller)
**Reviewing for:** Pacific Tech Distributors LLC (Reseller)
**Contract ID:** `Reseller_TechDistributors`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 4 | GT-01, GT-02, GT-03, GT-04 |
| T2 Material | 7 | GT-05, GT-06, GT-07, GT-08, GT-09, GT-10, GT-11 |
| T3 Minor | 2 | GT-12, GT-13 |

**Weighted Max Points:** 69

## T1: Critical Issues

### GT-01 | Clause 4.1 | [X] AMEND

**Unilateral price and discount changes with short notice**

**Contract Language:**

> Vendor may modify prices, discounts, or product offerings at any time upon thirty (30) days' prior written notice to Reseller. Price changes shall apply to orders placed after the effective date of such changes.

**Analysis:**

- Vendor can modify prices, discounts, or product offerings
- Only 30 days prior notice required
- ❌ No cap on increases
- ❌ No right to terminate on unacceptable increase
- Should extend notice to 60-90 days
- Add price cap (CPI or fixed %)
- Right to terminate if increase unacceptable

**Recommended Actions:**

1. Should extend notice to 60-90 days
2. Add price cap (CPI or fixed %)

---

### GT-02 | Clause 9.1 | [X] AMEND

**No termination for convenience during Term**

**Contract Language:**

> This Agreement shall commence on the Effective Date and continue for an initial term of two (2) years. Thereafter, this Agreement shall automatically renew for successive one (1) year periods unless either Party provides written notice of non-renewal at least ninety (90) days prior to the end of the then-current term. Neither Party may terminate this Agreement for convenience during the Term.

**Analysis:**

- Neither party can terminate for convenience during 2-year initial term
- Locked in even if relationship not working
- Should add mutual TfC right on reasonable notice
- Consider 30-90 day notice for convenience
- Allow termination for business reasons

**Recommended Actions:**

1. Should add mutual TfC right on reasonable notice
2. Consider 30-90 day notice for convenience

---

### GT-03 | Clause 11.2 | [!] AMEND

**Broad warranty disclaimer**

**Contract Language:**

> Vendor warrants that the Products will perform substantially as described in documentation. Vendor's warranty obligations to End Users are set forth in the EULA. EXCEPT AS EXPRESSLY SET FORTH HEREIN, VENDOR MAKES NO WARRANTIES OF ANY KIND.

**Analysis:**

- Vendor disclaims all warranties beyond basic performance
- Only warrants 'substantially as described in documentation'
- ❌ No merchantability, fitness, non-infringement
- Should add express warranties
- Non-infringement warranty important for software
- Specific warranty period needed

**Recommended Actions:**

1. Should add express warranties

---

### GT-04 | Clause N/A | [X] ADD

**No indemnification clause**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No indemnification clause exists in contract

**Analysis:**

- ❌ No IP infringement indemnification from Vendor
- ❌ No product liability indemnification
- Reseller exposed to End User claims for software defects
- Critical for software resale - End Users will sue Reseller
- Should add Vendor indemnification for IP claims
- Add indemnification for product defects and EULA breaches

**Recommended Actions:**

1. Should add Vendor indemnification for IP claims
2. Add indemnification for product defects and EULA breaches

---

## T2: Material Issues

### GT-05 | Clause 12.2 | [!] AMEND

**Vendor liability cap too low**

**Contract Language:**

> VENDOR'S TOTAL LIABILITY SHALL NOT EXCEED AMOUNTS PAID BY RESELLER IN THE TWELVE MONTHS PRECEDING THE CLAIM.

**Analysis:**

- Vendor liability capped at 12 months of Reseller purchases
- ❌ No carve-outs for IP infringement, willful misconduct
- May be insufficient for significant claims
- Increase to 24+ months
- Add carve-outs for critical claims
- Consider minimum floor amount

**Recommended Actions:**

1. Increase to 24+ months
2. Add carve-outs for critical claims
3. Consider minimum floor amount

---

### GT-06 | Clause 2.1 / Clause 2.2 | [!] AMEND

**Non-exclusive appointment with Vendor direct sales**

**Contract Language:**

> Vendor hereby appoints Reseller as a non-exclusive, authorised reseller of the Products within the Territory... Vendor reserves the right to sell Products directly and to appoint other resellers within the Territory.

**Analysis:**

- Non-exclusive reseller status
- Vendor reserves right to sell directly
- Vendor can appoint other resellers
- Reseller investment not protected
- Should negotiate exclusive territory or customer segment
- Limit direct Vendor competition on Reseller-sourced leads

**Recommended Actions:**

1. Should negotiate exclusive territory or customer segment

---

### GT-07 | Clause 8.1 | [!] AMEND

**Sales reports require End User information**

**Contract Language:**

> Reseller shall provide quarterly reports detailing Products sold, End User information, and sales pipeline. Reports are due within fifteen (15) days after each quarter end.

**Analysis:**

- Quarterly reports must include End User information
- Sales pipeline disclosure required
- Privacy/data protection concerns
- Could enable Vendor to go direct
- Limit to aggregate data
- Add confidentiality for End User data

**Recommended Actions:**

1. Add confidentiality for End User data

---

### GT-08 | Clause 12.1 | [!] AMEND

**Consequential damages exclusion**

**Contract Language:**

> NEITHER PARTY SHALL BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES.

**Analysis:**

- Neither party liable for indirect/consequential damages
- Blocks recovery for lost profits, business interruption
- Should add carve-outs for IP infringement
- Carve-outs for willful misconduct
- Carve-outs for confidentiality breaches

**Recommended Actions:**

1. Should add carve-outs for IP infringement

---

### GT-09 | Clause 9.3 | [X] AMEND

**Termination effects - no sell-off period**

**Contract Language:**

> Upon termination: (a) Reseller shall cease marketing and selling Products; (b) Reseller shall pay all outstanding amounts; (c) trademark licenses shall terminate.

**Analysis:**

- Reseller must cease marketing and selling IMMEDIATELY
- Must pay all outstanding amounts
- ❌ NO inventory sell-off period (unlike Distribution/License which have 90 days)
- ❌ No transition assistance
- Should add 90-day inventory sell-off
- Add transition support and customer handover

**Recommended Actions:**

1. Should add 90-day inventory sell-off
2. Add transition support and customer handover

---

### GT-10 | Clause N/A | [!] ADD

**No Data Protection / Privacy Clause**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No data protection or privacy provisions exist in contract. Note: 8.1 requires Reseller to report 'End User information' to Vendor.

**Analysis:**

- Reseller receives End User information (8.1)
- May handle End User personal data in sales process
- ❌ No GDPR/CCPA compliance requirements
- ❌ No data security obligations from Vendor
- Should add data protection clause
- Should clarify data handling responsibilities

**Recommended Actions:**

1. Should add data protection clause
2. Should clarify data handling responsibilities

---

### GT-11 | Clause 7.2 | [!] ADD

**Support SLAs Missing - No Service Level Commitments**

**Contract Language:**

> 7.2 Vendor shall provide technical support for the Products in accordance with Vendor's then-current support policies. [No SLA metrics defined]

**Analysis:**

- 7.2 references Vendor support but no SLA defined
- ❌ No response time commitments
- ❌ No resolution time targets
- ❌ No escalation path for critical issues
- Reseller cannot make commitments to End Users
- Should add tiered SLA (critical/high/medium/low)
- Should add remedies for SLA breach (credits, termination right)

**Recommended Actions:**

1. Should add tiered SLA (critical/high/medium/low)
2. Should add remedies for SLA breach (credits, termination right)

---

## T3: Minor Issues

### GT-12 | Clause 5.1 | [!] AMEND

**High late payment interest rate**

**Contract Language:**

> Reseller shall pay all invoices within thirty (30) days of invoice date. Late payments bear interest at 1.5% per month.

**Analysis:**

- 1.5% per month = 18% APR
- Above typical commercial rates
- Should reduce to 1% or prime + margin
- Exclude disputed amounts from interest

**Recommended Actions:**

1. Should reduce to 1% or prime + margin

---

### GT-13 | Clause 5.2 | [!] AMEND

**Vendor can require prepayment on credit issues**

**Contract Language:**

> Vendor may establish and modify credit limits for Reseller. Vendor may require prepayment if Reseller exceeds credit limits or has past-due balances.

**Analysis:**

- Vendor can require prepayment if credit limits exceeded
- Can require prepayment on past-due balances
- Could impact cash flow
- Standard credit management provision
- Consider notice requirement before prepayment

**Recommended Actions:**

1. Consider notice requirement before prepayment

---


# 8. Services Agreement

**Contract:** Services
**Parties:** Creative Digital Agency Inc. (Agency) ↔ [Unnamed Client] (Client)
**Reviewing for:** Client
**Contract ID:** `Services_DigitalAgency`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 4 | GT-01, GT-02, GT-03, GT-04 |
| T2 Material | 11 | GT-05, GT-06, GT-07, GT-08, GT-09, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15 |
| T3 Minor | 11 | GT-16, GT-17, GT-18, GT-19, GT-20, GT-21, GT-22, GT-23, GT-24, GT-25, GT-26 |

**Weighted Max Points:** 98

## T1: Critical Issues

### GT-01 | Clause 10.1 | [!] AMEND

**Exclusion of Damages - No Carve-outs**

**Contract Language:**

> NEITHER PARTY SHALL BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING FROM THIS AGREEMENT.

**Analysis:**

- Neither party liable for consequential damages
- ❌ No carve-outs for willful misconduct, gross negligence
- ❌ No carve-outs for confidentiality breach
- Should add standard carve-outs

**Recommended Actions:**

1. Should add standard carve-outs

---

### GT-02 | Clause 10.2 | [!] AMEND

**Liability Cap SOW-Based - Creates Variable Exposure Per Engagement**

**Contract Language:**

> AGENCY'S TOTAL LIABILITY SHALL NOT EXCEED THE FEES PAID BY CLIENT UNDER THE APPLICABLE STATEMENT OF WORK GIVING RISE TO THE CLAIM.

**Analysis:**

- Cap is per-SOW, not aggregate across relationship
- Structural issue: liability exposure varies by engagement size
- Small SOW with major deliverable creates disproportionate risk
- ❌ No carve-outs for IP infringement or confidentiality breach
- Should use aggregate fees or minimum floor (e.g., $500K)
- Should add carve-outs for critical categories

**Recommended Actions:**

1. Should use aggregate fees or minimum floor (e.g., $500K)
2. Should add carve-outs for critical categories

---

### GT-03 | Clause 5.2 | [!] AMEND

**Agency IP License Restrictive**

**Contract Language:**

> To the extent Agency IP is incorporated into any Deliverables, Agency hereby grants Client a non-exclusive, perpetual, royalty-free license to use such Agency IP solely as part of the Deliverables.

**Analysis:**

- License to Agency IP is non-exclusive, perpetual, royalty-free
- BUT 'solely as part of the Deliverables'
- Cannot modify, sublicense, or use independently
- If Agency IP is core component, Client is locked in
- Should add modification rights
- Should add sublicense rights to affiliates

**Recommended Actions:**

1. Should add modification rights
2. Should add sublicense rights to affiliates

---

### GT-04 | Clause 6.1 | [X] AMEND

**Silence = Rejection (UNUSUAL)**

**Contract Language:**

> Client shall review each Deliverable and provide written acceptance or detailed written rejection specifying deficiencies within fifteen (15) business days of delivery. If Client fails to provide written notice within such period, the Deliverable shall be deemed rejected and Agency shall have an opportunity to cure.

**Analysis:**

- If Client fails to respond in 15 days, deemed REJECTED
- Industry norm is silence = acceptance
- Creates perpetual revision loop if Client is slow
- Agency can keep reworking indefinitely
- Should change to silence = acceptance
- Or add deemed acceptance after cure period

**Recommended Actions:**

1. Should change to silence = acceptance

---

## T2: Material Issues

### GT-05 | Clause 4.3 | [!] AMEND

**Delays - Open-ended Fees**

**Contract Language:**

> If Client delays in providing materials, approvals, or feedback, project timelines shall be extended accordingly, and additional fees may apply.

**Analysis:**

- Client delays extend timelines AND 'additional fees may apply'
- ❌ No cap on additional fees
- ❌ No proportionality requirement
- ❌ No advance notice of fee amount
- Should cap additional fees
- Should require notice before charging

**Recommended Actions:**

1. Should cap additional fees
2. Should require notice before charging

---

### GT-06 | Clause 5.1 | [!] AMEND

**Ownership Excludes Non-Final Materials**

**Contract Language:**

> Upon full payment of all fees due, Client shall own all right, title, and interest in the final approved Deliverables created specifically for Client under this Agreement.

**Analysis:**

- Client owns only 'final approved Deliverables'
- Excludes drafts, concepts, underlying work
- Agency retains all non-final work (5.3)
- Client may need underlying assets
- Should include work product used in final

**Recommended Actions:**

1. Should include work product used in final

---

### GT-07 | Clause 5.3 | [!] AMEND

**Preliminary Work Retained by Agency**

**Contract Language:**

> All concepts, sketches, drafts, and preliminary work product that are not incorporated into final approved Deliverables shall remain Agency's property.

**Analysis:**

- All concepts, sketches, drafts remain Agency property
- Even if Client paid for development
- Agency could reuse or sell to competitors
- Should limit Agency's use of preliminary work
- Or transfer to Client with final

**Recommended Actions:**

1. Should limit Agency's use of preliminary work

---

### GT-08 | Clause 6.3 | [!] AMEND

**Use in Commerce = Final Acceptance**

**Contract Language:**

> Client's use of any Deliverable in commerce or public distribution shall constitute final acceptance of such Deliverable.

**Analysis:**

- Using deliverable in public = acceptance
- Even if defective or incomplete
- Client may need to use urgently
- Waives right to reject known defects
- Should allow use without waiving defect claims

**Recommended Actions:**

1. Should allow use without waiving defect claims

---

### GT-09 | Clause 8.1 | [!] AMEND

**Warranties - No Duration or Specific Remedy**

**Contract Language:**

> Agency represents and warrants that: (a) it has the right to enter into this Agreement; (b) the Services will be performed in a professional manner; (c) the Deliverables will conform to the specifications in the applicable SOW; and (d) the Deliverables will not infringe third-party intellectual property rights.

**Analysis:**

- Agency warrants professional manner and conformance
- ❌ No specified warranty period
- ❌ No remedies for breach stated
- Should add 90-180 day warranty period
- Should add re-performance remedy

**Recommended Actions:**

1. Should add 90-180 day warranty period
2. Should add re-performance remedy

---

### GT-10 | Clause 8.3 | [!] AMEND

**Broad Disclaimer**

**Contract Language:**

> EXCEPT AS EXPRESSLY SET FORTH HEREIN, AGENCY MAKES NO WARRANTIES, EXPRESS OR IMPLIED, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

**Analysis:**

- Disclaims merchantability and fitness
- May undermine express warranties in 8.1
- Should clarify which warranties survive

**Recommended Actions:**

1. Should clarify which warranties survive

---

### GT-11 | Clause 9.1 | [!] AMEND

**Confidentiality - 3 Years Only**

**Contract Language:**

> This obligation shall survive termination for three (3) years.

**Analysis:**

- 3-year survival insufficient for trade secrets
- Creative work may have longer commercial value
- Should extend to 5 years or indefinite for trade secrets

**Recommended Actions:**

1. Should extend to 5 years or indefinite for trade secrets

---

### GT-12 | Clause 12.4 | [!] AMEND

**Termination - No Data Return**

**Contract Language:**

> Upon termination: (a) Client shall pay for all Services performed and expenses incurred through termination; (b) Agency shall deliver all completed work product for which Client has paid.

**Analysis:**

- Only addresses delivery of completed work Client paid for
- ❌ No provision for return of Client Materials
- ❌ No transition assistance
- Should add data/materials return requirement

**Recommended Actions:**

1. Should add data/materials return requirement

---

### GT-13 | Clause 13.2 | [!] AMEND

**Mandatory Arbitration in NY**

**Contract Language:**

> Disputes shall be resolved by arbitration in New York, New York.

**Analysis:**

- New York arbitration required
- ❌ No negotiation/mediation step
- May be inconvenient for non-NY clients
- Should add mediation first
- Consider neutral venue option

**Recommended Actions:**

1. Should add mediation first
2. Consider neutral venue option

---

### GT-14 | Clause N/A | [!] ADD

**No Data Protection Clause**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No data protection provision exists in contract

**Analysis:**

- Agency may receive/process Client personal data
- ❌ No data protection or privacy obligations stated
- ❌ No GDPR/CCPA compliance requirements
- Should add data protection clause

**Recommended Actions:**

1. Should add data protection clause

---

### GT-15 | Clause N/A | [!] ADD

**No Insurance Requirements**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No insurance requirements provision exists in contract

**Analysis:**

- ❌ No E&O, CGL, or Cyber liability requirements
- Agency could be judgment-proof
- Should add minimum insurance requirements

**Recommended Actions:**

1. Should add minimum insurance requirements

---

## T3: Minor Issues

### GT-16 | Clause 3.4 | [!] AMEND

**High Late Fee**

**Contract Language:**

> Late payments shall bear interest at one and one-half percent (1.5%) per month.

**Analysis:**

- 1.5% per month = 18% APR
- ❌ No cure period before interest accrues
- Should reduce to 1% or prime + margin
- Should add grace period

**Recommended Actions:**

1. Should reduce to 1% or prime + margin
2. Should add grace period

---

### GT-17 | Clause 5.4 | [!] AMEND

**Portfolio Rights - Subject to Confidentiality**

**Contract Language:**

> Agency shall have the right to display Deliverables in Agency's portfolio, website, and marketing materials, subject to any confidentiality restrictions.

**Analysis:**

- Agency can display Deliverables in portfolio
- BUT 'subject to any confidentiality restrictions'
- Actually provides some protection
- Consider explicit opt-out right for sensitive work

**Recommended Actions:**

1. Consider explicit opt-out right for sensitive work

---

### GT-18 | Clause 1.1 | [!] AMEND

**Agency IP Definition Broad**

**Contract Language:**

> "Agency IP" means all intellectual property owned by or licensed to Agency prior to the Effective Date, including methodologies, frameworks, templates, software tools, and pre-existing creative works.

**Analysis:**

- Includes 'methodologies, frameworks, templates, software tools'
- May capture project-specific developments
- Should clarify what becomes Agency IP vs Client IP

**Recommended Actions:**

1. Should clarify what becomes Agency IP vs Client IP

---

### GT-19 | Clause 2.2 | [!] AMEND

**Change Orders - No Response Timeline**

**Contract Language:**

> Any changes to the scope, timeline, or fees must be documented in a written change order signed by both Parties.

**Analysis:**

- Changes require signed change order
- ❌ No deadline for Agency to respond to request
- ❌ No dispute process if parties disagree on scope
- Should add response timeline

**Recommended Actions:**

1. Should add response timeline

---

### GT-20 | Clause 3.2 | [!] AMEND

**Expenses - Documentation Unclear**

**Contract Language:**

> Client shall reimburse Agency for pre-approved out-of-pocket expenses... Expenses exceeding $500 require Client's prior written approval.

**Analysis:**

- Pre-approved expenses reimbursable
- $500+ requires written approval
- ❌ No documentation requirements for receipts
- Should add receipt requirement

**Recommended Actions:**

1. Should add receipt requirement

---

### GT-21 | Clause 3.3 | [!] AMEND

**Deposit Triggers Unclear**

**Contract Language:**

> For project work, Agency may require a deposit of up to fifty percent (50%) prior to commencing work.

**Analysis:**

- Up to 50% deposit 'may' be required
- When deposit is required not specified
- Should clarify deposit conditions

**Recommended Actions:**

1. Should clarify deposit conditions

---

### GT-22 | Clause 6.2 | [!] AMEND

**Revisions - No Definition**

**Contract Language:**

> Agency shall provide up to two (2) rounds of revisions to each Deliverable at no additional charge. Additional revisions shall be billed at Agency's then-current hourly rates.

**Analysis:**

- 2 rounds of revisions included
- What constitutes a 'revision' undefined
- Could be one minor change or complete redo
- Should define scope of revision

**Recommended Actions:**

1. Should define scope of revision

---

### GT-23 | Clause 13.1 | [!] AMEND

**Governing Law - No Flexibility**

**Contract Language:**

> This Agreement shall be governed by the laws of the State of New York.

**Analysis:**

- New York law governs
- ❌ No option for Client's jurisdiction
- May be unfamiliar to non-NY clients

---

### GT-24 | Clause N/A | [!] ADD

**No Force Majeure**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No force majeure provision exists in contract

**Analysis:**

- ❌ No excuse for uncontrollable events
- Could be liable for delay due to pandemic, disaster
- Should add FM clause

**Recommended Actions:**

1. Should add FM clause

---

### GT-25 | Clause N/A | [!] ADD

**No Service Level Commitments**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No service level commitments exist in contract

**Analysis:**

- ❌ No response time commitments
- ❌ No quality metrics
- ❌ No escalation path
- Should add SLA for retainer work

**Recommended Actions:**

1. Should add SLA for retainer work

---

### GT-26 | Clause 13.3 | [!] AMEND

**Assignment - No M&A Exception (Mutual)**

**Contract Language:**

> Neither Party may assign without prior written consent.

**Analysis:**

- Neither party can assign without consent
- Mutual restriction (not asymmetric)
- ❌ No M&A or affiliate exception for either party
- Should add standard exceptions for both parties

**Recommended Actions:**

1. Should add standard exceptions for both parties

---


# 9. SaaS License Agreement

**Contract:** SaaS License
**Parties:** Alpha Cloud Services Inc. (Licensor) ↔ [Unnamed Licensee] (Licensee)
**Reviewing for:** Licensee
**Contract ID:** `SLA_CloudServices_Alpha`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 8 | GT-01, GT-02, GT-03, GT-04, GT-05, GT-06, GT-07, GT-08 |
| T2 Material | 12 | GT-09, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15, GT-16, GT-17, GT-18, GT-19, GT-20 |
| T3 Minor | 6 | GT-21, GT-22, GT-23, GT-24, GT-25, GT-26 |

**Weighted Max Points:** 130

## T1: Critical Issues

### GT-01 | Clause 8.1 | [X] AMEND

**Unlimited Licensee Liability**

**Contract Language:**

> Licensee acknowledges that any breach of this Agreement may result in unlimited liability to Licensor for all direct and indirect damages suffered by Licensor as a result of such breach.

**Analysis:**

- Licensee acknowledges unlimited liability for breach
- Licensor liability is capped but Licensee's is not
- Grossly one-sided allocation
- Should add mutual liability cap
- At minimum remove unlimited liability acknowledgment

**Recommended Actions:**

1. Should add mutual liability cap

---

### GT-02 | Clause 8.3 | [!] AMEND

**Full AS-IS Disclaimer**

**Contract Language:**

> EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, THE SOFTWARE IS PROVIDED "AS IS" AND LICENSOR DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

**Analysis:**

- Software provided AS-IS
- Disclaims merchantability, fitness, non-infringement
- May override statutory protections
- Should retain basic warranties

**Recommended Actions:**

1. Should retain basic warranties

---

### GT-03 | Clause 10.1 | [X] AMEND

**Consequential Damages Exclusion - Licensor Only**

**Contract Language:**

> IN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES...

**Analysis:**

- Exclusion applies only to Licensor
- Licensee remains exposed to consequential damages claims
- One-sided protection
- Should be mutual exclusion

**Recommended Actions:**

1. Should be mutual exclusion

---

### GT-04 | Clause 10.2 | [!] AMEND

**Low Liability Cap - Licensor Only**

**Contract Language:**

> IN NO EVENT SHALL LICENSOR'S TOTAL LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT EXCEED THE AMOUNT OF SUBSCRIPTION FEES PAID BY LICENSEE TO LICENSOR IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.

**Analysis:**

- 12-month cap applies only to Licensor
- ❌ No cap on Licensee liability (see 8.1)
- Should be mutual
- Should add carve-outs for IP, data breach

**Recommended Actions:**

1. Should be mutual
2. Should add carve-outs for IP, data breach

---

### GT-05 | Clause 12.4 | [X] AMEND

**Asymmetric Assignment**

**Contract Language:**

> Licensee may not assign this Agreement without Licensor's prior written consent. Licensor may assign this Agreement without restriction.

**Analysis:**

- Licensee needs consent to assign
- Licensor can assign without restriction
- Could end up with unknown/hostile provider
- Should be mutual consent requirement
- Add M&A exception for Licensee

**Recommended Actions:**

1. Should be mutual consent requirement
2. Add M&A exception for Licensee

---

### GT-06 | Clause 9.1 / Clause 9.2 | [!] ADD

**Narrow Indemnification - No Licensee Protection Defined**

**Contract Language:**

> 9.1: Licensor shall indemnify, defend, and hold harmless Licensee from and against any third-party claims alleging that the Software... infringes any patent, copyright, or trademark... 9.2: [Reserved]

**Analysis:**

- 9.1 covers only IP infringement by Licensor
- 9.2 is [Reserved] - no Licensee indemnification defined
- ❌ No data breach, negligence, misconduct coverage
- Should expand Licensor indemnification
- Should add narrow, capped Licensee indemnification

**Recommended Actions:**

1. Should expand Licensor indemnification
2. Should add narrow, capped Licensee indemnification

---

### GT-07 | Clause 5.1 | [!] AMEND

**Vague Security Measures**

**Contract Language:**

> Licensor shall implement and maintain reasonable administrative, technical, and physical safeguards designed to protect the security, confidentiality, and integrity of Licensee Data.

**Analysis:**

- 'Reasonable' safeguards is subjective
- ❌ No specific standards (SOC 2, ISO 27001)
- ❌ No audit rights for Licensee
- ❌ No breach notification requirements
- Should specify security standards
- Should add audit rights

**Recommended Actions:**

1. Should specify security standards
2. Should add audit rights

---

### GT-08 | Clause 11.4 | [X] AMEND

**No Data Export on Termination**

**Contract Language:**

> Upon termination... each Party shall return or destroy all Confidential Information of the other Party in its possession. [No provision for Licensee Data export]

**Analysis:**

- 11.4 only addresses Confidential Information return
- ❌ No provision for Licensee Data export/return
- 5.2 confirms Licensee owns data but no termination mechanism
- Could lose all data on termination
- Should add data export period (30-60 days)
- Should specify format and assistance

**Recommended Actions:**

1. Should add data export period (30-60 days)
2. Should specify format and assistance

---

## T2: Material Issues

### GT-09 | Clause 2.1 | [!] AMEND

**Non-Transferable License**

**Contract Language:**

> Licensor hereby grants to Licensee a non-exclusive, non-transferable, non-sublicensable right to access and use the Software...

**Analysis:**

- License is non-exclusive, non-transferable, non-sublicensable
- Cannot extend to affiliates or contractors without explicit permission
- Should add affiliate rights
- Should add contractor exception

**Recommended Actions:**

1. Should add affiliate rights
2. Should add contractor exception

---

### GT-10 | Clause 4.1 | [!] AMEND

**Weak Uptime SLA**

**Contract Language:**

> Licensor shall use commercially reasonable efforts to make the Software available 99.5% of the time during each calendar month, excluding scheduled maintenance windows and circumstances beyond Licensor's reasonable control.

**Analysis:**

- 99.5% target with 'commercially reasonable efforts' only
- ❌ No measurement methodology specified
- ❌ No service credits for downtime
- Should add binding SLA with credits

**Recommended Actions:**

1. Should add binding SLA with credits

---

### GT-11 | Clause 4.2 | [!] AMEND

**Limited Support Hours**

**Contract Language:**

> Licensor shall provide technical support to Licensee during normal business hours (9:00 AM to 5:00 PM Pacific Time, Monday through Friday, excluding holidays).

**Analysis:**

- Business hours only (9-5 PT, M-F)
- ❌ No 24/7 emergency support
- ❌ No severity tiers or escalation
- Should add emergency support option

**Recommended Actions:**

1. Should add emergency support option

---

### GT-12 | Clause 11.1 | [!] AMEND

**Auto-Renewal Terms**

**Contract Language:**

> This Agreement shall automatically renew for successive one (1) year periods unless either Party provides written notice of non-renewal at least sixty (60) days prior...

**Analysis:**

- 60-day notice for non-renewal
- Auto-renews for successive 1-year periods
- ❌ No termination for convenience during term
- Should add TfC with notice

**Recommended Actions:**

1. Should add TfC with notice

---

### GT-13 | Clause 2.3 | [!] AMEND

**Usage Restrictions Overbroad**

**Contract Language:**

> Licensee shall not... (a) copy, modify, or create derivative works of the Software; (b) reverse engineer, disassemble, or decompile the Software...

**Analysis:**

- Cannot reverse engineer, modify, create derivative works
- ❌ No carve-outs for backup, DR, security testing
- Should add standard operational exceptions

**Recommended Actions:**

1. Should add standard operational exceptions

---

### GT-14 | Clause 5.3 | [!] AMEND

**DPA Optional / No Timing**

**Contract Language:**

> To the extent Licensor processes any personal data on behalf of Licensee, the Parties shall execute a separate Data Processing Agreement...

**Analysis:**

- DPA is 'separate' and optional
- ❌ No requirement to execute before processing
- Could process personal data without DPA
- Should require DPA before processing begins

**Recommended Actions:**

1. Should require DPA before processing begins

---

### GT-15 | Clause 8.2 | [!] AMEND

**Performance Warranty Weak**

**Contract Language:**

> Licensor's sole obligation and Licensee's exclusive remedy for any breach of this warranty shall be for Licensor to use commercially reasonable efforts to correct any material non-conformity.

**Analysis:**

- Only remedy is 'efforts to correct'
- ❌ No workaround, refund, or termination right
- Exclusive remedy clause limits options
- Should add meaningful remedies

**Recommended Actions:**

1. Should add meaningful remedies

---

### GT-16 | Clause 12.10 | [!] AMEND

**Survival Incomplete**

**Contract Language:**

> The provisions of Articles 6, 7, 8, 9, 10, and 12 shall survive any termination or expiration of this Agreement.

**Analysis:**

- Survival lists Articles 6,7,8,9,10,12
- Article 5 (Data Security) not included
- Payment obligations not explicitly survived
- Should add Article 5 to survival

**Recommended Actions:**

1. Should add Article 5 to survival

---

### GT-17 | Clause N/A | [!] ADD

**No Audit Rights**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No audit rights provision exists in contract

**Analysis:**

- ❌ No right to audit Licensor's security or compliance
- 5.1 makes security promises but no verification
- Should add annual audit right or SOC 2 report requirement

**Recommended Actions:**

1. Should add annual audit right or SOC 2 report requirement

---

### GT-18 | Clause N/A | [!] ADD

**No Business Continuity**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No business continuity provision exists in contract

**Analysis:**

- ❌ No RTO/RPO requirements
- ❌ No disaster recovery provisions
- ❌ No redundancy requirements
- Should add BC/DR commitments

**Recommended Actions:**

1. Should add BC/DR commitments

---

### GT-19 | Clause N/A | [!] ADD

**No Force Majeure**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No force majeure provision exists in contract

**Analysis:**

- ❌ No defined force majeure events
- ❌ No termination rights for extended FM
- Should add FM clause with termination right

**Recommended Actions:**

1. Should add FM clause with termination right

---

### GT-20 | Clause N/A | [!] ADD

**No Vendor Insurance Requirements**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No insurance requirements provision exists in contract

**Analysis:**

- ❌ No CGL, Cyber, E&O insurance requirements
- ❌ No certificate of insurance requirement
- Should add minimum insurance requirements

**Recommended Actions:**

1. Should add minimum insurance requirements

---

## T3: Minor Issues

### GT-21 | Clause 3.1 | [!] AMEND

**Annual Advance Payment**

**Contract Language:**

> Unless otherwise specified in the Order Form, all Subscription Fees are due and payable annually in advance.

**Analysis:**

- Full year payment due upfront
- ❌ No quarterly/monthly option
- Cash flow impact
- Should negotiate quarterly payment option

**Recommended Actions:**

1. Should negotiate quarterly payment option

---

### GT-22 | Clause 3.3 | [!] AMEND

**High Late Fee**

**Contract Language:**

> Any amounts not paid when due shall bear interest at the rate of one and one-half percent (1.5%) per month...

**Analysis:**

- 1.5% per month = 18% APR
- ❌ No cure period before interest
- Should reduce to 1% or prime + margin
- Add grace period

**Recommended Actions:**

1. Should reduce to 1% or prime + margin
2. Add grace period

---

### GT-23 | Clause 6.2 | [!] AMEND

**Feedback Ownership**

**Contract Language:**

> If Licensee provides any suggestions, ideas, or feedback... Licensor shall own all right, title, and interest in and to such Feedback...

**Analysis:**

- All feedback becomes Licensor property
- ❌ No restriction, no obligation to Licensee
- Could include valuable ideas
- Should add compensation for implemented features

**Recommended Actions:**

1. Should add compensation for implemented features

---

### GT-24 | Clause 6.3 | [!] AMEND

**Aggregated Data Use**

**Contract Language:**

> Licensor may collect and analyse aggregated, anonymised data derived from Licensee's use of the Software...

**Analysis:**

- Licensor can use 'aggregated, anonymised data'
- ❌ No re-identification prohibition
- Should add re-identification prohibition

**Recommended Actions:**

1. Should add re-identification prohibition

---

### GT-25 | Clause 12.2 | [!] AMEND

**Arbitration Required**

**Contract Language:**

> Any dispute arising out of or relating to this Agreement shall be resolved by binding arbitration... in San Francisco, California.

**Analysis:**

- San Francisco venue
- ❌ No mediation step
- AAA Commercial Rules
- Consider adding negotiation/mediation first

**Recommended Actions:**

1. Consider adding negotiation/mediation first

---

### GT-26 | Clause 4.3 | [!] AMEND

**Short Maintenance Notice**

**Contract Language:**

> Licensor shall use commercially reasonable efforts to provide Licensee with at least 48 hours' prior notice of any scheduled maintenance...

**Analysis:**

- 48-hour notice for maintenance
- May be insufficient for business planning
- Consider 5 business days for major maintenance

**Recommended Actions:**

1. Consider 5 business days for major maintenance

---


# 10. Supply Agreement

**Contract:** Supply
**Parties:** Precision Manufacturing Co. (Supplier) ↔ Apex Automotive Systems Inc. (Buyer)
**Reviewing for:** Apex Automotive Systems Inc. (Buyer)
**Contract ID:** `Supply_ManufacturingCo`
**GT Version:** 1.0_LOCKED

## Issue Summary

| Tier | Count | Issues |
|------|-------|--------|
| T1 Critical | 4 | GT-01, GT-02, GT-03, GT-04 |
| T2 Material | 8 | GT-05, GT-06, GT-07, GT-08, GT-09, GT-10, GT-11, GT-12 |
| T3 Minor | 2 | GT-13, GT-14 |

**Weighted Max Points:** 74

## T1: Critical Issues

### GT-01 | Clause 5.2 | [X] AMEND

**Limited warranty remedy - Supplier controls remediation**

**Contract Language:**

> Supplier's sole obligation shall be, at Supplier's option, to repair, replace, or refund the purchase price of defective Products.

**Analysis:**

- Supplier's 'sole obligation' limits Buyer recourse
- Supplier chooses repair/replace/refund at its option
- ❌ No right for Buyer to repair via third party and back-charge
- ❌ No extension of warranty for repaired/replaced products
- ❌ No coverage for consequential damages from defects
- ❌ No recall cost allocation

---

### GT-02 | Clause 5.3 | [!] AMEND

**Broad warranty disclaimer undermines quality assurance**

**Contract Language:**

> EXCEPT AS EXPRESSLY SET FORTH HEREIN, SUPPLIER MAKES NO WARRANTIES, EXPRESS OR IMPLIED, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

**Analysis:**

- Disclaims all implied warranties including merchantability and fitness
- Only 1-year express warranty survives
- Should add express fitness for intended purpose
- Should warrant compliance with specifications
- Should warrant free from defects in design (not just materials/workmanship)

**Recommended Actions:**

1. Should add express fitness for intended purpose
2. Should warrant compliance with specifications
3. Should warrant free from defects in design (not just materials/workmanship)

---

### GT-03 | Clause 11.1 | [!] AMEND

**Consequential damages exclusion blocks critical recovery**

**Contract Language:**

> NEITHER PARTY SHALL BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING FROM THIS AGREEMENT.

**Analysis:**

- Mutual exclusion of indirect/consequential/punitive damages
- Blocks Buyer recovery for production line shutdowns
- Blocks recovery for customer claims and recalls
- Need carve-outs for product liability claims
- Need carve-outs for IP infringement
- Need carve-outs for willful misconduct / gross negligence

---

### GT-04 | Clause 6.1 | [!] AMEND

**FCA terms shift all transit risk to Buyer**

**Contract Language:**

> Unless otherwise agreed, all Products shall be delivered FCA Supplier's facility (Incoterms 2020). Title and risk of loss shall pass to Buyer upon delivery to the carrier.

**Analysis:**

- FCA Supplier's facility means risk passes at Supplier dock
- Buyer bears all transit risk including damage, loss, delay
- Prefer DDP or DAP (risk passes at Buyer facility)
- At minimum require CIF/CIP with insurance
- Supplier should bear risk until delivery to Buyer
- Title transfer should align with risk transfer

---

## T2: Material Issues

### GT-05 | Clause 11.2 | [X] AMEND

**Supplier liability cap too low**

**Contract Language:**

> SUPPLIER'S TOTAL LIABILITY SHALL NOT EXCEED THE AMOUNTS PAID BY BUYER FOR PRODUCTS IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.

**Analysis:**

- Cap limited to 12 months of product payments
- May be insufficient for major quality failures or recalls
- Increase to 24+ months or fixed amount
- Add carve-outs for IP, willful misconduct, gross negligence
- Consider unlimited for indemnification obligations

**Recommended Actions:**

1. Increase to 24+ months or fixed amount
2. Add carve-outs for IP, willful misconduct, gross negligence
3. Consider unlimited for indemnification obligations

---

### GT-06 | Clause 2.2 | [X] AMEND

**No supply obligation - Supplier can reject purchase orders**

**Contract Language:**

> Buyer shall submit purchase orders to Supplier specifying the Products, quantities, requested delivery dates, and shipping instructions. Supplier shall accept or reject each purchase order within five (5) business days.

**Analysis:**

- Supplier can accept or reject each PO within 5 business days
- ❌ No obligation to accept orders within forecast quantities
- Creates supply uncertainty for Buyer
- Should require acceptance of orders within agreed capacity/forecast
- Add deemed acceptance if no rejection within period
- Include supply assurance for critical components

**Recommended Actions:**

1. Should require acceptance of orders within agreed capacity/forecast
2. Add deemed acceptance if no rejection within period

---

### GT-07 | Clause 7.1 / Clause 7.2 | [!] AMEND

**Short inspection period with deemed acceptance**

**Contract Language:**

> Buyer shall inspect all Products within ten (10) business days of receipt and shall notify Supplier in writing of any non-conformities or defects. Products shall be deemed accepted if Buyer fails to provide written notice of rejection within the inspection period.

**Analysis:**

- Only 10 business days to inspect
- Deemed accepted if no written rejection within period
- May be insufficient for complex components or high volumes
- Extend to 30 days or time of first use
- Latent defects should be discoverable beyond inspection period
- Link to warranty period for hidden defects

---

### GT-08 | Clause 12.1 | [!] ADD

**Indemnification lacks recall cost and unlimited coverage**

**Contract Language:**

> Supplier shall indemnify Buyer against third-party claims arising from: (a) defects in Products; (b) Supplier's negligence; or (c) infringement of intellectual property rights.

**Analysis:**

- Indemnifies for defects, negligence, IP infringement
- ❌ No explicit recall cost coverage
- Subject to liability cap in 11.2
- Should be uncapped or have higher cap for indemnification
- Should explicitly include recall, rework, and field service costs
- Should include defense costs

**Recommended Actions:**

1. Should be uncapped or have higher cap for indemnification
2. Should explicitly include recall, rework, and field service costs
3. Should include defense costs

---

### GT-09 | Clause N/A | [X] ADD

**No business continuity / supply assurance provisions**

**STATUS: CLAUSE MISSING — Addition required**

**Analysis:**

- ❌ No last-time-buy rights
- ❌ No dual sourcing or second source rights
- ❌ No capacity reservation requirements
- ❌ No disaster recovery or business continuity plan
- Should require advance notice of discontinuation
- Should allow qualification of alternative sources

**Recommended Actions:**

1. Should require advance notice of discontinuation
2. Should allow qualification of alternative sources

---

### GT-10 | Clause 13.1 | [!] AMEND

**Confidentiality Survival Inadequate for Trade Secrets**

**Contract Language:**

> 13.1 Confidentiality. Each Party shall maintain the confidentiality of all Confidential Information received from the other Party. This obligation survives termination for three (3) years.

**Analysis:**

- 3-year survival period for confidentiality
- Automotive supply chain involves proprietary tooling, processes, pricing
- Trade secrets (manufacturing specs, quality processes) have indefinite value
- 3 years insufficient for competitive protection in automotive industry
- Should add perpetual protection for trade secrets
- Should differentiate trade secrets from general confidential info

**Recommended Actions:**

1. Should add perpetual protection for trade secrets
2. Should differentiate trade secrets from general confidential info

---

### GT-11 | Clause N/A | [!] ADD

**No Insurance Requirements for Supplier**

**STATUS: CLAUSE MISSING — Addition required**

**Contract Language:**

> N/A - No insurance provisions exist in contract. Critical gap for manufacturing supply agreement given product liability exposure.

**Analysis:**

- ❌ No insurance clause exists in the contract
- Supplier manufactures critical automotive components
- ❌ No product liability insurance requirement
- ❌ No general liability insurance requirement
- ❌ No coverage verification mechanism
- Should require product liability insurance ($5M+ for automotive)
- Should require additional insured status for Buyer
- Should require insurance certificates and ongoing verification

**Recommended Actions:**

1. Should require product liability insurance ($5M+ for automotive)
2. Should require additional insured status for Buyer
3. Should require insurance certificates and ongoing verification

---

### GT-12 | Clause 14.2 | [!] AMEND

**Termination for Cause Asymmetric - Supplier-Favorable Cure Period**

**Contract Language:**

> 14.2 Either Party may terminate this Agreement upon written notice if the other Party commits a material breach and fails to cure such breach within thirty (30) days of written notice thereof.

**Analysis:**

- 30-day cure period for material breach applies to both parties
- But Supplier breaches (quality failures, supply disruption) need immediate remedy
- Buyer cannot wait 30 days for critical supply issues
- ❌ No expedited termination for repeated or serious quality failures
- Should have shorter or no cure for supply/quality breaches
- Should have immediate termination right for safety-critical defects
- Should differentiate between administrative and operational breaches

**Recommended Actions:**

1. Should have shorter or no cure for supply/quality breaches
2. Should have immediate termination right for safety-critical defects
3. Should differentiate between administrative and operational breaches

---

## T3: Minor Issues

### GT-13 | Clause 4.2 | [!] AMEND

**High late payment interest rate**

**Contract Language:**

> Late payments shall bear interest at the rate of one and one-half percent (1.5%) per month.

**Analysis:**

- 1.5% per month = 18% APR
- Above typical commercial rates
- Negotiate to 1% per month or prime + 2%
- Should not apply to disputed amounts
- Consider grace period before interest accrues

**Recommended Actions:**

1. Negotiate to 1% per month or prime + 2%
2. Should not apply to disputed amounts
3. Consider grace period before interest accrues

---

### GT-14 | Clause 3.2 | [!] AMEND

**Annual price adjustments compound over time**

**Contract Language:**

> After the initial twelve-month period, Supplier may adjust prices annually upon ninety (90) days' prior written notice, provided that no single adjustment shall exceed five percent (5%).

**Analysis:**

- 5% cap per year is reasonable individually
- Compounds to significant increase over contract term
- 90-day notice is adequate
- Consider CPI-linked adjustments instead
- Add Buyer right to terminate if increase unacceptable
- Require cost justification for increases

**Recommended Actions:**

1. Consider CPI-linked adjustments instead
2. Add Buyer right to terminate if increase unacceptable
3. Require cost justification for increases

---

