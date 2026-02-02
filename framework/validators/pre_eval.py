"""Pre-evaluation validation gate - checks GT and canonical JSON prerequisites."""

import json
from pathlib import Path
from typing import Union

from .base import ValidationResult, ValidationIssue, Severity


def validate_pre_evaluation(mode_dir: Union[Path, str], env: str) -> ValidationResult:
    """Validate prerequisites before evaluation stage.

    Checks:
    - Mode directory exists
    - Ground truth directory exists and has JSON files
    - Canonical JSON directory exists and has data
    - GT JSON files are parseable

    Args:
        mode_dir: Path to mode directory (e.g., freeform/)
        env: Environment name (e.g., hotfix, test_prod2)

    Returns:
        ValidationResult with errors/warnings
    """
    issues = []
    mode_dir = Path(mode_dir)

    # 1. Check mode directory exists
    if not mode_dir.exists():
        issues.append(ValidationIssue(
            severity=Severity.ERROR,
            message=f"Mode directory not found: {mode_dir}",
            location=str(mode_dir)
        ))
        # Can't proceed without mode directory
        return ValidationResult(valid=False, issues=issues)

    # 2. Check ground truth directory exists and has JSON files
    gt_dir = mode_dir / "ground_truth"
    if not gt_dir.exists():
        issues.append(ValidationIssue(
            severity=Severity.ERROR,
            message=f"Ground truth directory not found: {gt_dir}",
            location=str(gt_dir)
        ))
    else:
        # Get GT files (exclude changelog files starting with _)
        gt_files = [f for f in gt_dir.glob("*.json") if not f.name.startswith("_")]

        if not gt_files:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Ground truth directory empty: {gt_dir}",
                location=str(gt_dir),
                context={"expected": "JSON files for ground truth definitions"}
            ))
        else:
            # Validate GT JSON files are parseable
            for gt_file in gt_files:
                try:
                    with open(gt_file) as f:
                        data = json.load(f)

                    # Check if GT has expected structure (warning only)
                    if not isinstance(data, dict):
                        issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            message=f"GT file is not a dict: {gt_file.name}",
                            location=str(gt_file),
                            context={"type": str(type(data))}
                        ))
                    elif "ground_truth" not in data:
                        issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            message=f"GT file missing 'ground_truth' key: {gt_file.name}",
                            location=str(gt_file),
                            context={"keys": list(data.keys())}
                        ))

                except json.JSONDecodeError as e:
                    issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Invalid JSON in GT file: {gt_file.name} (line {e.lineno})",
                        location=str(gt_file),
                        context={"error": e.msg, "line": e.lineno}
                    ))
                except OSError as e:
                    issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Cannot read GT file: {gt_file.name}",
                        location=str(gt_file),
                        context={"error": str(e)}
                    ))

    # 3. Check canonical JSON directory exists and has data
    # Try multiple possible locations:
    #   1. environments/{env}/canonical_json (current structure)
    #   2. canonical_json_{env} (legacy)
    #   3. canonical_json (legacy)
    canonical_dir = mode_dir / "environments" / env / "canonical_json"
    checked_paths = [str(canonical_dir)]

    if not canonical_dir.exists():
        canonical_dir = mode_dir / f"canonical_json_{env}"
        checked_paths.append(str(canonical_dir))

    if not canonical_dir.exists():
        canonical_dir = mode_dir / "canonical_json"
        checked_paths.append(str(canonical_dir))

    if not canonical_dir.exists():
        paths_str = ", ".join(checked_paths)
        issues.append(ValidationIssue(
            severity=Severity.ERROR,
            message=f"Canonical JSON directory not found (checked: {paths_str})",
            location=str(mode_dir),
            context={"checked_paths": checked_paths}
        ))
    else:
        # Check for contract subdirectories
        contract_dirs = [d for d in canonical_dir.iterdir()
                        if d.is_dir() and not d.name.startswith("_")]

        if not contract_dirs:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"No contract subdirectories in canonical_json: {canonical_dir}",
                location=str(canonical_dir),
                context={"expected_structure": "{canonical_dir}/{contract}/{model}.json"}
            ))
        else:
            # Verify at least one contract has JSON files
            has_json = False
            for contract_dir in contract_dirs:
                json_files = list(contract_dir.glob("*.json"))
                if json_files:
                    has_json = True
                    break

            if not has_json:
                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"No model JSON files in canonical_json: {canonical_dir}",
                    location=str(canonical_dir),
                    context={"contracts_checked": len(contract_dirs)}
                ))

    # Determine if valid (no errors)
    valid = len([i for i in issues if i.severity == Severity.ERROR]) == 0

    return ValidationResult(valid=valid, issues=issues)
