"""Pre-workbook validation gate - checks aggregated results prerequisites."""

import json
from pathlib import Path
from typing import Union

from .base import ValidationResult, ValidationIssue, Severity


def validate_pre_workbook(mode_dir: Union[Path, str], env: str) -> ValidationResult:
    """Validate prerequisites before workbook generation stage.

    Checks:
    - Aggregated directory exists (either direct or environment-specific)
    - Aggregated directory has JSON files
    - At least one aggregated file has content
    - Zero-score anomalies (warning only)

    Args:
        mode_dir: Path to mode directory (e.g., freeform/)
        env: Environment name (e.g., hotfix, test_prod2)

    Returns:
        ValidationResult with errors/warnings
    """
    issues = []
    mode_dir = Path(mode_dir)

    # 1. Check aggregated directory exists
    # Try both locations:
    #   1. environments/{env}/aggregated (environment-specific)
    #   2. aggregated (direct path)
    aggregated_dir = mode_dir / "environments" / env / "aggregated"
    checked_paths = [str(aggregated_dir)]

    if not aggregated_dir.exists():
        aggregated_dir = mode_dir / "aggregated"
        checked_paths.append(str(aggregated_dir))

    if not aggregated_dir.exists():
        paths_str = ", ".join(checked_paths)
        issues.append(ValidationIssue(
            severity=Severity.ERROR,
            message=f"Aggregated directory not found (checked: {paths_str})",
            location=str(mode_dir),
            context={"checked_paths": checked_paths}
        ))
        # Can't proceed without aggregated directory
        return ValidationResult(valid=False, issues=issues)

    # 2. Check aggregated directory has JSON files
    # Files may be flat or in contract subdirectories
    json_files = list(aggregated_dir.rglob("*.json"))
    # Filter out internal files
    json_files = [f for f in json_files if not f.name.startswith("_")]

    if not json_files:
        issues.append(ValidationIssue(
            severity=Severity.ERROR,
            message=f"Aggregated directory is empty: {aggregated_dir}",
            location=str(aggregated_dir),
            context={"expected": "JSON files with aggregated evaluation results"}
        ))
        return ValidationResult(valid=False, issues=issues)

    # 3. Validate at least one aggregated file has content
    has_valid_content = False
    all_empty = True

    for agg_file in json_files[:10]:  # Check first 10 files (don't need to check all)
        try:
            with open(agg_file) as f:
                data = json.load(f)

            if not data:
                continue

            all_empty = False

            # Check if it's a non-empty dict (expected structure)
            if isinstance(data, dict) and data:
                has_valid_content = True

                # 4. Check for zero-score anomalies (warning only)
                _check_zero_scores(data, agg_file, issues)

        except json.JSONDecodeError as e:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Invalid JSON in aggregated file: {agg_file.name} (line {e.lineno})",
                location=str(agg_file),
                context={"error": e.msg, "line": e.lineno}
            ))
        except OSError as e:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                message=f"Cannot read aggregated file: {agg_file.name}",
                location=str(agg_file),
                context={"error": str(e)}
            ))

    if all_empty:
        issues.append(ValidationIssue(
            severity=Severity.ERROR,
            message=f"All aggregated files are empty: {aggregated_dir}",
            location=str(aggregated_dir),
            context={"files_checked": len(json_files[:10])}
        ))

    # Determine if valid (no errors)
    valid = len([i for i in issues if i.severity == Severity.ERROR]) == 0

    return ValidationResult(valid=valid, issues=issues)


def _check_zero_scores(data: dict, file_path: Path, issues: list):
    """Check for zero-score anomalies in aggregated data.

    Zero scores with GT items present may indicate data/config issues.
    These are warnings not errors (may be legitimate poor model performance).

    Args:
        data: Loaded aggregated JSON data
        file_path: Path to aggregated file
        issues: List to append ValidationIssue objects to
    """
    # Check summary section for zero scores
    summary = data.get("summary", {})

    # Check if total_points is zero but gt_evaluations exist
    total_points = summary.get("total_points", 0)
    weighted_score = summary.get("weighted_score", 0)

    # Check if there are GT items that were evaluated
    gt_evaluations = data.get("gt_evaluations", [])
    has_gt = len(gt_evaluations) > 0

    if has_gt and total_points == 0 and weighted_score == 0:
        issues.append(ValidationIssue(
            severity=Severity.WARNING,
            message=f"Zero score with GT items present: {file_path.name}",
            location=str(file_path),
            context={
                "total_points": total_points,
                "weighted_score": weighted_score,
                "gt_items": len(gt_evaluations),
                "note": "May indicate data issue or legitimately poor model performance"
            }
        ))

    # Check part-specific zero scores (for multi-part evaluations)
    for part_key in ["part_a", "part_b", "part_c"]:
        part_data = summary.get(part_key, {})
        if not part_data:
            continue

        part_score = part_data.get("total_score") or part_data.get("weighted_score")
        if part_score == 0 and has_gt:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                message=f"Zero {part_key} score: {file_path.name}",
                location=str(file_path),
                context={
                    "part": part_key,
                    "score": part_score,
                    "note": "May indicate missing part data or poor performance"
                }
            ))
