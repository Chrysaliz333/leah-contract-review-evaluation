# Ground Truth Principles

Ground truth (GT) is the benchmark standard against which model outputs are measured. It defines **what a competent lawyer should identify** when reviewing a contract on behalf of a specified party. A well-constructed ground truth dataset ensures that evaluation results are meaningful, reproducible, and legally defensible.

Ground truth is not:

- A comprehensive clause-by-clause audit
- A list of every possible improvement
- A style guide or drafting preference document
- A balanced assessment of both parties' positions

GT answers a single question: "If this review missed issue X, would the commissioning party have a legitimate complaint?"

---

## Jurisdiction Scope

**Current GT Set: US Commercial Contracts**

This evaluation framework covers contracts governed by US law (state laws including Texas, California, Delaware, Nevada). The legal analysis reflects US statutory and common law principles, including:

- Work-for-hire doctrine under 17 U.S.C. Section 101
- UCC Article 2 for goods/supply contracts
- State-specific contract and corporate law

| Jurisdiction | Status | Notes |
|--------------|--------|-------|
| **US** | Current | 10 contract types, 160 issues |
| **UK** | Planned | Different statutory protections (UCTA, CRA 2015), employer IP rules |
| **EU** | Planned | GDPR-native DPAs, consumer protection directives |
| **APAC** | Future | Jurisdiction-specific requirements |

**Why this matters:** Leah serves clients globally. A UK client reviewing a UK-governed contract needs GT calibrated to UK law. The same structural issue may have different severity across jurisdictions (e.g., work-for-hire is effective for employees under UK CDPA 1988 but limited under US copyright law).

---

## Representing Party

### Core Principle

GT is authored from the perspective of the **commissioning party** -- whoever engaged the review. This is an **input parameter**, not an inferred property.

The same contract template may require different GTs depending on which party is being represented:

| Scenario | Commissioning Party | Focus Areas |
|----------|---------------------|-------------|
| SaaS procurement | Licensee | Uptime, data rights, liability caps |
| SaaS vendor review | Licensor | Payment terms, usage restrictions, indemnification from customer |
| Bank lending | Lender | Security, covenants, enforcement, events of default |
| Borrower review | Borrower | Cure periods, prepayment, covenant headroom |
| Supplier onboarding | Supplier | Payment terms, liability limits, IP retention |
| Procurement | Buyer | Warranties, indemnification, supply assurance |

### Power Dynamic Awareness

The commissioning party may or may not have negotiating leverage:

| Your Client | Counterparty | Typical Dynamic |
|-------------|--------------|-----------------|
| SME licensee | Enterprise SaaS vendor | Counterparty has leverage (take-it-or-leave-it terms) |
| Bank lender | Corporate borrower | Your client has leverage |
| Supplier | Large retailer procurement | Counterparty has leverage |
| Enterprise buyer | Niche vendor | Your client has leverage |

GT issues should reflect **what the client should ask for**, regardless of whether they will get it. Commercial reality (likelihood of success) is a separate consideration from legal completeness.

### Documentation Requirement

Every GT file must explicitly state:

```json
"representing_party": "Party Name (Role)"
```

Example: `"representing_party": "Apex Automotive Systems Inc. (Buyer)"`

---

## Tiering Framework

The tiering framework assigns severity to each issue, reflecting its legal materiality and the consequences of missing it.

### T1: Critical (8 points)

**Definition:** Issues that materially affect rights, obligations, or risk allocation. Missing these would likely constitute professional negligence.

**Test:** Would a senior partner call a meeting if this was missed?

**Characteristics:**
- Structural defects, not commercial preferences
- Cannot be fixed by "commercial discussion" post-signature
- Creates legal exposure, not just unfavourable terms
- No fallback or safety net if the issue materialises

### T2: Material (5 points)

**Definition:** Significant issues that should be raised in negotiations but may be acceptable depending on commercial context.

**Test:** Would you flag this in a review memo but accept client instruction to proceed?

