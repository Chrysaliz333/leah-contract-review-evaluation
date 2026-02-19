"""Tests for stacking mode validators (freeform_stacking and rules_stacking)."""

import pytest

from framework.validators.stacking_validators import (
    validate_cp_redline_action,
    detect_critical_failures,
    score_part_a_redline,
    determine_stacking_pass_fail,
    detect_scope_violations,
    _normalise_clause_ref,
    _is_meaningful_comment,
    build_redline_clause_set,
    score_rules_stacking_redline,
    calculate_rules_stacking_pass_fail
)


# === Freeform Stacking Tests ===

class TestValidateCpRedlineAction:
    """Tests for validate_cp_redline_action function."""

    def test_correct_accept_action(self):
        """Test correct ACCEPT action."""
        result = validate_cp_redline_action("ACCEPT", ["ACCEPT", "MODIFY"], "RL001")

        assert result["action_correct"] is True
        assert result["is_adversarial"] is False
        assert result["critical_failure"] is None

    def test_correct_modify_action(self):
        """Test correct MODIFY action."""
        result = validate_cp_redline_action("MODIFY", ["MODIFY", "REJECT"], "RL001")

        assert result["action_correct"] is True
        assert result["is_adversarial"] is True  # No ACCEPT allowed = adversarial

    def test_correct_reject_action(self):
        """Test correct REJECT action."""
        result = validate_cp_redline_action("REJECT", ["REJECT"], "RL001")

        assert result["action_correct"] is True
        assert result["is_adversarial"] is True

    def test_wrong_action_no_critical(self):
        """Test wrong action on non-adversarial redline."""
        result = validate_cp_redline_action("MODIFY", ["ACCEPT", "REJECT"], "RL001")

        assert result["action_correct"] is False
        assert result["is_adversarial"] is False
        assert result["critical_failure"] is None

    def test_adversarial_accept_critical_failure(self):
        """Test ACCEPT on adversarial redline triggers critical failure."""
        result = validate_cp_redline_action("ACCEPT", ["MODIFY", "REJECT"], "RL001")

        assert result["action_correct"] is False
        assert result["is_adversarial"] is True
        assert result["critical_failure"] is not None
        assert result["critical_failure"]["failure_type"] == "ACCEPT_ON_ADVERSARIAL"
        assert result["critical_failure"]["severity"] == "CRITICAL"
        assert result["critical_failure"]["redline_id"] == "RL001"

    def test_case_insensitive_action_matching(self):
        """Test action matching is case-insensitive."""
        result = validate_cp_redline_action("accept", ["ACCEPT"], "RL001")

        assert result["action_correct"] is True

    def test_empty_action_nmi(self):
        """Test empty action treated as NMI."""
        result = validate_cp_redline_action("", ["ACCEPT"], "RL001")

        assert result["action_correct"] is False


class TestDetectCriticalFailures:
    """Tests for detect_critical_failures function."""

    def test_extract_critical_failures(self):
        """Test extraction of critical failures from evaluations."""
        evaluations = [
            {"redline_id": "RL001", "critical_failure": {"type": "ADVERSARIAL_ACCEPT"}},
            {"redline_id": "RL002", "critical_failure": None},
            {"redline_id": "RL003", "critical_failure": {"type": "NOT_MENTIONED"}},
        ]

        failures = detect_critical_failures(evaluations)

        assert len(failures) == 2
        assert failures[0]["type"] == "ADVERSARIAL_ACCEPT"
        assert failures[1]["type"] == "NOT_MENTIONED"

    def test_no_critical_failures(self):
        """Test when no critical failures exist."""
        evaluations = [
            {"redline_id": "RL001", "critical_failure": None},
            {"redline_id": "RL002", "critical_failure": None},
        ]

        failures = detect_critical_failures(evaluations)

        assert failures == []


