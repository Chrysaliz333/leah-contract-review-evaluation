# Sales Evaluation Metrics

Generated: 2026-02-03 18:18

## Risk Identification Accuracy

| Model | Detection Rate | Y | P | N | NMI | GT Issues |
|-------|---------------|---|---|---|-----|-----------|
| Sonnet 4.5 | 94.4% | 148 | 3 | 1 | 8 | 160 |
| Pioneer Deep | 95.6% | 148 | 5 | 1 | 6 | 160 |
| Pathfinder | 82.5% | 116 | 16 | 5 | 23 | 160 |
| Starliner | 86.9% | 124 | 15 | 3 | 18 | 160 |
| Scale | 84.4% | 114 | 21 | 2 | 23 | 160 |
| Velocity | 65.6% | 71 | 34 | 0 | 55 | 160 |

## Precision, Recall & F1

| Model | Weighted Recall | Precision | F1 |
|-------|----------------|-----------|-----|
| Sonnet 4.5 | 93.27% | 100.00% | 96.52% |
| Pioneer Deep | 93.20% | 100.00% | 96.48% |
| Pathfinder | 80.56% | 100.00% | 89.23% |
| Starliner | 84.94% | 100.00% | 91.86% |
| Scale | 81.32% | 100.00% | 89.70% |
| Velocity | 58.39% | 100.00% | 73.73% |

## Additional Issues (False Positive Rate)

| Model | Valid | Not Material | Hallucination | Total | FP Rate | Audit |
|-------|-------|-------------|---------------|-------|---------|-------|
| Sonnet 4.5 | 589 | 0 | 0 | 589 | 0.0% | pending |
| Pioneer Deep | 565 | 0 | 0 | 565 | 0.0% | pending |
| Pathfinder | 376 | 0 | 0 | 376 | 0.0% | pending |
| Starliner | 339 | 0 | 0 | 339 | 0.0% | pending |
| Scale | 313 | 0 | 0 | 313 | 0.0% | pending |
| Velocity | 252 | 0 | 0 | 252 | 0.0% | pending |

## Quality Scores (1-3 scale)

| Model | Amendment | Rationale | Redline | Overall |
|-------|-----------|-----------|---------|---------|
| Sonnet 4.5 | 2.97 | 2.98 | 2.81 | 2.92 |
| Pioneer Deep | 2.86 | 2.89 | 2.89 | 2.88 |
| Pathfinder | 2.72 | 2.76 | 2.8 | 2.76 |
| Starliner | 2.55 | 2.64 | 2.57 | 2.59 |
| Scale | 2.61 | 2.69 | 2.63 | 2.64 |
| Velocity | 2.23 | 2.44 | 2.36 | 2.34 |

## T1 Critical Issue Gate

| Model | Passes | Total | Pass Rate |
|-------|--------|-------|-----------|
| Sonnet 4.5 | 8 | 10 | 80.0% |
| Pioneer Deep | 8 | 10 | 80.0% |
| Pathfinder | 8 | 10 | 80.0% |
| Starliner | 6 | 10 | 60.0% |
| Scale | 8 | 10 | 80.0% |
| Velocity | 4 | 10 | 40.0% |

## Data Traceability

| Model | With Refs | Detected | Traceability |
|-------|-----------|----------|--------------|
| Sonnet 4.5 | 110 | 151 | 72.8% |
| Pioneer Deep | 138 | 153 | 90.2% |
| Pathfinder | 110 | 132 | 83.3% |
| Starliner | 101 | 139 | 72.7% |
| Scale | 114 | 135 | 84.4% |
| Velocity | 64 | 105 | 61.0% |

## Freeform Stacking: Redline Response (Part A)

| Model | Avg Part A % | Pass Rate | Passes | Total |
|-------|-------------|-----------|--------|-------|
| Sonnet 4.5 | 86.7% | 90.0% | 9 | 10 |
| Pioneer Deep | 94.2% | 100.0% | 10 | 10 |
| Pathfinder | 92.5% | 100.0% | 10 | 10 |
| Starliner | 55.0% | 50.0% | 5 | 10 |

## Cross-Validation Warnings

- pioneer_deep: detection rate mismatch — computed 95.6% (from gt_evaluations), summary 95.0% (stale cache)
- pathfinder: detection rate mismatch — computed 82.5% (from gt_evaluations), summary 83.9% (stale cache)
- starliner: detection rate mismatch — computed 86.9% (from gt_evaluations), summary 87.5% (stale cache)
- velocity: detection rate mismatch — computed 65.6% (from gt_evaluations), summary 66.2% (stale cache)
