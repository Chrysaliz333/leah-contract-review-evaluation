"""Recall calculation - unweighted and tier-weighted."""

from typing import Sequence

def calculate_recall(
    detected_count: int,
    total_count: int,
) -> float:
    """
    Calculate simple recall (detected / total).

    Returns 0.0 if total_count is 0.
    """
    if total_count == 0:
        return 0.0
    return detected_count / total_count


def calculate_weighted_recall(
    scored_issues: Sequence[dict],
    tier_config: dict[str, dict[str, float]],
    detection_field: str = "detection",
    tier_field: str = "gt_tier",
) -> tuple[float, float, float]:
    """
    Calculate tier-weighted recall.

    Args:
        scored_issues: List of dicts with detection and tier fields
        tier_config: Mapping from tier to detection values
            e.g., {"T1": {"Y": 8, "P": 4, "N": 0, "NMI": 0}, ...}
        detection_field: Key for detection value in issue dict
        tier_field: Key for tier in issue dict

    Returns:
        Tuple of (actual_score, max_score, weighted_recall)
        weighted_recall is actual_score / max_score (0.0 if max is 0)
    """
    actual_score = 0.0
    max_score = 0.0

    for issue in scored_issues:
        tier = issue.get(tier_field, "T3")
        detection = issue.get(detection_field, "NMI")

        # Get max points for this tier (Y detection)
        tier_points = tier_config.get(tier, {})
        max_for_tier = tier_points.get("Y", 1)
        max_score += max_for_tier

        # Get actual points for this detection
        actual_score += tier_points.get(detection, 0)

    weighted_recall = actual_score / max_score if max_score > 0 else 0.0

    return actual_score, max_score, weighted_recall
