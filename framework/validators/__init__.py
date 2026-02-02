"""Validation infrastructure for pipeline gates."""

from .base import ValidationResult, ValidationIssue, Severity, ValidationError
from .pre_aggregate import validate_pre_aggregation
from .pre_eval import validate_pre_evaluation
from .pre_workbook import validate_pre_workbook
from .stacking_validators import (
    validate_cp_redline_action,
    detect_critical_failures,
    determine_stacking_pass_fail,
    score_part_a_redline,
    detect_scope_violations,
    build_redline_clause_set,
    score_rules_stacking_redline,
    calculate_rules_stacking_pass_fail,
)
from .rules_validators import score_rule_evaluation, calculate_rules_pass_fail
from .guidelines_validators import (
    check_red_flag_gate,
    score_guidelines_issue,
    calculate_guidelines_pass_fail,
)

__all__ = [
    'ValidationResult', 'ValidationIssue', 'Severity', 'ValidationError',
    'validate_pre_aggregation', 'validate_pre_evaluation', 'validate_pre_workbook',
    'validate_cp_redline_action', 'detect_critical_failures',
    'determine_stacking_pass_fail', 'score_part_a_redline',
    'detect_scope_violations', 'build_redline_clause_set',
    'score_rules_stacking_redline', 'calculate_rules_stacking_pass_fail',
    'score_rule_evaluation', 'calculate_rules_pass_fail',
    'check_red_flag_gate', 'score_guidelines_issue', 'calculate_guidelines_pass_fail',
]
