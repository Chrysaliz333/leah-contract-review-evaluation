"""Tests for pre-aggregation validation gate."""

import json
import tempfile
from pathlib import Path
import pytest

from framework.validators.pre_aggregate import validate_pre_aggregation
from framework.validators.base import Severity


class TestValidatePreAggregation:
    """Tests for validate_pre_aggregation function."""

    def test_valid_complete_coverage(self):
        """Test validation passes when all runs have identical coverage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create two runs with identical coverage
            for run_num in [1, 2]:
                run_dir = tmpdir / f"run{run_num}"
                eval_dir = run_dir / "evaluations"

                # Contract 1
                contract1_dir = eval_dir / "contract1"
                contract1_dir.mkdir(parents=True)
                for model in ["model_a", "model_b"]:
                    with open(contract1_dir / f"{model}.json", "w") as f:
                        json.dump({
                            "contract": "contract1",
                            "model": model,
                            "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 8}],
                            "summary": {"total_points": 8}
                        }, f)

                # Contract 2
                contract2_dir = eval_dir / "contract2"
                contract2_dir.mkdir(parents=True)
                for model in ["model_a", "model_b"]:
                    with open(contract2_dir / f"{model}.json", "w") as f:
                        json.dump({
                            "contract": "contract2",
                            "model": model,
                            "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 5}],
                            "summary": {"total_points": 5}
                        }, f)

            result = validate_pre_aggregation([tmpdir / "run1", tmpdir / "run2"])

            assert result.valid is True
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert len(errors) == 0

    def test_no_run_directories_found(self):
        """Test returns warning (not error) when no run directories exist."""
        result = validate_pre_aggregation([Path("/nonexistent/run1"), Path("/nonexistent/run2")])

        # Should be valid but with warning (no runs = nothing to aggregate)
        assert result.valid is True
        warnings = [i for i in result.issues if i.severity == Severity.WARNING]
        assert len(warnings) == 1
        assert "No run directories found" in warnings[0].message

    def test_run_missing_evaluations_directory(self):
        """Test validation fails when run directory missing evaluations subdirectory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create run directory but no evaluations subdirectory
            run_dir = tmpdir / "run1"
            run_dir.mkdir()

            result = validate_pre_aggregation([run_dir])

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("Run missing evaluations directory" in e.message for e in errors)

    def test_no_contracts_found_warning(self):
        """Test warning issued when no contracts found across runs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create run with empty evaluations directory
            run_dir = tmpdir / "run1"
            eval_dir = run_dir / "evaluations"
            eval_dir.mkdir(parents=True)

            result = validate_pre_aggregation([run_dir])

            # Should be valid (no errors) but with warning
            assert result.valid is True
            warnings = [i for i in result.issues if i.severity == Severity.WARNING]
            assert any("No contracts found across all runs" in w.message for w in warnings)

    def test_incomplete_coverage_in_one_run(self):
        """Test validation fails when one run has incomplete coverage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Run 1: complete coverage (2 contracts × 2 models = 4 files)
            run1_dir = tmpdir / "run1"
            eval1_dir = run1_dir / "evaluations"
            for contract in ["contract1", "contract2"]:
                contract_dir = eval1_dir / contract
                contract_dir.mkdir(parents=True)
                for model in ["model_a", "model_b"]:
                    with open(contract_dir / f"{model}.json", "w") as f:
                        json.dump({"gt_evaluations": [], "summary": {"total_points": 0}}, f)

            # Run 2: incomplete coverage (missing one model)
            run2_dir = tmpdir / "run2"
            eval2_dir = run2_dir / "evaluations"
            for contract in ["contract1", "contract2"]:
                contract_dir = eval2_dir / contract
                contract_dir.mkdir(parents=True)
                # Only model_a, missing model_b
                with open(contract_dir / "model_a.json", "w") as f:
                    json.dump({"gt_evaluations": [], "summary": {"total_points": 0}}, f)

            result = validate_pre_aggregation([run1_dir, run2_dir])

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("Incomplete coverage" in e.message for e in errors)

    def test_run_coverage_differs(self):
        """Test validation fails when runs have different coverage counts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Run 1: 2 contracts × 2 models = 4 evaluations
            run1_dir = tmpdir / "run1"
            eval1_dir = run1_dir / "evaluations"
            for contract in ["contract1", "contract2"]:
                contract_dir = eval1_dir / contract
                contract_dir.mkdir(parents=True)
                for model in ["model_a", "model_b"]:
                    with open(contract_dir / f"{model}.json", "w") as f:
                        json.dump({"gt_evaluations": [], "summary": {"total_points": 0}}, f)

            # Run 2: only 1 contract × 2 models = 2 evaluations
            run2_dir = tmpdir / "run2"
            eval2_dir = run2_dir / "evaluations"
            contract_dir = eval2_dir / "contract1"
            contract_dir.mkdir(parents=True)
            for model in ["model_a", "model_b"]:
                with open(contract_dir / f"{model}.json", "w") as f:
                    json.dump({"gt_evaluations": [], "summary": {"total_points": 0}}, f)

            result = validate_pre_aggregation([run1_dir, run2_dir])

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            # Should have both incomplete coverage and coverage differs errors
            assert any("coverage" in e.message.lower() for e in errors)

    def test_invalid_json_in_evaluation_file(self):
        """Test validation fails when evaluation file contains invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            run_dir = tmpdir / "run1"
            eval_dir = run_dir / "evaluations"
            contract_dir = eval_dir / "contract1"
            contract_dir.mkdir(parents=True)

            # Create valid file
            with open(contract_dir / "model_a.json", "w") as f:
                json.dump({"gt_evaluations": [], "summary": {"total_points": 0}}, f)

            # Create invalid JSON file
            with open(contract_dir / "model_b.json", "w") as f:
                f.write("{invalid json")

            result = validate_pre_aggregation([run_dir])

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("Invalid JSON" in e.message for e in errors)

    def test_zero_score_anomaly_warning(self):
        """Test warning issued for zero score with GT items present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            run_dir = tmpdir / "run1"
            eval_dir = run_dir / "evaluations"
            contract_dir = eval_dir / "contract1"
            contract_dir.mkdir(parents=True)

            # Create evaluation with GT items but zero score
            with open(contract_dir / "model_a.json", "w") as f:
                json.dump({
                    "gt_evaluations": [
                        {"gt_id": "GT001", "detection": "N", "points": 0},
                        {"gt_id": "GT002", "detection": "N", "points": 0}
                    ],
                    "summary": {"total_points": 0}
                }, f)

            result = validate_pre_aggregation([run_dir])

            # Should be valid (zero score is a warning, not error)
            assert result.valid is True
            warnings = [i for i in result.issues if i.severity == Severity.WARNING]
            assert any("Zero score" in w.message for w in warnings)

    def test_multiple_runs_identical_coverage(self):
        """Test validation passes with 3+ runs having identical coverage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create 3 runs with identical coverage
            for run_num in [1, 2, 3]:
                run_dir = tmpdir / f"run{run_num}"
                eval_dir = run_dir / "evaluations"
                contract_dir = eval_dir / "contract1"
                contract_dir.mkdir(parents=True)

                for model in ["model_a"]:
                    with open(contract_dir / f"{model}.json", "w") as f:
                        json.dump({
                            "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 8}],
                            "summary": {"total_points": 8}
                        }, f)

            result = validate_pre_aggregation([
                tmpdir / "run1",
                tmpdir / "run2",
                tmpdir / "run3"
            ])

            assert result.valid is True
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert len(errors) == 0

    def test_empty_evaluations_directory_no_subdirs(self):
        """Test when evaluations directory exists but has no contract subdirectories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            run_dir = tmpdir / "run1"
            eval_dir = run_dir / "evaluations"
            eval_dir.mkdir(parents=True)

            # Create a file instead of directory (should be ignored)
            with open(eval_dir / "README.txt", "w") as f:
                f.write("test")

            result = validate_pre_aggregation([run_dir])

            assert result.valid is True
            warnings = [i for i in result.issues if i.severity == Severity.WARNING]
            assert any("No contracts found" in w.message for w in warnings)

    def test_missing_count_in_error_context(self):
        """Test that incomplete coverage error includes missing file details."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Run with incomplete coverage
            run_dir = tmpdir / "run1"
            eval_dir = run_dir / "evaluations"

            # Contract 1: only 1 of 2 models
            contract1_dir = eval_dir / "contract1"
            contract1_dir.mkdir(parents=True)
            with open(contract1_dir / "model_a.json", "w") as f:
                json.dump({"gt_evaluations": [], "summary": {"total_points": 0}}, f)
            # model_b is missing

            # Contract 2: complete
            contract2_dir = eval_dir / "contract2"
            contract2_dir.mkdir(parents=True)
            for model in ["model_a", "model_b"]:
                with open(contract2_dir / f"{model}.json", "w") as f:
                    json.dump({"gt_evaluations": [], "summary": {"total_points": 0}}, f)

            result = validate_pre_aggregation([run_dir])

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            incomplete_errors = [e for e in errors if "Incomplete coverage" in e.message]
            assert len(incomplete_errors) > 0
            # Check that error context includes missing files
            assert "missing" in incomplete_errors[0].context


class TestValidationResultStructure:
    """Test ValidationResult structure and fields."""

    def test_result_has_valid_flag(self):
        """Test that result includes valid boolean flag."""
        result = validate_pre_aggregation([Path("/nonexistent")])
        assert hasattr(result, "valid")
        assert isinstance(result.valid, bool)

    def test_result_has_issues_list(self):
        """Test that result includes issues list."""
        result = validate_pre_aggregation([Path("/nonexistent")])
        assert hasattr(result, "issues")
        assert isinstance(result.issues, list)

    def test_issues_have_required_fields(self):
        """Test that issues have severity, message, location fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create invalid structure to trigger issues
            run_dir = Path(tmpdir) / "run1"
            run_dir.mkdir()

            result = validate_pre_aggregation([run_dir])

            if result.issues:
                issue = result.issues[0]
                assert hasattr(issue, "severity")
                assert hasattr(issue, "message")
                assert hasattr(issue, "location")
                assert hasattr(issue, "context")
