"""
Command-line interface for evaluation pipeline.

Usage:
    leah-eval freeform hotfix
    leah-eval rules test_prod2 --mode-dir /path/to/rules
    leah-eval freeform hotfix --validate-only
"""

import argparse
import sys
from pathlib import Path

from .pipeline import EvaluationPipeline


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Leah Evaluation Pipeline CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  leah-eval freeform hotfix
  leah-eval rules test_prod2 --mode-dir ./rules
  leah-eval freeform hotfix --validate-only
  leah-eval guidelines prod --output-dir ./custom_output
        """
    )

    parser.add_argument(
        "mode",
        help="Evaluation mode (freeform, freeform_stacking, rules, rules_stacking, guidelines)"
    )

    parser.add_argument(
        "env",
        help="Environment name (e.g., hotfix, test_prod2, prod)"
    )

    parser.add_argument(
        "--mode-dir",
        type=Path,
        help="Override mode directory (default: inferred from config)"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Override output directory (default: {mode_dir}/results)"
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only run validation gates, skip aggregation and workbook generation"
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to mode config JSON (default: framework/config/{mode}.json)"
    )

    args = parser.parse_args()

    try:
        # Initialize pipeline
        print(f"Initializing {args.mode} evaluation pipeline...")
        pipeline = EvaluationPipeline(
            mode=args.mode,
            mode_dir=args.mode_dir,
            config_path=args.config
        )

        print(f"Mode directory: {pipeline.mode_dir}")

        if args.validate_only:
            # Run validation only
            print(f"\nValidating prerequisites for environment: {args.env}")
            pipeline.validate_prerequisites("pre_eval", env=args.env)
            print("✓ Pre-evaluation validation passed")

            # Try to discover and validate runs
            env_dir = pipeline.mode_dir / "environments" / args.env
            if env_dir.exists():
                run_dirs = [
                    d for d in env_dir.iterdir()
                    if d.is_dir() and (d / "evaluations").exists()
                ]
                if run_dirs:
                    print(f"\nValidating {len(run_dirs)} evaluation runs...")
                    pipeline.validate_runs(run_dirs)
                    print("✓ Pre-aggregation validation passed")
                else:
                    print(f"\nNo evaluation runs found in {env_dir}")
            else:
                print(f"\nEnvironment directory not found: {env_dir}")

            print("\n✓ Validation complete - no errors found")
            return 0

        # Run full pipeline
        print(f"\nRunning full evaluation pipeline for environment: {args.env}")
        summary = pipeline.run_full_pipeline(
            env=args.env,
            output_dir=args.output_dir
        )

        print("\n" + "=" * 60)
        print("Pipeline execution complete!")
        print("=" * 60)
        print(f"Mode:            {summary['mode']}")
        print(f"Environment:     {summary['env']}")
        print(f"Runs processed:  {summary['runs_processed']}")
        print(f"Output directory: {summary['output_dir']}")
        print(f"Workbook:        {summary['workbook']}")
        print("=" * 60)

        return 0

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        print(f"\n✗ Invalid argument: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
