"""Validation utilities for stacking evaluation modes.

Handles:
- Freeform_stacking: CP redline action validation, adversarial detection
- Rules_stacking: Scope violation detection (added in 07-04)
"""

from typing import Optional


def validate_cp_redline_action(
    leah_action: str,
    acceptable_actions: list[str],
    redline_id: str
) -> dict:
    """Validate Leah's action against acceptable actions for a CP redline.

    Args:
        leah_action: The action Leah took (ACCEPT, MODIFY, REJECT)
        acceptable_actions: List of acceptable actions from GT
        redline_id: ID of the redline for error context

    Returns:
        Dict with action_correct, is_adversarial, critical_failure
    """
    leah_action_norm = leah_action.upper().strip() if leah_action else "NMI"
    acceptable_norm = [a.upper().strip() for a in acceptable_actions]

    is_adversarial = "ACCEPT" not in acceptable_norm
    action_correct = leah_action_norm in acceptable_norm

    critical_failure = None
    if is_adversarial and leah_action_norm == "ACCEPT":
        critical_failure = {
            "redline_id": redline_id,
            "failure_type": "ACCEPT_ON_ADVERSARIAL",
            "expected": acceptable_actions,
            "actual": leah_action,
            "severity": "CRITICAL",
            "message": f"Leah accepted adversarial redline {redline_id} that should be REJECT/MODIFY"
        }

    return {
        "action_correct": action_correct,
        "is_adversarial": is_adversarial,
        "critical_failure": critical_failure
    }


def detect_critical_failures(evaluations: list[dict]) -> list[dict]:
    """Extract all critical failures from Part A evaluations."""
    return [
        e["critical_failure"]
        for e in evaluations
        if e.get("critical_failure")
    ]


def score_part_a_redline(
    leah_response: Optional[dict],
    gt_redline: dict,
    config: dict
) -> dict:
    """Score a single Part A CP redline evaluation.

    Scoring dimensions (per_redline: 6 max):
    - action: 2 points (correct action per acceptable_actions)
    - revision: 2 points (quality of proposed revision)
    - reasoning: 2 points (explanation quality)
    """
    part_a_config = config.get("detection_points", {}).get("part_a", {})
    max_per_dimension = part_a_config.get("max_per_dimension", 2)
    max_total = part_a_config.get("per_redline", 6)

    redline_id = gt_redline.get("test_id", "")
    acceptable_actions = gt_redline.get("acceptable_actions", [])

    if not leah_response:
        is_adversarial = "ACCEPT" not in [a.upper() for a in acceptable_actions]
        return {
            "redline_id": redline_id,
            "clause_ref": gt_redline.get("clause_ref"),
            "expected_actions": acceptable_actions,
            "leah_action": "NMI",
            "action_correct": False,
            "action_score": 0,
            "revision_score": 0,
            "reasoning_score": 0,
            "total_score": 0,
            "max_score": max_total,
            "is_adversarial": is_adversarial,
            "critical_failure": {
                "redline_id": redline_id,
                "failure_type": "NOT_MENTIONED",
                "severity": "HIGH"
            } if is_adversarial else None
        }

    leah_action = leah_response.get("action", leah_response.get("recommendation", ""))
    leah_revision = leah_response.get("proposed_text", leah_response.get("redline_text", ""))
    leah_reasoning = leah_response.get("rationale", leah_response.get("detailed_reasoning", ""))

    validation = validate_cp_redline_action(leah_action, acceptable_actions, redline_id)
    action_score = max_per_dimension if validation["action_correct"] else 0

    # Score revision quality
    revision_score = 0
    if leah_revision and len(leah_revision) > 20:
        key_elements = gt_redline.get("key_elements", [])
        if key_elements:
            revision_lower = leah_revision.lower()
            matched = sum(1 for elem in key_elements if any(word in revision_lower for word in elem.lower().split()[:3]))
            revision_score = min(max_per_dimension, matched)
        else:
            revision_score = 1

    # Score reasoning quality
    reasoning_score = 0
    if leah_reasoning and len(leah_reasoning) > 30:
        reasoning_must_address = gt_redline.get("reasoning_must_address", "")
        if reasoning_must_address:
            reasoning_lower = leah_reasoning.lower()
            must_lower = reasoning_must_address.lower()
            if any(word in reasoning_lower for word in must_lower.split()[:5] if len(word) > 4):
                reasoning_score = max_per_dimension
            else:
                reasoning_score = 1
        else:
            reasoning_score = 1

    return {
        "redline_id": redline_id,
        "clause_ref": gt_redline.get("clause_ref"),
        "section": gt_redline.get("section"),
        "expected_actions": acceptable_actions,
        "leah_action": leah_action,
        "action_correct": validation["action_correct"],
        "is_adversarial": validation["is_adversarial"],
        "action_score": action_score,
        "revision_score": revision_score,
        "reasoning_score": reasoning_score,
        "total_score": action_score + revision_score + reasoning_score,
        "max_score": max_total,
        "critical_failure": validation["critical_failure"]
    }


