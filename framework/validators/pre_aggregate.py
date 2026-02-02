"""Pre-aggregation validation gate.

Validates that all runs have identical, complete contract/model coverage
before aggregation begins.
"""

import json
from pathlib import Path
from typing import Optional

from .base import ValidationResult, ValidationIssue, Severity


def validate_pre_aggregation(runs: list[Path]) -> ValidationResult:
    """Validate all prerequisites for aggregation.

    Gates:
    - All runs have identical contract/model coverage
    - No missing evaluations
    - All evaluation files are valid JSON
    - Zero-score anomalies flagged as warnings

    Args:
        runs: List of run directories to validate

    Returns:
        ValidationResult with valid=True only if no ERROR-severity issues
    """
    issues: list[ValidationIssue] = []

    # Gate 0: Check runs exist
    existing_runs = [r for r in runs if r.exists()]
    if not existing_runs:
        return ValidationResult(
            valid=True,  # No runs = nothing to aggregate, not an error
            issues=[ValidationIssue(
                severity=Severity.WARNING,
                message="No run directories found",
                location="aggregation",
                context={"runs_requested": [str(r) for r in runs]}
            )]
        )

    # Gate 1: Discover expected scope from all runs
    all_contracts: set[str] = set()
    all_models: set[str] = set()

    for run in existing_runs:
        eval_dir = run / "evaluations"
        if not eval_dir.exists():
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message="Run missing evaluations directory",
                location=str(run),
                context={"expected_path": str(eval_dir)}
            ))
            continue

        for contract_dir in eval_dir.iterdir():
            if contract_dir.is_dir() and not contract_dir.name.startswith("_"):
                all_contracts.add(contract_dir.name)
                for model_file in contract_dir.glob("*.json"):
                    all_models.add(model_file.stem)

    if not all_contracts:
        issues.append(ValidationIssue(
            severity=Severity.WARNING,
            message="No contracts found across all runs",
            location="aggregation",
            context={"runs_checked": [r.name for r in existing_runs]}
        ))
        return ValidationResult(
            valid=len([i for i in issues if i.severity == Severity.ERROR]) == 0,
            issues=issues
        )

    expected_total = len(all_contracts) * len(all_models)

    # Gate 2: Verify each run has complete coverage
    run_coverage: dict[str, int] = {}
    for run in existing_runs:
        eval_dir = run / "evaluations"
        actual = 0
        missing: list[str] = []

        for contract in sorted(all_contracts):
            for model in sorted(all_models):
                path = eval_dir / contract / f"{model}.json"
                if path.exists():
                    actual += 1
                else:
                    missing.append(f"{contract}/{model}")

        run_coverage[run.name] = actual

        if actual != expected_total:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Incomplete coverage: {actual}/{expected_total} evaluations",
                location=str(run),
                context={
                    "missing": missing[:5],  # First 5 for brevity
                    "total_missing": len(missing)
                }
            ))

    # Gate 3: Verify all runs have identical coverage
    coverages = list(run_coverage.values())
    if len(set(coverages)) > 1:
        issues.append(ValidationIssue(
            severity=Severity.ERROR,
            message=f"Run coverage differs: {run_coverage}",
            location="aggregation",
            context={"coverage_by_run": run_coverage}
        ))

    # Gate 4: Validate JSON integrity and check for anomalies
    for run in existing_runs:
        eval_dir = run / "evaluations"
        for contract in all_contracts:
            for model in all_models:
                path = eval_dir / contract / f"{model}.json"
                if not path.exists():
                    continue  # Already flagged in Gate 2

                # JSON integrity check
                try:
                    with open(path) as f:
                        data = json.load(f)
                except json.JSONDecodeError as e:
                    issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Invalid JSON at line {e.lineno}: {e.msg}",
                        location=str(path),
                        context={"error": str(e)}
                    ))
                    continue

                # Semantic validation: zero-score anomaly
                gt_evals = data.get("gt_evaluations", [])
                summary = data.get("summary", {})
                total_pts = summary.get("total_points", 0)

                if total_pts == 0 and len(gt_evals) > 0:
                    issues.append(ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"Zero score with {len(gt_evals)} GT items - verify data/config",
                        location=f"{run.name}/{contract}/{model}",
                        context={
                            "gt_count": len(gt_evals),
                            "total_points": total_pts
                        }
                    ))

    return ValidationResult(
        valid=len([i for i in issues if i.severity == Severity.ERROR]) == 0,
        issues=issues
    )