class TestScorePartARedline:
    """Tests for score_part_a_redline function."""

    @pytest.fixture
    def config(self):
        """Standard Part A config."""
        return {
            "detection_points": {
                "part_a": {
                    "per_redline": 6,
                    "max_per_dimension": 2
                }
            }
        }

    @pytest.fixture
    def gt_redline(self):
        """Standard GT redline."""
        return {
            "test_id": "RL001",
            "clause_ref": "5.1",
            "acceptable_actions": ["MODIFY", "REJECT"],
            "key_elements": ["reasonable notice", "mutual consultation"],
            "reasoning_must_address": "indemnification concerns"
        }

    def test_perfect_score(self, config, gt_redline):
        """Test perfect score with all dimensions correct."""
        leah_response = {
            "action": "MODIFY",
            "proposed_text": "Add reasonable notice period for mutual consultation process",
            "rationale": "This addresses indemnification concerns by providing adequate notice"
        }

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["action_correct"] is True
        assert result["action_score"] == 2
        assert result["revision_score"] == 2
        assert result["reasoning_score"] == 2
        assert result["total_score"] == 6
        assert result["max_score"] == 6

    def test_no_leah_response_nmi(self, config, gt_redline):
        """Test no Leah response returns NMI with zero scores."""
        result = score_part_a_redline(None, gt_redline, config)

        assert result["leah_action"] == "NMI"
        assert result["action_correct"] is False
        assert result["total_score"] == 0
        assert result["max_score"] == 6
        assert result["critical_failure"] is not None  # Adversarial redline not mentioned

    def test_no_leah_response_non_adversarial(self, config):
        """Test no Leah response on non-adversarial redline."""
        gt_redline = {
            "test_id": "RL001",
            "acceptable_actions": ["ACCEPT", "MODIFY"]
        }

        result = score_part_a_redline(None, gt_redline, config)

        assert result["is_adversarial"] is False
        assert result["critical_failure"] is None  # Not critical for non-adversarial

    def test_action_correct(self, config, gt_redline):
        """Test action scoring."""
        leah_response = {"action": "REJECT"}

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["action_score"] == 2
        assert result["action_correct"] is True

    def test_action_wrong(self, config, gt_redline):
        """Test wrong action gets zero score."""
        leah_response = {"action": "ACCEPT"}

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["action_score"] == 0
        assert result["action_correct"] is False
        assert result["critical_failure"] is not None  # Adversarial accept

    def test_revision_score_with_key_elements(self, config, gt_redline):
        """Test revision scoring when key elements present."""
        # key_elements: ["reasonable notice", "mutual consultation"]
        leah_response = {
            "action": "MODIFY",
            "proposed_text": "Reasonable notice and mutual consultation required"
        }

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["revision_score"] == 2  # Both key elements matched

    def test_revision_score_no_key_elements(self, config, gt_redline):
        """Test revision scoring when no key elements specified."""
        gt_redline["key_elements"] = []

        leah_response = {
            "action": "MODIFY",
            "proposed_text": "Some revision text here that is long enough"
        }

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["revision_score"] == 1  # Baseline score for having revision

    def test_revision_too_short_no_score(self, config, gt_redline):
        """Test revision that's too short gets no score."""
        leah_response = {
            "action": "MODIFY",
            "proposed_text": "Too short"  # Less than 20 chars
        }

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["revision_score"] == 0

    def test_reasoning_score_matches_must_address(self, config, gt_redline):
        """Test reasoning scoring when must_address matched."""
        leah_response = {
            "action": "MODIFY",
            "rationale": "This change addresses the indemnification concerns raised by the clause"
        }

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["reasoning_score"] == 2

    def test_reasoning_score_no_must_address(self, config, gt_redline):
        """Test reasoning scoring when no must_address specified."""
        gt_redline["reasoning_must_address"] = ""

        leah_response = {
            "action": "MODIFY",
            "rationale": "Some reasoning that is long enough to get baseline score"
        }

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["reasoning_score"] == 1  # Baseline score

    def test_reasoning_too_short_no_score(self, config, gt_redline):
        """Test reasoning that's too short gets no score."""
        leah_response = {
            "action": "MODIFY",
            "rationale": "Short"  # Less than 30 chars
        }

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["reasoning_score"] == 0

    def test_fallback_field_names(self, config, gt_redline):
        """Test fallback field names work."""
        leah_response = {
            "recommendation": "MODIFY",  # fallback for action
            "redline_text": "reasonable notice mutual consultation",  # fallback for proposed_text
            "detailed_reasoning": "indemnification concerns need addressing"  # fallback for rationale
        }

        result = score_part_a_redline(leah_response, gt_redline, config)

        assert result["action_score"] == 2
        assert result["revision_score"] > 0
        assert result["reasoning_score"] > 0


