"""Detection point calculation with config-driven weights."""

from typing import Literal

Detection = Literal["Y", "P", "N", "NMI"]
Tier = Literal["T1", "T2", "T3"]

def calculate_detection_points(
    detection: Detection,
    tier: Tier,
    tier_config: dict[str, dict[str, float]],
) -> float:
    """
    Calculate points for a single detection.

    Args:
        detection: One of Y, P, N, NMI
        tier: One of T1, T2, T3
        tier_config: Mapping from tier to detection values
            e.g., {"T1": {"Y": 8, "P": 4, "N": -5, "NMI": -5}, ...}

    Returns:
        Point value for this detection.

    Raises:
        ValueError: If detection or tier not in expected set.
    """
    if detection not in ("Y", "P", "N", "NMI"):
        raise ValueError(
            f"Invalid detection value: {detection!r}. "
            f"Expected one of: Y, P, N, NMI"
        )

    if tier not in tier_config:
        raise ValueError(
            f"Unknown tier: {tier!r}. "
            f"Expected one of: {list(tier_config.keys())}"
        )

    return tier_config[tier].get(detection, 0)
