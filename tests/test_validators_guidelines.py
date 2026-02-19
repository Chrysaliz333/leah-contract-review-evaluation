"""Tests for guidelines mode scoring and validation."""

import pytest

from framework.validators.guidelines_validators import (
    check_red_flag_gate,
    score_guidelines_issue,
    calculate_guidelines_pass_fail,
    _clause_refs_match,
    _clause_refs_same_article
)


class TestCheckRedFlagGate:
    """Tests for Red Flag gate checking."""

    def test_pass_when_no_red_flags(self):
        """Test gate passes when no Red Flag issues in GT."""
        gt_issues = [
            {"test_id": "G001", "playbook_standard": "Gold Standard"},
            {"test_id": "G002", "playbook_standard": "Fallback 1"}
        ]
        evaluations = []

        result = check_red_flag_gate(evaluations, gt_issues)

        assert result["gate"] == "PASS"
        assert result["red_flags_total"] == 0
        assert result["missed_red_flags"] == []

    def test_pass_when_all_red_flags_detected(self):
        """Test gate passes when all Red Flags detected (Y or P)."""
        gt_issues = [
            {"test_id": "RF001", "playbook_standard": "Red Flag"},
            {"test_id": "RF002", "playbook_standard": "red flag"}
        ]
        evaluations = [
            {"test_id": "RF001", "detected": "Y"},
            {"test_id": "RF002", "detection": "P"}  # alt field name
        ]

        result = check_red_flag_gate(evaluations, gt_issues)

        assert result["gate"] == "PASS"
        assert result["red_flags_total"] == 2
        assert result["red_flags_detected"] == 2
        assert result["missed_red_flags"] == []

    def test_fail_when_red_flag_missed(self):
        """Test gate fails when any Red Flag missed."""
        gt_issues = [
            {"test_id": "RF001", "playbook_standard": "Red Flag", "clause_ref": "5.1"},
            {"test_id": "RF002", "playbook_standard": "Red Flag", "clause_ref": "7.2"}
        ]
        evaluations = [
            {"test_id": "RF001", "detected": "Y"},
            {"test_id": "RF002", "detected": "NMI"}  # missed
        ]

        result = check_red_flag_gate(evaluations, gt_issues)

        assert result["gate"] == "FAIL"
        assert result["red_flags_total"] == 2
        assert result["red_flags_detected"] == 1
        assert len(result["missed_red_flags"]) == 1
        assert result["missed_red_flags"][0]["test_id"] == "RF002"

    def test_fail_when_no_evaluation_for_red_flag(self):
        """Test gate fails when Red Flag has no evaluation at all."""
        gt_issues = [
            {"test_id": "RF001", "playbook_standard": "Red Flag"}
        ]
        evaluations = []  # No evaluation for RF001

        result = check_red_flag_gate(evaluations, gt_issues)

        assert result["gate"] == "FAIL"
        assert len(result["missed_red_flags"]) == 1