class TestDetermineStackingPassFail:
    """Tests for determine_stacking_pass_fail function."""

    @pytest.fixture
    def config(self):
        """Standard stacking config."""
        return {
            "gates": {
                "critical_failure_gate": True,
                "t1_gate": True,
                "t1_gate_applies_to": "part_b"
            },
            "pass_criteria": {
                "pass": {"min_percentage": 70},
                "marginal": {"min_percentage": 50}
            }
        }

    def test_pass_with_high_score(self, config):
        """Test PASS when combined score >= 70%."""
        part_a_summary = {"percentage": 80}
        part_b_summary = {"weighted_recall": 0.9, "by_tier": {"T1": {"total": 2, "detected": 2}}}
        critical_failures = []

        result = determine_stacking_pass_fail(part_a_summary, part_b_summary, critical_failures, config)

        # Combined: 80*0.4 + 90*0.6 = 32 + 54 = 86%
        assert result["pass_fail"] == "PASS"
        assert result["gate_triggered"] is None

    def test_fail_on_critical_failure_gate(self, config):
        """Test FAIL when critical failure gate triggered."""
        part_a_summary = {"percentage": 100}
        part_b_summary = {"weighted_recall": 1.0, "by_tier": {"T1": {"total": 2, "detected": 2}}}
        critical_failures = [{"type": "ADVERSARIAL_ACCEPT", "redline_id": "RL001"}]

        result = determine_stacking_pass_fail(part_a_summary, part_b_summary, critical_failures, config)

        assert result["pass_fail"] == "FAIL"
        assert result["gate_triggered"] == "critical_failure_gate"
        assert "adversarial" in result["reason"].lower()

    def test_fail_on_t1_gate(self, config):
        """Test FAIL when T1 gate triggered."""
        part_a_summary = {"percentage": 80}
        part_b_summary = {"weighted_recall": 0.9, "by_tier": {"T1": {"total": 3, "detected": 1}}}
        critical_failures = []

        result = determine_stacking_pass_fail(part_a_summary, part_b_summary, critical_failures, config)

        assert result["pass_fail"] == "FAIL"
        assert result["gate_triggered"] == "t1_gate"
        assert "1/3" in result["reason"]

    def test_marginal_score_50_to_70(self, config):
        """Test MARGINAL when score between 50% and 70%."""
        part_a_summary = {"percentage": 50}
        part_b_summary = {"weighted_recall": 0.65, "by_tier": {"T1": {"total": 2, "detected": 2}}}
        critical_failures = []

        result = determine_stacking_pass_fail(part_a_summary, part_b_summary, critical_failures, config)

        # Combined: 50*0.4 + 65*0.6 = 20 + 39 = 59%
        assert result["pass_fail"] == "MARGINAL"
        assert 50 <= float(result["reason"].split()[2].rstrip("%")) < 70

    def test_fail_with_low_score(self, config):
        """Test FAIL when score < 50%."""
        part_a_summary = {"percentage": 30}
        part_b_summary = {"weighted_recall": 0.4, "by_tier": {"T1": {"total": 2, "detected": 2}}}
        critical_failures = []

        result = determine_stacking_pass_fail(part_a_summary, part_b_summary, critical_failures, config)

        # Combined: 30*0.4 + 40*0.6 = 12 + 24 = 36%
        assert result["pass_fail"] == "FAIL"
        assert result["gate_triggered"] == "score_threshold"


# === Rules Stacking Tests ===

class TestNormaliseClauseRef:
    """Tests for _normalise_clause_ref helper."""

    def test_normalise_section_prefix(self):
        """Test normalisation with Section prefix."""
        assert _normalise_clause_ref("Section 5.1") == "5.1"

    def test_normalise_clause_prefix(self):
        """Test normalisation with Clause prefix."""
        assert _normalise_clause_ref("Clause 7.2") == "7.2"

    def test_normalise_article_prefix(self):
        """Test normalisation with Article prefix."""
        assert _normalise_clause_ref("Article 3.4") == "3.4"

    def test_normalise_paragraph_symbol(self):
        """Test normalisation with § symbol."""
        assert _normalise_clause_ref("§ 10.1") == "10.1"
        assert _normalise_clause_ref("§10.1") == "10.1"

    def test_normalise_multi_level(self):
        """Test normalisation of multi-level clauses."""
        assert _normalise_clause_ref("Section 5.1.2") == "5.1.2"

    def test_normalise_case_insensitive(self):
        """Test normalisation is case-insensitive."""
        assert _normalise_clause_ref("SECTION 5.1") == "5.1"
        assert _normalise_clause_ref("section 5.1") == "5.1"

    def test_normalise_plain_number(self):
        """Test normalisation of plain number."""
        assert _normalise_clause_ref("5.1") == "5.1"

    def test_normalise_empty_string(self):
        """Test normalisation of empty string."""
        assert _normalise_clause_ref("") == ""


