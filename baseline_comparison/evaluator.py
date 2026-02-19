"""Evaluator: checks whether raw LLM contract reviews detected ground truth issues.

Detection-only evaluation (recall). One Claude Sonnet call per GT issue.
No quality scoring — raw LLMs weren't asked to produce amendments.
"""

import json
import logging
import re
from typing import Any

from .llm_clients import call_anthropic, LLMResponse
from .config import EVALUATOR_MODEL, DETECTION_POINTS

# Import framework scoring functions
import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from framework.scoring.detection import calculate_detection_points

logger = logging.getLogger(__name__)


EVALUATOR_SYSTEM = """\
You are an expert legal contract reviewer acting as an evaluation judge.

Your task: determine whether a raw, unstructured contract review identified a
specific risk issue from our ground truth. The review was produced by a general-
purpose LLM given only "Review this contract" as a prompt — it has no structured
output format, no risk tables, and no tracked changes.

You must assess the review text holistically, looking for any mention, discussion,
or implication of the ground truth issue, even if phrased differently."""


def build_evaluator_prompt(
    raw_review: str,
    gt_issue: dict[str, Any],
    contract_id: str,
) -> str:
    """Build the per-issue evaluator prompt.

    Args:
        raw_review: The raw text output from the LLM being evaluated.
        gt_issue: A single ground truth issue dict.
        contract_id: Short name of the contract.

    Returns:
        The formatted prompt string for the evaluator.
    """
    key_elements = gt_issue.get("key_elements", [])
    key_elements_text = "\n".join(f"  - {e}" for e in key_elements) if key_elements else "  (none specified)"

    contract_text = gt_issue.get("contract_text", "N/A")
    # Some GT issues have split contract_text fields (e.g. contract_text_6_4)
    if contract_text == "N/A" or not contract_text:
        alt_texts = []
        for k, v in gt_issue.items():
            if k.startswith("contract_text_") and v:
                alt_texts.append(v)
        if alt_texts:
            contract_text = "\n---\n".join(alt_texts)

    return f"""\
## Ground Truth Issue

- **Contract:** {contract_id}
- **GT ID:** {gt_issue["gt_id"]}
- **Clause:** {gt_issue.get("clause", "N/A")}
- **Tier:** {gt_issue["tier"]}
- **Issue:** {gt_issue["issue"]}
- **Key elements to look for:**
{key_elements_text}
- **Relevant contract text:** {contract_text}

## Raw LLM Review (to evaluate)

<review>
{raw_review}
</review>

## Your Task

Search the raw review above for ANY mention, discussion, or implication of the
ground truth issue described. The review is unstructured prose — the model may
have used different terminology, grouped multiple issues together, or mentioned
the risk in passing.

Determine detection status:

- **Y (Yes):** The review clearly identifies this risk. It discusses the core
  concern even if using different words or clause references.
- **P (Partial):** The review touches on a related concern but misses the core
  risk, or identifies the clause but mischaracterises the issue.
- **N (No):** The review does not mention this risk at all despite it being
  present in the contract.
- **NMI (Not Mentioned in Input):** Only use if the risk relates to something
  genuinely absent from the contract text provided to the model.

## Response Format

Respond with ONLY a JSON object (no markdown fences, no commentary):

{{
  "detection": "Y|P|N|NMI",
  "evidence_excerpt": "Brief quote from the review that relates to this issue (or empty string if N/NMI)",
  "reasoning": "1-2 sentence explanation of your detection decision"
}}"""


def parse_evaluator_response(response_text: str) -> dict[str, Any]:
    """Parse the evaluator's JSON response, with regex fallback.

    Returns:
        Dict with detection, evidence_excerpt, reasoning.

    Raises:
        ValueError: If the response cannot be parsed at all.
    """
    text = response_text.strip()

    # Strip markdown fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Regex fallback — extract detection value
        data = _extract_fields_regex(text)
        if data is None:
            raise ValueError(f"Failed to parse evaluator response.\nText: {text[:500]}")

    detection = data.get("detection", "").upper().strip()
    if detection not in ("Y", "P", "N", "NMI"):
        raise ValueError(f"Invalid detection value: {detection!r}")

    return {
        "detection": detection,
        "evidence_excerpt": data.get("evidence_excerpt", ""),
        "reasoning": data.get("reasoning", ""),
    }


