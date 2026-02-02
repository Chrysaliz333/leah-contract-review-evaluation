"""Config-driven field resolution for multi-mode evaluation.

Extracts issue ID, tier, clause, and other fields using the field names
specified in mode configuration, eliminating hardcoded field access.
"""

from typing import Optional, Union


def get_issue_id(issue: dict, config: dict, part: str = None) -> str:
    """Get issue ID using config-specified field name."""
    gt_config = config.get("gt_structure", {})

    # Handle dual_part modes
    if part and "parts" in gt_config:
        part_config = gt_config.get("parts", {}).get(part, {})
        id_field = part_config.get("id_field", gt_config.get("id_field", "gt_id"))
    else:
        id_field = gt_config.get("id_field", "gt_id")

    return issue.get(id_field, issue.get("gt_id", issue.get("test_id", "")))


def get_tier(issue: dict, config: dict, part: str = None) -> Optional[str]:
    """Get tier using config-specified field name. Returns normalised T1/T2/T3."""
    gt_config = config.get("gt_structure", {})

    if part and "parts" in gt_config:
        part_config = gt_config.get("parts", {}).get(part, {})
        tier_field = part_config.get("tier_field", gt_config.get("tier_field"))
    else:
        tier_field = gt_config.get("tier_field")

    if not tier_field:
        return None

    tier = issue.get(tier_field)
    if tier is None:
        tier = issue.get("tier", issue.get("gt_tier"))

    return _normalise_tier(tier)


def _normalise_tier(tier: Union[str, int, None]) -> Optional[str]:
    """Normalise tier to T1/T2/T3 format."""
    if tier is None:
        return None

    if isinstance(tier, int):
        return f"T{tier}"

    tier_str = str(tier).strip().upper()

    if tier_str in ("T1", "T2", "T3"):
        return tier_str

    if tier_str.isdigit():
        return f"T{tier_str}"

    if tier_str.startswith("TIER"):
        num = tier_str.replace("TIER", "").strip()
        if num.isdigit():
            return f"T{num}"

    return tier_str


def get_clause(issue: dict, config: dict, part: str = None) -> str:
    """Get clause reference using config-specified field name."""
    gt_config = config.get("gt_structure", {})

    if part and "parts" in gt_config:
        part_config = gt_config.get("parts", {}).get(part, {})
        clause_field = part_config.get("clause_field", gt_config.get("clause_field", "clause"))
    else:
        clause_field = gt_config.get("clause_field", "clause")

    return issue.get(clause_field, issue.get("clause", issue.get("clause_ref", "")))


def get_issue_text(issue: dict, config: dict, part: str = None) -> str:
    """Get issue description using config-specified field name."""
    gt_config = config.get("gt_structure", {})

    if part and "parts" in gt_config:
        part_config = gt_config.get("parts", {}).get(part, {})
        issue_field = part_config.get("issue_field", gt_config.get("issue_field", "issue"))
    else:
        issue_field = gt_config.get("issue_field", "issue")

    return issue.get(issue_field, issue.get("issue", ""))


def get_detection_points(
    detection: str,
    tier: str,
    config: dict,
    part: str = None
) -> float:
    """Get detection points using config-specified mapping."""
    points_config = config.get("detection_points", {})

    # Dual-part mode: select correct sub-config
    if part and part in points_config:
        points_config = points_config[part]

    # Tier-based lookup (freeform, guidelines, freeform_stacking part_b)
    if tier and tier in points_config:
        tier_config = points_config[tier]
        return tier_config.get(detection, 0)

    # Check for per_rule_max (rules mode uses dimension scoring)
    if "per_rule_max" in points_config:
        return 0  # Rules mode: caller should use dimension-specific scoring

    return 0


def get_acceptable_actions(issue: dict, config: dict) -> list[str]:
    """Get acceptable actions for stacking modes."""
    return issue.get("acceptable_actions", [])


def extract_contract_type(contract: str, config: dict) -> Optional[str]:
    """Extract contract type from contract ID."""
    contract_types = config.get("contract_types", [])
    if not contract_types:
        return None

    contract_lower = contract.lower()

    for ct in contract_types:
        if contract_lower.startswith(ct.lower()):
            return ct.lower()

    for ct in contract_types:
        if ct.lower() in contract_lower:
            return ct.lower()

    return None
