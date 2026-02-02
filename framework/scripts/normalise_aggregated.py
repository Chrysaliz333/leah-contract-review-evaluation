#!/usr/bin/env python3
"""
Normalise aggregated evaluation JSONs to the canonical schema.

Fixes test_prod2-style JSONs that use a different field naming convention:
- amendment_quality -> amendment_score
- rationale_quality -> rationale_score
- evidence.matched_clause -> clause (top-level)
- Adds issue text from ground truth lookup
- Computes detection_by_tier from gt_evaluations
- Maps t1_detected -> t1_all_detected

Usage:
    python3 normalise_aggregated.py --env test_prod2
    python3 normalise_aggregated.py --env test_prod2 --dry-run
"""

import json
import argparse
from pathlib import Path
from copy import deepcopy


CONTRACTS = [
    "consulting", "dpa", "distribution", "jv", "license",
    "partnership", "reseller", "services", "sla", "supply"
]


def load_gt_lookup(gt_dir: Path) -> dict:
    """Build gt_id -> {clause, issue} lookup from ground truth files."""
    lookup = {}
    for contract in CONTRACTS:
        gt_path = gt_dir / f"{contract}.json"
        if not gt_path.exists():
            print(f"  WARNING: GT file not found: {gt_path}")
            continue
        with open(gt_path) as f:
            gt = json.load(f)
        issues = gt.get("ground_truth", [])
        lookup[contract] = {}
        for issue in issues:
            gt_id = issue.get("gt_id", "")
            lookup[contract][gt_id] = {
                "clause": issue.get("clause", ""),
                "issue": issue.get("issue", ""),
                "tier": issue.get("tier", ""),
            }
    return lookup


def needs_normalisation(eval_data: dict) -> bool:
    """Check if this evaluation uses the non-canonical schema."""
    gt_evals = eval_data.get("gt_evaluations", [])
    if not gt_evals:
        return False
    first = gt_evals[0]
    # Non-canonical if it has amendment_quality instead of amendment_score
    if "amendment_quality" in first and "amendment_score" not in first:
        return True
    # Non-canonical if clause is missing at top level
    if "clause" not in first and "evidence" in first:
        evidence = first.get("evidence", {})
        if "matched_clause" in evidence:
            return True
    return False


def compute_detection_by_tier(gt_evals: list) -> dict:
    """Compute detection_by_tier from gt_evaluations."""
    tiers = {"T1": {"Y": 0, "P": 0, "N": 0, "NMI": 0},
             "T2": {"Y": 0, "P": 0, "N": 0, "NMI": 0},
             "T3": {"Y": 0, "P": 0, "N": 0, "NMI": 0}}
    for gt in gt_evals:
        tier = gt.get("tier", "")
        det = gt.get("detection", "NMI")
        if tier in tiers and det in tiers[tier]:
            tiers[tier][det] += 1
    return tiers


def normalise_evaluation(eval_data: dict, gt_lookup: dict, contract: str) -> dict:
    """Normalise a single evaluation to the canonical schema."""
    data = deepcopy(eval_data)
    contract_gt = gt_lookup.get(contract, {})

    # Normalise gt_evaluations
    for gt in data.get("gt_evaluations", []):
        gt_id = gt.get("gt_id", "")
        gt_info = contract_gt.get(gt_id, {})

        # Extract clause from evidence if missing, with GT as fallback
        if "clause" not in gt or not gt["clause"]:
            evidence = gt.get("evidence", {})
            matched = evidence.get("matched_clause")
            gt["clause"] = matched if matched else gt_info.get("clause", "")

        # Add issue text from GT if missing
        if "issue" not in gt or not gt["issue"]:
            gt["issue"] = gt_info.get("issue", "")

        # Map field names
        if "amendment_quality" in gt and "amendment_score" not in gt:
            gt["amendment_score"] = gt.pop("amendment_quality")
        if "rationale_quality" in gt and "rationale_score" not in gt:
            gt["rationale_score"] = gt.pop("rationale_quality")

        # Add redline_quality_score if missing (null = not scored)
        if "redline_quality_score" not in gt:
            gt["redline_quality_score"] = None

        # Add matched_redline_id if missing
        if "matched_redline_id" not in gt:
            gt["matched_redline_id"] = None

        # Restructure evidence to canonical format if needed
        if "evidence" in gt:
            ev = gt["evidence"]
            if "judge_reasoning" not in ev:
                # Build judge_reasoning from excerpt
                reasoning = ev.get("excerpt", "")
                if ev.get("matched_source"):
                    reasoning = f"[{ev['matched_source']}] {reasoning}"
                ev["judge_reasoning"] = reasoning
            if "proposed_revision_excerpt" not in ev:
                ev["proposed_revision_excerpt"] = ev.get("excerpt")
            if "effective_rationale_excerpt" not in ev:
                ev["effective_rationale_excerpt"] = None

    # Normalise summary
    summary = data.get("summary", {})

    # Map t1_detected (bool) -> t1_all_detected
    if "t1_detected" in summary and "t1_all_detected" not in summary:
        summary["t1_all_detected"] = summary["t1_detected"]

    # Compute detection_by_tier if missing
    if "detection_by_tier" not in summary:
        summary["detection_by_tier"] = compute_detection_by_tier(
            data.get("gt_evaluations", [])
        )

    data["summary"] = summary
    return data


