# Raw LLM Baseline Comparison Report

Generated: 2026-02-03 21:19 UTC
Contracts: 10 | Models: 4

> **Detection-only evaluation (recall).** Raw LLMs were given the prompt
> "Review this contract" with no further guidance. Scores reflect issue
> detection only — no amendment quality scoring.

## Overall Scores

| Model | Detection Pts | Max Pts | Score % | Detection Rate | T1 Gates |
|-------|--------------|---------|---------|----------------|----------|
| OpenAI o3 | 629.5 | 787 | 80.0% | 85.6% | 9/10 |
| GPT-4.1 | 411.5 | 787 | 52.3% | 65.6% | 4/10 |
| Claude Sonnet 4 | 361.5 | 787 | 45.9% | 55.0% | 3/10 |
| Claude 3.5 Haiku | 157.5 | 787 | 20.0% | 30.0% | 0/10 |

## Per-Contract Breakdown

### consulting

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 27.5 | 50 | 55.0% | 72.7% | PASS |
| GPT-4.1 | 16.0 | 50 | 32.0% | 54.5% | FAIL |
| Claude Sonnet 4 | 10.5 | 50 | 21.0% | 36.4% | FAIL |
| Claude 3.5 Haiku | 13.5 | 50 | 27.0% | 45.5% | FAIL |

### dpa

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 55.0 | 57 | 96.5% | 83.3% | PASS |
| GPT-4.1 | 29.0 | 57 | 50.9% | 66.7% | PASS |
| Claude Sonnet 4 | 35.5 | 57 | 62.3% | 83.3% | PASS |
| Claude 3.5 Haiku | 10.0 | 57 | 17.5% | 33.3% | FAIL |

### distribution

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 58.5 | 75 | 78.0% | 84.6% | FAIL |
| GPT-4.1 | 44.0 | 75 | 58.7% | 76.9% | PASS |
| Claude Sonnet 4 | 35.5 | 75 | 47.3% | 53.8% | FAIL |
| Claude 3.5 Haiku | 17.0 | 75 | 22.7% | 38.5% | FAIL |

### jv

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 70.0 | 93 | 75.3% | 83.3% | PASS |
| GPT-4.1 | 55.0 | 93 | 59.1% | 77.8% | FAIL |
| Claude Sonnet 4 | 56.5 | 93 | 60.8% | 61.1% | PASS |
| Claude 3.5 Haiku | 24.0 | 93 | 25.8% | 38.9% | FAIL |

### license

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 66.5 | 71 | 93.7% | 93.3% | PASS |
| GPT-4.1 | 48.0 | 71 | 67.6% | 86.7% | PASS |
| Claude Sonnet 4 | 43.0 | 71 | 60.6% | 80.0% | PASS |
| Claude 3.5 Haiku | 17.0 | 71 | 23.9% | 26.7% | FAIL |

### partnership

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 62.0 | 70 | 88.6% | 91.7% | PASS |
| GPT-4.1 | 32.5 | 70 | 46.4% | 41.7% | FAIL |
| Claude Sonnet 4 | 41.0 | 70 | 58.6% | 58.3% | FAIL |
| Claude 3.5 Haiku | 26.5 | 70 | 37.9% | 33.3% | FAIL |

### reseller

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 66.5 | 69 | 96.4% | 100.0% | PASS |
| GPT-4.1 | 42.5 | 69 | 61.6% | 76.9% | FAIL |
| Claude Sonnet 4 | 31.0 | 69 | 44.9% | 46.2% | FAIL |
| Claude 3.5 Haiku | 11.5 | 69 | 16.7% | 23.1% | FAIL |

### services

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 63.5 | 98 | 64.8% | 76.9% | PASS |
| GPT-4.1 | 36.5 | 98 | 37.2% | 57.7% | FAIL |
| Claude Sonnet 4 | 20.0 | 98 | 20.4% | 30.8% | FAIL |
| Claude 3.5 Haiku | 14.0 | 98 | 14.3% | 23.1% | FAIL |

### sla

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 103.0 | 130 | 79.2% | 84.6% | PASS |
| GPT-4.1 | 62.0 | 130 | 47.7% | 50.0% | FAIL |
| Claude Sonnet 4 | 66.0 | 130 | 50.8% | 65.4% | FAIL |
| Claude 3.5 Haiku | 15.0 | 130 | 11.5% | 26.9% | FAIL |

### supply

| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |
|-------|--------------|-----|---------|----------------|---------|
| OpenAI o3 | 57.0 | 74 | 77.0% | 92.9% | PASS |
| GPT-4.1 | 46.0 | 74 | 62.2% | 78.6% | PASS |
| Claude Sonnet 4 | 22.5 | 74 | 30.4% | 42.9% | FAIL |
| Claude 3.5 Haiku | 9.0 | 74 | 12.2% | 21.4% | FAIL |

## Detection Breakdown

| Model | Y | P | N | NMI | Total |
|-------|---|---|---|-----|-------|
| OpenAI o3 | 101 | 36 | 23 | 0 | 160 |
| GPT-4.1 | 48 | 57 | 55 | 0 | 160 |
| Claude Sonnet 4 | 43 | 45 | 72 | 0 | 160 |
| Claude 3.5 Haiku | 8 | 40 | 112 | 0 | 160 |
