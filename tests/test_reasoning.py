import pytest
from framework.scoring.reasoning import validate_reasoning, check_false_favorable


class TestValidateReasoning:
    """Test reasoning validation logic."""

    def test_no_requirements_is_valid(self):
        """Empty requirements = always valid."""
        result = validate_reasoning("Any reasoning", [], [])
        assert result["valid"] is True
        assert result["confidence"] == 1.0

    def test_required_phrase_present(self):
        """Required phrase in reasoning = valid."""
        result = validate_reasoning(
            "The supplier can reject orders at their discretion",
            must_contain=["reject", "discretion"],
            must_not_contain=[],
        )
        assert result["valid"] is True
        assert result["missing_required"] == []

    def test_required_phrase_missing(self):
        """Required phrase missing = invalid."""
        result = validate_reasoning(
            "The 5-day response time provides certainty",
            must_contain=["reject", "discretion"],
            must_not_contain=[],
        )
        assert result["valid"] is False
        assert "reject" in result["missing_required"]
        assert "discretion" in result["missing_required"]

    def test_forbidden_phrase_present(self):
        """Forbidden phrase in reasoning = invalid."""
        result = validate_reasoning(
            "The binding commitment provides certainty",
            must_contain=[],
            must_not_contain=["certainty", "guaranteed"],
        )
        assert result["valid"] is False
        assert "certainty" in result["forbidden_found"]

    def test_forbidden_phrase_absent(self):
        """No forbidden phrases = valid."""
        result = validate_reasoning(
            "The supplier has discretion to reject orders",
            must_contain=[],
            must_not_contain=["certainty", "guaranteed"],
        )
        assert result["valid"] is True
        assert result["forbidden_found"] == []

    def test_case_insensitive(self):
        """Matching is case-insensitive."""
        result = validate_reasoning(
            "The SUPPLIER can REJECT orders",
            must_contain=["reject", "supplier"],
            must_not_contain=[],
        )
        assert result["valid"] is True

    def test_confidence_full_compliance(self):
        """Full compliance = 1.0 confidence."""
        result = validate_reasoning(
            "Supplier can reject with discretion",
            must_contain=["reject", "discretion"],
            must_not_contain=["certainty"],
        )
        assert result["confidence"] == 1.0

    def test_confidence_partial_violations(self):
        """Partial violations reduce confidence proportionally."""
        result = validate_reasoning(
            "The 5-day response provides certainty",
            must_contain=["reject", "discretion"],  # Both missing
            must_not_contain=["certainty"],  # Present
        )
        # 3 total checks, 3 violations = 0.0 confidence
        assert result["confidence"] == 0.0

    def test_confidence_single_violation(self):
        """Single violation out of 3 = 2/3 confidence."""
        result = validate_reasoning(
            "Supplier can reject but certainty is provided",
            must_contain=["reject", "discretion"],  # discretion missing
            must_not_contain=["certainty"],  # Present
        )
        # 3 checks, 2 violations = 1/3 = 0.33
        assert abs(result["confidence"] - 0.33) < 0.01


class TestCheckFalseFavorable:
    """Test false favorable detection."""

    def test_no_validation_rules(self):
        """No validation rules = can't be false favorable."""
        gt_item = {}
        result = check_false_favorable(
            "✅ Favorable",
            "Any reasoning here",
            gt_item,
        )
        assert result["is_false_favorable"] is False
        assert result["reason"] == "No reasoning validation rules defined"

    def test_unfavorable_classification_not_checked(self):
        """❌ classifications don't trigger false favorable check."""
        gt_item = {
            "reasoning_must_contain": ["reject"],
            "reasoning_must_not_contain": ["certainty"],
        }
        result = check_false_favorable(
            "❌ Unfavorable",
            "This provides certainty",  # Would fail if checked
            gt_item,
        )
        assert result["is_false_favorable"] is False
        assert result["reason"] == "Classification is not favorable"

    def test_warning_classification_not_checked(self):
        """⚠️ classifications don't trigger false favorable check."""
        gt_item = {
            "reasoning_must_contain": ["reject"],
            "reasoning_must_not_contain": ["certainty"],
        }
        result = check_false_favorable(
            "⚠️ Needs Review",
            "This provides certainty",
            gt_item,
        )
        assert result["is_false_favorable"] is False

    def test_favorable_with_missing_required(self):
        """✅ with missing required phrase = false favorable."""
        gt_item = {
            "reasoning_must_contain": ["reject", "discretion"],
            "reasoning_must_not_contain": [],
        }
        result = check_false_favorable(
            "✅ Favorable",
            "The response time provides clarity",
            gt_item,
        )
        assert result["is_false_favorable"] is True
        assert "reject" in result["reason"]
        assert "discretion" in result["reason"]

    def test_favorable_with_forbidden_found(self):
        """✅ with forbidden phrase = false favorable."""
        gt_item = {
            "reasoning_must_contain": [],
            "reasoning_must_not_contain": ["certainty", "binding"],
        }
        result = check_false_favorable(
            "✅ Favorable",
            "The binding commitment provides certainty",
            gt_item,
        )
        assert result["is_false_favorable"] is True
        assert "certainty" in result["reason"] or "binding" in result["reason"]

    def test_favorable_passes_validation(self):
        """✅ that passes all checks = not false favorable."""
        gt_item = {
            "reasoning_must_contain": ["reject"],
            "reasoning_must_not_contain": ["certainty"],
        }
        result = check_false_favorable(
            "✅ Favorable",
            "Note: supplier can reject but this is acceptable given volume commitments",
            gt_item,
        )
        assert result["is_false_favorable"] is False
        assert result["reason"] == "Reasoning validation passed"

    def test_validation_result_included(self):
        """Validation result is included in output."""
        gt_item = {
            "reasoning_must_contain": ["reject"],
            "reasoning_must_not_contain": [],
        }
        result = check_false_favorable(
            "✅ Favorable",
            "Supplier can reject orders",
            gt_item,
        )
        assert result["validation_result"] is not None
        assert result["validation_result"]["valid"] is True
        assert result["validation_result"]["confidence"] == 1.0

    def test_combined_violations(self):
        """Both missing required and forbidden found = false favorable."""
        gt_item = {
            "reasoning_must_contain": ["reject", "discretion"],
            "reasoning_must_not_contain": ["guaranteed", "binding"],
        }
        result = check_false_favorable(
            "✅ Favorable",
            "The guaranteed response provides binding commitment",
            gt_item,
        )
        assert result["is_false_favorable"] is True
        assert "Missing required" in result["reason"]
        assert "Contains forbidden" in result["reason"]
