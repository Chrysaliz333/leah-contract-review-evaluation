"""
Tests for polarity-aware detection assignment.
"""

import pytest
from framework.scoring.polarity import (
    assign_detection_with_polarity,
    assess_detection_level,
    calculate_concept_coverage,
    concept_coverage_to_detection,
)


class TestPolarityDetection:
    """Test polarity-aware detection assignment."""

    def test_negative_polarity_unfavorable_detected(self):
        """Standard case: unfavorable classification on negative polarity = Y/P."""
        gt_item = {"polarity": "negative", "required_concepts": []}
        match = {"item": {"classification": "❌ Unfavorable"}}
        assert assign_detection_with_polarity(gt_item, [match]) == "Y"

    def test_negative_polarity_favorable_is_N(self):
        """Marking favorable when issue exists = N."""
        gt_item = {"polarity": "negative", "required_concepts": []}
        match = {"item": {"classification": "✅ Favorable"}}
        assert assign_detection_with_polarity(gt_item, [match]) == "N"

    def test_positive_polarity_favorable_detected(self):
        """Compliance item: favorable classification = Y/P."""
        gt_item = {"polarity": "positive", "required_concepts": []}
        match = {"item": {"classification": "✅ Favorable"}}
        assert assign_detection_with_polarity(gt_item, [match]) == "Y"

    def test_positive_polarity_unfavorable_is_N(self):
        """Compliance item: flagging as unfavorable = N (incorrectly flagged)."""
        gt_item = {"polarity": "positive", "required_concepts": []}
        match = {"item": {"classification": "❌ Unfavorable"}}
        assert assign_detection_with_polarity(gt_item, [match]) == "N"

    def test_no_matches_is_NMI(self):
        """No matches = NMI regardless of polarity."""
        gt_item = {"polarity": "negative", "required_concepts": []}
        assert assign_detection_with_polarity(gt_item, []) == "NMI"

        gt_item = {"polarity": "positive", "required_concepts": []}
        assert assign_detection_with_polarity(gt_item, []) == "NMI"

    def test_ambiguous_classification_is_P(self):
        """Ambiguous classification = P for both polarities."""
        gt_item = {"polarity": "negative", "required_concepts": []}
        match = {"item": {"classification": "Unknown"}}
        assert assign_detection_with_polarity(gt_item, [match]) == "P"

        gt_item = {"polarity": "positive", "required_concepts": []}
        match = {"item": {"classification": "Unknown"}}
        assert assign_detection_with_polarity(gt_item, [match]) == "P"

    def test_default_polarity_is_negative(self):
        """Missing polarity field defaults to negative."""
        gt_item = {"required_concepts": []}  # No polarity specified
        match = {"item": {"classification": "❌ Unfavorable"}}
        assert assign_detection_with_polarity(gt_item, [match]) == "Y"


class TestRequiredConcepts:
    """Test required_concepts influence on Y vs P."""

    def test_no_required_concepts_is_Y(self):
        """Without required_concepts, any match is Y."""
        gt_item = {"required_concepts": []}
        match = {"item": {"rationale": "Some reasoning"}}
        result = assess_detection_level(gt_item, match)
        assert result == "Y"

    def test_all_concepts_matched_is_Y(self):
        """All required concepts in reasoning = Y."""
        gt_item = {"required_concepts": ["work for hire", "17 U.S.C."]}
        match = {"item": {"rationale": "Work for hire under 17 U.S.C. § 101 is ineffective"}}
        result = assess_detection_level(gt_item, match)
        assert result == "Y"

    def test_partial_concepts_is_P(self):
        """Less than 50% concepts matched = P."""
        gt_item = {"required_concepts": ["work for hire", "17 U.S.C.", "assignment", "moral rights"]}
        match = {"item": {"rationale": "Work for hire clause needs attention"}}
        result = assess_detection_level(gt_item, match)
        assert result == "P"  # Only 1/4 = 25% < 50%

    def test_exactly_50_percent_is_Y(self):
        """Exactly 50% concepts = Y (threshold is >=)."""
        gt_item = {"required_concepts": ["work for hire", "assignment"]}
        match = {"item": {"rationale": "Work for hire issues identified"}}
        result = assess_detection_level(gt_item, match)
        assert result == "Y"  # 1/2 = 50%

    def test_concepts_case_insensitive(self):
        """Concept matching is case-insensitive."""
        gt_item = {"required_concepts": ["Work For Hire", "ASSIGNMENT"]}
        match = {"item": {"rationale": "work for hire and assignment issues identified"}}
        result = assess_detection_level(gt_item, match)
        assert result == "Y"

    def test_reasoning_from_multiple_fields(self):
        """Reasoning checked across rationale and detailed_reasoning."""
        gt_item = {"required_concepts": ["work for hire", "assignment"]}
        match = {
            "item": {
                "rationale": "Work for hire issue",
                "detailed_reasoning": "Assignment clause needs review"
            }
        }
        result = assess_detection_level(gt_item, match)
        assert result == "Y"  # Both concepts found across fields


class TestConceptCoverage:
    """Test concept coverage calculation."""

    def test_empty_concepts_full_coverage(self):
        """No required concepts = 100% coverage."""
        assert calculate_concept_coverage([], "any reasoning") == 1.0

    def test_all_concepts_present(self):
        """All concepts in reasoning = 100% coverage."""
        concepts = ["liability", "indemnification", "cap"]
        reasoning = "The liability cap and indemnification clause are problematic"
        assert calculate_concept_coverage(concepts, reasoning) == 1.0

    def test_partial_concepts(self):
        """Some concepts present = fractional coverage."""
        concepts = ["liability", "indemnification", "cap"]
        reasoning = "The liability issue is significant"
        coverage = calculate_concept_coverage(concepts, reasoning)
        assert 0.3 < coverage < 0.4  # 1/3 = 0.333

    def test_no_concepts_present(self):
        """No concepts in reasoning = 0% coverage."""
        concepts = ["liability", "indemnification"]
        reasoning = "This clause is about termination"
        coverage = calculate_concept_coverage(concepts, reasoning)
        assert coverage == 0.0

    def test_multi_word_concept_partial_match(self):
        """Multi-word concepts allow partial word matches."""
        concepts = ["work for hire"]
        reasoning = "This is a work product clause"
        coverage = calculate_concept_coverage(concepts, reasoning)
        assert coverage == 0.5  # Partial match on "work"

    def test_case_insensitive_matching(self):
        """Concept matching is case-insensitive."""
        concepts = ["Work For Hire", "ASSIGNMENT"]
        reasoning = "work for hire and assignment issues"
        assert calculate_concept_coverage(concepts, reasoning) == 1.0


class TestCoverageToDetection:
    """Test coverage to detection conversion."""

    def test_high_coverage_is_Y(self):
        """Coverage >= 50% = Y."""
        assert concept_coverage_to_detection(1.0) == "Y"
        assert concept_coverage_to_detection(0.75) == "Y"
        assert concept_coverage_to_detection(0.5) == "Y"

    def test_low_coverage_is_P(self):
        """Coverage < 50% = P."""
        assert concept_coverage_to_detection(0.49) == "P"
        assert concept_coverage_to_detection(0.25) == "P"
        assert concept_coverage_to_detection(0.1) == "P"
        assert concept_coverage_to_detection(0.0) == "P"
