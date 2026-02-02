"""Guidelines mode scoring and validation.

Guidelines mode uses playbook-driven evaluation with:
- Tier-based scoring (T1: max 7, T2: max 5, T3: max 0.5)
- Red Flag gate: ALL Red Flag issues must be detected to pass
- Position hierarchy: Gold Standard > Fallback 1 > Fallback 2 > Red Flag
"""

from pathlib import Path
from typing import Optional
import re


def check_red_flag_gate(evaluations: list[dict], gt_issues: list[dict]) -> dict:
    """Check if all Red Flag issues were detected.

    Red Flag gate is CRITICAL: Any missed Red Flag = FAIL regardless of score.
    """
    red_flag_issues = [
        gt for gt in gt_issues
        if gt.get("playbook_standard", "").lower() == "red flag"
    ]

    if not red_flag_issues:
        return {
            "gate": "PASS",
            "reason": "No Red Flag issues in GT",
            "red_flags_total": 0,
            "red_flags_detected": 0,
            "missed_red_flags": []
        }

    eval_by_id = {e.get("test_id", e.get("gt_id")): e for e in evaluations}

    detected = []
    missed = []

    for rf in red_flag_issues:
        rf_id = rf.get("test_id", rf.get("gt_id"))
        eval_result = eval_by_id.get(rf_id, {})
        detection = eval_result.get("detected", eval_result.get("detection", "NMI"))

        if detection in ["Y", "P"]:
            detected.append(rf_id)
        else:
            missed.append({
                "test_id": rf_id,
                "clause_ref": rf.get("clause_ref"),
                "clause_name": rf.get("clause_name"),
                "trigger_phrase": rf.get("trigger_phrase"),
                "detection": detection
            })

    return {
        "gate": "PASS" if not missed else "FAIL",
        "reason": "All Red Flags detected" if not missed else f"Missed {len(missed)} Red Flag(s)",
        "red_flags_total": len(red_flag_issues),
        "red_flags_detected": len(detected),
        "missed_red_flags": missed
    }


def score_guidelines_issue(
    leah_output: Optional[dict],
    gt_issue: dict,
    config: dict,
    playbook_loader=None
) -> dict:
    """Score a single guidelines issue with tier-based scoring.

    Scoring varies by tier:
    - T1: Detection(1) + Location(1) + Action(1) + Amendment(2) + Rationale(2) = 7
    - T2: Detection(1) + Location(1) + Action(1) + Amendment(1) + Rationale(1) = 5
    - T3: Detection(0.5) = 0.5
    """
    test_id = gt_issue.get("test_id", "")
    tier = gt_issue.get("tier", 3)
    tier_str = f"T{tier}" if isinstance(tier, int) else tier
    playbook_standard = gt_issue.get("playbook_standard", "")
    trigger_phrase = gt_issue.get("trigger_phrase", "")
    expected_action = gt_issue.get("expected_action", "")
    expected_amendment = gt_issue.get("expected_amendment", "")

    quality_config = config.get("quality_scores", {})
    max_by_tier = quality_config.get("max_per_dimension", {})

    if tier_str == "T1":
        max_detection, max_location, max_action, max_amendment, max_rationale = 1, 1, 1, 2, 2
    elif tier_str == "T2":
        max_detection, max_location, max_action, max_amendment, max_rationale = 1, 1, 1, 1, 1
    else:  # T3
        max_detection, max_location, max_action, max_amendment, max_rationale = 0.5, 0, 0, 0, 0

    max_total = max_detection + max_location + max_action + max_amendment + max_rationale

    if not leah_output:
        return {
            "test_id": test_id,
            "clause_ref": gt_issue.get("clause_ref", ""),
            "clause_name": gt_issue.get("clause_name", ""),
            "tier": tier_str,
            "playbook_standard": playbook_standard,
            "detected": "NMI",
            "detection_score": 0,
            "location_score": 0,
            "action_score": 0,
            "amendment_score": 0,
            "rationale_score": 0,
            "total_score": 0,
            "max_score": max_total,
        }

    leah_action = leah_output.get("action", leah_output.get("recommendation", ""))
    leah_amendment = leah_output.get("proposed_text", leah_output.get("redline_text", ""))
    leah_rationale = leah_output.get("rationale", leah_output.get("detailed_reasoning", ""))
    leah_classification = leah_output.get("classification", "")
    leah_clause = leah_output.get("clause_ref", "")

    # Score detection
    detected = "NMI"
    detection_score = 0
    if leah_classification and any(m in leah_classification for m in ["❌", "⚠️", "Unfavourable"]):
        detected = "Y"
        detection_score = max_detection
        if trigger_phrase:
            combined = (leah_rationale + " " + leah_amendment).lower()
            if trigger_phrase.lower() not in combined:
                detected = "P"
                detection_score = max_detection * 0.5

    # Score location
    location_score = 0
    if max_location > 0 and detected != "NMI":
        gt_clause = gt_issue.get("clause_ref", "")
        if leah_clause and gt_clause and _clause_refs_match(leah_clause, gt_clause):
            location_score = max_location
        elif leah_clause and gt_clause and _clause_refs_same_article(leah_clause, gt_clause):
            location_score = max_location * 0.5

    # Score action
    action_score = 0
    if max_action > 0 and detected != "NMI" and leah_action and expected_action:
        if leah_action.upper() == expected_action.upper():
            action_score = max_action

    # Score amendment
    amendment_score = 0
    if max_amendment > 0 and detected != "NMI" and leah_amendment and expected_amendment:
        expected_words = set(w.lower() for w in expected_amendment.split() if len(w) > 3)
        leah_words = set(w.lower() for w in leah_amendment.split() if len(w) > 3)
        overlap = len(expected_words & leah_words) / len(expected_words) if expected_words else 0
        if overlap >= 0.5:
            amendment_score = max_amendment
        elif overlap > 0:
            amendment_score = max_amendment * 0.5

    # Score rationale
    rationale_score = 0
    if max_rationale > 0 and detected != "NMI" and leah_rationale:
        rationale_must = gt_issue.get("rationale_must_include", [])
        if rationale_must:
            rationale_lower = leah_rationale.lower()
            matched = sum(1 for r in rationale_must if any(w.lower() in rationale_lower for w in r.split()[:3] if len(w) > 3))
            if matched >= len(rationale_must) * 0.5:
                rationale_score = max_rationale
            elif matched > 0:
                rationale_score = max_rationale * 0.5
        else:
            rationale_score = max_rationale * 0.5

    return {
        "test_id": test_id,
        "clause_ref": gt_issue.get("clause_ref", ""),
        "clause_name": gt_issue.get("clause_name", ""),
        "tier": tier_str,
        "playbook_standard": playbook_standard,
        "detected": detected,
        "detection_score": detection_score,
        "location_score": location_score,
        "action_score": action_score,
        "amendment_score": amendment_score,
        "rationale_score": rationale_score,
        "total_score": detection_score + location_score + action_score + amendment_score + rationale_score,
        "max_score": max_total,
    }


