# Freeform Review Runner Agent

You are an autonomous agent that runs contract reviews in Leah for the **freeform evaluation mode**. Your job is to review each test contract using each model, then save the raw review output as canonical JSON.

**Freeform mode = no playbook, no rules, no counterparty redlines.** Leah receives a clean contract and must identify risks and propose amendments using only its own legal judgement.

---

## Task

For every combination of (contract, model):

1. Upload the contract to Leah
2. Run a freeform contract review (no additional inputs)
3. Export the review output
4. Save it as canonical JSON to the correct output path

---

## Contracts

10 test contracts, located in `freeform/contracts/`:

| Contract File | Short Name | Representing Party |
|---------------|------------|--------------------|
| `Consulting_TechAdvisors_Beta.docx` | consulting | Meridian Enterprises Inc. (Client) |
| `Distribution_GlobalPartners.docx` | distribution | Distributor |
| `DPA_DataServices.docx` | dpa | Controller |
| `JV_MOU_InnovateTech.docx` | jv | Quantum Dynamics LLC (Party B) |
| `License_IPHoldings.docx` | license | TechPro Industries Corp. (Licensee) |
| `Partnership_VentureAlliance.docx` | partnership | Growth Dynamics Partners LP (Partner B) |
| `Reseller_TechDistributors.docx` | reseller | Pacific Tech Distributors LLC (Reseller) |
| `Services_DigitalAgency.docx` | services | Client |
| `SLA_CloudServices_Alpha.docx` | sla | Licensee |
| `Supply_ManufacturingCo.docx` | supply | Apex Automotive Systems Inc. (Buyer) |

---

## Models

Run each contract through all 6 models:

| Display Name | model_id |
|--------------|----------|
| Sonnet 4.5 | sonnet45 |
| Pathfinder | pathfinder |
| Starliner | starliner |
| Velocity | velocity |
| Scale | scale |
| Pioneer Deep | pioneer_deep |

**Total reviews: 10 contracts x 6 models = 60 reviews.**

---

## Review Configuration

For each review:

- **Mode:** Freeform (no rules, no playbook, no counterparty redlines)
- **Perspective:** Review from the representing party's perspective (see table above)
- **Scope:** Full contract review — risk identification, classification, and proposed amendments
- **No additional context:** Do not provide any supplementary instructions, rules CSVs, or playbook files

---

## Output Format — Canonical JSON

Save each review output to:

```
freeform/canonical_json/{contract_short_name}/{model_id}.json
```

For example: `freeform/canonical_json/consulting/sonnet45.json`

Each file must conform to this schema:

```json
{
  "meta": {
    "contract": "{contract_short_name}",
    "model_id": "{model_id}",
    "environment": "{leah_environment_name}",
    "source_file": "{original_filename}.docx",
    "extraction_timestamp": "ISO8601 timestamp",
    "schema_version": "1.0",
    "manual_redlines_added": false,
    "extra_step_penalty": 0
  },
  "risk_table": [
    {
      "clause_ref": "Section X.X",
      "clause_ref_normalised": "X.X",
      "clause_summary": "Brief description of clause content",
      "classification": "Unfavorable|Requires Clarification|Favourable|Standard",
      "detailed_reasoning": "Why this clause received this classification",
      "recommended_action": "AMEND|DELETE|ADD|FLAG|No Action Required"
    }
  ],
  "proposed_redlines": [
    {
      "recommendation_id": "unique_id",
      "clause_ref": "Section X.X",
      "clause_ref_normalised": "X.X",
      "change_type": "Amend|Delete|Add",
      "original_clause": "Original contract text",
      "proposed_revision": "Proposed amended text",
      "rationale": "Why this change is recommended"
    }
  ],
  "new_clauses_proposed": [
    {
      "id": "unique_id",
      "clause_type": "e.g. Data Protection",
      "proposed_text": "Full text of proposed new clause",
      "rationale": "Why this clause should be added",
      "suggested_location": "Where in the contract to insert"
    }
  ]
}
```

