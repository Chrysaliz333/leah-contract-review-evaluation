"""Main orchestrator for raw LLM baseline comparison.

Usage:
    python -m baseline_comparison.run_comparison [--phase 1|2|3|all] \
        [--contracts consulting,sla] [--models o3,gpt41] [--dry-run] [--verbose]
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# Ensure project root is on path for framework imports
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from baseline_comparison.config import (
    ALL_CONTRACTS,
    ALL_MODELS,
    CONTRACT_FILES,
    CONTRACTS_DIR,
    ENV_FILE,
    GT_DIR,
    MODELS,
    RAW_RESPONSES_DIR,
    RAW_REVIEW_PROMPT,
    RESULTS_DIR,
    REPORTS_DIR,
)
from baseline_comparison.contracts import extract_text
from baseline_comparison.llm_clients import call_openai, call_anthropic, LLMResponse
from baseline_comparison.evaluator import evaluate_single_issue, build_result_summary
from baseline_comparison.report import (
    load_all_results,
    generate_summary_json,
    generate_report_md,
)

logger = logging.getLogger("baseline_comparison")


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def load_api_keys() -> dict[str, str]:
    """Load API keys from env vars first, then .env file as fallback."""
    from dotenv import dotenv_values

    keys = {}
    key_map = [("OPENAI_API_KEY", "openai"), ("ANTHROPIC_API_KEY", "anthropic")]

    # 1. Check existing env vars (e.g. passed via CLI)
    for name, provider in key_map:
        val = os.getenv(name)
        if val:
            keys[provider] = val

    # 2. Fill gaps from .env file (read values directly to avoid
    #    override/no-override issues with empty env vars)
    env_vals = dotenv_values(ENV_FILE)
    for name, provider in key_map:
        if provider not in keys:
            val = env_vals.get(name)
            if val:
                keys[provider] = val
                os.environ[name] = val  # set for any downstream code

    return keys


def load_ground_truth(contract_id: str) -> list[dict]:
    """Load the ground truth issues for a contract."""
    gt_path = GT_DIR / f"{contract_id}.json"
    if not gt_path.exists():
        raise FileNotFoundError(f"Ground truth not found: {gt_path}")

    with open(gt_path) as f:
        gt_data = json.load(f)

    return gt_data["ground_truth"]


# ---------------------------------------------------------------------------
# Phase 1: Generate raw reviews
# ---------------------------------------------------------------------------

def phase1_generate_reviews(
    contracts: list[str],
    models: list[str],
    api_keys: dict[str, str],
    dry_run: bool = False,
) -> None:
    """Send contracts to raw LLMs and save responses."""
    logger.info("=== Phase 1: Generate Raw Reviews ===")

    for contract in contracts:
        docx_path = CONTRACTS_DIR / CONTRACT_FILES[contract]
        logger.info("Extracting text from %s", docx_path.name)
        contract_text = extract_text(docx_path)
        logger.info("  Extracted %d characters", len(contract_text))

        for model_id in models:
            model_cfg = MODELS[model_id]
            out_dir = RAW_RESPONSES_DIR / contract
            out_dir.mkdir(parents=True, exist_ok=True)

            response_path = out_dir / f"{model_id}.txt"
            meta_path = out_dir / f"{model_id}.meta.json"

            if response_path.exists():
                logger.info("  [SKIP] %s/%s — response already exists", contract, model_id)
                continue

            prompt = f"{RAW_REVIEW_PROMPT}\n\n{contract_text}"

            if dry_run:
                logger.info("  [DRY RUN] Would call %s for %s (%d chars prompt)",
                           model_cfg["api_model"], contract, len(prompt))
                continue

            provider = model_cfg["provider"]
            if provider not in api_keys:
                logger.error("  No API key for provider %s — skipping %s", provider, model_id)
                continue

            logger.info("  Calling %s for %s...", model_cfg["display_name"], contract)

            try:
                if provider == "openai":
                    response: LLMResponse = call_openai(
                        prompt,
                        model=model_cfg["api_model"],
                        api_key=api_keys[provider],
                    )
                elif provider == "anthropic":
                    response: LLMResponse = call_anthropic(
                        prompt,
                        model=model_cfg["api_model"],
                        api_key=api_keys[provider],
                        max_tokens=model_cfg.get("max_tokens", 16_000),
                    )
                else:
                    logger.error("  Unknown provider %s — skipping", provider)
                    continue
            except Exception:
                logger.exception("  FAILED %s/%s", contract, model_id)
                continue

            # Save raw text
            with open(response_path, "w") as f:
                f.write(response.text)

            # Save metadata
            meta = {
                "contract": contract,
                "model_id": model_id,
                "api_model": response.model,
                "prompt": RAW_REVIEW_PROMPT,
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens,
                "latency_seconds": response.latency_seconds,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=2)

            logger.info("  Saved %s/%s (%d tokens, %.1fs)",
                       contract, model_id, response.output_tokens, response.latency_seconds)

    logger.info("Phase 1 complete.")


# ---------------------------------------------------------------------------
# Phase 2: Evaluate against ground truth
# ---------------------------------------------------------------------------

def phase2_evaluate(
    contracts: list[str],
    models: list[str],
    api_keys: dict[str, str],
    dry_run: bool = False,
) -> None:
    """Evaluate raw responses against ground truth using Claude as judge."""
    logger.info("=== Phase 2: Evaluate Against Ground Truth ===")

    if "anthropic" not in api_keys and not dry_run:
        logger.error("No ANTHROPIC_API_KEY — cannot run Phase 2")
        return

    anthropic_key = api_keys.get("anthropic", "")

    total_calls = 0
    total_skipped = 0

    for contract in contracts:
        gt_issues = load_ground_truth(contract)
        logger.info("%s: %d GT issues", contract, len(gt_issues))

        for model_id in models:
            result_dir = RESULTS_DIR / contract
            result_dir.mkdir(parents=True, exist_ok=True)
            result_path = result_dir / f"{model_id}.json"

            if result_path.exists():
                logger.info("  [SKIP] %s/%s — result already exists", contract, model_id)
                total_skipped += 1
                continue

            # Load raw response
            response_path = RAW_RESPONSES_DIR / contract / f"{model_id}.txt"
            if not response_path.exists():
                logger.warning("  [MISSING] No raw response for %s/%s — skipping", contract, model_id)
                continue

            raw_review = response_path.read_text()
            logger.info("  Evaluating %s/%s (%d GT issues)...", contract, model_id, len(gt_issues))

            evaluations = []
            for i, gt_issue in enumerate(gt_issues):
                gt_id = gt_issue["gt_id"]
                logger.debug("    %s/%s/%s (%d/%d)", contract, model_id, gt_id, i + 1, len(gt_issues))

                ev = evaluate_single_issue(
                    raw_review=raw_review,
                    gt_issue=gt_issue,
                    contract_id=contract,
                    anthropic_api_key=anthropic_key,
                    dry_run=dry_run,
                )
                evaluations.append(ev)
                total_calls += 1

            # Build summary
            summary = build_result_summary(evaluations)

            # Load metadata if available
            meta_path = RAW_RESPONSES_DIR / contract / f"{model_id}.meta.json"
            meta_info = {}
            if meta_path.exists():
                with open(meta_path) as f:
                    meta_info = json.load(f)

            # Assemble result in existing schema format
            result = {
                "meta": {
                    "contract": contract,
                    "model_id": model_id,
                    "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
                    "evaluator_model": "sonnet",
                    "gt_version": _get_gt_version(contract),
                    "raw_llm_baseline": True,
                    "raw_model": MODELS[model_id]["api_model"],
                    "raw_prompt": RAW_REVIEW_PROMPT,
                    "raw_input_tokens": meta_info.get("input_tokens"),
                    "raw_output_tokens": meta_info.get("output_tokens"),
                    "raw_latency_seconds": meta_info.get("latency_seconds"),
                },
                "gt_evaluations": evaluations,
                "additional_issues": [],
                "summary": summary,
            }

            with open(result_path, "w") as f:
                json.dump(result, f, indent=2)

            logger.info("  Saved %s/%s: %.1f det pts (%s, T1 gate %s)",
                       contract, model_id,
                       summary["total_detection_points"],
                       f"{summary['detection_counts']['Y']}Y/{summary['detection_counts']['P']}P/{summary['detection_counts']['N']}N",
                       "PASS" if summary["t1_gate_pass"] else "FAIL")

    logger.info("Phase 2 complete. %d evaluator calls, %d skipped.", total_calls, total_skipped)


def _get_gt_version(contract_id: str) -> str:
    """Read the GT version from a contract's ground truth file."""
    gt_path = GT_DIR / f"{contract_id}.json"
    if gt_path.exists():
        with open(gt_path) as f:
            data = json.load(f)
        return data.get("gt_metadata", {}).get("gt_version", "unknown")
    return "unknown"