class TestIsMeaningfulComment:
    """Tests for _is_meaningful_comment helper."""

    def test_unfavourable_marker_meaningful(self):
        """Test unfavourable marker indicates meaningful comment."""
        assert _is_meaningful_comment("❌ Unfavourable") is True

    def test_warning_marker_meaningful(self):
        """Test warning marker indicates meaningful comment."""
        assert _is_meaningful_comment("⚠️ Requires review") is True

    def test_favourable_marker_not_meaningful(self):
        """Test favourable marker indicates no meaningful comment."""
        assert _is_meaningful_comment("✅ Standard") is False
        assert _is_meaningful_comment("Standard clause") is False
        assert _is_meaningful_comment("Compliant") is False
        assert _is_meaningful_comment("Acceptable") is False

    def test_favourable_text_not_meaningful(self):
        """Test 'Favourable' text (without 'Unfavourable') is not meaningful."""
        assert _is_meaningful_comment("Favourable terms") is False

    def test_unfavourable_text_meaningful(self):
        """Test 'Unfavourable' text is meaningful."""
        assert _is_meaningful_comment("Unfavourable clause") is True

    def test_empty_classification_not_meaningful(self):
        """Test empty classification is not meaningful."""
        assert _is_meaningful_comment("") is False


class TestBuildRedlineClauseSet:
    """Tests for build_redline_clause_set function."""

    def test_build_from_clause_refs(self):
        """Test building set from clause_ref fields."""
        gt_redlines = [
            {"clause_ref": "Section 5.1"},
            {"clause_ref": "Clause 7.2"},
            {"clause_ref": "10.3"}
        ]

        result = build_redline_clause_set(gt_redlines)

        assert "5.1" in result
        assert "7.2" in result
        assert "10.3" in result

    def test_build_from_section_field(self):
        """Test building set from section field."""
        gt_redlines = [
            {"section": "5"},
            {"section": "7"}
        ]

        result = build_redline_clause_set(gt_redlines)

        assert "5" in result
        assert "7" in result

    def test_build_from_mixed_fields(self):
        """Test building set from both clause_ref and section."""
        gt_redlines = [
            {"clause_ref": "Section 5.1", "section": "5"},
            {"clause_ref": "7.2"}
        ]

        result = build_redline_clause_set(gt_redlines)

        assert "5.1" in result
        assert "5" in result
        assert "7.2" in result

    def test_empty_redlines(self):
        """Test with empty redlines list."""
        result = build_redline_clause_set([])

        assert result == set()


