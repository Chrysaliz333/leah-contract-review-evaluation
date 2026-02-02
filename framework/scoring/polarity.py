"""
Polarity-aware detection assignment for GT Schema v4.

Handles both standard (negative) and compliance (positive) polarity items:
- Negative polarity: ❌/⚠️ = issue detected (default behaviour)
- Positive polarity: ✅ = compliance confirmed (inverted logic)
"""

from typing import Optional
from .classification import is_issue_detected


def assign_detection_with_polarity(gt_item: dict, matches: list[dict]) -> str:
    """
    Assign detection value respecting polarity.

    For polarity=negative (default): ❌/⚠️ = detected, ✅ = not detected
    For polarity=positive: ✅ = detected (confirmed present), ❌/⚠️ = not detected (incorrectly flagged)

    Args:
        gt_item: Ground truth item with optional 'polarity' field
        matches: List of matched Leah outputs with classification info

    Returns:
        Detection value: "Y", "P", "N", or "NMI"
    """
    polarity = gt_item.get("polarity", "negative")

    if not matches:
        return "NMI"

    best_match = matches[0]
    classification = best_match["item"].get("classification")
    detected = is_issue_detected(classification)

    if polarity == "negative":
        # Standard: issue should be flagged
        if detected is False:
            return "N"  # Marked favorable when issue exists
        elif detected is True:
            return assess_detection_level(gt_item, best_match)  # Y or P
        else:
            return "P"  # Ambiguous

    elif polarity == "positive":
        # Compliance confirmation: should be marked favorable
        if detected is False:
            # ✅ Favorable — correct! This is what we wanted
            return assess_detection_level(gt_item, best_match)  # Y or P based on reasoning
        elif detected is True:
            # ❌/⚠️ — incorrectly flagged a compliant clause
            return "N"
        else:
            return "P"  # Ambiguous

    return "NMI"


def assess_detection_level(gt_item: dict, match: dict) -> str:
    """
    Determine Y vs P based on required_concepts coverage.

    If gt_item has required_concepts, check how many appear in reasoning.

    Args:
        gt_item: Ground truth item with optional 'required_concepts' field
        match: Matched Leah output with reasoning text

    Returns:
        "Y" if sufficient concept coverage (>=50% or no requirements)
        "P" if partial coverage (<50%)
    """
    required_concepts = gt_item.get("required_concepts", [])

    if not required_concepts:
        # No required_concepts — full detection if match found
        return "Y"

    # Check concept coverage in reasoning
    reasoning = match["item"].get("rationale", "") + " " + match["item"].get("detailed_reasoning", "")
    reasoning_lower = reasoning.lower()

    matched_concepts = sum(1 for concept in required_concepts if concept.lower() in reasoning_lower)
    coverage = matched_concepts / len(required_concepts)

    if coverage >= 0.5:
        return "Y"  # Sufficient concept coverage
    else:
        return "P"  # Partial — detected but reasoning incomplete


def calculate_concept_coverage(required_concepts: list[str], reasoning: str) -> float:
    """
    Calculate what fraction of required concepts appear in reasoning.

    Args:
        required_concepts: List of concepts that should appear in reasoning
        reasoning: Leah's reasoning text to check

    Returns:
        Coverage ratio 0.0-1.0
    """
    if not required_concepts:
        return 1.0  # No requirements = full coverage

    reasoning_lower = reasoning.lower()
    matched = 0.0

    for concept in required_concepts:
        # Check for concept or close variants
        concept_lower = concept.lower()
        if concept_lower in reasoning_lower:
            matched += 1.0
        elif any(word in reasoning_lower for word in concept_lower.split()):
            # Partial match: at least one word from multi-word concept
            matched += 0.5

    return min(matched / len(required_concepts), 1.0)


def concept_coverage_to_detection(coverage: float) -> str:
    """
    Convert concept coverage to detection level.

    Args:
        coverage: Concept coverage ratio 0.0-1.0

    Returns:
        "Y" if >= 50% coverage
        "P" if > 0% coverage
    """
    if coverage >= 0.5:
        return "Y"
    else:
        return "P"
