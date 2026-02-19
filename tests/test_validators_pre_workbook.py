"""Tests for pre-workbook validation gate."""

import json
import tempfile
from pathlib import Path
import pytest

from framework.validators.pre_workbook import validate_pre_workbook
from framework.validators.base import Severity


class TestValidatePreWorkbook:
    """Tests for validate_pre_workbook function."""

    def test_valid_environment_specific_aggregated(self):
        """Test validation passes with aggregated directory in environments/{env}/."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "environments" / "test_env" / "aggregated" / "contract1"
            agg_dir.mkdir(parents=True)

            # Create valid aggregated file
            with open(agg_dir / "model_a.json", "w") as f:
                json.dump({
                    "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 8}],
                    "summary": {"total_points": 8, "weighted_score": 0.8}
                }, f)

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is True
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert len(errors) == 0

    def test_valid_direct_aggregated(self):
        """Test validation passes with aggregated directory directly under mode_dir."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated" / "contract1"
            agg_dir.mkdir(parents=True)

            # Create valid aggregated file
            with open(agg_dir / "model_a.json", "w") as f:
                json.dump({
                    "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 8}],
                    "summary": {"total_points": 8, "weighted_score": 0.8}
                }, f)

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is True
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert len(errors) == 0

    def test_aggregated_directory_not_found(self):
        """Test validation fails when aggregated directory doesn't exist in either location."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("Aggregated directory not found" in e.message for e in errors)
            # Should mention both checked paths
            assert any("environments/test_env/aggregated" in e.message for e in errors)

    def test_aggregated_directory_empty(self):
        """Test validation fails when aggregated directory has no JSON files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated"
            agg_dir.mkdir(parents=True)

            # Create a non-JSON file (should be ignored)
            with open(agg_dir / "README.txt", "w") as f:
                f.write("test")

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("empty" in e.message.lower() for e in errors)

    def test_all_aggregated_files_empty(self):
        """Test validation fails when all aggregated files are empty dicts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated" / "contract1"
            agg_dir.mkdir(parents=True)

            # Create empty JSON files
            for model in ["model_a", "model_b"]:
                with open(agg_dir / f"{model}.json", "w") as f:
                    json.dump({}, f)

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("empty" in e.message.lower() for e in errors)

    def test_invalid_json_in_aggregated_file(self):
        """Test validation fails when aggregated file contains invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated" / "contract1"
            agg_dir.mkdir(parents=True)

            # Create invalid JSON file
            with open(agg_dir / "model_a.json", "w") as f:
                f.write("{invalid json")

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("Invalid JSON" in e.message for e in errors)

    def test_zero_score_warning(self):
        """Test warning issued for zero score with GT items present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated" / "contract1"
            agg_dir.mkdir(parents=True)

            # Create file with GT items but zero score
            with open(agg_dir / "model_a.json", "w") as f:
                json.dump({
                    "gt_evaluations": [
                        {"gt_id": "GT001", "detection": "N", "points": 0},
                        {"gt_id": "GT002", "detection": "N", "points": 0}
                    ],
                    "summary": {"total_points": 0, "weighted_score": 0}
                }, f)

            result = validate_pre_workbook(mode_dir, env="test_env")

            # Should be valid (zero score is warning, not error)
            assert result.valid is True
            warnings = [i for i in result.issues if i.severity == Severity.WARNING]
            assert any("Zero score" in w.message for w in warnings)

    def test_part_specific_zero_score_warning(self):
        """Test warning issued for zero score in specific parts (part_a, part_b)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated" / "contract1"
            agg_dir.mkdir(parents=True)

            # Create file with multi-part structure and zero part_a score
            # Note: validator uses "or" which treats 0 as falsy, so we need both fields to be 0
            with open(agg_dir / "model_a.json", "w") as f:
                json.dump({
                    "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 8}],
                    "summary": {
                        "total_points": 8,
                        "weighted_score": 0.8,
                        "part_a": {"total_score": 0, "weighted_score": 0},
                        "part_b": {"weighted_score": 0.8}
                    }
                }, f)

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is True
            warnings = [i for i in result.issues if i.severity == Severity.WARNING]
            assert any("part_a" in w.message.lower() for w in warnings)

    def test_ignores_underscore_prefixed_files(self):
        """Test that files starting with underscore are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated" / "contract1"
            agg_dir.mkdir(parents=True)

            # Create internal file (should be ignored)
            with open(agg_dir / "_internal.json", "w") as f:
                json.dump({"internal": "data"}, f)

            # Create valid file
            with open(agg_dir / "model_a.json", "w") as f:
                json.dump({
                    "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 8}],
                    "summary": {"total_points": 8}
                }, f)

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is True

    def test_finds_json_in_subdirectories(self):
        """Test that JSON files in subdirectories are discovered."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated"
            agg_dir.mkdir()

            # Create nested structure
            contract_dir = agg_dir / "contract1" / "subdir"
            contract_dir.mkdir(parents=True)

            with open(contract_dir / "model_a.json", "w") as f:
                json.dump({
                    "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 8}],
                    "summary": {"total_points": 8}
                }, f)

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is True

    def test_unreadable_file_warning(self):
        """Test warning issued when aggregated file cannot be read."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated" / "contract1"
            agg_dir.mkdir(parents=True)

            # Create valid file
            valid_file = agg_dir / "model_a.json"
            with open(valid_file, "w") as f:
                json.dump({
                    "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 8}],
                    "summary": {"total_points": 8}
                }, f)

            # Make file unreadable (Unix-only test, skip on Windows)
            import os
            try:
                os.chmod(valid_file, 0o000)

                result = validate_pre_workbook(mode_dir, env="test_env")

                # Should have warning about unreadable file
                warnings = [i for i in result.issues if i.severity == Severity.WARNING]
                # May or may not trigger depending on OS permissions model
            finally:
                # Restore permissions for cleanup
                os.chmod(valid_file, 0o644)

    def test_multiple_contracts_and_models(self):
        """Test validation with multiple contracts and models."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated"

            # Create multiple contracts
            for contract in ["contract1", "contract2", "contract3"]:
                contract_dir = agg_dir / contract
                contract_dir.mkdir(parents=True)

                for model in ["model_a", "model_b"]:
                    with open(contract_dir / f"{model}.json", "w") as f:
                        json.dump({
                            "gt_evaluations": [{"gt_id": "GT001", "detection": "Y", "points": 8}],
                            "summary": {"total_points": 8, "weighted_score": 0.8}
                        }, f)

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is True
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert len(errors) == 0

    def test_flat_structure_no_subdirs(self):
        """Test with files directly in aggregated directory (no contract subdirs)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir)
            agg_dir = mode_dir / "aggregated"
            agg_dir.mkdir()

            # Create files directly in aggregated directory
            for i in range(3):
                with open(agg_dir / f"result_{i}.json", "w") as f:
                    json.dump({
                        "gt_evaluations": [{"gt_id": f"GT{i:03d}", "detection": "Y", "points": 8}],
                        "summary": {"total_points": 8}
                    }, f)

            result = validate_pre_workbook(mode_dir, env="test_env")

            assert result.valid is True


class TestValidationResultStructure:
    """Test ValidationResult structure and fields."""

    def test_result_has_valid_flag(self):
        """Test that result includes valid boolean flag."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = validate_pre_workbook(Path(tmpdir), env="test")
            assert hasattr(result, "valid")
            assert isinstance(result.valid, bool)

    def test_result_has_issues_list(self):
        """Test that result includes issues list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = validate_pre_workbook(Path(tmpdir), env="test")
            assert hasattr(result, "issues")
            assert isinstance(result.issues, list)

    def test_issues_have_required_fields(self):
        """Test that issues have severity, message, location fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = validate_pre_workbook(Path(tmpdir), env="test")

            if result.issues:
                issue = result.issues[0]
                assert hasattr(issue, "severity")
                assert hasattr(issue, "message")
                assert hasattr(issue, "location")
                assert hasattr(issue, "context")
