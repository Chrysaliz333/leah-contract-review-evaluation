"""
Scoring module - pure functions for evaluation scoring.

All functions take configuration as explicit parameters.
No global state, no file I/O, no LLM calls.
"""

from .normalisation import (
    normalise_detection,
    CANONICAL_DETECTIONS,
    DETECTION_ALIASES,
)
from .detection import (
    calculate_detection_points,
    Detection,
    Tier,
)
from .quality import validate_quality_score
from .recall import calculate_recall, calculate_weighted_recall
from .precision import calculate_precision
from .f1 import calculate_f1

__all__ = [
    # Normalisation
    "normalise_detection",
    "CANONICAL_DETECTIONS",
    "DETECTION_ALIASES",
    # Detection
    "calculate_detection_points",
    "Detection",
    "Tier",
    # Quality
    "validate_quality_score",
    # Recall
    "calculate_recall",
    "calculate_weighted_recall",
    # Precision
    "calculate_precision",
    # F1
    "calculate_f1",
]
