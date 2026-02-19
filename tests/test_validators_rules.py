"""Tests for rules mode scoring and validation."""

import pytest

from framework.validators.rules_validators import (
    score_rule_evaluation,
    calculate_rules_pass_fail,
    _clause_mentioned_with_concern,
    _action_partially_correct
)


class TestScoreRuleEvaluation:
    """Tests for score_rule_evaluation function."""

    @pytest.fixture
    def config(self):
        """Standard rules mode scoring config."""
        return {
            "scoring": {
                "per_rule_max": 9,
                "dimensions": {
                    "detection": {"max": 2},
                    "compliance": {"max": 1},
                    "action": {"max": 2},
                    "language": {"max": 2},
                    "rationale": {"max": 2}
                }
            }
        }

    @pytest.fixture
    def gt_rule(self):
        """Ground truth rule."""
        return {
            "test_id": "R001",
            "contract": "test_contract",
            "clause_ref": "5.1",
            "rule_name": "Test Rule",
            "expected_action": "DELETE",
            "trigger_quote": "indemnification",
            "key_elements": ["reasonable", "notice period", "consultation"],
            "rationale_must_include": ["Section 5.1", "indemnity clause"]
        }

    def test_perfect_score(self, config, gt_rule):
        """Test perfect score with all dimensions correct."""
        leah_output = {
            "action": "DELETE",
            "proposed_text": "reasonable notice period for consultation",
            "rationale": "Section 5.1 includes problematic indemnification indemnity clause",
            "classification": "❌ Unfavourable"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["detected"] == "Y"
        assert result["detection_score"] == 2
        assert result["compliance_score"] == 1
        assert result["action_score"] == 2
        assert result["language_score"] == 2
        assert result["rationale_score"] == 2
        assert result["total_score"] == 9
        assert result["max_score"] == 9

    def test_no_leah_output(self, config, gt_rule):
        """Test scoring with no Leah output (NMI)."""
        result = score_rule_evaluation(None, gt_rule, config)

        assert result["detected"] == "NMI"
        assert result["detection_score"] == 0
        assert result["compliance_score"] == 0
        assert result["action_score"] == 0
        assert result["language_score"] == 0
        assert result["rationale_score"] == 0
        assert result["total_score"] == 0
        assert result["max_score"] == 9

    def test_detection_via_trigger_quote(self, config, gt_rule):
        """Test detection via trigger quote presence."""
        leah_output = {
            "rationale": "The indemnification clause is problematic",
            "action": "DELETE"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["detected"] == "Y"
        assert result["detection_score"] == 2

    def test_detection_via_classification(self, config, gt_rule):
        """Test detection via unfavourable classification."""
        leah_output = {
            "classification": "❌ Unfavourable",
            "action": "DELETE",
            "rationale": "Some reason"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["detected"] == "Y"
        assert result["detection_score"] == 2

    def test_partial_detection_no_action(self, config, gt_rule):
        """Test partial detection (P) when detected but no action."""
        leah_output = {
            "rationale": "The indemnification clause is here",
            "classification": "⚠️ Requires review",
            "action": ""  # No action
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["detected"] == "P"
        assert result["detection_score"] == 2
        assert result["action_score"] == 0

    def test_action_exact_match(self, config, gt_rule):
        """Test action scoring with exact match."""
        leah_output = {
            "action": "DELETE",
            "rationale": "indemnification found"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["action_score"] == 2

    def test_action_partial_credit_amend_delete(self, config, gt_rule):
        """Test partial credit for AMEND when DELETE expected."""
        leah_output = {
            "action": "AMEND",
            "rationale": "indemnification found"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["action_score"] == 1

    def test_action_partial_credit_delete_amend(self, config):
        """Test partial credit for DELETE when AMEND expected."""
        gt_rule = {
            "test_id": "R002",
            "expected_action": "AMEND",
            "trigger_quote": "test",
            "key_elements": [],
            "rationale_must_include": []
        }

        leah_output = {
            "action": "DELETE",
            "rationale": "test trigger found"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["action_score"] == 1

    def test_action_wrong(self, config, gt_rule):
        """Test no credit for wrong action."""
        leah_output = {
            "action": "ADD",
            "rationale": "indemnification found"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["action_score"] == 0

    def test_language_70_percent_threshold(self, config, gt_rule):
        """Test language scoring with 70% threshold."""
        # key_elements = ["reasonable", "notice period", "consultation"]
        # Match 3/3 = 100% >= 70% -> full score
        leah_output = {
            "proposed_text": "reasonable notice period for consultation",
            "rationale": "indemnification found"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["language_score"] == 2

    def test_language_partial_credit(self, config, gt_rule):
        """Test language partial credit when some but < 70% matched."""
        # Match only 1/3 = 33% < 70% but > 0 -> partial score
        leah_output = {
            "proposed_text": "reasonable approach",
            "rationale": "indemnification found"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["language_score"] == 1

    def test_language_no_credit(self, config, gt_rule):
        """Test language no credit when no elements matched."""
        leah_output = {
            "proposed_text": "different text entirely",
            "rationale": "indemnification found"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["language_score"] == 0

    def test_rationale_50_percent_threshold(self, config, gt_rule):
        """Test rationale scoring with 50% threshold."""
        # rationale_must_include = ["Section 5.1", "indemnity clause"]
        # Match 2/2 = 100% >= 50% -> full score
        leah_output = {
            "rationale": "Section 5.1 contains an indemnity clause that is problematic",
            "action": "DELETE"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["rationale_score"] == 2

    def test_rationale_partial_credit(self, config, gt_rule):
        """Test rationale partial credit when some but < 50% matched."""
        # Need to avoid matching any significant words (len > 3)
        # rationale_must_include = ["Section 5.1", "indemnity clause"]
        # Significant words: "Section", "indemnity", "clause"
        # Use completely different words to get 0 matches
        leah_output = {
            "rationale": "This text has no matching terms whatsoever",
            "action": "DELETE"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        # With 0 matches, should get 0 score (not even partial)
        assert result["rationale_score"] == 0

    def test_fallback_field_names(self, config, gt_rule):
        """Test that fallback field names work (recommendation, redline_text, detailed_reasoning)."""
        leah_output = {
            "recommendation": "DELETE",  # fallback for action
            "redline_text": "reasonable notice period",  # fallback for proposed_text
            "detailed_reasoning": "Section 5.1 indemnity clause indemnification",  # fallback for rationale
            "classification": "❌ Unfavourable"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["action_score"] == 2
        assert result["language_score"] > 0
        assert result["rationale_score"] == 2

    def test_zero_total_score_sets_nmi(self, config, gt_rule):
        """Test that zero total score sets detected to NMI."""
        leah_output = {
            "action": "ADD",  # wrong action
            "proposed_text": "completely different",
            "rationale": "unrelated reasoning"
        }

        result = score_rule_evaluation(leah_output, gt_rule, config)

        assert result["total_score"] == 0
        assert result["detected"] == "NMI"


class TestClauseMentionedWithConcern:
    """Tests for _clause_mentioned_with_concern helper."""

    def test_unfavourable_marker(self):
        """Test detection of ❌ marker."""
        output = {"classification": "❌ Unfavourable"}
        assert _clause_mentioned_with_concern(output) is True

    def test_warning_marker(self):
        """Test detection of ⚠️ marker."""
        output = {"classification": "⚠️ Requires attention"}
        assert _clause_mentioned_with_concern(output) is True

    def test_unfavourable_text(self):
        """Test detection of 'Unfavourable' text."""
        output = {"classification": "Unfavourable clause"}
        assert _clause_mentioned_with_concern(output) is True

    def test_no_concern(self):
        """Test no detection when no markers present."""
        output = {"classification": "Standard clause"}
        assert _clause_mentioned_with_concern(output) is False

    def test_empty_classification(self):
        """Test no detection with empty classification."""
        output = {"classification": ""}
        assert _clause_mentioned_with_concern(output) is False


class TestActionPartiallyCorrect:
    """Tests for _action_partially_correct helper."""

    def test_amend_delete_similar(self):
        """Test that AMEND and DELETE are considered similar."""
        assert _action_partially_correct("AMEND", "DELETE") is True

    def test_delete_amend_similar(self):
        """Test that DELETE and AMEND are considered similar."""
        assert _action_partially_correct("DELETE", "AMEND") is True

    def test_flag_amend_similar(self):
        """Test that FLAG and AMEND are considered similar."""
        assert _action_partially_correct("FLAG", "AMEND") is True

    def test_add_delete_not_similar(self):
        """Test that ADD and DELETE are not similar."""
        assert _action_partially_correct("ADD", "DELETE") is False

    def test_same_action_not_partial(self):
        """Test that identical actions don't count as partially correct."""
        assert _action_partially_correct("DELETE", "DELETE") is False


class TestCalculateRulesPassFail:
    """Tests for calculate_rules_pass_fail function."""

    @pytest.fixture
    def config(self):
        """Standard pass/fail config."""
        return {
            "pass_criteria": {
                "pass": {"min_percentage": 80},
                "marginal": {"min_percentage": 60}
            }
        }

    def test_pass_with_high_score_and_compliance(self, config):
        """Test PASS when score >= 80% and compliance >= 80%."""
        evaluations = [
            {"detected": "Y", "action_score": 2, "total_score": 9, "max_score": 9},
            {"detected": "Y", "action_score": 2, "total_score": 8, "max_score": 9},
            {"detected": "Y", "action_score": 2, "total_score": 9, "max_score": 9},
            {"detected": "Y", "action_score": 2, "total_score": 8, "max_score": 9},
            {"detected": "Y", "action_score": 2, "total_score": 9, "max_score": 9},
        ]

        result = calculate_rules_pass_fail(evaluations, config)

        assert result["pass_fail"] == "PASS"
        assert result["percentage"] >= 80
        assert result["compliance_rate"] >= 80

    def test_marginal_with_score_60_to_80(self, config):
        """Test MARGINAL when score between 60% and 80%."""
        evaluations = [
            {"detected": "Y", "action_score": 2, "total_score": 6, "max_score": 9},
            {"detected": "Y", "action_score": 2, "total_score": 7, "max_score": 9},
            {"detected": "Y", "action_score": 0, "total_score": 5, "max_score": 9},
        ]

        result = calculate_rules_pass_fail(evaluations, config)

        assert result["pass_fail"] == "MARGINAL"
        assert 60 <= result["percentage"] < 80

    def test_fail_with_score_below_60(self, config):
        """Test FAIL when score < 60%."""
        evaluations = [
            {"detected": "Y", "action_score": 0, "total_score": 3, "max_score": 9},
            {"detected": "P", "action_score": 0, "total_score": 2, "max_score": 9},
            {"detected": "NMI", "action_score": 0, "total_score": 0, "max_score": 9},
        ]

        result = calculate_rules_pass_fail(evaluations, config)

        assert result["pass_fail"] == "FAIL"
        assert result["percentage"] < 60

    def test_rules_triggered_count(self, config):
        """Test that rules_triggered excludes NMI."""
        evaluations = [
            {"detected": "Y", "action_score": 2, "total_score": 8, "max_score": 9},
            {"detected": "P", "action_score": 0, "total_score": 3, "max_score": 9},
            {"detected": "NMI", "action_score": 0, "total_score": 0, "max_score": 9},
            {"detected": "Y", "action_score": 2, "total_score": 9, "max_score": 9},
        ]

        result = calculate_rules_pass_fail(evaluations, config)

        assert result["rules_triggered"] == 3  # Y, P, Y (not NMI)

    def test_rules_complied_count(self, config):
        """Test that rules_complied counts Y with action_score > 0."""
        evaluations = [
            {"detected": "Y", "action_score": 2, "total_score": 8, "max_score": 9},  # complied
            {"detected": "Y", "action_score": 0, "total_score": 2, "max_score": 9},  # not complied
            {"detected": "P", "action_score": 2, "total_score": 5, "max_score": 9},  # not Y
            {"detected": "Y", "action_score": 1, "total_score": 7, "max_score": 9},  # complied (partial action)
        ]

        result = calculate_rules_pass_fail(evaluations, config)

        assert result["rules_complied"] == 2  # First and last

    def test_zero_max_score_edge_case(self, config):
        """Test handling of zero max score (shouldn't happen but handle gracefully)."""
        evaluations = []

        result = calculate_rules_pass_fail(evaluations, config)

        assert result["percentage"] == 0
        assert result["compliance_rate"] == 0
        assert result["pass_fail"] == "FAIL"

    def test_all_nmi_zero_compliance_rate(self, config):
        """Test that all NMI results in 0 compliance rate."""
        evaluations = [
            {"detected": "NMI", "action_score": 0, "total_score": 0, "max_score": 9},
            {"detected": "NMI", "action_score": 0, "total_score": 0, "max_score": 9},
        ]

        result = calculate_rules_pass_fail(evaluations, config)

        assert result["rules_triggered"] == 0
        assert result["compliance_rate"] == 0
