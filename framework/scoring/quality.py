"""Quality score validation (Q-Rat, Q-Amd)."""

from typing import Optional

def validate_quality_score(
    score: Optional[int | float],
    dimension: str,
    min_value: int = 0,
    max_value: int = 3,
) -> Optional[int]:
    """
    Validate and bound a quality score.

    Args:
        score: Raw score (may be None for undetected issues)
        dimension: Name for error messages (e.g., "rationale_score")
        min_value: Minimum valid score (default 0)
        max_value: Maximum valid score (default 3)

    Returns:
        Validated integer score, or None if input was None.

    Raises:
        ValueError: If score is out of range or invalid type.
    """
    if score is None:
        return None

    if not isinstance(score, (int, float)):
        raise ValueError(
            f"Quality score {dimension} must be numeric, got: {type(score).__name__}"
        )

    int_score = int(round(score))

    if int_score < min_value or int_score > max_value:
        raise ValueError(
            f"Quality score {dimension}={int_score} out of range. "
            f"Must be {min_value}-{max_value}."
        )

    return int_score
