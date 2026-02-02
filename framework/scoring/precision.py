"""Precision calculation for additional issues."""

def calculate_precision(
    valid_additional: int,
    not_material: int,
) -> float:
    """
    Calculate precision score for additional issues.

    Precision = Valid Additional / (Valid + Not Material)

    Args:
        valid_additional: Count of valid additional issues found
        not_material: Count of issues marked "Not Material"

    Returns:
        Precision as float 0.0-1.0, or 1.0 if no denominator.
    """
    denominator = valid_additional + not_material
    if denominator == 0:
        return 1.0  # No additional issues = no false positives

    return valid_additional / denominator
