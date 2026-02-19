# Leah Contract Review Evaluation Framework

## What This Is

Pure scoring engine for benchmarking AI contract review against expert legal ground truth. Not a product — a measurement tool. No API calls, no external services, no deployment.

## Architecture

```
Contracts (.docx) + Ground Truth (JSON) + Scoring Config (JSON)
    ↓                    ↓                       ↓
┌──────────────────────────────────────────────────────┐
│              Evaluation Pipeline                      │
│  Detection Matching → Scoring → Quality → Aggregation │
└──────────────────────────────────────────────────────┘
    ↓
Results: per-model scores, T1 gate pass/fail, quality metrics
```

All scoring functions are **pure** — no global state, no file I/O, no external API calls. Input data in, scores out.

## Five Evaluation Modes

| Mode | Tests | Context Given |
|------|-------|---------------|
| **Freeform** | Risk identification with no guidance | None |
| **Freeform Stacking** | Counterparty redline response + whole-doc risk | Redlined contracts |
| **Rules** | Deterministic rule compliance | Rule CSV |
| **Rules Stacking** | Redline-specific rule application | Redlined contracts + Rule CSV |
| **Guidelines** | Playbook position guidance (GS/FB1/FB2/RF) | Playbook |

## Three-Tier Scoring

| Tier | Points | Gate Rule |
|------|--------|-----------|
| T1 (Critical) | 8 | Miss = automatic FAIL |
| T2 (Material) | 5 | Weighted |
| T3 (Minor) | 1 | Weighted |

Quality dimensions: detection (Y/P/N/NMI), amendment quality (1–3), rationale quality (1–3), redline quality (1–3).

Detection is **semantic** — "did the model find THIS risk?" not "did it cite THIS clause number?"

## Models Under Evaluation

| Display Name | ID |
|--------------|----|
| Sonnet 4.5 | sonnet45 |
| Pathfinder | pathfinder |
| Starliner | starliner |
| Velocity | velocity |
| Scale | scale |
| Pioneer Deep | pioneer_deep |

## Project Structure

```
leah-contract-review-evaluation/
├── framework/              # Scoring engine
│   ├── config/             # Mode-specific scoring configs
│   ├── scoring/            # Pure scoring functions
│   ├── scripts/            # GT loaders, validators, generators
│   ├── validators/         # Schema and data validators
│   └── schemas/            # JSON schemas
├── prompts/                # Evaluation agent specifications (per mode)
├── tests/                  # Scoring module tests (pytest)
├── notebooks/              # Interactive pipeline walkthrough
├── docs/                   # Methodology, GT principles, integrity
│   └── modes/              # Per-mode documentation
├── freeform/               # COMPLETE: 10 contracts, 160+ GT issues, 6 models
│   ├── contracts/          # .docx files
│   ├── ground_truth/       # Hand-authored JSON (T1/T2/T3)
│   ├── results/            # Aggregated evaluations
│   └── workbooks/          # Excel deliverables
├── freeform_stacking/      # COMPLETE: redlined contracts + dual GT
├── rules/                  # GT + inputs ready (evaluation pending)
├── rules_stacking/         # GT + inputs ready (evaluation pending)
├── guidelines/             # GT + inputs ready (evaluation pending)
└── pyproject.toml          # Python >=3.11, deps: openpyxl, pandas, matplotlib
```

## Development Patterns

- **Pure functions** — scoring functions take data in, return scores. No side effects.
- **Hand-authored ground truth** — every GT issue written by a human with specific legal reasoning, statutory references, and remediation guidance. Never generated.
- **Semantic matching** — three criteria: same risk type, same party affected, similar remediation.
- **No ORM, no DB** — everything is JSON files + Excel workbooks.
- **Notebooks for exploration** — `notebooks/01_evaluation_pipeline.ipynb` walks through the full pipeline.

## Key Commands

```bash
# Run scoring tests
pytest tests/ -v

# Launch evaluation pipeline notebook
jupyter notebook notebooks/01_evaluation_pipeline.ipynb

# Install dependencies
pip install -r requirements.txt
```

## What NOT to Do

- Don't modify ground truth files without understanding the tiering rationale
- Don't add external API calls to the scoring engine — it must stay pure
- Don't auto-generate ground truth — all GT is hand-authored
- Don't change the JSONL schema without updating all mode configs
