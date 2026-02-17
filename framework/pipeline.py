"""
Evaluation Pipeline Orchestration.

Provides high-level API for running evaluations end-to-end.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import warnings

from .config_loader import load_mode_config
from .scripts.gt_loader import GTLoader
from .validators.pre_eval import validate_pre_evaluation
from .validators.pre_aggregate import validate_pre_aggregation
from .validators.pre_workbook import validate_pre_workbook


class EvaluationPipeline:
    """
    Orchestrates evaluation pipeline from GT loading through workbook generation.

    Usage:
        pipeline = EvaluationPipeline(mode="freeform", mode_dir=Path("freeform"))
        pipeline.validate_prerequisites("pre_eval", env="hotfix")
        result = pipeline.score_evaluation("consulting", "pathfinder", canonical_json_path)
        summary = pipeline.run_full_pipeline(env="hotfix")
    """

    def __init__(
        self,
        mode: str,
        mode_dir: Optional[Path] = None,
        config_path: Optional[Path] = None
    ):
        """
        Initialize pipeline for a specific evaluation mode.

        Args:
            mode: Mode name (freeform, rules, guidelines, etc.)
            mode_dir: Path to mode directory. If None, infers from config.
            config_path: Path to mode config JSON. If None, uses default location.
        """
        self.mode = mode

        # Load and validate configuration
        if config_path is None:
            config_path = Path("framework/config") / f"{mode}.json"

        self.config = load_mode_config(config_path, validate=True)

        # Set mode directory
        if mode_dir is None:
            base_dir = self.config.get("paths", {}).get("base_dir", mode)
            mode_dir = Path(base_dir)

        self.mode_dir = Path(mode_dir)

        if not self.mode_dir.exists():
            raise FileNotFoundError(f"Mode directory not found: {self.mode_dir}")

        # Initialize GT loader
        self.gt_loader = GTLoader(self.mode_dir, self.config)

    def load_ground_truth(
        self,
        contract: str,
        contract_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Load ground truth for a contract using mode-specific structure.

        Args:
            contract: Contract identifier
            contract_type: Contract type (for modes organized by type)

        Returns:
            Dictionary containing GT data with resolved fields
        """
        result = self.gt_loader.load(contract, contract_type=contract_type)
        return {
            "data": result.data,
            "gt_type": result.gt_type,
            "source_files": [str(f) for f in result.source_files]
        }

    def validate_prerequisites(
        self,
        stage: str,
        env: Optional[str] = None,
        run_dirs: Optional[List[Path]] = None
    ) -> None:
        """
        Run validation gate for a specific pipeline stage.

        Args:
            stage: Stage to validate (pre_eval, pre_aggregate, pre_workbook)
            env: Environment name (required for pre_eval)
            run_dirs: Run directories (required for pre_aggregate, pre_workbook)

        Raises:
            ValidationError: If validation fails with ERROR-severity issues
        """
        if stage == "pre_eval":
            if env is None:
                raise ValueError("env parameter required for pre_eval validation")

            result = validate_pre_evaluation(self.mode_dir, env)
            result.abort_if_errors("pre-evaluation")

            if result.warnings:
                for warning in result.warnings:
                    warnings.warn(f"{warning.message} (at {warning.location})", UserWarning)

        elif stage == "pre_aggregate":
            if run_dirs is None:
                raise ValueError("run_dirs parameter required for pre_aggregate validation")

            result = validate_pre_aggregation(run_dirs)
            result.abort_if_errors("pre-aggregation")

            if result.warnings:
                for warning in result.warnings:
                    warnings.warn(f"{warning.message} (at {warning.location})", UserWarning)

        elif stage == "pre_workbook":
            if run_dirs is None:
                raise ValueError("run_dirs parameter required for pre_workbook validation")

            result = validate_pre_workbook(run_dirs)
            result.abort_if_errors("pre-workbook")

            if result.warnings:
                for warning in result.warnings:
                    warnings.warn(f"{warning.message} (at {warning.location})", UserWarning)

        else:
            raise ValueError(f"Unknown validation stage: {stage}")

    def validate_runs(self, run_dirs: List[Path]) -> None:
        """
        Validate multiple evaluation runs for aggregation.

        Args:
            run_dirs: List of run directory paths

        Raises:
            ValidationError: If coverage is incomplete or inconsistent
        """
        self.validate_prerequisites("pre_aggregate", run_dirs=run_dirs)

    def score_evaluation(
        self,
        contract: str,
        model: str,
        canonical_json_path: Path,
        contract_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Score a single evaluation using mode-specific scoring logic.

        Note: This is a placeholder. Actual scoring logic varies by mode
        and should be implemented per-mode or called from existing scoring modules.

        Args:
            contract: Contract identifier
            model: Model identifier
            canonical_json_path: Path to canonical JSON output
            contract_type: Contract type (for rules/guidelines modes)

        Returns:
            Dictionary containing scored evaluation with summary
        """
        # Load GT
        gt_result = self.load_ground_truth(contract, contract_type=contract_type)

        # Load canonical JSON
        with open(canonical_json_path) as f:
            canonical_json = json.load(f)

        # Mode-specific scoring would go here
        # For now, return placeholder structure
        return {
            "contract": contract,
            "model": model,
            "gt_count": len(gt_result["data"].get("ground_truth", [])),
            "scoring": "not_implemented",
            "note": "Use mode-specific scoring functions from framework/scoring"
        }

    def aggregate_results(
        self,
        run_dirs: List[Path],
        output_dir: Path
    ) -> Dict[str, Any]:
        """
        Aggregate evaluations from multiple runs.

        Args:
            run_dirs: List of run directories to aggregate
            output_dir: Directory to write aggregated results

        Returns:
            Dictionary with aggregation summary
        """
        # Validate runs first
        self.validate_runs(run_dirs)

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Aggregation logic would go here
        # This is a placeholder for the actual aggregation implementation

        return {
            "runs_aggregated": len(run_dirs),
            "output_dir": str(output_dir),
            "status": "placeholder_implementation"
        }

    def generate_workbook(
        self,
        aggregated_dir: Path,
        output_path: Path,
        env: str
    ) -> Path:
        """
        Generate Excel workbook from aggregated results.

        Args:
            aggregated_dir: Directory containing aggregated JSON results
            output_path: Path for output workbook
            env: Environment name

        Returns:
            Path to generated workbook
        """
        # Validate prerequisites
        self.validate_prerequisites("pre_workbook", run_dirs=[aggregated_dir])

        # Workbook generation logic would go here
        # This is a placeholder for the actual workbook generation

        output_path.parent.mkdir(parents=True, exist_ok=True)

        return output_path

    def run_full_pipeline(
        self,
        env: str,
        run_dirs: Optional[List[Path]] = None,
        output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Run complete pipeline: validate → aggregate → workbook.

        Args:
            env: Environment name
            run_dirs: Run directories to aggregate (auto-discovers if None)
            output_dir: Output directory (defaults to mode_dir/results)

        Returns:
            Dictionary with execution summary
        """
        # Auto-discover runs if not provided
        if run_dirs is None:
            env_dir = self.mode_dir / "environments" / env
            if env_dir.exists():
                run_dirs = [
                    d for d in env_dir.iterdir()
                    if d.is_dir() and (d / "evaluations").exists()
                ]
            else:
                # Legacy structure
                run_dirs = [
                    d for d in self.mode_dir.iterdir()
                    if d.is_dir() and d.name.startswith("run") and (d / "evaluations").exists()
                ]

        if not run_dirs:
            raise ValueError(f"No evaluation runs found for environment: {env}")

        # Set output directory
        if output_dir is None:
            output_dir = self.mode_dir / "results"

        output_dir = Path(output_dir)

        # Step 1: Validate
        print(f"Validating {len(run_dirs)} runs...")
        self.validate_prerequisites("pre_eval", env=env)
        self.validate_runs(run_dirs)

        # Step 2: Aggregate
        print(f"Aggregating results to {output_dir}...")
        agg_summary = self.aggregate_results(run_dirs, output_dir)

        # Step 3: Generate workbook
        workbook_path = output_dir / f"{self.mode}_{env}.xlsx"
        print(f"Generating workbook: {workbook_path}...")
        self.generate_workbook(output_dir, workbook_path, env)

        return {
            "mode": self.mode,
            "env": env,
            "runs_processed": len(run_dirs),
            "output_dir": str(output_dir),
            "workbook": str(workbook_path),
            "status": "completed"
        }