def determine_stacking_pass_fail(
    part_a_summary: dict,
    part_b_summary: dict,
    critical_failures: list[dict],
    config: dict
) -> dict:
    """Determine overall pass/fail for freeform_stacking evaluation."""
    gates = config.get("gates", {})

    if gates.get("critical_failure_gate", True) and critical_failures:
        return {
            "pass_fail": "FAIL",
            "reason": f"Critical failure: {len(critical_failures)} adversarial redline(s) accepted",
            "gate_triggered": "critical_failure_gate",
            "critical_failures": critical_failures
        }

    if gates.get("t1_gate", True):
        applies_to = gates.get("t1_gate_applies_to", "part_b")
        if applies_to == "part_b":
            t1_stats = part_b_summary.get("by_tier", {}).get("T1", {})
            t1_total = t1_stats.get("total", 0)
            t1_detected = t1_stats.get("detected", 0)

            if t1_total > 0 and t1_detected < t1_total:
                return {
                    "pass_fail": "FAIL",
                    "reason": f"T1 gate failed: {t1_detected}/{t1_total} T1 issues detected",
                    "gate_triggered": "t1_gate",
                    "critical_failures": []
                }

    part_a_pct = part_a_summary.get("percentage", 0)
    part_b_pct = part_b_summary.get("weighted_recall", 0) * 100
    combined_pct = (part_a_pct * 0.4) + (part_b_pct * 0.6)

    if combined_pct >= 70:
        return {"pass_fail": "PASS", "reason": f"Combined score {combined_pct:.1f}% >= 70%", "gate_triggered": None, "critical_failures": []}
    elif combined_pct >= 50:
        return {"pass_fail": "MARGINAL", "reason": f"Combined score {combined_pct:.1f}% >= 50% but < 70%", "gate_triggered": None, "critical_failures": []}
    else:
        return {"pass_fail": "FAIL", "reason": f"Combined score {combined_pct:.1f}% < 50%", "gate_triggered": "score_threshold", "critical_failures": []}


# === Rules Stacking Functions (added for 07-04) ===

