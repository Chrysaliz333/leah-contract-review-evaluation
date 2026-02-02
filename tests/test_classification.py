"""Tests for classification normalisation."""

import pytest
from framework.scoring.classification import is_issue_detected, normalise_classification


class TestIsIssueDetected:
    """Test classification detection logic."""

    @pytest.mark.parametrize("classification,expected", [
        # Emoji variants
        ("\u274c", True),  # Red X
        ("\u26a0\ufe0f", True),  # Warning sign
        ("\u2705", False),  # Check mark
        # Text variants
        ("Unfavorable", True),
        ("Unfavourable", True),  # UK spelling
        ("Requires Clarification", True),
        ("Favorable", False),
        ("Favourable", False),  # UK spelling
        ("Standard", False),
        # Mixed/compound
        ("\u274c Unfavorable", True),
        ("\u2705 Favorable", False),
        ("\u26a0\ufe0f Requires Clarification", True),
        # Edge cases
        (None, None),
        ("", None),
        ("Unknown Status", None),
    ])
    def test_classification_detection(self, classification, expected):
        assert is_issue_detected(classification) == expected

    def test_whitespace_handling(self):
        """Test that whitespace is trimmed."""
        assert is_issue_detected("  Unfavorable  ") is True
        assert is_issue_detected("\tFavorable\n") is False

    def test_case_insensitivity(self):
        """Test case-insensitive matching for text variants."""
        assert is_issue_detected("UNFAVORABLE") is True
        assert is_issue_detected("favorable") is False
        assert is_issue_detected("High RISK") is True


class TestNormaliseClassification:
    """Test classification normalisation for display."""

    @pytest.mark.parametrize("classification,expected", [
        # Unfavorable cases
        ("\u274c", "Unfavorable"),
        ("Unfavorable", "Unfavorable"),
        ("High Risk", "Unfavorable"),
        # Clarification cases
        ("\u26a0\ufe0f", "Clarification"),
        ("Requires Clarification", "Clarification"),
        ("\u26a0\ufe0f Requires Clarification", "Clarification"),
        # Favorable cases
        ("\u2705", "Favorable"),
        ("Favorable", "Favorable"),
        ("Standard", "Favorable"),
        # Unknown cases
        (None, "Unknown"),
        ("", "Unknown"),
        ("Ambiguous", "Unknown"),
    ])
    def test_normalisation(self, classification, expected):
        assert normalise_classification(classification) == expected
