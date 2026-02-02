"""Reasoning validation for catching false favorable assessments."""

from typing import Optional


def validate_reasoning(
    reasoning: str,
    must_contain: list[str],
    must_not_contain: list[str],
) -> dict:
    """
    Validate reasoning against required/forbidden phrases.

    Returns:
        {
            "valid": bool,
            "missing_required": list[str],  # Required phrases not found
            "forbidden_found": list[str],   # Forbidden phrases that were found
            "confidence": float,            # 0.0-1.0 based on violations
        }
    """
    reasoning_lower = reasoning.lower()

    # Check required phrases
    missing_required = []
    for phrase in must_contain:
        if phrase.lower() not in reasoning_lower:
            missing_required.append(phrase)

    # Check forbidden phrases
    forbidden_found = []
    for phrase in must_not_contain:
        if phrase.lower() in reasoning_lower:
            forbidden_found.append(phrase)

    # Calculate validity and confidence
    valid = len(missing_required) == 0 and len(forbidden_found) == 0

    # Confidence degrades with violations
    total_checks = len(must_contain) + len(must_not_contain)
    violations = len(missing_required) + len(forbidden_found)

    if total_checks == 0:
        confidence = 1.0
    else:
        confidence = max(0.0, 1.0 - (violations / total_checks))

    return {
        "valid": valid,
        "missing_required": missing_required,
        "forbidden_found": forbidden_found,
        "confidence": confidence,
    }


def check_false_favorable(
    classification: str,
    reasoning: str,
    gt_item: dict,
) -> dict:
    """
    Check if a ✅ Favorable classification is actually a false favorable.

    Only applies when:
    1. Classification is favorable (✅)
    2. GT item has reasoning_must_contain or reasoning_must_not_contain

    Returns:
        {
            "is_false_favorable": bool,
            "reason": str,
            "validation_result": dict,  # From validate_reasoning
        }
    """
    from .classification import is_issue_detected

    must_contain = gt_item.get("reasoning_must_contain", [])
    must_not_contain = gt_item.get("reasoning_must_not_contain", [])

    # No validation rules = can't be false favorable
    if not must_contain and not must_not_contain:
        return {
            "is_false_favorable": False,
            "reason": "No reasoning validation rules defined",
            "validation_result": None,
        }

    # Only check if classification is favorable
    detected = is_issue_detected(classification)
    if detected is not False:
        return {
            "is_false_favorable": False,
            "reason": "Classification is not favorable",
            "validation_result": None,
        }

    # Validate reasoning
    result = validate_reasoning(reasoning, must_contain, must_not_contain)

    if not result["valid"]:
        # Reasoning validation failed — this is a false favorable
        reasons = []
        if result["missing_required"]:
            reasons.append(f"Missing required: {result['missing_required']}")
        if result["forbidden_found"]:
            reasons.append(f"Contains forbidden: {result['forbidden_found']}")

        return {
            "is_false_favorable": True,
            "reason": "; ".join(reasons),
            "validation_result": result,
        }

    return {
        "is_false_favorable": False,
        "reason": "Reasoning validation passed",
        "validation_result": result,
    }