def _extract_fields_regex(text: str) -> dict[str, Any] | None:
    """Regex fallback for malformed JSON — extract detection at minimum."""
    det_match = re.search(r'"detection"\s*:\s*"(Y|P|N|NMI)"', text, re.IGNORECASE)
    if not det_match:
        return None

    result: dict[str, Any] = {"detection": det_match.group(1).upper()}

    reasoning_match = re.search(r'"reasoning"\s*:\s*"([^"]*(?:\\.[^"]*)*)"', text)
    if reasoning_match:
        result["reasoning"] = reasoning_match.group(1)

    return result


def evaluate_single_issue(
    raw_review: str,
    gt_issue: dict[str, Any],
    contract_id: str,
    anthropic_api_key: str,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Evaluate a single GT issue against a raw review (detection only).

    Returns:
        Evaluation dict with detection and detection_points.
    """
    gt_id = gt_issue["gt_id"]

    if dry_run:
        return _build_evaluation_dict(
            gt_issue=gt_issue,
            detection="N",
            evidence_excerpt="[DRY RUN]",
            reasoning="[DRY RUN - no API call made]",
        )

    prompt = build_evaluator_prompt(raw_review, gt_issue, contract_id)

    try:
        response: LLMResponse = call_anthropic(
            prompt,
            system=EVALUATOR_SYSTEM,
            model=EVALUATOR_MODEL,
            api_key=anthropic_api_key,
            max_tokens=500,
        )
        scores = parse_evaluator_response(response.text)
    except Exception:
        logger.exception("Evaluator failed for %s/%s", contract_id, gt_id)
        raise

    return _build_evaluation_dict(gt_issue=gt_issue, **scores)


def _build_evaluation_dict(
    gt_issue: dict[str, Any],
    detection: str,
    evidence_excerpt: str = "",
    reasoning: str = "",
) -> dict[str, Any]:
    """Build a single evaluation entry (detection only, no quality scores)."""
    tier = gt_issue["tier"]
    det_points = calculate_detection_points(detection, tier, DETECTION_POINTS)

    return {
        "gt_id": gt_issue["gt_id"],
        "clause": gt_issue.get("clause", "N/A"),
        "tier": tier,
        "issue": gt_issue["issue"],
        "detection": detection,
        "detection_points": det_points,
        "evidence": {
            "excerpt": evidence_excerpt,
            "judge_reasoning": reasoning,
        },
    }


def build_result_summary(evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    """Build the summary block from a list of evaluated GT issues."""
    detection_counts = {"Y": 0, "P": 0, "N": 0, "NMI": 0}
    detection_by_tier: dict[str, dict[str, int]] = {}

    total_detection_points = 0.0
    t1_count = 0
    t1_detected = 0

    for ev in evaluations:
        det = ev["detection"]
        tier = ev["tier"]

        detection_counts[det] += 1

        if tier not in detection_by_tier:
            detection_by_tier[tier] = {"Y": 0, "P": 0, "N": 0, "NMI": 0}
        detection_by_tier[tier][det] += 1

        total_detection_points += ev["detection_points"]

        if tier == "T1":
            t1_count += 1
            if det in ("Y", "P"):
                t1_detected += 1

    t1_gate_pass = t1_detected == t1_count if t1_count > 0 else True

    # Calculate weighted max from the evaluations' tiers
    tier_counts: dict[str, int] = {}
    for ev in evaluations:
        tier_counts[ev["tier"]] = tier_counts.get(ev["tier"], 0) + 1
    weighted_max = sum(
        count * DETECTION_POINTS[tier]["Y"]
        for tier, count in tier_counts.items()
    )

    total_issues = sum(detection_counts.values())
    detection_rate = (detection_counts["Y"] + detection_counts["P"]) / total_issues if total_issues > 0 else 0

    return {
        "detection_counts": detection_counts,
        "detection_by_tier": detection_by_tier,
        "t1_all_detected": t1_gate_pass,
        "t1_gate_pass": t1_gate_pass,
        "t1_count": t1_count,
        "t1_detected": t1_detected,
        "total_detection_points": total_detection_points,
        "weighted_max": weighted_max,
        "detection_rate": round(detection_rate, 4),
    }