**Characteristics:**
- Risk exists but is bounded
- Commercial judgement applies
- Standard negotiation points
- Client might accept with eyes open

### T3: Minor (1 point)

**Definition:** Lower-priority issues representing best practice improvements or minor risk mitigation.

**Test:** Nice to have, but would not delay closing.

**Characteristics:**
- Convenience issues
- Commercial preferences
- Standard market terms that favour counterparty
- Process improvements

---

## Universal T1 Issues

Certain structural defects are **T1 regardless of contract type**. When reviewing any contract, check for:

| Issue | Why T1 | Contract Types |
|-------|--------|----------------|
| **Missing indemnification** | Commissioning party exposed to third-party claims with no recourse | Distribution, Reseller, Licence, Services, Supply |
| **Unlimited liability exposure** | Uncapped damages for one party | All |
| **No termination rights** | Trapped in non-working relationship | All |
| **IP ownership defects** | Work-for-hire ineffective, unclear assignment | Services, Consulting, Licence, JV |
| **Deadlock with no resolution** | 50/50 structures with no tiebreaker | JV, Partnership |
| **One-sided liability cap** | Cap protects counterparty only | SLA, Licence, Services |
| **Missing data protection** | Regulatory exposure (GDPR, CCPA) | Any contract involving personal data |
| **No exit/buyout mechanism** | Locked into long-term commitment | JV, Partnership, Distribution |

If any of these exist in a contract, they start at T1 unless there is a documented reason to demote.

---

## Tiering Principles

### Promote to T1 if:

1. **Structural defect** -- The clause fundamentally does not work (e.g., work-for-hire for independent contractors in jurisdictions where it is ineffective)
2. **No fallback** -- If this fails, there is no safety net
3. **Unlimited exposure** -- No cap on liability/damages for the commissioning party
4. **Irreversible harm** -- Cannot be remedied post-signature
5. **Regulatory breach** -- Creates compliance exposure (GDPR, export controls, sanctions)

### Demote to T3 if:

1. **Commercial preference** -- Reasonable lawyers could disagree
2. **Standard market term** -- Counterparty position is common in this contract type
3. **Quantified exposure** -- Risk is bounded and insurable
4. **Negotiable** -- Can be addressed in commercial discussion
5. **Convenience** -- Affects process, not rights

### The "So What?" Test

For every issue, ask: "If this goes wrong, what is the worst case for the commissioning party?"

| Answer | Tier |
|--------|------|
| "Client loses IP rights to their core product" | T1 |
| "Client faces uncapped liability for vendor's negligence" | T1 |
| "Client pays 20% more in a dispute" | T2 |
| "Client has to litigate in Texas instead of Nevada" | T3 |
| "Client has 30 days notice instead of 60" | T3 |

### Tier Decision Tree

```
Is the clause structurally defective?
+-- Yes --> T1
+-- No
    |
    Does it create unlimited/uncapped exposure for commissioning party?
    +-- Yes --> T1
    +-- No
        |
        Is it on the Universal T1 list for this contract type?
        +-- Yes --> T1 (unless documented exception)
        +-- No
            |
            Would missing it be professionally negligent?
            +-- Yes --> T1
            +-- No
                |
                Is it a significant negotiation point that affects material rights?
                +-- Yes --> T2
                +-- No
                    |
                    Is it a commercial preference or convenience issue?
                    +-- Yes --> T3
                    +-- No --> Consider excluding from GT
```

### Cross-Contract Consistency

The same structural defect should have the same tier across contract types:

- Missing indemnification = T1 (Distribution, Reseller, Licence, Services)
- High late payment interest = T3 (all contracts)
- Non-exclusive appointment = T2 for resellers (lower capital), T1 for distributors (higher investment)

Document any tier variation with rationale.

---

## Issue Structure

Each GT item must include the following fields:

