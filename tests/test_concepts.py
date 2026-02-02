"""
Tests for pattern matching and detection strategy logic.
"""

import pytest
from framework.scoring.concepts import (
    matches_output_patterns,
    calculate_pattern_match_score,
    get_detection_strategy,
    assess_concept_coverage,
    should_search_section,
)


class TestPatternMatching:
    """Test expected_output_patterns matching."""

    def test_single_pattern_match(self):
        """Single pattern found in output = match."""
        gt_item = {"expected_output_patterns": ["force majeure"]}
        leah_output = {"rationale": "Missing force majeure clause"}
        assert matches_output_patterns(gt_item, leah_output) is True

    def test_multiple_patterns_partial_match(self):
        """At least one pattern matched = success."""
        gt_item = {"expected_output_patterns": ["force majeure", "liability cap"]}
        leah_output = {"rationale": "Missing force majeure clause"}
        assert matches_output_patterns(gt_item, leah_output) is True

    def test_no_patterns_no_match(self):
        """No patterns defined = no match."""
        gt_item = {"expected_output_patterns": []}
        leah_output = {"rationale": "Some reasoning"}
        assert matches_output_patterns(gt_item, leah_output) is False

    def test_pattern_not_found(self):
        """Pattern not in output = no match."""
        gt_item = {"expected_output_patterns": ["force majeure"]}
        leah_output = {"rationale": "Liability concerns"}
        assert matches_output_patterns(gt_item, leah_output) is False

    def test_case_insensitive_matching(self):
        """Pattern matching is case-insensitive."""
        gt_item = {"expected_output_patterns": ["Force Majeure"]}
        leah_output = {"rationale": "Missing FORCE MAJEURE clause"}
        assert matches_output_patterns(gt_item, leah_output) is True

    def test_multiple_fields_searched(self):
        """Patterns searched across all output fields."""
        gt_item = {"expected_output_patterns": ["termination"]}
        leah_output = {
            "clause_name": "Exit Clause",
            "rationale": "Issues found",
            "proposed_text": "Add termination rights"
        }
        assert matches_output_patterns(gt_item, leah_output) is True

    def test_partial_pattern_match(self):
        """Substring matches count."""
        gt_item = {"expected_output_patterns": ["indemnif"]}
        leah_output = {"rationale": "Indemnification clause is problematic"}
        assert matches_output_patterns(gt_item, leah_output) is True


class TestPatternMatchScore:
    """Test pattern match scoring."""

    def test_all_patterns_matched(self):
        """All patterns found = 100% score."""
        gt_item = {"expected_output_patterns": ["liability", "cap"]}
        leah_output = {"rationale": "Liability cap is unlimited"}
        score = calculate_pattern_match_score(gt_item, leah_output)
        assert score == 1.0

    def test_partial_patterns_matched(self):
        """Some patterns found = fractional score."""
        gt_item = {"expected_output_patterns": ["liability", "cap", "indemnity"]}
        leah_output = {"rationale": "Liability cap is unlimited"}
        score = calculate_pattern_match_score(gt_item, leah_output)
        assert abs(score - 0.667) < 0.01  # 2/3

    def test_no_patterns_zero_score(self):
        """No patterns = 0 score."""
        gt_item = {"expected_output_patterns": []}
        leah_output = {"rationale": "Some reasoning"}
        score = calculate_pattern_match_score(gt_item, leah_output)
        assert score == 0.0

    def test_no_matches_zero_score(self):
        """Patterns defined but none found = 0 score."""
        gt_item = {"expected_output_patterns": ["termination", "breach"]}
        leah_output = {"rationale": "Liability concerns"}
        score = calculate_pattern_match_score(gt_item, leah_output)
        assert score == 0.0


class TestDetectionStrategy:
    """Test detection_logic branching."""

    def test_standard_strategy_default(self):
        """Missing detection_logic defaults to standard."""
        gt_item = {}
        assert get_detection_strategy(gt_item) == "standard"

    def test_explicit_strategies(self):
        """Explicit detection_logic values returned."""
        assert get_detection_strategy({"detection_logic": "standard"}) == "standard"
        assert get_detection_strategy({"detection_logic": "new_clause_recommendation"}) == "new_clause_recommendation"
        assert get_detection_strategy({"detection_logic": "pattern_match"}) == "pattern_match"
        assert get_detection_strategy({"detection_logic": "any_mention"}) == "any_mention"


