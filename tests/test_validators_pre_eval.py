"""Tests for pre-evaluation validation gate."""

import json
import tempfile
from pathlib import Path
import pytest

from framework.validators.pre_eval import validate_pre_evaluation
from framework.validators.base import Severity


class TestValidatePreEvaluation:
    """Tests for validate_pre_evaluation function."""

    def test_valid_mode_directory(self):
        """Test validation passes for valid mode directory."""
        fixture_path = Path("tests/fixtures/validators/pre_eval/valid_mode")
        result = validate_pre_evaluation(fixture_path, env="test_env")

        assert result.valid is True
        assert len([i for i in result.issues if i.severity == Severity.ERROR]) == 0

    def test_missing_mode_directory(self):
        """Test validation fails when mode directory doesn't exist."""
        result = validate_pre_evaluation(Path("/nonexistent/path"), env="test")

        assert result.valid is False
        errors = [i for i in result.issues if i.severity == Severity.ERROR]
        assert len(errors) == 1
        assert "Mode directory not found" in errors[0].message

    def test_missing_ground_truth_directory(self):
        """Test validation fails when ground_truth directory missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir) / "mode"
            mode_dir.mkdir()

            result = validate_pre_evaluation(mode_dir, env="test")

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("Ground truth directory not found" in e.message for e in errors)

    def test_empty_ground_truth_directory(self):
        """Test validation fails when ground_truth directory is empty."""
        fixture_path = Path("tests/fixtures/validators/pre_eval/empty_gt")
        result = validate_pre_evaluation(fixture_path, env="test")

        assert result.valid is False
        errors = [i for i in result.issues if i.severity == Severity.ERROR]
        assert any("Ground truth directory empty" in e.message for e in errors)

    def test_invalid_json_in_ground_truth(self):
        """Test validation fails when GT file contains invalid JSON."""
        fixture_path = Path("tests/fixtures/validators/pre_eval/invalid_json")
        result = validate_pre_evaluation(fixture_path, env="test")

        assert result.valid is False
        errors = [i for i in result.issues if i.severity == Severity.ERROR]
        assert any("Invalid JSON in GT file" in e.message for e in errors)

    def test_ground_truth_not_dict_warning(self):
        """Test warning issued when GT file is not a dict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir) / "mode"
            gt_dir = mode_dir / "ground_truth"
            gt_dir.mkdir(parents=True)

            # Create GT file that's an array instead of dict
            with open(gt_dir / "test.json", "w") as f:
                json.dump([{"gt_id": "GT001"}], f)

            # Create canonical JSON
            canonical_dir = mode_dir / "environments" / "test" / "canonical_json" / "test"
            canonical_dir.mkdir(parents=True)
            with open(canonical_dir / "model.json", "w") as f:
                json.dump({"model": "test"}, f)

            result = validate_pre_evaluation(mode_dir, env="test")

            warnings = [i for i in result.issues if i.severity == Severity.WARNING]
            assert any("GT file is not a dict" in w.message for w in warnings)

    def test_ground_truth_missing_key_warning(self):
        """Test warning issued when GT file missing 'ground_truth' key."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir) / "mode"
            gt_dir = mode_dir / "ground_truth"
            gt_dir.mkdir(parents=True)

            # Create GT file without 'ground_truth' key
            with open(gt_dir / "test.json", "w") as f:
                json.dump({"some_other_key": []}, f)

            # Create canonical JSON
            canonical_dir = mode_dir / "environments" / "test" / "canonical_json" / "test"
            canonical_dir.mkdir(parents=True)
            with open(canonical_dir / "model.json", "w") as f:
                json.dump({"model": "test"}, f)

            result = validate_pre_evaluation(mode_dir, env="test")

            warnings = [i for i in result.issues if i.severity == Severity.WARNING]
            assert any("missing 'ground_truth' key" in w.message for w in warnings)

    def test_canonical_json_fallback_path_resolution(self):
        """Test canonical JSON found via fallback paths."""
        fixture_path = Path("tests/fixtures/validators/pre_eval/legacy_canonical")

        # Test canonical_json_{env} pattern (second fallback)
        result = validate_pre_evaluation(fixture_path, env="test_env")

        assert result.valid is True
        errors = [i for i in result.issues if i.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_canonical_json_legacy_fallback(self):
        """Test canonical JSON found via legacy path (third fallback)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir) / "mode"
            gt_dir = mode_dir / "ground_truth"
            gt_dir.mkdir(parents=True)

            # Create GT file
            with open(gt_dir / "test.json", "w") as f:
                json.dump({"ground_truth": [{"gt_id": "GT001"}]}, f)

            # Create canonical JSON in legacy location
            canonical_dir = mode_dir / "canonical_json" / "test"
            canonical_dir.mkdir(parents=True)
            with open(canonical_dir / "model.json", "w") as f:
                json.dump({"model": "test"}, f)

            result = validate_pre_evaluation(mode_dir, env="test_env")

            assert result.valid is True

    def test_missing_canonical_json_all_paths(self):
        """Test validation fails when canonical JSON not in any fallback path."""
        fixture_path = Path("tests/fixtures/validators/pre_eval/no_canonical")
        result = validate_pre_evaluation(fixture_path, env="test")

        assert result.valid is False
        errors = [i for i in result.issues if i.severity == Severity.ERROR]
        assert any("Canonical JSON directory not found" in e.message for e in errors)
        # Check that all 3 paths were checked
        assert any("checked:" in e.message for e in errors)

    def test_empty_canonical_json_directory(self):
        """Test validation fails when canonical JSON has no contract subdirectories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir) / "mode"
            gt_dir = mode_dir / "ground_truth"
            gt_dir.mkdir(parents=True)

            # Create GT file
            with open(gt_dir / "test.json", "w") as f:
                json.dump({"ground_truth": [{"gt_id": "GT001"}]}, f)

            # Create empty canonical JSON directory
            canonical_dir = mode_dir / "environments" / "test" / "canonical_json"
            canonical_dir.mkdir(parents=True)

            result = validate_pre_evaluation(mode_dir, env="test")

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("No contract subdirectories" in e.message for e in errors)

    def test_canonical_json_no_model_files(self):
        """Test validation fails when contract dirs exist but no JSON files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir) / "mode"
            gt_dir = mode_dir / "ground_truth"
            gt_dir.mkdir(parents=True)

            # Create GT file
            with open(gt_dir / "test.json", "w") as f:
                json.dump({"ground_truth": [{"gt_id": "GT001"}]}, f)

            # Create contract subdirectory but no JSON files
            canonical_dir = mode_dir / "environments" / "test" / "canonical_json" / "test_contract"
            canonical_dir.mkdir(parents=True)

            result = validate_pre_evaluation(mode_dir, env="test")

            assert result.valid is False
            errors = [i for i in result.issues if i.severity == Severity.ERROR]
            assert any("No model JSON files" in e.message for e in errors)

    def test_ignores_underscore_prefixed_files(self):
        """Test validator ignores _changelog and other underscore-prefixed files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mode_dir = Path(tmpdir) / "mode"
            gt_dir = mode_dir / "ground_truth"
            gt_dir.mkdir(parents=True)

            # Create underscore-prefixed file (should be ignored)
            with open(gt_dir / "_changelog.json", "w") as f:
                json.dump({"changes": []}, f)

            # Create valid GT file
            with open(gt_dir / "test.json", "w") as f:
                json.dump({"ground_truth": [{"gt_id": "GT001"}]}, f)

            # Create canonical JSON
            canonical_dir = mode_dir / "environments" / "test" / "canonical_json" / "test"
            canonical_dir.mkdir(parents=True)
            # Also test ignoring underscore-prefixed contract dirs
            ignored_dir = mode_dir / "environments" / "test" / "canonical_json" / "_archive"
            ignored_dir.mkdir()

            with open(canonical_dir / "model.json", "w") as f:
                json.dump({"model": "test"}, f)

            result = validate_pre_evaluation(mode_dir, env="test")

            assert result.valid is True

    def test_path_as_string(self):
        """Test validator accepts path as string (not just Path object)."""
        fixture_path = "tests/fixtures/validators/pre_eval/valid_mode"
        result = validate_pre_evaluation(fixture_path, env="test_env")

        assert result.valid is True


class TestValidationResultStructure:
    """Tests for ValidationResult structure returned by pre_eval validator."""

    def test_validation_result_has_valid_flag(self):
        """Test result has valid boolean flag."""
        fixture_path = Path("tests/fixtures/validators/pre_eval/valid_mode")
        result = validate_pre_evaluation(fixture_path, env="test_env")

        assert hasattr(result, "valid")
        assert isinstance(result.valid, bool)

    def test_validation_result_has_issues_list(self):
        """Test result has issues list."""
        fixture_path = Path("tests/fixtures/validators/pre_eval/valid_mode")
        result = validate_pre_evaluation(fixture_path, env="test_env")

        assert hasattr(result, "issues")
        assert isinstance(result.issues, list)

    def test_issues_have_severity(self):
        """Test issues have severity attribute."""
        result = validate_pre_evaluation(Path("/nonexistent"), env="test")

        assert len(result.issues) > 0
        for issue in result.issues:
            assert hasattr(issue, "severity")
            assert issue.severity in (Severity.ERROR, Severity.WARNING)

    def test_issues_have_message(self):
        """Test issues have message attribute."""
        result = validate_pre_evaluation(Path("/nonexistent"), env="test")

        assert len(result.issues) > 0
        for issue in result.issues:
            assert hasattr(issue, "message")
            assert isinstance(issue.message, str)
            assert len(issue.message) > 0

    def test_issues_have_location(self):
        """Test issues have location attribute."""
        result = validate_pre_evaluation(Path("/nonexistent"), env="test")

        assert len(result.issues) > 0
        for issue in result.issues:
            assert hasattr(issue, "location")
            assert isinstance(issue.location, str)