| Field | Required | Purpose |
|-------|----------|---------|
| `gt_id` | Yes | Unique identifier (GT-01, GT-02, ...) |
| `clause` | Yes | Section reference or "N/A (Missing)" |
| `tier` | Yes | T1, T2, or T3 |
| `issue` | Yes | One-line summary of the problem |
| `expected_classification` | Yes | UNFAVOURABLE or CLARIFY |
| `acceptable_classification` | Yes | Alternative valid classification |
| `key_elements` | Yes | What a good response must address (array) |
| `contract_text` | Yes | Verbatim quote from contract |

### Extended Schema Fields

Additional optional fields improve evaluator matching accuracy:

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `detection_logic` | string | "standard" | Specifies where to search for matches |
| `expected_output_patterns` | array | [] | Keywords indicating correct detection |
| `polarity` | string | "negative" | Distinguishes "flag problem" from "confirm present" |
| `required_concepts` | array | [] | Concepts required for full detection (Y) |
| `reasoning_must_contain` | array | [] | Required phrases to avoid false positives |
| `reasoning_must_not_contain` | array | [] | Phrases indicating misunderstanding |

#### detection_logic

Specifies where the evaluator should search for issue detection:

| Value | Meaning | Search Locations |
|-------|---------|------------------|
| `standard` | Default matching | risk_table, proposed_redlines |
| `new_clause_recommendation` | Expects clause to be added | risk_table, proposed_redlines, new_clauses_proposed |
| `pattern_match` | Match against regex patterns | All sections, uses expected_output_patterns |
| `any_mention` | Any reference counts | All sections including notes |

**When to use:**
- `new_clause_recommendation`: For items with `expected_action: "ADD"` or `clause: "N/A (Missing)"`
- `pattern_match`: For abstract concepts that may appear anywhere (e.g., "risk allocation")
- `any_mention`: Rarely used; when any acknowledgement of the issue counts as detection

**Example:**
```json
{
  "gt_id": "GT-24",
  "clause": "N/A (Missing)",
  "issue": "No Force Majeure clause",
  "expected_action": "ADD",
  "detection_logic": "new_clause_recommendation",
  "expected_output_patterns": ["force majeure", "act of god", "beyond control"]
}
```

#### polarity

Distinguishes issues to flag (negative) from compliance confirmations (positive):

| Value | Meaning |
|-------|---------|
| `negative` | Problem to flag (default) |
| `positive` | Should be present and correct |

Use `positive` for GT items confirming GDPR compliance, regulatory requirements, or expected protections.

#### required_concepts

Concepts that must appear in the model's reasoning for full detection. Used for complex legal analysis where understanding must be demonstrated.

**Matching logic:**
- Y: Issue detected AND at least 50% of required_concepts mentioned in reasoning
- P: Issue detected BUT fewer than 50% of required_concepts mentioned
- N/NMI: Issue not detected

**Example:**
```json
{
  "gt_id": "GT-01",
  "tier": "T1",
  "issue": "Work-for-hire ineffective for independent contractors",
  "required_concepts": ["17 U.S.C.", "work for hire", "independent contractor", "assignment"]
}
```

#### reasoning_must_contain / reasoning_must_not_contain

Validates reasoning quality to catch false favourable classifications. If the model marks an issue as favourable but reasoning contains `must_not_contain` phrases or lacks `must_contain` phrases, detection downgrades to N.

**Example:**
```json
{
  "gt_id": "GT-11",
  "tier": "T1",
  "issue": "Supplier can reject orders at discretion",
  "expected_classification": "UNFAVOURABLE",
  "reasoning_must_contain": ["reject", "discretion", "no obligation"],
  "reasoning_must_not_contain": ["certainty", "guaranteed", "binding"]
}
```

### Key Elements

Key elements form the scoring rubric for each issue. They must be specific and testable:

**Good:**
```json
"key_elements": [
  "Must identify work-for-hire limitation under 17 U.S.C. Section 101",
  "Must flag that contractors are not 'employees' for work-for-hire",
  "Should propose express assignment with moral rights waiver",
  "Should address pre-existing IP carve-out"
]
```