class TestConceptCoverageAssessment:
    """Test concept coverage assessment with detailed output."""

    def test_all_concepts_present(self):
        """All concepts in reasoning = Y with full coverage."""
        concepts = ["liability", "cap", "indemnification"]
        reasoning = "The liability cap and indemnification clause are problematic"
        result = assess_concept_coverage(concepts, reasoning)

        assert result["coverage"] == 1.0
        assert len(result["matched_concepts"]) == 3
        assert len(result["missing_concepts"]) == 0
        assert result["detection_level"] == "Y"

    def test_partial_concepts_present(self):
        """Some concepts present = P with fractional coverage."""
        concepts = ["liability", "cap", "indemnification"]
        reasoning = "The liability issue is significant"
        result = assess_concept_coverage(concepts, reasoning)

        assert 0.3 < result["coverage"] < 0.4  # 1/3
        assert "liability" in result["matched_concepts"]
        assert "cap" in result["missing_concepts"]
        assert "indemnification" in result["missing_concepts"]
        assert result["detection_level"] == "P"

    def test_no_concepts_required(self):
        """Empty required_concepts = Y with 100% coverage."""
        result = assess_concept_coverage([], "any reasoning")

        assert result["coverage"] == 1.0
        assert result["matched_concepts"] == []
        assert result["missing_concepts"] == []
        assert result["detection_level"] == "Y"

    def test_exactly_50_percent_is_Y(self):
        """Exactly 50% coverage = Y (threshold)."""
        concepts = ["liability", "indemnification"]
        reasoning = "Liability issues exist"
        result = assess_concept_coverage(concepts, reasoning)

        assert result["coverage"] == 0.5
        assert result["detection_level"] == "Y"

    def test_multi_word_partial_match(self):
        """Multi-word concepts allow partial matches."""
        concepts = ["work for hire"]
        reasoning = "This is a work product clause"
        result = assess_concept_coverage(concepts, reasoning, strict=False)

        assert result["coverage"] == 0.5  # Partial match
        assert "work for hire (partial)" in result["matched_concepts"]
        assert result["detection_level"] == "Y"

    def test_strict_mode_no_partial(self):
        """Strict mode requires exact phrase match."""
        concepts = ["work for hire"]
        reasoning = "This is a work product clause"
        result = assess_concept_coverage(concepts, reasoning, strict=True)

        assert result["coverage"] == 0.0
        assert "work for hire" in result["missing_concepts"]
        assert result["detection_level"] == "P"

    def test_case_insensitive(self):
        """Concept matching is case-insensitive."""
        concepts = ["Liability", "INDEMNIFICATION"]
        reasoning = "liability and indemnification clauses"
        result = assess_concept_coverage(concepts, reasoning)

        assert result["coverage"] == 1.0
        assert len(result["matched_concepts"]) == 2


class TestSectionSearch:
    """Test section search logic based on detection_logic."""

    def test_standard_searches_risk_and_redlines(self):
        """Standard detection_logic searches risk_table and proposed_redlines."""
        gt_item = {"detection_logic": "standard"}

        assert should_search_section(gt_item, "risk_table") is True
        assert should_search_section(gt_item, "proposed_redlines") is True
        assert should_search_section(gt_item, "new_clauses_proposed") is False

    def test_ncr_searches_all_standard_sections(self):
        """NCR detection_logic includes new_clauses_proposed."""
        gt_item = {"detection_logic": "new_clause_recommendation"}

        assert should_search_section(gt_item, "risk_table") is True
        assert should_search_section(gt_item, "proposed_redlines") is True
        assert should_search_section(gt_item, "new_clauses_proposed") is True

    def test_pattern_match_searches_everywhere(self):
        """Pattern matching searches all sections."""
        gt_item = {"detection_logic": "pattern_match"}

        assert should_search_section(gt_item, "risk_table") is True
        assert should_search_section(gt_item, "proposed_redlines") is True
        assert should_search_section(gt_item, "new_clauses_proposed") is True

    def test_any_mention_searches_everywhere(self):
        """Any mention searches all sections."""
        gt_item = {"detection_logic": "any_mention"}

        assert should_search_section(gt_item, "risk_table") is True
        assert should_search_section(gt_item, "proposed_redlines") is True
        assert should_search_section(gt_item, "new_clauses_proposed") is True

    def test_default_is_standard(self):
        """Missing detection_logic defaults to standard behaviour."""
        gt_item = {}

        assert should_search_section(gt_item, "risk_table") is True
        assert should_search_section(gt_item, "proposed_redlines") is True
        assert should_search_section(gt_item, "new_clauses_proposed") is False
