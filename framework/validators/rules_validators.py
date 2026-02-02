"""Rules mode scoring and validation.

Rules mode uses deterministic 5-dimension scoring per rule:
- Detection (2 pts): Rule trigger correctly identified
- Compliance (1 pt): Compliance status determined
- Action (2 pts): Correct action selected (DELETE/AMEND/ADD/FLAG)
- Language (2 pts): Prescribed language used
- Rationale (2 pts): Rule citation present

Total: 9 points per rule
"""

from typing import Optional


def score_rule_evaluation(
    leah_output: Optional[dict],
    gt_rule: dict,
    config: dict
) -> dict:
    """Score a single rule evaluation with 5 dimensions."""
    scoring_config = config.get("scoring", config.get("detection_points", {}))
    dimensions = scoring_config.get("dimensions", {})

    test_id = gt_rule.get("test_id", "")
    expected_action = gt_rule.get("expected_action", "")
    trigger_quote = gt_rule.get("trigger_quote", "")
    key_elements = gt_rule.get("key_elements", [])
    rationale_must_include = gt_rule.get("rationale_must_include", [])

    if not leah_output:
        return {
            "test_id": test_id,
            "contract": gt_rule.get("contract", ""),
            "clause_ref": gt_rule.get("clause_ref", ""),
            "rule_name": gt_rule.get("rule_name", ""),
            "expected_action": expected_action,
            "detected": "NMI",
            "detection_score": 0,
            "compliance_score": 0,
            "action_score": 0,
            "language_score": 0,
            "rationale_score": 0,
            "total_score": 0,
            "max_score": scoring_config.get("per_rule_max", 9),
        }

    leah_action = leah_output.get("action", leah_output.get("recommendation", ""))
    leah_language = leah_output.get("proposed_text", leah_output.get("redline_text", ""))
    leah_rationale = leah_output.get("rationale", leah_output.get("detailed_reasoning", ""))
    leah_classification = leah_output.get("classification", "")

    # Score detection (2 pts)
    detection_score = 0
    detected = "NMI"
    trigger_found = trigger_quote and trigger_quote.lower() in (leah_rationale + leah_language).lower()
    if trigger_found or _clause_mentioned_with_concern(leah_output):
        detection_score = dimensions.get("detection", {}).get("max", 2)
        detected = "Y"

    # Score compliance (1 pt)
    compliance_score = 0
    if leah_classification:
        if any(marker in leah_classification for marker in ["❌", "⚠️", "Unfavourable", "Requires"]):
            compliance_score = dimensions.get("compliance", {}).get("max", 1)
            if detected == "NMI":
                detected = "P"

    # Score action (2 pts)
    action_score = 0
    if leah_action:
        leah_action_norm = leah_action.upper().strip()
        expected_norm = expected_action.upper().strip()
        if leah_action_norm == expected_norm:
            action_score = dimensions.get("action", {}).get("max", 2)
        elif _action_partially_correct(leah_action_norm, expected_norm):
            action_score = 1

    # Score language (2 pts)
    language_score = 0
    if leah_language and key_elements:
        language_lower = leah_language.lower()
        matched = sum(1 for elem in key_elements
                     if any(word.lower() in language_lower for word in elem.split()[:3] if len(word) > 3))
        if matched >= len(key_elements) * 0.7:
            language_score = dimensions.get("language", {}).get("max", 2)
        elif matched > 0:
            language_score = 1

    # Score rationale (2 pts)
    rationale_score = 0
    if leah_rationale and rationale_must_include:
        rationale_lower = leah_rationale.lower()
        matched = sum(1 for citation in rationale_must_include
                     if any(word.lower() in rationale_lower for word in citation.split()[:3] if len(word) > 3))
        if matched >= len(rationale_must_include) * 0.5:
            rationale_score = dimensions.get("rationale", {}).get("max", 2)
        elif matched > 0:
            rationale_score = 1

    total_score = detection_score + compliance_score + action_score + language_score + rationale_score

    if total_score == 0:
        detected = "NMI"
    elif action_score == 0 and detection_score > 0:
        detected = "P"
    elif total_score > 0 and detected == "NMI":
        detected = "P"

    return {
        "test_id": test_id,
        "contract": gt_rule.get("contract", ""),
        "clause_ref": gt_rule.get("clause_ref", ""),
        "rule_name": gt_rule.get("rule_name", ""),
        "expected_action": expected_action,
        "detected": detected,
        "detection_score": detection_score,
        "compliance_score": compliance_score,
        "action_score": action_score,
        "language_score": language_score,
        "rationale_score": rationale_score,
        "total_score": total_score,
        "max_score": scoring_config.get("per_rule_max", 9),
    }


def _clause_mentioned_with_concern(leah_output: dict) -> bool:
    classification = leah_output.get("classification", "")
    return any(marker in classification for marker in ["❌", "⚠️", "Unfavourable"])


def _action_partially_correct(leah_action: str, expected_action: str) -> bool:
    similar_pairs = [("AMEND", "DELETE"), ("DELETE", "AMEND"), ("FLAG", "AMEND")]
    return (leah_action, expected_action) in similar_pairs


def calculate_rules_pass_fail(evaluations: list[dict], config: dict) -> dict:
    """Calculate pass/fail for rules mode."""
    pass_criteria = config.get("pass_criteria", {})

    total_score = sum(e.get("total_score", 0) for e in evaluations)
    max_score = sum(e.get("max_score", 9) for e in evaluations)
    percentage = (total_score / max_score * 100) if max_score > 0 else 0

    rules_triggered = len([e for e in evaluations if e.get("detected") != "NMI"])
    rules_complied = len([e for e in evaluations if e.get("detected") == "Y" and e.get("action_score", 0) > 0])
    compliance_rate = (rules_complied / rules_triggered * 100) if rules_triggered > 0 else 0

    pass_threshold = pass_criteria.get("pass", {}).get("min_percentage", 80)
    marginal_threshold = pass_criteria.get("marginal", {}).get("min_percentage", 60)

    if percentage >= pass_threshold and compliance_rate >= 80:
        pass_fail, reason = "PASS", f"Score {percentage:.1f}% >= {pass_threshold}%"
    elif percentage >= marginal_threshold:
        pass_fail, reason = "MARGINAL", f"Score {percentage:.1f}% >= {marginal_threshold}% but < {pass_threshold}%"
    else:
        pass_fail, reason = "FAIL", f"Score {percentage:.1f}% < {marginal_threshold}%"

    return {
        "pass_fail": pass_fail,
        "reason": reason,
        "total_score": total_score,
        "max_score": max_score,
        "percentage": round(percentage, 2),
        "rules_triggered": rules_triggered,
        "rules_complied": rules_complied,
        "compliance_rate": round(compliance_rate, 2),
    }