**Bad:**
```json
"key_elements": [
  "Should improve the clause",
  "Needs attention",
  "Consider revising"
]
```

### Contract Text

Contract text must be **verbatim** from the source document. Do not paraphrase, fix typos, modernise language, or truncate without indication (`...`).

For missing clauses:
```json
"contract_text": "N/A - Clause does not exist in current contract"
```

For multi-clause issues:
```json
"contract_text_6_4": "Upon termination...",
"contract_text_13_10": "The provisions of Articles 5, 6..."
```

### Clause Reference Flexibility

GT clause references are **targets, not exact match requirements**. During evaluation:

- The model may identify the correct issue at an adjacent clause
- Semantic matching applies: "Did the model identify THIS risk?" -- not "Did the model reference THIS clause?"
- Clause reference mismatches do not automatically mean NMI

See [scoring methodology](scoring_methodology.md) for full semantic matching rules.

---

## Actions

| Action | When to Use |
|--------|-------------|
| **AMEND** | Clause exists but needs modification |
| **ADD** | Clause or provision missing entirely |
| **DELETE** | Clause should be removed |
| **FLAG** | Issue to raise but no specific drafting change |

### Classification Mapping

| Classification | Typical Actions |
|----------------|-----------------|
| UNFAVOURABLE | AMEND, DELETE, ADD (if missing) |
| CLARIFY | AMEND, ADD, FLAG |

---

## Issue Selection

### Include if:

- A competent lawyer would flag it
- The commissioning party is disadvantaged
- There is a concrete risk or gap
- The issue is specific to this contract (not generic advice)

### Exclude if:

- It is a drafting preference (semicolons, defined terms style)
- It is market standard and balanced
- It affects neither party materially
- It requires commercial context not available
- It is favourable to the commissioning party

### Coverage Balance

Aim for comprehensive coverage of material risks without bloat:

| Contract Complexity | Target Range |
|--------------------|--------------|
| Simple (NDA, short-form) | 8--12 issues |
| Medium (Services, Licence, Supply) | 12--18 issues |
| Complex (JV, M&A-adjacent, Partnership) | 18--25 issues |

**Warning signs of bloat:**
- More than 5 T3 issues
- Multiple issues on same clause with minor variations
- Issues that start with "Consider..." or "Could..."
- More than 30% of issues at T3

---

## GT for Different Evaluation Modes

### Freeform Review

- Whole document review
- All issues relevant to commissioning party
- Tiered scoring (T1: 8pts, T2: 5pts, T3: 1pt)
- T1 gate: must detect all T1 issues to pass

### Rules-Based Review

- Deterministic triggers from rule definitions
- Binary compliance (rule met or not)
- Actions prescribed by rule definitions
- No tiering -- rules are pass/fail

### Playbook/Guidelines Review

- Position matching against gold standard / fallback / red flag
- Hierarchy-based scoring
- May combine with freeform for comprehensive evaluation

### Stacked Review (Freeform + Redlines)

- Base GT for whole document issues
- Additional items for counterparty redline responses
- Dual evaluation: baseline detection + redline quality

---

## Version Control

### Versioning Scheme

```
{major}.{minor}_{status}

Examples:
- 1.0_DRAFT      (initial development)
- 1.0_LOCKED     (frozen for evaluation)
- 2.0_LOCKED     (structural changes, re-evaluation required)
- 2.1_corrected  (minor fixes, no re-evaluation required)
```

**Major increment:** Issues added/removed, tier changes
**Minor increment:** Wording refinements, key_elements updates, clause reference corrections
**Status:** DRAFT (in development), LOCKED (frozen), corrected (minor fixes applied)

### Locking Rules

Once evaluation begins, GT is LOCKED. Any changes require:

1. New version number
2. Documentation of change rationale
3. Assessment of impact on existing evaluations
4. Re-scoring of affected model runs if tier changes affect T1 gate

---

## Maintaining GT Over Time

