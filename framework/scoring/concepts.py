"""
Pattern matching and detection logic branching for GT Schema v4.

Supports:
- expected_output_patterns: Flexible pattern matching across Leah outputs
- detection_logic field: Different matching strategies based on GT item type
"""

from typing import Optional


def matches_output_patterns(gt_item: dict, leah_output: dict) -> bool:
    """
    Check if Leah output matches expected_output_patterns.

    Used when detection_logic is "pattern_match" or "new_clause_recommendation".

    Args:
        gt_item: Ground truth item with optional 'expected_output_patterns' field
        leah_output: Leah output item to check against patterns

    Returns:
        True if at least one pattern matches
        False if no patterns or no matches
    """
    patterns = gt_item.get("expected_output_patterns", [])
    if not patterns:
        return False

    # Combine all Leah output text
    output_text = " ".join([
        leah_output.get("clause_name", ""),
        leah_output.get("rationale", ""),
        leah_output.get("proposed_text", ""),
        leah_output.get("issue_summary", ""),
        leah_output.get("clause_summary", ""),
        leah_output.get("detailed_reasoning", ""),
    ]).lower()

    # Check how many patterns match
    matched = sum(1 for p in patterns if p.lower() in output_text)

    # Require at least one pattern match
    return matched >= 1


def calculate_pattern_match_score(gt_item: dict, leah_output: dict) -> float:
    """
    Calculate pattern match score as fraction of patterns found.

    Args:
        gt_item: Ground truth item with expected_output_patterns
        leah_output: Leah output item to score

    Returns:
        Score 0.0-1.0 representing fraction of patterns matched
    """
    patterns = gt_item.get("expected_output_patterns", [])
    if not patterns:
        return 0.0

    # Combine all Leah output text
    output_text = " ".join([
        leah_output.get("clause_name", ""),
        leah_output.get("rationale", ""),
        leah_output.get("proposed_text", ""),
        leah_output.get("issue_summary", ""),
        leah_output.get("clause_summary", ""),
        leah_output.get("detailed_reasoning", ""),
    ]).lower()

    matched = sum(1 for p in patterns if p.lower() in output_text)
    return matched / len(patterns)


def get_detection_strategy(gt_item: dict) -> str:
    """
    Determine which detection strategy to use based on detection_logic field.

    Args:
        gt_item: Ground truth item with optional 'detection_logic' field

    Returns:
        Strategy name: "standard", "new_clause_recommendation", "pattern_match", "any_mention"
    """
    return gt_item.get("detection_logic", "standard")


def assess_concept_coverage(
    required_concepts: list[str],
    reasoning: str,
    strict: bool = False
) -> dict:
    """
    Assess coverage of required concepts in Leah's reasoning.

    Args:
        required_concepts: List of concepts that should appear
        reasoning: Leah's reasoning text
        strict: If True, require exact phrase match; if False, allow word-level partial matches

    Returns:
        Dict with coverage stats:
        - coverage: float 0.0-1.0
        - matched_concepts: list of concepts found
        - missing_concepts: list of concepts not found
        - detection_level: "Y" or "P"
    """
    if not required_concepts:
        return {
            "coverage": 1.0,
            "matched_concepts": [],
            "missing_concepts": [],
            "detection_level": "Y"
        }

    reasoning_lower = reasoning.lower()
    matched = []
    missing = []
    total_score = 0.0

    for concept in required_concepts:
        concept_lower = concept.lower()

        if concept_lower in reasoning_lower:
            # Full concept match
            matched.append(concept)
            total_score += 1.0
        elif not strict and any(word in reasoning_lower for word in concept_lower.split()):
            # Partial match: at least one word from multi-word concept
            matched.append(f"{concept} (partial)")
            total_score += 0.5
        else:
            missing.append(concept)

    coverage = min(total_score / len(required_concepts), 1.0)

    return {
        "coverage": coverage,
        "matched_concepts": matched,
        "missing_concepts": missing,
        "detection_level": "Y" if coverage >= 0.5 else "P"
    }


def should_search_section(gt_item: dict, section: str) -> bool:
    """
    Determine if a GT item should be matched against a specific output section.

    Args:
        gt_item: Ground truth item with detection_logic
        section: Section name ("risk_table", "proposed_redlines", "new_clauses_proposed")

    Returns:
        True if this section should be searched for matches
    """
    detection_logic = get_detection_strategy(gt_item)

    if detection_logic == "standard":
        # Standard items search risk_table and proposed_redlines
        return section in ["risk_table", "proposed_redlines"]

    elif detection_logic == "new_clause_recommendation":
        # NCR items search all sections including new_clauses_proposed
        return section in ["risk_table", "proposed_redlines", "new_clauses_proposed"]

    elif detection_logic == "pattern_match":
        # Pattern matching searches all sections
        return True

    elif detection_logic == "any_mention":
        # Any mention searches everywhere
        return True

    return False
