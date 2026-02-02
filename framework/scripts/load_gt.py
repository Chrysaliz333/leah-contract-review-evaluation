#!/usr/bin/env python3
"""
Load Ground Truth JSON files with GT Schema v4 defaults.

Usage:
    from framework.scripts.load_gt import load_gt_with_defaults

    gt = load_gt_with_defaults(Path("freeform/ground_truth/consulting.json"))
"""

import json
from pathlib import Path
from typing import Union


def load_gt_with_defaults(gt_path: Union[Path, str]) -> dict:
    """
    Load GT file and apply v4 defaults for missing fields.

    Args:
        gt_path: Path to ground truth JSON file

    Returns:
        Ground truth data with v4 defaults applied

    Raises:
        FileNotFoundError: If GT file doesn't exist
        json.JSONDecodeError: If GT file is invalid JSON
    """
    gt_path = Path(gt_path)

    if not gt_path.exists():
        raise FileNotFoundError(f"GT file not found: {gt_path}")

    with open(gt_path) as f:
        data = json.load(f)

    # Handle both "ground_truth" and "issues" keys
    issues = data.get("ground_truth", data.get("issues", []))

    for issue in issues:
        # Apply v4 defaults for optional fields
        issue.setdefault("detection_logic", "standard")
        issue.setdefault("expected_output_patterns", [])
        issue.setdefault("polarity", "negative")
        issue.setdefault("required_concepts", [])
        issue.setdefault("reasoning_must_contain", [])
        issue.setdefault("reasoning_must_not_contain", [])

        # Infer detection_logic from expected_action if still at default
        if issue["detection_logic"] == "standard":
            expected_action = issue.get("expected_action", "")
            clause = issue.get("clause", "")

            # ADD action suggests new clause recommendation
            if expected_action == "ADD":
                issue["detection_logic"] = "new_clause_recommendation"
            # Missing clause indicators
            elif "N/A" in clause or "Missing" in clause.lower():
                issue["detection_logic"] = "new_clause_recommendation"

    return data


def main():
    """Example usage and testing."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python load_gt.py <gt_file.json>")
        sys.exit(1)

    gt_path = Path(sys.argv[1])

    try:
        data = load_gt_with_defaults(gt_path)

        # Show sample issue with v4 fields
        issues = data.get("ground_truth", data.get("issues", []))
        if issues:
            sample = issues[0]
            print(f"Sample GT item: {sample.get('gt_id')}")
            print(f"  detection_logic: {sample['detection_logic']}")
            print(f"  polarity: {sample['polarity']}")
            print(f"  required_concepts: {sample['required_concepts']}")

        print(f"\n✓ Loaded {len(issues)} GT items with v4 defaults")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