class TestDetectScopeViolations:
    """Tests for detect_scope_violations function."""

    @pytest.fixture
    def config(self):
        """Standard config."""
        return {}

    def test_no_violations_all_in_scope(self, config):
        """Test no violations when all comments in scope."""
        canonical_json = {
            "risk_table": [
                {"clause_ref": "5.1", "classification": "❌ Unfavourable"}
            ],
            "proposed_redlines": []
        }
        redline_clauses = {"5.1"}

        violations = detect_scope_violations(canonical_json, redline_clauses, config)

        assert violations == []

    def test_violation_out_of_scope_comment(self, config):
        """Test violation for comment on non-redlined clause."""
        canonical_json = {
            "risk_table": [
                {"clause_ref": "7.2", "classification": "❌ Unfavourable", "clause_summary": "Issue here"}
            ],
            "proposed_redlines": []
        }
        redline_clauses = {"5.1"}

        violations = detect_scope_violations(canonical_json, redline_clauses, config)

        assert len(violations) == 1
        assert violations[0]["clause_ref"] == "7.2"
        assert violations[0]["violation_type"] == "OUT_OF_SCOPE_COMMENT"
        assert violations[0]["severity"] == "CRITICAL"

    def test_violation_out_of_scope_redline(self, config):
        """Test violation for redline on non-redlined clause."""
        canonical_json = {
            "risk_table": [],
            "proposed_redlines": [
                {"clause_ref": "10.1", "change_summary": "Added language"}
            ]
        }
        redline_clauses = {"5.1"}

        violations = detect_scope_violations(canonical_json, redline_clauses, config)

        assert len(violations) == 1
        assert violations[0]["clause_ref"] == "10.1"
        assert violations[0]["violation_type"] == "OUT_OF_SCOPE_REDLINE"

    def test_no_violation_favourable_comment(self, config):
        """Test favourable comment not counted as violation."""
        canonical_json = {
            "risk_table": [
                {"clause_ref": "7.2", "classification": "✅ Standard"}
            ],
            "proposed_redlines": []
        }
        redline_clauses = {"5.1"}

        violations = detect_scope_violations(canonical_json, redline_clauses, config)

        assert violations == []  # Favourable comment not counted

    def test_multiple_violations(self, config):
        """Test multiple violations detected."""
        canonical_json = {
            "risk_table": [
                {"clause_ref": "7.2", "classification": "❌ Unfavourable"},
                {"clause_ref": "8.1", "classification": "⚠️ Requires review"}
            ],
            "proposed_redlines": [
                {"clause_ref": "10.1", "proposed_text": "New text"}
            ]
        }
        redline_clauses = {"5.1"}

        violations = detect_scope_violations(canonical_json, redline_clauses, config)

        assert len(violations) == 3


class TestScoreRulesStackingRedline:
    """Tests for score_rules_stacking_redline function."""

    @pytest.fixture
    def config(self):
        """Standard rules stacking config."""
        return {
            "scoring": {
                "per_redline_max": 6
            }
        }

    @pytest.fixture
    def gt_redline(self):
        """Standard GT redline."""
        return {
            "test_id": "RL001",
            "clause_ref": "5.1",
            "expected_action": "MODIFY",
            "key_elements": ["reasonable notice", "mutual consultation"],
            "rationale_must_include": ["Rule 123", "indemnification"]
        }

    def test_perfect_score(self, config, gt_redline):
        """Test perfect score with all dimensions correct."""
        leah_response = {
            "action": "MODIFY",
            "proposed_text": "Add reasonable notice period for mutual consultation",
            "rationale": "Per Rule 123, indemnification requires notice"
        }

        result = score_rules_stacking_redline(leah_response, gt_redline, config)

        assert result["detected"] == "Y"
        assert result["action_score"] == 2
        assert result["revision_score"] == 2
        assert result["reasoning_score"] == 2
        assert result["total_score"] == 6
        assert result["max_score"] == 6

    def test_no_leah_response_nmi(self, config, gt_redline):
        """Test no Leah response returns NMI."""
        result = score_rules_stacking_redline(None, gt_redline, config)

        assert result["detected"] == "NMI"
        assert result["leah_action"] == "NMI"
        assert result["total_score"] == 0

    def test_action_exact_match(self, config, gt_redline):
        """Test action exact match gets full score."""
        leah_response = {"action": "MODIFY"}

        result = score_rules_stacking_redline(leah_response, gt_redline, config)

        assert result["action_score"] == 2

    def test_action_wrong_partial_credit(self, config, gt_redline):
        """Test wrong action gets partial credit if provided."""
        leah_response = {"action": "REJECT"}  # Expected MODIFY

        result = score_rules_stacking_redline(leah_response, gt_redline, config)

        assert result["detected"] == "P"
        assert result["action_score"] == 1  # Partial credit

    def test_revision_50_percent_threshold(self, config, gt_redline):
        """Test revision scoring with 50% threshold."""
        # key_elements: ["reasonable notice", "mutual consultation"]
        leah_response = {
            "action": "MODIFY",
            "proposed_text": "Add reasonable notice period provision"  # 1/2 key elements
        }

        result = score_rules_stacking_redline(leah_response, gt_redline, config)

        assert result["revision_score"] == 2  # >= 50% threshold

    def test_revision_partial_credit(self, config):
        """Test revision partial credit when some but < 50% matched."""
        # Need 3 key elements so 1/3 = 33% < 50%
        gt_redline = {
            "test_id": "RL001",
            "expected_action": "MODIFY",
            "key_elements": ["reasonable notice", "mutual consultation", "indemnification"],
            "rationale_must_include": []
        }

        leah_response = {
            "action": "MODIFY",
            "proposed_text": "Add reasonable approach here"  # 1/3 = 33% < 50%
        }

        result = score_rules_stacking_redline(leah_response, gt_redline, config)

        assert result["revision_score"] == 1  # Partial credit

    def test_revision_no_key_elements_baseline(self, config, gt_redline):
        """Test revision baseline score when no key elements."""
        gt_redline["key_elements"] = []

        leah_response = {
            "action": "MODIFY",
            "proposed_text": "Some revision text that is long enough"
        }

        result = score_rules_stacking_redline(leah_response, gt_redline, config)

        assert result["revision_score"] == 1  # Baseline

    def test_reasoning_50_percent_threshold(self, config, gt_redline):
        """Test reasoning scoring with 50% threshold."""
        leah_response = {
            "action": "MODIFY",
            "rationale": "According to Rule 123, indemnification requires notice provisions"
        }

        result = score_rules_stacking_redline(leah_response, gt_redline, config)

        assert result["reasoning_score"] == 2

    def test_fallback_field_names(self, config, gt_redline):
        """Test fallback field names work."""
        leah_response = {
            "recommendation": "MODIFY",
            "redline_text": "reasonable notice mutual consultation",
            "detailed_reasoning": "Rule 123 indemnification requirements"
        }

        result = score_rules_stacking_redline(leah_response, gt_redline, config)

        assert result["action_score"] == 2
        assert result["revision_score"] > 0
        assert result["reasoning_score"] > 0