def detect_scope_violations(
    canonical_json: dict,
    redline_clauses: set[str],
    config: dict
) -> list[dict]:
    """Detect scope violations where Leah comments on non-redlined text.

    Rules_stacking CRITICAL constraint: Evaluation scope is ONLY redlined clauses.
    Any comment on unchanged text is a scope violation.
    """
    violations = []

    for entry in canonical_json.get("risk_table", []):
        clause = entry.get("clause_ref", "")
        clause_norm = _normalise_clause_ref(clause)

        if clause_norm and clause_norm not in redline_clauses:
            classification = entry.get("classification", "")
            if _is_meaningful_comment(classification):
                violations.append({
                    "clause_ref": clause,
                    "clause_normalised": clause_norm,
                    "issue": entry.get("clause_summary", entry.get("issue_summary", "")),
                    "source": "risk_table",
                    "severity": "CRITICAL",
                    "violation_type": "OUT_OF_SCOPE_COMMENT",
                    "message": f"Leah commented on non-redlined clause {clause}"
                })

    for redline in canonical_json.get("proposed_redlines", []):
        clause = redline.get("clause_ref", "")
        clause_norm = _normalise_clause_ref(clause)

        if clause_norm and clause_norm not in redline_clauses:
            violations.append({
                "clause_ref": clause,
                "clause_normalised": clause_norm,
                "issue": redline.get("change_summary", redline.get("proposed_text", "")[:100]),
                "source": "proposed_redlines",
                "severity": "CRITICAL",
                "violation_type": "OUT_OF_SCOPE_REDLINE",
                "message": f"Leah proposed redline on non-redlined clause {clause}"
            })

    return violations


def _normalise_clause_ref(clause: str) -> str:
    """Normalise clause reference for scope matching."""
    if not clause:
        return ""
    import re
    text = clause.strip()
    for prefix in ["Section ", "Clause ", "Article ", "§ ", "§"]:
        if text.lower().startswith(prefix.lower()):
            text = text[len(prefix):].strip()
    match = re.match(r'^(\d+(?:\.\d+)*)', text)
    return match.group(1).lower() if match else text.split()[0].lower() if text else ""


def _is_meaningful_comment(classification: str) -> bool:
    """Check if classification indicates a meaningful comment."""
    if not classification:
        return False
    # Check for favourable indicators - these are NOT meaningful comments (no issue detected)
    favourable_markers = ["✅", "Standard", "Compliant", "Acceptable"]
    if any(marker.lower() in classification.lower() for marker in favourable_markers):
        return False
    # Check for "Favourable" but NOT "Unfavourable"
    if "favourable" in classification.lower() and "unfavourable" not in classification.lower():
        return False
    # Everything else is a meaningful comment
    return True


def build_redline_clause_set(gt_redlines: list) -> set[str]:
    """Build set of normalised clause references from GT redlines."""
    clauses = set()
    for redline in gt_redlines:
        clause_ref = redline.get("clause_ref", "")
        if clause_ref:
            clauses.add(_normalise_clause_ref(clause_ref))
        section = redline.get("section", "")
        if section:
            clauses.add(_normalise_clause_ref(str(section)))
    return clauses