def main():
    parser = argparse.ArgumentParser(description="Normalise aggregated JSONs to canonical schema")
    parser.add_argument("--env", required=True, help="Environment name (e.g., test_prod2)")
    parser.add_argument("--base-dir", help="Override aggregated data directory")
    parser.add_argument("--gt-dir", help="Override ground truth directory")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()

    project_dir = Path(__file__).parent.parent.parent
    mode_dir = project_dir / "freeform"

    agg_dir = Path(args.base_dir) if args.base_dir else mode_dir / "environments" / args.env / "aggregated"
    gt_dir = Path(args.gt_dir) if args.gt_dir else mode_dir / "ground_truth"

    if not agg_dir.exists():
        print(f"ERROR: Aggregated directory not found: {agg_dir}")
        exit(1)
    if not gt_dir.exists():
        print(f"ERROR: Ground truth directory not found: {gt_dir}")
        exit(1)

    print("=" * 60)
    print(f"NORMALISING AGGREGATED DATA — {args.env.upper()}")
    print("=" * 60)
    print(f"Aggregated: {agg_dir}")
    print(f"Ground truth: {gt_dir}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Load GT lookup
    gt_lookup = load_gt_lookup(gt_dir)
    print(f"Loaded GT for {len(gt_lookup)} contracts")
    print()

    normalised = 0
    skipped = 0
    errors = 0

    for contract in CONTRACTS:
        contract_dir = agg_dir / contract
        if not contract_dir.exists():
            print(f"  {contract}: SKIPPED (no directory)")
            continue

        for json_file in sorted(contract_dir.glob("*.json")):
            model = json_file.stem
            with open(json_file) as f:
                eval_data = json.load(f)

            if not needs_normalisation(eval_data):
                print(f"  {contract}/{model}: already canonical")
                skipped += 1
                continue

            try:
                normalised_data = normalise_evaluation(eval_data, gt_lookup, contract)

                if args.dry_run:
                    # Show what would change
                    first_gt = normalised_data["gt_evaluations"][0] if normalised_data["gt_evaluations"] else {}
                    print(f"  {contract}/{model}: WOULD NORMALISE")
                    print(f"    clause: {first_gt.get('clause', '?')}")
                    print(f"    issue: {first_gt.get('issue', '?')[:50]}")
                    print(f"    amendment_score: {first_gt.get('amendment_score')}")
                    has_dbt = "detection_by_tier" in normalised_data.get("summary", {})
                    print(f"    detection_by_tier: {'added' if has_dbt else 'missing'}")
                else:
                    with open(json_file, 'w') as f:
                        json.dump(normalised_data, f, indent=2, ensure_ascii=False)
                    print(f"  {contract}/{model}: NORMALISED")

                normalised += 1
            except Exception as e:
                print(f"  {contract}/{model}: ERROR - {e}")
                errors += 1

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Normalised: {normalised}")
    print(f"Already canonical: {skipped}")
    if errors:
        print(f"Errors: {errors}")
    if args.dry_run:
        print("\nDry run — no files were modified. Remove --dry-run to apply.")


if __name__ == "__main__":
    main()