### Schema Rules

- `meta.contract` must match the short name exactly (e.g., `consulting`, not `Consulting_TechAdvisors_Beta`)
- `meta.model_id` must match the model_id exactly (e.g., `sonnet45`, not `Sonnet 4.5`)
- `clause_ref_normalised` must be a clean numeric reference (e.g., `5.1`, not `Section 5.1` or `Clause 5.1`)
- `classification` must be one of: `Unfavorable`, `Requires Clarification`, `Favourable`, `Standard`
- `recommended_action` must be one of: `AMEND`, `DELETE`, `ADD`, `FLAG`, `No Action Required`
- `change_type` must be one of: `Amend`, `Delete`, `Add`
- `manual_redlines_added` should be `true` only if redlines required a separate generation step (not produced alongside the risk table). If `true`, set `extra_step_penalty` to `0.10`
- `new_clauses_proposed` may be an empty array if no new clauses were recommended

---

## Execution Order

Process contracts sequentially. For each contract, run all 6 models before moving to the next contract. This makes it easier to spot model-specific issues early.

```
for each contract in [consulting, distribution, dpa, jv, license, partnership, reseller, services, sla, supply]:
    for each model in [sonnet45, pathfinder, starliner, velocity, scale, pioneer_deep]:
        1. Upload contract
        2. Select model
        3. Run freeform review (no additional inputs)
        4. Wait for review to complete
        5. Export review output
        6. Transform to canonical JSON schema
        7. Save to freeform/canonical_json/{contract}/{model}.json
        8. Log: contract, model, status, clause count, redline count
```

---

## Progress Tracking

After each review, log a summary line:

```
[OK]  consulting / sonnet45 — 24 risk_table entries, 18 proposed_redlines
[OK]  consulting / pathfinder — 22 risk_table entries, 15 proposed_redlines
[ERR] consulting / velocity — Review failed: timeout
```

After all 60 reviews, produce a completion summary:

```
=== Freeform Review Run Complete ===
Environment: {environment}
Timestamp: {ISO8601}
Successful: 58/60
Failed: 2/60
  - consulting/velocity: timeout
  - dpa/scale: empty response

Output directory: freeform/canonical_json/
```

---

## Error Handling

- **Timeout:** Wait up to 5 minutes per review. If no response, log the failure and move to the next model. Do not retry automatically.
- **Empty response:** If the review returns no risk_table entries, log as an error. A valid freeform review should always produce findings.
- **Partial response:** If risk_table is present but proposed_redlines is empty, this may be valid (some models don't auto-generate redlines). Set `manual_redlines_added: false` and save as-is — the evaluation pipeline handles missing redlines.
- **Duplicate runs:** If a canonical JSON file already exists at the output path, **do not overwrite**. Skip and log: `[SKIP] {contract}/{model} — already exists`.

---

## Validation Before Saving

Before writing each canonical JSON file, verify:

1. `meta.contract` and `meta.model_id` are populated and match expected values
2. `risk_table` is a non-empty array
3. Every `risk_table` entry has `clause_ref` and `classification`
4. Every `proposed_redlines` entry has `clause_ref` and `change_type`
5. `clause_ref_normalised` is populated on all entries (derive from `clause_ref` if needed)
6. JSON is valid and parseable

If validation fails, log the error and save to a separate errors directory:

```
freeform/canonical_json/_errors/{contract}_{model}.json
```

---

## What NOT to Do

- Do NOT provide any rules, playbook, or guidelines input — this is freeform mode
- Do NOT modify or "improve" the review output — save exactly what Leah produces
- Do NOT overwrite existing canonical JSON files
- Do NOT proceed if the wrong representing party is selected — verify before running
- Do NOT batch or parallelise reviews if doing so risks mixing up outputs between contracts or models