def score_rules_stacking_redline(
    leah_response: Optional[dict],
    gt_redline: dict,
    config: dict
) -> dict:
    """Score a single rules_stacking redline evaluation.

    Scoring dimensions (per_redline: 6 max):
    - action (2): Correct ACCEPT/MODIFY/REJECT per rules
    - revision (2): Follows prescribed language from rules
    - reasoning (2): Rule citation present
    """
    scoring_config = config.get("scoring", {})
    max_per_dimension = 2
    max_total = scoring_config.get("per_redline_max", 6)

    test_id = gt_redline.get("test_id", gt_redline.get("redline_id", ""))
    expected_action = gt_redline.get("expected_action", "")
    key_elements = gt_redline.get("key_elements", [])
    rationale_must_include = gt_redline.get("rationale_must_include", [])

    if not leah_response:
        return {
            "test_id": test_id,
            "clause_ref": gt_redline.get("clause_ref", ""),
            "expected_action": expected_action,
            "leah_action": "NMI",
            "detected": "NMI",
            "action_score": 0,
            "revision_score": 0,
            "reasoning_score": 0,
            "total_score": 0,
            "max_score": max_total,
        }

    leah_action = leah_response.get("action", leah_response.get("recommendation", ""))
    leah_revision = leah_response.get("proposed_text", leah_response.get("redline_text", ""))
    leah_reasoning = leah_response.get("rationale", leah_response.get("detailed_reasoning", ""))

    leah_action_norm = leah_action.upper().strip() if leah_action else ""
    expected_norm = expected_action.upper().strip() if expected_action else ""

    detected = "NMI"
    if leah_action_norm:
        detected = "Y" if leah_action_norm == expected_norm else "P"

    action_score = max_per_dimension if leah_action_norm == expected_norm else (1 if leah_action_norm else 0)

    revision_score = 0
    if leah_revision and key_elements:
        revision_lower = leah_revision.lower()
        matched = sum(1 for elem in key_elements if any(word.lower() in revision_lower for word in elem.split()[:3] if len(word) > 3))
        revision_score = max_per_dimension if matched >= len(key_elements) * 0.5 else (1 if matched > 0 else 0)
    elif leah_revision and len(leah_revision) > 20:
        revision_score = 1

    reasoning_score = 0
    if leah_reasoning and rationale_must_include:
        reasoning_lower = leah_reasoning.lower()
        matched = sum(1 for r in rationale_must_include if any(word.lower() in reasoning_lower for word in r.split()[:3] if len(word) > 3))
        reasoning_score = max_per_dimension if matched >= len(rationale_must_include) * 0.5 else (1 if matched > 0 else 0)
    elif leah_reasoning and len(leah_reasoning) > 30:
        reasoning_score = 1

    return {
        "test_id": test_id,
        "clause_ref": gt_redline.get("clause_ref", ""),
        "section": gt_redline.get("section", ""),
        "expected_action": expected_action,
        "leah_action": leah_action,
        "detected": detected,
        "action_score": action_score,
        "revision_score": revision_score,
        "reasoning_score": reasoning_score,
        "total_score": action_score + revision_score + reasoning_score,
        "max_score": max_total,
    }


def calculate_rules_stacking_pass_fail(
    evaluations: list[dict],
    scope_violations: list[dict],
    config: dict
) -> dict:
    """Calculate pass/fail for rules_stacking mode.

    Pass requires: >= 70% score AND ZERO scope violations.
    """
    pass_criteria = config.get("pass_criteria", {})

    if scope_violations:
        max_allowed = pass_criteria.get("pass", {}).get("max_scope_violations", 0)
        if len(scope_violations) > max_allowed:
            return {
                "pass_fail": "FAIL",
                "reason": f"{len(scope_violations)} scope violation(s) (max allowed: {max_allowed})",
                "gate_triggered": "scope_violation_gate",
                "scope_violations": scope_violations,
                "total_score": sum(e.get("total_score", 0) for e in evaluations),
                "max_score": sum(e.get("max_score", 6) for e in evaluations),
                "percentage": 0,
            }

    total_score = sum(e.get("total_score", 0) for e in evaluations)
    max_score = sum(e.get("max_score", 6) for e in evaluations)
    percentage = (total_score / max_score * 100) if max_score > 0 else 0

    pass_threshold = pass_criteria.get("pass", {}).get("min_percentage", 70)
    marginal_threshold = pass_criteria.get("marginal", {}).get("min_percentage", 50)

    if percentage >= pass_threshold:
        return {"pass_fail": "PASS", "reason": f"Score {percentage:.1f}% >= {pass_threshold}% with 0 scope violations", "gate_triggered": None, "scope_violations": [], "total_score": total_score, "max_score": max_score, "percentage": round(percentage, 2)}
    elif percentage >= marginal_threshold:
        return {"pass_fail": "MARGINAL", "reason": f"Score {percentage:.1f}% >= {marginal_threshold}% but < {pass_threshold}%", "gate_triggered": None, "scope_violations": [], "total_score": total_score, "max_score": max_score, "percentage": round(percentage, 2)}
    else:
        return {"pass_fail": "FAIL", "reason": f"Score {percentage:.1f}% < {marginal_threshold}%", "gate_triggered": "score_threshold", "scope_violations": [], "total_score": total_score, "max_score": max_score, "percentage": round(percentage, 2)}
