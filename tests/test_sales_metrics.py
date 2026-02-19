"""Tests for sales metrics compute functions."""

import pytest

from framework.scripts.sales_metrics import (
    compute_additional_issues_stats,
    compute_detection_rate,
    compute_model_metrics,
    compute_precision_recall_f1,
    compute_quality_scores,
    compute_stacking_metrics,
    compute_t1_gate,
    compute_traceability,
    cross_validate,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_gt_issue(detection: str, tier: str = "T2", **kwargs) -> dict:
    """Build a minimal gt_evaluation entry."""
    base = {
        "gt_id": "GT-01",
        "clause": "1.1",
        "tier": tier,
        "issue": "Test issue",
        "detection": detection,
        "detection_points": 0,
        "amendment_score": None,
        "rationale_score": None,
        "redline_quality_score": None,
        "matched_redline_id": None,
    }
    base.update(kwargs)
    return base


def _make_evaluation(
    gt_issues: list[dict] | None = None,
    additional_issues: list[dict] | None = None,
    t1_gate_pass: bool = True,
) -> dict:
    """Build a minimal evaluation result dict."""
    return {
        "gt_evaluations": gt_issues or [],
        "additional_issues": additional_issues or [],
        "summary": {"t1_gate_pass": t1_gate_pass},
    }


# ---------------------------------------------------------------------------
# Detection rate
# ---------------------------------------------------------------------------

class TestComputeDetectionRate:

    def test_all_detected(self):
        evals = [_make_evaluation([
            _make_gt_issue("Y"),
            _make_gt_issue("Y"),
            _make_gt_issue("P"),
        ])]
        result = compute_detection_rate(evals)
        assert result["Y"] == 2
        assert result["P"] == 1
        assert result["N"] == 0
        assert result["NMI"] == 0
        assert result["total_gt_issues"] == 3
        assert result["detected"] == 3
        assert result["detection_rate"] == 100.0

    def test_partial_detection(self):
        evals = [_make_evaluation([
            _make_gt_issue("Y"),
            _make_gt_issue("N"),
            _make_gt_issue("NMI"),
            _make_gt_issue("P"),
        ])]
        result = compute_detection_rate(evals)
        assert result["detected"] == 2
        assert result["detection_rate"] == 50.0

    def test_no_issues(self):
        evals = [_make_evaluation([])]
        result = compute_detection_rate(evals)
        assert result["total_gt_issues"] == 0
        assert result["detection_rate"] == 0.0

    def test_multiple_evaluations(self):
        evals = [
            _make_evaluation([_make_gt_issue("Y"), _make_gt_issue("Y")]),
            _make_evaluation([_make_gt_issue("N"), _make_gt_issue("NMI")]),
        ]
        result = compute_detection_rate(evals)
        assert result["Y"] == 2
        assert result["N"] == 1
        assert result["NMI"] == 1
        assert result["detection_rate"] == 50.0


# ---------------------------------------------------------------------------
# Additional issues / false positive rate
# ---------------------------------------------------------------------------

class TestComputeAdditionalIssuesStats:

    def test_all_valid(self):
        evals = [_make_evaluation(additional_issues=[
            {"assessment": "Valid"},
            {"assessment": "Valid"},
        ])]
        result = compute_additional_issues_stats(evals)
        assert result["valid"] == 2
        assert result["not_material"] == 0
        assert result["hallucination"] == 0
        assert result["false_positive_rate"] == 0.0
        assert result["audit_status"] == "pending"

    def test_mixed_assessments(self):
        evals = [_make_evaluation(additional_issues=[
            {"assessment": "Valid"},
            {"assessment": "Not Material"},
            {"assessment": "Hallucination"},
        ])]
        result = compute_additional_issues_stats(evals)
        assert result["valid"] == 1
        assert result["not_material"] == 1
        assert result["hallucination"] == 1
        assert result["total_additional"] == 3
        assert result["false_positive_rate"] == pytest.approx(66.7, abs=0.1)
        assert result["audit_status"] == "complete"

    def test_no_additional_issues(self):
        evals = [_make_evaluation(additional_issues=[])]
        result = compute_additional_issues_stats(evals)
        assert result["total_additional"] == 0
        assert result["false_positive_rate"] == 0.0

    def test_unknown_assessment(self):
        evals = [_make_evaluation(additional_issues=[
            {"assessment": "SomethingElse"},
        ])]
        result = compute_additional_issues_stats(evals)
        assert result["other"] == 1


# ---------------------------------------------------------------------------
# Precision / recall / F1
# ---------------------------------------------------------------------------

class TestComputePrecisionRecallF1:

    def test_perfect_scores(self):
        evals = [_make_evaluation([
            _make_gt_issue("Y", tier="T1"),
            _make_gt_issue("Y", tier="T2"),
        ])]
        additional = {"valid": 5, "not_material": 0}
        result = compute_precision_recall_f1(evals, additional)
        assert result["weighted_recall"] == 1.0
        assert result["precision"] == 1.0
        assert result["f1"] == 1.0

    def test_zero_recall(self):
        evals = [_make_evaluation([
            _make_gt_issue("NMI", tier="T1"),
            _make_gt_issue("N", tier="T2"),
        ])]
        additional = {"valid": 0, "not_material": 0}
        result = compute_precision_recall_f1(evals, additional)
        assert result["weighted_recall"] == 0.0

    def test_partial_recall_with_tiers(self):
        """T1 Y (8pts) + T2 N (0pts) => 8 / (8+5) = 0.6154"""
        evals = [_make_evaluation([
            _make_gt_issue("Y", tier="T1"),
            _make_gt_issue("N", tier="T2"),
        ])]
        additional = {"valid": 3, "not_material": 1}
        result = compute_precision_recall_f1(evals, additional)
        assert result["weighted_recall"] == pytest.approx(0.6154, abs=0.001)
        assert result["precision"] == pytest.approx(0.75, abs=0.01)


# ---------------------------------------------------------------------------
# Quality scores
# ---------------------------------------------------------------------------

class TestComputeQualityScores:

    def test_quality_averaging(self):
        evals = [_make_evaluation([
            _make_gt_issue("Y", amendment_score=3, rationale_score=2, redline_quality_score=3),
            _make_gt_issue("Y", amendment_score=2, rationale_score=3, redline_quality_score=2),
        ])]
        result = compute_quality_scores(evals)
        assert result["dimensions"]["amendment_score"] == 2.5
        assert result["dimensions"]["rationale_score"] == 2.5
        assert result["dimensions"]["redline_quality_score"] == 2.5
        assert result["overall_avg"] == 2.5

    def test_nulls_excluded(self):
        """N/NMI issues have null quality scores — should be excluded."""
        evals = [_make_evaluation([
            _make_gt_issue("Y", amendment_score=3, rationale_score=3, redline_quality_score=3),
            _make_gt_issue("NMI"),  # all nulls
        ])]
        result = compute_quality_scores(evals)
        assert result["dimensions"]["amendment_score"] == 3.0
        assert result["scored_issues"] == 1

    def test_no_scored_issues(self):
        evals = [_make_evaluation([_make_gt_issue("NMI")])]
        result = compute_quality_scores(evals)
        assert result["overall_avg"] is None


# ---------------------------------------------------------------------------
# T1 gate
# ---------------------------------------------------------------------------

class TestComputeT1Gate:

    def test_all_pass(self):
        """All T1 issues detected => passes."""
        evals = [
            _make_evaluation([_make_gt_issue("Y", tier="T1"), _make_gt_issue("P", tier="T1")]),
            _make_evaluation([_make_gt_issue("Y", tier="T1")]),
        ]
        result = compute_t1_gate(evals)
        assert result["passes"] == 2
        assert result["total"] == 2
        assert result["pass_rate"] == 100.0

    def test_mixed(self):
        """One contract misses a T1 => fails that contract."""
        evals = [
            _make_evaluation([_make_gt_issue("Y", tier="T1")]),
            _make_evaluation([_make_gt_issue("NMI", tier="T1")]),
            _make_evaluation([_make_gt_issue("N", tier="T1")]),
            _make_evaluation([_make_gt_issue("Y", tier="T1"), _make_gt_issue("P", tier="T1")]),
        ]
        result = compute_t1_gate(evals)
        assert result["passes"] == 2
        assert result["pass_rate"] == 50.0

    def test_no_t1_issues_passes(self):
        """Contract with no T1 issues vacuously passes."""
        evals = [_make_evaluation([_make_gt_issue("Y", tier="T2")])]
        result = compute_t1_gate(evals)
        assert result["passes"] == 1
        assert result["pass_rate"] == 100.0

    def test_empty(self):
        result = compute_t1_gate([])
        assert result["pass_rate"] == 0.0


# ---------------------------------------------------------------------------
# Traceability
# ---------------------------------------------------------------------------

class TestComputeTraceability:

    def test_full_traceability(self):
        evals = [_make_evaluation([
            _make_gt_issue("Y", clause="1.1", matched_redline_id="R-01"),
            _make_gt_issue("P", clause="2.3", matched_redline_id="R-05"),
        ])]
        result = compute_traceability(evals)
        assert result["traceability_pct"] == 100.0

    def test_partial_traceability(self):
        evals = [_make_evaluation([
            _make_gt_issue("Y", clause="1.1", matched_redline_id="R-01"),
            _make_gt_issue("Y", clause="2.3", matched_redline_id=None),
        ])]
        result = compute_traceability(evals)
        assert result["traceability_pct"] == 50.0

    def test_undetected_excluded(self):
        """N/NMI issues should not count toward traceability."""
        evals = [_make_evaluation([
            _make_gt_issue("N", clause="1.1", matched_redline_id=None),
        ])]
        result = compute_traceability(evals)
        assert result["detected_total"] == 0
        assert result["traceability_pct"] == 0.0


# ---------------------------------------------------------------------------
# Stacking metrics
# ---------------------------------------------------------------------------

class TestComputeStackingMetrics:

    def test_stacking_with_part_a_summary(self):
        evals = [
            {"part_a_summary": {"percentage": 90, "pass_fail": "PASS"}},
            {"part_a_summary": {"percentage": 80, "pass_fail": "PASS"}},
        ]
        result = compute_stacking_metrics(evals)
        assert result is not None
        assert result["avg_part_a_pct"] == 85.0
        assert result["passes"] == 2
        assert result["part_a_pass_rate"] == 100.0

    def test_stacking_none_for_empty(self):
        result = compute_stacking_metrics([])
        assert result is None

    def test_stacking_with_nested_summary(self):
        evals = [
            {"summary": {"part_a": {"percentage": 70, "pass_fail": "FAIL"}}},
        ]
        result = compute_stacking_metrics(evals)
        assert result is not None
        assert result["avg_part_a_pct"] == 70.0
        assert result["passes"] == 0


# ---------------------------------------------------------------------------
# Cross-validation
# ---------------------------------------------------------------------------

class TestCrossValidate:

    def test_no_warnings_when_matching(self):
        metrics = {
            "sonnet45": {
                "risk_identification_accuracy": {"detection_rate": 94.4},
            },
        }
        summary = {
            "model_comparison": {
                "sonnet45": {"detection_rate": 94.4},
            },
        }
        warnings = cross_validate(metrics, summary)
        assert warnings == []

    def test_warning_on_mismatch(self):
        metrics = {
            "sonnet45": {
                "risk_identification_accuracy": {"detection_rate": 90.0},
            },
        }
        summary = {
            "model_comparison": {
                "sonnet45": {"detection_rate": 94.4},
            },
        }
        warnings = cross_validate(metrics, summary)
        assert len(warnings) == 1
        assert "sonnet45" in warnings[0]
        assert "mismatch" in warnings[0]

    def test_within_tolerance(self):
        """Difference <= 0.2% should not warn."""
        metrics = {
            "sonnet45": {
                "risk_identification_accuracy": {"detection_rate": 94.3},
            },
        }
        summary = {
            "model_comparison": {
                "sonnet45": {"detection_rate": 94.4},
            },
        }
        warnings = cross_validate(metrics, summary)
        assert warnings == []

    def test_no_summary(self):
        warnings = cross_validate({}, None)
        assert len(warnings) == 1
        assert "No freeform" in warnings[0]


# ---------------------------------------------------------------------------
# Integration: compute_model_metrics
# ---------------------------------------------------------------------------

class TestComputeModelMetrics:

    def test_full_pipeline(self):
        freeform = [_make_evaluation(
            gt_issues=[
                _make_gt_issue("Y", tier="T1", amendment_score=3,
                               rationale_score=3, redline_quality_score=3,
                               clause="1.1", matched_redline_id="R-01"),
                _make_gt_issue("P", tier="T2", amendment_score=2,
                               rationale_score=2, redline_quality_score=2,
                               clause="2.1", matched_redline_id="R-02"),
            ],
            additional_issues=[{"assessment": "Valid"}],
            t1_gate_pass=True,
        )]
        stacking = [
            {"part_a_summary": {"percentage": 95, "pass_fail": "PASS"}},
        ]

        result = compute_model_metrics("sonnet45", freeform, stacking)

        assert result["model"] == "sonnet45"
        assert result["display_name"] == "Sonnet 4.5"
        assert result["risk_identification_accuracy"]["detection_rate"] == 100.0
        assert result["additional_issues"]["audit_status"] == "pending"
        assert result["precision_recall_f1"]["weighted_recall"] == pytest.approx(0.8077, abs=0.001)
        assert result["quality_score"]["overall_avg"] == 2.5
        assert result["t1_gate"]["pass_rate"] == 100.0
        assert result["traceability"]["traceability_pct"] == 100.0
        assert result["stacking"]["avg_part_a_pct"] == 95.0

    def test_no_stacking(self):
        """velocity/scale have no stacking data."""
        freeform = [_make_evaluation([_make_gt_issue("Y")])]
        result = compute_model_metrics("velocity", freeform, [])
        assert result["stacking"] is None
