"""Tests for framework/validators/base.py"""

import pytest
from framework.validators.base import (
    Severity,
    ValidationIssue,
    ValidationResult,
    ValidationError,
)


class TestSeverity:
    """Test Severity enum."""

    def test_severity_values(self):
        """Verify severity levels exist."""
        assert Severity.ERROR
        assert Severity.WARNING


class TestValidationIssue:
    """Test ValidationIssue dataclass."""

    def test_create_error(self):
        """Create an error issue."""
        issue = ValidationIssue(
            severity=Severity.ERROR,
            message="Test error",
            location="test/path.json"
        )
        assert issue.severity == Severity.ERROR
        assert issue.message == "Test error"
        assert issue.location == "test/path.json"
        assert issue.context == {}

    def test_create_warning_with_context(self):
        """Create a warning with context."""
        issue = ValidationIssue(
            severity=Severity.WARNING,
            message="Test warning",
            location="test/file.json",
            context={"field": "value", "count": 42}
        )
        assert issue.severity == Severity.WARNING
        assert issue.context["field"] == "value"
        assert issue.context["count"] == 42


class TestValidationResult:
    """Test ValidationResult dataclass."""

    def test_valid_result_no_issues(self):
        """Valid result with no issues."""
        result = ValidationResult(valid=True)
        assert result.valid is True
        assert result.issues == []
        assert result.errors == []
        assert result.warnings == []

    def test_invalid_result_with_errors(self):
        """Invalid result with error issues."""
        errors = [
            ValidationIssue(Severity.ERROR, "Error 1", "loc1"),
            ValidationIssue(Severity.ERROR, "Error 2", "loc2"),
        ]
        result = ValidationResult(valid=False, issues=errors)
        assert result.valid is False
        assert len(result.errors) == 2
        assert len(result.warnings) == 0

    def test_valid_result_with_warnings_only(self):
        """Valid result with only warnings."""
        warnings = [
            ValidationIssue(Severity.WARNING, "Warning 1", "loc1"),
            ValidationIssue(Severity.WARNING, "Warning 2", "loc2"),
        ]
        result = ValidationResult(valid=True, issues=warnings)
        assert result.valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 2

    def test_mixed_issues_filters_correctly(self):
        """Result with both errors and warnings filters correctly."""
        issues = [
            ValidationIssue(Severity.ERROR, "Error 1", "loc1"),
            ValidationIssue(Severity.WARNING, "Warning 1", "loc2"),
            ValidationIssue(Severity.ERROR, "Error 2", "loc3"),
            ValidationIssue(Severity.WARNING, "Warning 2", "loc4"),
        ]
        result = ValidationResult(valid=False, issues=issues)

        assert len(result.errors) == 2
        assert all(i.severity == Severity.ERROR for i in result.errors)

        assert len(result.warnings) == 2
        assert all(i.severity == Severity.WARNING for i in result.warnings)

    def test_abort_if_errors_with_no_errors(self):
        """abort_if_errors does not raise when no errors."""
        result = ValidationResult(valid=True, issues=[
            ValidationIssue(Severity.WARNING, "Just a warning", "loc1")
        ])
        # Should not raise
        result.abort_if_errors("test_stage")

    def test_abort_if_errors_raises_with_errors(self):
        """abort_if_errors raises ValidationError when errors present."""
        result = ValidationResult(valid=False, issues=[
            ValidationIssue(Severity.ERROR, "Critical error", "test/file.json"),
            ValidationIssue(Severity.WARNING, "Minor warning", "test/other.json"),
        ])

        with pytest.raises(ValidationError) as exc_info:
            result.abort_if_errors("pre_evaluation")

        error_msg = str(exc_info.value)
        assert "pre_evaluation" in error_msg
        assert "Critical error" in error_msg
        assert "test/file.json" in error_msg
        # Warning should not be in error message
        assert "Minor warning" not in error_msg

    def test_abort_if_errors_formats_multiple_errors(self):
        """abort_if_errors formats multiple errors correctly."""
        result = ValidationResult(valid=False, issues=[
            ValidationIssue(Severity.ERROR, "Error 1", "loc1"),
            ValidationIssue(Severity.ERROR, "Error 2", "loc2"),
            ValidationIssue(Severity.ERROR, "Error 3", "loc3"),
        ])

        with pytest.raises(ValidationError) as exc_info:
            result.abort_if_errors("test_stage")

        error_msg = str(exc_info.value)
        assert "Error 1" in error_msg
        assert "Error 2" in error_msg
        assert "Error 3" in error_msg
        assert "loc1" in error_msg
        assert "loc2" in error_msg
        assert "loc3" in error_msg


class TestValidationError:
    """Test ValidationError exception."""

    def test_raise_and_catch(self):
        """Can raise and catch ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Test validation failed")

        assert "Test validation failed" in str(exc_info.value)