### When to Update

- Contract template changes (new version from client)
- Legal landscape shifts (new regulation, significant case law)
- Systematic tier miscalibration discovered
- Genuine gap discovered during evaluation (true T1 missed by GT)

### When NOT to Update

- Model performed poorly (that is what we are measuring)
- Single edge case (capture as additional issue instead)
- Preference change (maintain consistency across evaluations)
- To "help" a model pass (defeats the purpose)

---

## Validation Checklist

Before finalising GT:

**Structure**
- All issues have unique GT-IDs (GT-01, GT-02, ...)
- GT-IDs are sequential with no gaps
- Tier counts match tier summary
- Weighted max calculated correctly: `(T1 x 8) + (T2 x 5) + (T3 x 1)`

**Content**
- Contract text is verbatim (not paraphrased)
- Clause references verified against actual contract
- No phantom clauses (references to sections that do not exist)
- Key elements are specific and testable
- No duplicate issues (same clause, same concern)

**Tiering**
- Universal T1 issues checked
- "So What?" test applied to each issue
- Cross-contract consistency verified
- No more than approximately 30% T3 issues
- At least one T1 issue (or explicit justification why not)

**Metadata**
- Representing party stated explicitly
- GT version follows naming convention
- Revision notes document changes from prior version

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Over-tiering | Everything is T1 | Apply "So What?" test rigorously |
| Under-tiering | Structural defects at T2 | Check Universal T1 list |
| Bloat | 40+ issues per contract | Cut T3s, merge related issues |
| Vague key elements | "Should be improved" | Specify what improvement means |
| Wrong perspective | Issues favour counterparty | Review from commissioning party only |
| Stale contract text | Quotes do not match source | Re-verify against original |
| Phantom clauses | Reference to non-existent section | Verify every clause reference |
| Duplicate issues | Same concern, different GT-IDs | Merge into single issue |

### Examples of Tiering Mistakes

**Over-tiered (should be T3, not T1):**
> "Late payment interest at 1.5% per month is excessive"

This is a commercial preference. The exposure is quantified and bounded. Demote to T3.

**Under-tiered (should be T1, not T2):**
> "No indemnification clause for product defects"

Distributor is exposed to third-party claims with no recourse to supplier. This is a structural defect. Promote to T1.

**Vague versus Specific Key Elements:**

| Vague (Bad) | Specific (Good) |
|-------------|-----------------|
| "Improve liability provisions" | "Add carve-outs for IP infringement, gross negligence, wilful misconduct" |
| "Address IP concerns" | "Clarify ownership of improvements developed by Licensee using Licensed IP" |
| "Termination needs work" | "Add termination for convenience with 30-day notice after initial term" |

---

## Current Evaluation Set (US Commercial)

**Jurisdiction:** United States (various state laws)

| Contract | Representing Party | T1 | T2 | T3 | Total | Max Pts |
|----------|-------------------|----|----|----|----|---------|
| Consulting | Meridian Enterprises Inc. (Client) | 1 | 8 | 2 | 11 | 50 |
| DPA | Controller | 3 | 6 | 3 | 12 | 57 |
| Distribution | Distributor | 6 | 5 | 2 | 13 | 75 |
| JV | Quantum Dynamics LLC (Party B) | 5 | 10 | 3 | 18 | 93 |
| Licence | TechPro Industries Corp. (Licensee) | 4 | 7 | 4 | 15 | 71 |
| Partnership | Growth Dynamics Partners LP (Partner B) | 6 | 4 | 2 | 12 | 70 |
| Reseller | Pacific Tech Distributors LLC (Reseller) | 4 | 7 | 2 | 13 | 69 |
| Services | Client | 4 | 11 | 11 | 26 | 98 |
| SLA | Licensee | 8 | 12 | 6 | 26 | 130 |
| Supply | Apex Automotive Systems Inc. (Buyer) | 4 | 8 | 2 | 14 | 74 |

**Total:** 160 issues, 787 maximum points
