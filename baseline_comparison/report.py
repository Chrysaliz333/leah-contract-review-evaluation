"""Generate comparison reports from baseline evaluation results.

Detection-only reports — no quality scoring for raw LLM baselines.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import DETECTION_POINTS, MODELS, RESULTS_DIR, REPORTS_DIR

logger = logging.getLogger(__name__)


def load_all_results(
    contracts: list[str],
    models: list[str],
    results_dir: Path = RESULTS_DIR,
) -> dict[str, dict[str, dict]]:
    """Load all evaluation result files.

    Returns:
        Nested dict: results[contract][model] = result_dict
    """
    results: dict[str, dict[str, dict]] = {}
    for contract in contracts:
        results[contract] = {}
        for model in models:
            path = results_dir / contract / f"{model}.json"
            if path.exists():
                with open(path) as f:
                    results[contract][model] = json.load(f)
            else:
                logger.warning("Missing result: %s", path)
    return results


def aggregate_model_scores(
    results: dict[str, dict[str, dict]],
    models: list[str],
) -> dict[str, dict[str, Any]]:
    """Aggregate per-model detection scores across all contracts.

    Returns:
        Dict keyed by model_id with aggregated metrics.
    """
    aggregated: dict[str, dict[str, Any]] = {}

    for model in models:
        total_detection_points = 0.0
        total_weighted_max = 0
        total_issues = 0
        total_detected = 0  # Y or P
        total_y = 0
        total_p = 0
        total_n = 0
        total_nmi = 0
        t1_gates_passed = 0
        t1_gates_total = 0
        contract_scores: list[dict] = []

        for contract, model_results in results.items():
            if model not in model_results:
                continue

            result = model_results[model]
            summary = result.get("summary", {})

            det_counts = summary.get("detection_counts", {})
            y = det_counts.get("Y", 0)
            p = det_counts.get("P", 0)
            n = det_counts.get("N", 0)
            nmi = det_counts.get("NMI", 0)

            total_y += y
            total_p += p
            total_n += n
            total_nmi += nmi
            total_detected += y + p
            total_issues += y + p + n + nmi

            det_pts = summary.get("total_detection_points", 0)
            w_max = summary.get("weighted_max", 0)

            total_detection_points += det_pts
            total_weighted_max += w_max

            if summary.get("t1_count", 0) > 0:
                t1_gates_total += 1
                if summary.get("t1_gate_pass", False):
                    t1_gates_passed += 1

            contract_scores.append({
                "contract": contract,
                "detection_points": det_pts,
                "weighted_max": w_max,
                "detection_rate": (y + p) / (y + p + n + nmi) if (y + p + n + nmi) > 0 else 0,
                "t1_gate_pass": summary.get("t1_gate_pass", None),
            })

        detection_rate = total_detected / total_issues if total_issues > 0 else 0
        score_pct = total_detection_points / total_weighted_max if total_weighted_max > 0 else 0

        aggregated[model] = {
            "model_id": model,
            "display_name": MODELS[model]["display_name"],
            "total_detection_points": total_detection_points,
            "total_weighted_max": total_weighted_max,
            "score_percentage": round(score_pct, 4),
            "detection_rate": round(detection_rate, 4),
            "detection_counts": {
                "Y": total_y, "P": total_p, "N": total_n, "NMI": total_nmi,
            },
            "t1_gates_passed": t1_gates_passed,
            "t1_gates_total": t1_gates_total,
            "contract_scores": contract_scores,
        }

    return aggregated


def generate_summary_json(
    results: dict[str, dict[str, dict]],
    models: list[str],
    contracts: list[str],
    output_path: Path | None = None,
) -> dict:
    """Generate the machine-readable comparison summary."""
    aggregated = aggregate_model_scores(results, models)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "contracts_evaluated": contracts,
        "models_evaluated": models,
        "evaluation_type": "detection_only",
        "model_scores": aggregated,
    }

    if output_path is None:
        output_path = REPORTS_DIR / "comparison_summary.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)

    logger.info("Summary JSON written to %s", output_path)
    return summary


def generate_report_md(
    results: dict[str, dict[str, dict]],
    models: list[str],
    contracts: list[str],
    output_path: Path | None = None,
) -> str:
    """Generate a human-readable Markdown comparison report (detection only)."""
    aggregated = aggregate_model_scores(results, models)

    lines: list[str] = []
    lines.append("# Raw LLM Baseline Comparison Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"Contracts: {len(contracts)} | Models: {len(models)}")
    lines.append("")
    lines.append("> **Detection-only evaluation (recall).** Raw LLMs were given the prompt")
    lines.append('> "Review this contract" with no further guidance. Scores reflect issue')
    lines.append("> detection only — no amendment quality scoring.")
    lines.append("")

    # --- Overall leaderboard ---
    lines.append("## Overall Scores")
    lines.append("")
    lines.append("| Model | Detection Pts | Max Pts | Score % | Detection Rate | T1 Gates |")
    lines.append("|-------|--------------|---------|---------|----------------|----------|")

    sorted_models = sorted(
        models,
        key=lambda m: aggregated.get(m, {}).get("total_detection_points", 0),
        reverse=True,
    )

    for model in sorted_models:
        agg = aggregated.get(model)
        if not agg:
            continue
        lines.append(
            f"| {agg['display_name']} "
            f"| {agg['total_detection_points']:.1f} "
            f"| {agg['total_weighted_max']:.0f} "
            f"| {agg['score_percentage']:.1%} "
            f"| {agg['detection_rate']:.1%} "
            f"| {agg['t1_gates_passed']}/{agg['t1_gates_total']} |"
        )

    lines.append("")

    # --- Per-contract breakdown ---
    lines.append("## Per-Contract Breakdown")
    lines.append("")

    for contract in contracts:
        lines.append(f"### {contract}")
        lines.append("")
        lines.append("| Model | Detection Pts | Max | Score % | Detection Rate | T1 Gate |")
        lines.append("|-------|--------------|-----|---------|----------------|---------|")

        for model in sorted_models:
            agg = aggregated.get(model)
            if not agg:
                continue
            cs = next((c for c in agg["contract_scores"] if c["contract"] == contract), None)
            if not cs:
                lines.append(f"| {agg['display_name']} | — | — | — | — | — |")
                continue

            t1_str = "PASS" if cs["t1_gate_pass"] else "FAIL" if cs["t1_gate_pass"] is not None else "—"
            score_pct = cs["detection_points"] / cs["weighted_max"] if cs["weighted_max"] > 0 else 0
            lines.append(
                f"| {agg['display_name']} "
                f"| {cs['detection_points']:.1f} "
                f"| {cs['weighted_max']:.0f} "
                f"| {score_pct:.1%} "
                f"| {cs['detection_rate']:.1%} "
                f"| {t1_str} |"
            )

        lines.append("")

    # --- Detection breakdown ---
    lines.append("## Detection Breakdown")
    lines.append("")
    lines.append("| Model | Y | P | N | NMI | Total |")
    lines.append("|-------|---|---|---|-----|-------|")

    for model in sorted_models:
        agg = aggregated.get(model)
        if not agg:
            continue
        dc = agg["detection_counts"]
        total = dc["Y"] + dc["P"] + dc["N"] + dc["NMI"]
        lines.append(
            f"| {agg['display_name']} "
            f"| {dc['Y']} | {dc['P']} | {dc['N']} | {dc['NMI']} | {total} |"
        )

    lines.append("")

    md_text = "\n".join(lines)

    if output_path is None:
        output_path = REPORTS_DIR / "comparison_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(md_text)

    logger.info("Report written to %s", output_path)
    return md_text