class TestScoreGuidelinesIssue:
    """Tests for score_guidelines_issue function."""

    @pytest.fixture
    def config(self):
        """Standard guidelines config."""
        return {
            "quality_scores": {
                "max_per_dimension": {
                    "T1": {"detection": 1, "location": 1, "action": 1, "amendment": 2, "rationale": 2},
                    "T2": {"detection": 1, "location": 1, "action": 1, "amendment": 1, "rationale": 1},
                    "T3": {"detection": 0.5}
                }
            }
        }

    @pytest.fixture
    def t1_gt_issue(self):
        """T1 ground truth issue."""
        return {
            "test_id": "G001",
            "tier": 1,
            "clause_ref": "5.1",
            "clause_name": "Indemnification",
            "playbook_standard": "Gold Standard",
            "trigger_phrase": "indemnify",
            "expected_action": "DELETE",
            "expected_amendment": "reasonable notice period for consultation",
            "rationale_must_include": ["Section 5.1", "indemnity risk"]
        }

    def test_t1_perfect_score(self, config, t1_gt_issue):
        """Test perfect T1 score (7 points)."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "clause_ref": "5.1",
            "action": "DELETE",
            "proposed_text": "reasonable notice period for consultation",
            "rationale": "Section 5.1 creates indemnity risk through indemnify clause"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["detected"] == "Y"
        assert result["detection_score"] == 1
        assert result["location_score"] == 1
        assert result["action_score"] == 1
        assert result["amendment_score"] == 2
        assert result["rationale_score"] == 2
        assert result["total_score"] == 7
        assert result["max_score"] == 7

    def test_t2_perfect_score(self, config):
        """Test perfect T2 score (5 points)."""
        gt_issue = {
            "test_id": "G002",
            "tier": "T2",
            "clause_ref": "3.2",
            "playbook_standard": "Fallback 1",
            "trigger_phrase": "termination",
            "expected_action": "AMEND",
            "expected_amendment": "mutual termination rights",
            "rationale_must_include": ["Section 3.2"]
        }

        leah_output = {
            "classification": "⚠️ Requires review",
            "clause_ref": "3.2",
            "action": "AMEND",
            "proposed_text": "mutual termination rights established",
            "rationale": "Section 3.2 termination provisions need balancing"
        }

        result = score_guidelines_issue(leah_output, gt_issue, config)

        assert result["detected"] == "Y"
        assert result["total_score"] == 5
        assert result["max_score"] == 5

    def test_t3_detection_only(self, config):
        """Test T3 scoring (0.5 points for detection only)."""
        gt_issue = {
            "test_id": "G003",
            "tier": 3,
            "playbook_standard": "Fallback 2",
            "trigger_phrase": "notice"
        }

        leah_output = {
            "classification": "❌ Unfavourable",
            "rationale": "Notice period is insufficient"
        }

        result = score_guidelines_issue(leah_output, gt_issue, config)

        assert result["detected"] == "Y"
        assert result["detection_score"] == 0.5
        assert result["location_score"] == 0
        assert result["action_score"] == 0
        assert result["amendment_score"] == 0
        assert result["rationale_score"] == 0
        assert result["total_score"] == 0.5
        assert result["max_score"] == 0.5

    def test_no_leah_output_returns_nmi(self, config, t1_gt_issue):
        """Test that no Leah output returns NMI with zero scores."""
        result = score_guidelines_issue(None, t1_gt_issue, config)

        assert result["detected"] == "NMI"
        assert result["total_score"] == 0
        assert result["max_score"] == 7

    def test_detection_via_classification_markers(self, config, t1_gt_issue):
        """Test detection via classification markers."""
        for marker in ["❌", "⚠️", "Unfavourable"]:
            leah_output = {
                "classification": f"{marker} Issue",
                "rationale": "indemnify clause present"
            }

            result = score_guidelines_issue(leah_output, t1_gt_issue, config)

            assert result["detected"] == "Y"
            assert result["detection_score"] == 1

    def test_partial_detection_missing_trigger(self, config, t1_gt_issue):
        """Test partial detection (P) when trigger phrase missing."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "rationale": "This clause is problematic"  # No "indemnify"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["detected"] == "P"
        assert result["detection_score"] == 0.5

    def test_location_exact_match(self, config, t1_gt_issue):
        """Test location scoring with exact clause match."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "clause_ref": "5.1",
            "rationale": "indemnify issue"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["location_score"] == 1

    def test_location_same_article_partial(self, config, t1_gt_issue):
        """Test location partial credit for same article."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "clause_ref": "5.2",  # Same article (5) different section
            "rationale": "indemnify issue"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["location_score"] == 0.5

    def test_location_different_article_no_credit(self, config, t1_gt_issue):
        """Test no location credit for different article."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "clause_ref": "7.1",  # Different article
            "rationale": "indemnify issue"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["location_score"] == 0

    def test_action_exact_match(self, config, t1_gt_issue):
        """Test action scoring with exact match."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "action": "DELETE",
            "rationale": "indemnify issue"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["action_score"] == 1

    def test_action_case_insensitive(self, config, t1_gt_issue):
        """Test action matching is case-insensitive."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "action": "delete",  # lowercase
            "rationale": "indemnify issue"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["action_score"] == 1

    def test_amendment_50_percent_threshold(self, config, t1_gt_issue):
        """Test amendment scoring with 50% word overlap threshold."""
        # expected_amendment: "reasonable notice period for consultation"
        # Significant words (>3 chars): reasonable, notice, period, consultation = 4 words
        # Match 2/4 = 50% -> full score
        leah_output = {
            "classification": "❌ Unfavourable",
            "proposed_text": "reasonable notice provisions",  # 2/4 match
            "rationale": "indemnify issue"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["amendment_score"] == 2

    def test_amendment_partial_credit(self, config, t1_gt_issue):
        """Test amendment partial credit when some but < 50% overlap."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "proposed_text": "reasonable approach",  # 1/4 = 25% < 50%
            "rationale": "indemnify issue"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["amendment_score"] == 1

    def test_rationale_50_percent_threshold(self, config, t1_gt_issue):
        """Test rationale scoring with 50% threshold."""
        # rationale_must_include: ["Section 5.1", "indemnity risk"]
        # Match both -> full score
        leah_output = {
            "classification": "❌ Unfavourable",
            "rationale": "Section 5.1 creates indemnity risk"
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["rationale_score"] == 2

    def test_rationale_partial_when_some_matched(self, config, t1_gt_issue):
        """Test rationale partial credit when some but < 50% matched."""
        # Match 0/2 = 0% -> need to test this carefully
        leah_output = {
            "classification": "❌ Unfavourable",
            "rationale": "This clause is problematic"  # No matches
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["rationale_score"] == 0

    def test_rationale_fallback_when_no_must_include(self, config):
        """Test rationale gets 50% credit when no must_include specified."""
        gt_issue = {
            "test_id": "G004",
            "tier": 1,
            "playbook_standard": "Gold Standard",
            "trigger_phrase": "test",
            "rationale_must_include": []  # Empty
        }

        leah_output = {
            "classification": "❌ Unfavourable",
            "rationale": "Any rationale text here"
        }

        result = score_guidelines_issue(leah_output, gt_issue, config)

        assert result["rationale_score"] == 1  # 50% of max (2) = 1

    def test_fallback_field_names(self, config, t1_gt_issue):
        """Test fallback field names work."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "recommendation": "DELETE",  # fallback for action
            "redline_text": "reasonable notice period",  # fallback for proposed_text
            "detailed_reasoning": "Section 5.1 indemnify risk"  # fallback for rationale
        }

        result = score_guidelines_issue(leah_output, t1_gt_issue, config)

        assert result["action_score"] == 1
        assert result["amendment_score"] > 0
        assert result["rationale_score"] > 0


class TestClauseRefsMatch:
    """Tests for _clause_refs_match helper."""

    def test_exact_match(self):
        """Test exact clause reference match."""
        assert _clause_refs_match("5.1", "5.1") is True

    def test_match_with_section_prefix(self):
        """Test match with 'Section' prefix."""
        assert _clause_refs_match("Section 5.1", "5.1") is True
        assert _clause_refs_match("5.1", "Section 5.1") is True

    def test_match_with_clause_prefix(self):
        """Test match with 'Clause' prefix."""
        assert _clause_refs_match("Clause 5.1", "5.1") is True

    def test_case_insensitive(self):
        """Test matching is case-insensitive."""
        assert _clause_refs_match("SECTION 5.1", "section 5.1") is True

    def test_multi_level_clause(self):
        """Test multi-level clause references."""
        assert _clause_refs_match("5.1.2", "5.1.2") is True

    def test_no_match(self):
        """Test non-matching clauses."""
        assert _clause_refs_match("5.1", "5.2") is False


class TestClauseRefsSameArticle:
    """Tests for _clause_refs_same_article helper."""

    def test_same_article_different_section(self):
        """Test same article (top-level number) but different section."""
        assert _clause_refs_same_article("5.1", "5.2") is True

    def test_different_article(self):
        """Test different articles."""
        assert _clause_refs_same_article("5.1", "7.1") is False

    def test_with_section_prefix(self):
        """Test with Section prefix."""
        assert _clause_refs_same_article("Section 5.1", "5.2") is True

    def test_single_digit_clauses(self):
        """Test single-digit clause references."""
        assert _clause_refs_same_article("5", "5.1") is True


class TestCalculateGuidelinesPassFail:
    """Tests for calculate_guidelines_pass_fail function."""

    @pytest.fixture
    def config(self):
        """Standard config."""
        return {
            "pass_criteria": {
                "pass": {"min_percentage": 70},
                "marginal": {"min_percentage": 50}
            }
        }

    def test_pass_with_high_score_and_no_red_flags(self, config):
        """Test PASS when score >= 70% and no Red Flags."""
        evaluations = [
            {"test_id": "G001", "detected": "Y", "total_score": 7, "max_score": 7},
            {"test_id": "G002", "detected": "Y", "total_score": 5, "max_score": 5},
        ]
        gt_issues = [
            {"test_id": "G001", "playbook_standard": "Gold Standard"},
            {"test_id": "G002", "playbook_standard": "Fallback 1"}
        ]

        result = calculate_guidelines_pass_fail(evaluations, gt_issues, config)

        assert result["pass_fail"] == "PASS"
        assert result["percentage"] == 100
        assert result["gate_triggered"] is None

    def test_fail_on_red_flag_gate_regardless_of_score(self, config):
        """Test FAIL when Red Flag gate fails, even with high score."""
        evaluations = [
            {"test_id": "G001", "detected": "Y", "total_score": 7, "max_score": 7},
            {"test_id": "RF001", "detected": "NMI", "total_score": 0, "max_score": 7},  # Missed RF
        ]
        gt_issues = [
            {"test_id": "G001", "playbook_standard": "Gold Standard"},
            {"test_id": "RF001", "playbook_standard": "Red Flag"}
        ]

        result = calculate_guidelines_pass_fail(evaluations, gt_issues, config)

        assert result["pass_fail"] == "FAIL"
        assert result["gate_triggered"] == "red_flag_gate"
        assert "Red Flag" in result["reason"]
        # Score might be 50%, but Red Flag gate overrides
        assert result["percentage"] == 50.0

    def test_marginal_score_50_to_70(self, config):
        """Test MARGINAL when score between 50% and 70%."""
        evaluations = [
            {"test_id": "G001", "detected": "Y", "total_score": 4, "max_score": 7},  # 4/7 = 57%
            {"test_id": "G002", "detected": "Y", "total_score": 3, "max_score": 5},  # 3/5 = 60%
        ]
        gt_issues = [
            {"test_id": "G001", "playbook_standard": "Gold Standard"},
            {"test_id": "G002", "playbook_standard": "Fallback 1"}
        ]

        result = calculate_guidelines_pass_fail(evaluations, gt_issues, config)

        # Total: 7/12 = 58.33%
        assert result["pass_fail"] == "MARGINAL"
        assert 50 <= result["percentage"] < 70

    def test_fail_with_score_below_50(self, config):
        """Test FAIL when score < 50%."""
        evaluations = [
            {"test_id": "G001", "detected": "P", "total_score": 2, "max_score": 7},
            {"test_id": "G002", "detected": "NMI", "total_score": 0, "max_score": 5},
        ]
        gt_issues = [
            {"test_id": "G001", "playbook_standard": "Gold Standard"},
            {"test_id": "G002", "playbook_standard": "Fallback 1"}
        ]

        result = calculate_guidelines_pass_fail(evaluations, gt_issues, config)

        assert result["pass_fail"] == "FAIL"
        assert result["percentage"] < 50
        assert result["gate_triggered"] is None  # Failed on score, not gate

    def test_red_flag_gate_details_included(self, config):
        """Test that Red Flag gate details included in result."""
        evaluations = [
            {"test_id": "G001", "detected": "Y", "total_score": 7, "max_score": 7},
        ]
        gt_issues = [
            {"test_id": "G001", "playbook_standard": "Gold Standard"},
        ]

        result = calculate_guidelines_pass_fail(evaluations, gt_issues, config)

        assert "red_flag_gate" in result
        assert result["red_flag_gate"]["gate"] == "PASS"
        assert result["red_flag_gate"]["red_flags_total"] == 0