def _clause_refs_match(clause1: str, clause2: str) -> bool:
    def normalise(c):
        c = c.lower().replace("section", "").replace("clause", "").strip()
        match = re.match(r'^(\d+(?:\.\d+)*)', c)
        return match.group(1) if match else c
    return normalise(clause1) == normalise(clause2)


def _clause_refs_same_article(clause1: str, clause2: str) -> bool:
    def get_article(c):
        match = re.match(r'^(\d+)', c.replace("Section", "").replace("Clause", "").strip())
        return match.group(1) if match else None
    a1, a2 = get_article(clause1), get_article(clause2)
    return a1 and a2 and a1 == a2


def calculate_guidelines_pass_fail(
    evaluations: list[dict],
    gt_issues: list[dict],
    config: dict
) -> dict:
    """Calculate pass/fail for guidelines mode with Red Flag gate."""
    red_flag_result = check_red_flag_gate(evaluations, gt_issues)

    total_score = sum(e.get("total_score", 0) for e in evaluations)
    max_score = sum(e.get("max_score", 0) for e in evaluations)
    percentage = (total_score / max_score * 100) if max_score > 0 else 0

    if red_flag_result["gate"] == "FAIL":
        return {
            "pass_fail": "FAIL",
            "reason": red_flag_result["reason"],
            "gate_triggered": "red_flag_gate",
            "total_score": total_score,
            "max_score": max_score,
            "percentage": round(percentage, 2),
            "red_flag_gate": red_flag_result
        }

    if percentage >= 70:
        pass_fail, reason = "PASS", f"Score {percentage:.1f}% >= 70% and all Red Flags detected"
    elif percentage >= 50:
        pass_fail, reason = "MARGINAL", f"Score {percentage:.1f}% >= 50% but < 70%"
    else:
        pass_fail, reason = "FAIL", f"Score {percentage:.1f}% < 50%"

    return {
        "pass_fail": pass_fail,
        "reason": reason,
        "gate_triggered": None,
        "total_score": total_score,
        "max_score": max_score,
        "percentage": round(percentage, 2),
        "red_flag_gate": red_flag_result
    }