# ---------------------------------------------------------------------------
# Phase 3: Generate reports
# ---------------------------------------------------------------------------

def phase3_report(
    contracts: list[str],
    models: list[str],
) -> None:
    """Load results and generate comparison reports."""
    logger.info("=== Phase 3: Generate Reports ===")

    results = load_all_results(contracts, models)

    # Check we have at least some data
    has_data = any(
        model in model_results
        for model_results in results.values()
        for model in models
    )
    if not has_data:
        logger.error("No results found — run Phase 2 first.")
        return

    generate_summary_json(results, models, contracts)
    generate_report_md(results, models, contracts)

    logger.info("Phase 3 complete. Reports in %s", REPORTS_DIR)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Raw LLM Baseline Comparison Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # Dry run — verify paths and GT loading
  python -m baseline_comparison.run_comparison --dry-run

  # Single contract + single model (Phase 1 only)
  python -m baseline_comparison.run_comparison --phase 1 --contracts consulting --models gpt41

  # Full pipeline
  python -m baseline_comparison.run_comparison --phase all

  # Just regenerate reports from existing results
  python -m baseline_comparison.run_comparison --phase 3
""",
    )

    parser.add_argument(
        "--phase",
        choices=["1", "2", "3", "all"],
        default="all",
        help="Which phase to run (default: all)",
    )
    parser.add_argument(
        "--contracts",
        type=str,
        default=None,
        help="Comma-separated contract IDs (default: all 10)",
    )
    parser.add_argument(
        "--models",
        type=str,
        default=None,
        help="Comma-separated model IDs (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Verify paths and config without making API calls",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )

    return parser.parse_args()


def validate_inputs(contracts: list[str], models: list[str]) -> bool:
    """Validate that requested contracts and models exist."""
    ok = True

    for c in contracts:
        if c not in CONTRACT_FILES:
            logger.error("Unknown contract: %s (valid: %s)", c, ", ".join(ALL_CONTRACTS))
            ok = False
        else:
            docx_path = CONTRACTS_DIR / CONTRACT_FILES[c]
            if not docx_path.exists():
                logger.error("Contract file missing: %s", docx_path)
                ok = False

            gt_path = GT_DIR / f"{c}.json"
            if not gt_path.exists():
                logger.error("Ground truth missing: %s", gt_path)
                ok = False

    for m in models:
        if m not in MODELS:
            logger.error("Unknown model: %s (valid: %s)", m, ", ".join(ALL_MODELS))
            ok = False

    return ok


def main() -> None:
    args = parse_args()
    setup_logging(args.verbose)

    contracts = args.contracts.split(",") if args.contracts else ALL_CONTRACTS
    models = args.models.split(",") if args.models else ALL_MODELS

    if not validate_inputs(contracts, models):
        sys.exit(1)

    # Count GT issues for summary
    total_gt = 0
    for c in contracts:
        gt = load_ground_truth(c)
        total_gt += len(gt)

    logger.info("Pipeline config: %d contracts, %d models, %d GT issues",
               len(contracts), len(models), total_gt)
    logger.info("Estimated evaluator calls (Phase 2): %d", total_gt * len(models))

    if args.dry_run:
        logger.info("[DRY RUN MODE] No API calls will be made.")

    api_keys = load_api_keys()

    if not args.dry_run:
        phase = args.phase
        # Check which providers are needed for the selected models
        needed_providers = {MODELS[m]["provider"] for m in models}
        if phase in ("1", "all"):
            for provider in needed_providers:
                if provider not in api_keys:
                    logger.error("%s API key not found in %s", provider.upper(), ENV_FILE)
                    sys.exit(1)
        if phase in ("2", "all") and "anthropic" not in api_keys:
            logger.error("ANTHROPIC_API_KEY not found in %s", ENV_FILE)
            sys.exit(1)

    phase = args.phase

    if phase in ("1", "all"):
        phase1_generate_reviews(contracts, models, api_keys, dry_run=args.dry_run)

    if phase in ("2", "all"):
        phase2_evaluate(contracts, models, api_keys, dry_run=args.dry_run)

    if phase in ("3", "all"):
        phase3_report(contracts, models)


if __name__ == "__main__":
    main()
