#!/usr/bin/env python3
"""
Compute sales-friendly metrics from evaluation results.

Loads freeform + freeform stacking result JSONs, reuses framework.scoring
functions, and produces per-model metrics mapped to the sales narrative.

Usage:
    python -m framework.scripts.sales_metrics
    python -m framework.scripts.sales_metrics --model sonnet45
    python -m framework.scripts.sales_metrics --format markdown
    python -m framework.scripts.sales_metrics --output-dir ./output
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from framework.scoring import (
    calculate_f1,
    calculate_precision,
    calculate_recall,
    calculate_weighted_recall,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FREEFORM_MODELS = [
    "sonnet45", "pioneer_deep", "pathfinder", "starliner", "scale", "velocity",
]
STACKING_MODELS = ["sonnet45", "pioneer_deep", "pathfinder", "starliner"]
CONTRACTS = [
    "consulting", "distribution", "dpa", "jv", "license",
    "partnership", "reseller", "services", "sla", "supply",
]

MODEL_DISPLAY = {
    "sonnet45": "Sonnet 4.5",
    "pioneer_deep": "Pioneer Deep",
    "pathfinder": "Pathfinder",
    "starliner": "Starliner",
    "scale": "Scale",
    "velocity": "Velocity",
}

TIER_CONFIG = {
    "T1": {"Y": 8, "P": 4, "N": 0, "NMI": 0},
    "T2": {"Y": 5, "P": 2.5, "N": 0, "NMI": 0},
    "T3": {"Y": 1, "P": 0.5, "N": 0, "NMI": 0},
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_evaluation(results_dir: Path, contract: str, model: str) -> dict | None:
    """Load a single evaluation JSON file."""
    path = results_dir / contract / f"{model}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def load_all_evaluations(
    results_dir: Path,
    contracts: list[str],
    models: list[str],
) -> dict[str, list[dict]]:
    """Load all evaluations grouped by model, skipping baseline/."""
    by_model: dict[str, list[dict]] = {m: [] for m in models}
    for contract in contracts:
        for model in models:
            data = load_evaluation(results_dir, contract, model)
            if data is not None:
                data["_contract"] = contract
                by_model[model].append(data)
    return by_model


def load_summary(results_dir: Path) -> dict | None:
    """Load _summary.json for cross-validation."""
    path = results_dir / "_summary.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Pure compute functions
# ---------------------------------------------------------------------------

def compute_detection_rate(evaluations: list[dict]) -> dict:
    """
    Compute risk identification accuracy across all contracts for one model.

    Returns dict with y, p, n, nmi counts and detection_rate = (Y+P)/total.
    """
    y = p = n = nmi = 0
    for ev in evaluations:
        for issue in ev.get("gt_evaluations", []):
            det = issue.get("detection", "NMI")
            if det == "Y":
                y += 1
            elif det == "P":
                p += 1
            elif det == "N":
                n += 1
            else:
                nmi += 1
    total = y + p + n + nmi
    rate = calculate_recall(y + p, total)
    return {
        "Y": y, "P": p, "N": n, "NMI": nmi,
        "total_gt_issues": total,
        "detected": y + p,
        "detection_rate": round(rate * 100, 1),
    }


def compute_additional_issues_stats(evaluations: list[dict]) -> dict:
    """
    Compute false positive / additional issues statistics.

    Returns assessment counts and flags audit status.
    """
    valid = not_material = hallucination = other = 0
    for ev in evaluations:
        for ai in ev.get("additional_issues", []):
            assessment = ai.get("assessment", "")
            if assessment == "Valid":
                valid += 1
            elif assessment == "Not Material":
                not_material += 1
            elif assessment == "Hallucination":
                hallucination += 1
            else:
                other += 1

    total = valid + not_material + hallucination + other
    all_valid = (not_material == 0 and hallucination == 0 and total > 0)

    return {
        "valid": valid,
        "not_material": not_material,
        "hallucination": hallucination,
        "other": other,
        "total_additional": total,
        "false_positive_rate": round(
            (hallucination + not_material) / total * 100, 1
        ) if total > 0 else 0.0,
        "audit_status": "pending" if all_valid else "complete",
    }


def compute_precision_recall_f1(
    evaluations: list[dict],
    additional_stats: dict,
) -> dict:
    """
    Compute precision, weighted recall, and F1 from evaluations.

    Uses framework.scoring functions with tier_field="tier" (matching result JSONs).
    """
    # Gather all scored issues for weighted recall
    all_issues: list[dict] = []
    for ev in evaluations:
        all_issues.extend(ev.get("gt_evaluations", []))

    _, _, weighted_recall = calculate_weighted_recall(
        all_issues, TIER_CONFIG, tier_field="tier",
    )

    precision = calculate_precision(
        additional_stats["valid"], additional_stats["not_material"],
    )

    f1 = calculate_f1(weighted_recall, precision)

    return {
        "weighted_recall": round(weighted_recall, 4),
        "precision": round(precision, 4),
        "f1": round(f1, 4),
    }


def compute_quality_scores(evaluations: list[dict]) -> dict:
    """
    Compute average quality across amendment, rationale, redline dimensions.

    Only includes issues where detection is Y or P (quality scores are null for N/NMI).
    """
    dims = ["amendment_score", "rationale_score", "redline_quality_score"]
    totals = {d: 0.0 for d in dims}
    counts = {d: 0 for d in dims}

    for ev in evaluations:
        for issue in ev.get("gt_evaluations", []):
            for d in dims:
                val = issue.get(d)
                if val is not None:
                    totals[d] += val
                    counts[d] += 1

    averages = {}
    for d in dims:
        averages[d] = round(totals[d] / counts[d], 2) if counts[d] > 0 else None

    scored_count = max(counts.values()) if counts else 0
    overall = sum(v for v in averages.values() if v is not None)
    n_dims = sum(1 for v in averages.values() if v is not None)

    return {
        "dimensions": averages,
        "overall_avg": round(overall / n_dims, 2) if n_dims > 0 else None,
        "scored_issues": scored_count,
    }


def compute_t1_gate(evaluations: list[dict]) -> dict:
    """
    Compute T1 gate pass rate across contracts.

    Computed directly from gt_evaluations (source of truth), not from
    summary.t1_gate_pass which may be stale.
    """
    passes = 0
    total = len(evaluations)
    for ev in evaluations:
        t1_issues = [
            i for i in ev.get("gt_evaluations", [])
            if i.get("tier") == "T1"
        ]
        if t1_issues and all(
            i.get("detection") in ("Y", "P") for i in t1_issues
        ):
            passes += 1
        elif not t1_issues:
            # No T1 issues in this contract — vacuously passes
            passes += 1
    return {
        "passes": passes,
        "total": total,
        "pass_rate": round(passes / total * 100, 1) if total > 0 else 0.0,
    }


def compute_traceability(evaluations: list[dict]) -> dict:
    """
    Compute data traceability: % of detected issues with clause ref + redline match.
    """
    detected_with_ref = 0
    detected_total = 0
    for ev in evaluations:
        for issue in ev.get("gt_evaluations", []):
            det = issue.get("detection", "NMI")
            if det in ("Y", "P"):
                detected_total += 1
                has_clause = bool(issue.get("clause"))
                has_redline = bool(issue.get("matched_redline_id"))
                if has_clause and has_redline:
                    detected_with_ref += 1
    return {
        "detected_with_refs": detected_with_ref,
        "detected_total": detected_total,
        "traceability_pct": round(
            detected_with_ref / detected_total * 100, 1
        ) if detected_total > 0 else 0.0,
    }


def compute_stacking_metrics(evaluations: list[dict]) -> dict | None:
    """
    Compute stacking-specific metrics from Part A evaluations.

    Returns None if no stacking data available.
    """
    if not evaluations:
        return None

    pct_sum = 0.0
    passes = 0
    total = len(evaluations)

    for ev in evaluations:
        part_a_summary = ev.get("part_a_summary", {})
        if not part_a_summary:
            part_a_summary = ev.get("summary", {}).get("part_a", {})

        pct_sum += part_a_summary.get("percentage", 0)

        if part_a_summary.get("pass_fail") == "PASS":
            passes += 1

    return {
        "avg_part_a_pct": round(pct_sum / total, 1) if total > 0 else 0.0,
        "part_a_pass_rate": round(passes / total * 100, 1) if total > 0 else 0.0,
        "passes": passes,
        "total": total,
    }


def compute_model_metrics(
    model: str,
    freeform_evals: list[dict],
    stacking_evals: list[dict],
) -> dict:
    """Compute all sales metrics for a single model."""
    detection = compute_detection_rate(freeform_evals)
    additional = compute_additional_issues_stats(freeform_evals)
    prf = compute_precision_recall_f1(freeform_evals, additional)
    quality = compute_quality_scores(freeform_evals)
    t1_gate = compute_t1_gate(freeform_evals)
    traceability = compute_traceability(freeform_evals)
    stacking = compute_stacking_metrics(stacking_evals)

    return {
        "model": model,
        "display_name": MODEL_DISPLAY.get(model, model),
        "contracts_evaluated": len(freeform_evals),
        "risk_identification_accuracy": detection,
        "additional_issues": additional,
        "precision_recall_f1": prf,
        "quality_score": quality,
        "t1_gate": t1_gate,
        "traceability": traceability,
        "stacking": stacking,
    }


# ---------------------------------------------------------------------------
# Cross-validation
# ---------------------------------------------------------------------------

def cross_validate(
    metrics: dict[str, dict],
    freeform_summary: dict | None,
) -> list[str]:
    """
    Cross-validate computed metrics against _summary.json.

    This script computes from gt_evaluations (source of truth). The
    _summary.json is a derived cache that may be stale. Warnings here
    indicate the _summary.json needs regeneration.

    Returns list of discrepancy warnings (empty = all good).
    """
    warnings: list[str] = []
    if not freeform_summary:
        warnings.append("No freeform _summary.json found for cross-validation")
        return warnings

    model_comparison = freeform_summary.get("model_comparison", {})
    for model, m_metrics in metrics.items():
        summary_data = model_comparison.get(model, {})
        if not summary_data:
            continue

        expected_rate = summary_data.get("detection_rate", 0)
        computed_rate = m_metrics["risk_identification_accuracy"]["detection_rate"]

        if abs(expected_rate - computed_rate) > 0.2:
            warnings.append(
                f"{model}: detection rate mismatch — "
                f"computed {computed_rate}% (from gt_evaluations), "
                f"summary {expected_rate}% (stale cache)"
            )

    return warnings


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_markdown(
    all_metrics: dict[str, dict],
    stacking_summary: dict | None,
    warnings: list[str],
) -> str:
    """Format metrics as markdown tables for presentation."""
    lines: list[str] = []
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines.append(f"# Sales Evaluation Metrics\n")
    lines.append(f"Generated: {ts}\n")

    # --- Risk Identification Accuracy ---
    lines.append("## Risk Identification Accuracy\n")
    lines.append("| Model | Detection Rate | Y | P | N | NMI | GT Issues |")
    lines.append("|-------|---------------|---|---|---|-----|-----------|")
    for model in FREEFORM_MODELS:
        m = all_metrics.get(model)
        if not m:
            continue
        d = m["risk_identification_accuracy"]
        lines.append(
            f"| {m['display_name']} | {d['detection_rate']}% "
            f"| {d['Y']} | {d['P']} | {d['N']} | {d['NMI']} | {d['total_gt_issues']} |"
        )
    lines.append("")

    # --- Precision / Recall / F1 ---
    lines.append("## Precision, Recall & F1\n")
    lines.append("| Model | Weighted Recall | Precision | F1 |")
    lines.append("|-------|----------------|-----------|-----|")
    for model in FREEFORM_MODELS:
        m = all_metrics.get(model)
        if not m:
            continue
        p = m["precision_recall_f1"]
        lines.append(
            f"| {m['display_name']} "
            f"| {p['weighted_recall']:.2%} "
            f"| {p['precision']:.2%} "
            f"| {p['f1']:.2%} |"
        )
    lines.append("")

    # --- Additional Issues / False Positive Rate ---
    lines.append("## Additional Issues (False Positive Rate)\n")
    lines.append("| Model | Valid | Not Material | Hallucination | Total | FP Rate | Audit |")
    lines.append("|-------|-------|-------------|---------------|-------|---------|-------|")
    for model in FREEFORM_MODELS:
        m = all_metrics.get(model)
        if not m:
            continue
        a = m["additional_issues"]
        lines.append(
            f"| {m['display_name']} "
            f"| {a['valid']} | {a['not_material']} | {a['hallucination']} "
            f"| {a['total_additional']} | {a['false_positive_rate']}% "
            f"| {a['audit_status']} |"
        )
    lines.append("")

    # --- Quality Scores ---
    lines.append("## Quality Scores (1-3 scale)\n")
    lines.append("| Model | Amendment | Rationale | Redline | Overall |")
    lines.append("|-------|-----------|-----------|---------|---------|")
    for model in FREEFORM_MODELS:
        m = all_metrics.get(model)
        if not m:
            continue
        q = m["quality_score"]
        dims = q["dimensions"]
        lines.append(
            f"| {m['display_name']} "
            f"| {dims['amendment_score'] or 'N/A'} "
            f"| {dims['rationale_score'] or 'N/A'} "
            f"| {dims['redline_quality_score'] or 'N/A'} "
            f"| {q['overall_avg'] or 'N/A'} |"
        )
    lines.append("")

    # --- T1 Gate Pass Rate ---
    lines.append("## T1 Critical Issue Gate\n")
    lines.append("| Model | Passes | Total | Pass Rate |")
    lines.append("|-------|--------|-------|-----------|")
    for model in FREEFORM_MODELS:
        m = all_metrics.get(model)
        if not m:
            continue
        t = m["t1_gate"]
        lines.append(
            f"| {m['display_name']} "
            f"| {t['passes']} | {t['total']} | {t['pass_rate']}% |"
        )
    lines.append("")

    # --- Traceability ---
    lines.append("## Data Traceability\n")
    lines.append("| Model | With Refs | Detected | Traceability |")
    lines.append("|-------|-----------|----------|--------------|")
    for model in FREEFORM_MODELS:
        m = all_metrics.get(model)
        if not m:
            continue
        tr = m["traceability"]
        lines.append(
            f"| {m['display_name']} "
            f"| {tr['detected_with_refs']} | {tr['detected_total']} "
            f"| {tr['traceability_pct']}% |"
        )
    lines.append("")

    # --- Stacking ---
    has_stacking = any(
        all_metrics.get(m, {}).get("stacking") is not None
        for m in STACKING_MODELS
    )
    if has_stacking:
        lines.append("## Freeform Stacking: Redline Response (Part A)\n")
        lines.append("| Model | Avg Part A % | Pass Rate | Passes | Total |")
        lines.append("|-------|-------------|-----------|--------|-------|")
        for model in STACKING_MODELS:
            m = all_metrics.get(model)
            if not m or m.get("stacking") is None:
                continue
            s = m["stacking"]
            lines.append(
                f"| {m['display_name']} "
                f"| {s['avg_part_a_pct']}% "
                f"| {s['part_a_pass_rate']}% "
                f"| {s['passes']} | {s['total']} |"
            )
        lines.append("")

    # --- Warnings ---
    if warnings:
        lines.append("## Cross-Validation Warnings\n")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    return "\n".join(lines)


def format_json(
    all_metrics: dict[str, dict],
    warnings: list[str],
) -> dict[str, Any]:
    """Format metrics as a structured dict for JSON serialisation."""
    return {
        "meta": {
            "generated": datetime.now().isoformat(),
            "freeform_models": FREEFORM_MODELS,
            "stacking_models": STACKING_MODELS,
            "contracts": CONTRACTS,
        },
        "models": all_metrics,
        "cross_validation_warnings": warnings,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute sales-friendly metrics from evaluation results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m framework.scripts.sales_metrics
    python -m framework.scripts.sales_metrics --model sonnet45
    python -m framework.scripts.sales_metrics --format markdown
    python -m framework.scripts.sales_metrics --output-dir ./output
        """,
    )
    parser.add_argument(
        "--model", "-m",
        help="Compute metrics for a single model only",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown", "both"],
        default="both",
        help="Output format (default: both)",
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        help="Output directory (default: freeform/results/)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path("."),
        help="Project root directory (default: current directory)",
    )
    args = parser.parse_args()

    root = args.project_root.resolve()
    freeform_results = root / "freeform" / "results"
    stacking_results = root / "freeform_stacking" / "results"
    output_dir = args.output_dir or freeform_results

    if not freeform_results.exists():
        print(f"ERROR: Freeform results not found: {freeform_results}")
        exit(1)

    # Determine models to process
    freeform_models = [args.model] if args.model else FREEFORM_MODELS
    stacking_models = (
        [args.model] if args.model and args.model in STACKING_MODELS
        else (STACKING_MODELS if not args.model else [])
    )

    # Load data
    print(f"Loading freeform evaluations from {freeform_results}")
    freeform_by_model = load_all_evaluations(
        freeform_results, CONTRACTS, freeform_models,
    )

    stacking_by_model: dict[str, list[dict]] = {}
    if stacking_results.exists() and stacking_models:
        print(f"Loading stacking evaluations from {stacking_results}")
        stacking_by_model = load_all_evaluations(
            stacking_results, CONTRACTS, stacking_models,
        )

    # Compute metrics
    all_metrics: dict[str, dict] = {}
    for model in freeform_models:
        evals = freeform_by_model.get(model, [])
        if not evals:
            print(f"  WARNING: No evaluations found for {model}")
            continue
        stacking_evals = stacking_by_model.get(model, [])
        print(f"  {model}: {len(evals)} freeform, {len(stacking_evals)} stacking")
        all_metrics[model] = compute_model_metrics(model, evals, stacking_evals)

    # Cross-validate
    freeform_summary = load_summary(freeform_results)
    stacking_summary = load_summary(stacking_results)
    warnings = cross_validate(all_metrics, freeform_summary)
    if warnings:
        print("\nCross-validation warnings:")
        for w in warnings:
            print(f"  - {w}")

    # Output
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.format in ("json", "both"):
        json_path = output_dir / "sales_metrics.json"
        with open(json_path, "w") as f:
            json.dump(format_json(all_metrics, warnings), f, indent=2)
        print(f"\nJSON output: {json_path}")

    if args.format in ("markdown", "both"):
        md_path = output_dir / "sales_metrics.md"
        md_content = format_markdown(all_metrics, stacking_summary, warnings)
        with open(md_path, "w") as f:
            f.write(md_content)
        print(f"Markdown output: {md_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