class TestCalculateRulesStackingPassFail:
    """Tests for calculate_rules_stacking_pass_fail function."""

    @pytest.fixture
    def config(self):
        """Standard pass/fail config."""
        return {
            "pass_criteria": {
                "pass": {"min_percentage": 70, "max_scope_violations": 0},
                "marginal": {"min_percentage": 50}
            }
        }

    def test_pass_with_high_score_no_violations(self, config):
        """Test PASS when score >= 70% and zero violations."""
        evaluations = [
            {"test_id": "RL001", "total_score": 6, "max_score": 6},
            {"test_id": "RL002", "total_score": 5, "max_score": 6},
        ]
        scope_violations = []

        result = calculate_rules_stacking_pass_fail(evaluations, scope_violations, config)

        assert result["pass_fail"] == "PASS"
        assert result["percentage"] >= 70
        assert result["gate_triggered"] is None

    def test_fail_on_scope_violations(self, config):
        """Test FAIL when scope violations exceed threshold."""
        evaluations = [
            {"test_id": "RL001", "total_score": 6, "max_score": 6},
        ]
        scope_violations = [
            {"clause_ref": "7.2", "violation_type": "OUT_OF_SCOPE_COMMENT"}
        ]

        result = calculate_rules_stacking_pass_fail(evaluations, scope_violations, config)

        assert result["pass_fail"] == "FAIL"
        assert result["gate_triggered"] == "scope_violation_gate"
        assert "scope violation" in result["reason"].lower()

    def test_marginal_score_50_to_70(self, config):
        """Test MARGINAL when score between 50% and 70%."""
        evaluations = [
            {"test_id": "RL001", "total_score": 4, "max_score": 6},
            {"test_id": "RL002", "total_score": 3, "max_score": 6},
        ]
        scope_violations = []

        result = calculate_rules_stacking_pass_fail(evaluations, scope_violations, config)

        # 7/12 = 58.33%
        assert result["pass_fail"] == "MARGINAL"
        assert 50 <= result["percentage"] < 70

    def test_fail_with_low_score(self, config):
        """Test FAIL when score < 50%."""
        evaluations = [
            {"test_id": "RL001", "total_score": 2, "max_score": 6},
            {"test_id": "RL002", "total_score": 1, "max_score": 6},
        ]
        scope_violations = []

        result = calculate_rules_stacking_pass_fail(evaluations, scope_violations, config)

        # 3/12 = 25%
        assert result["pass_fail"] == "FAIL"
        assert result["percentage"] < 50
        assert result["gate_triggered"] == "score_threshold"

    def test_zero_max_score_edge_case(self, config):
        """Test handling of zero max score."""
        evaluations = []
        scope_violations = []

        result = calculate_rules_stacking_pass_fail(evaluations, scope_violations, config)

        assert result["percentage"] == 0
        assert result["pass_fail"] == "FAIL"
