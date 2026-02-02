#!/usr/bin/env python3
"""
Validate Ground Truth JSON files.

Usage:
    python validate_gt.py ground_truth/consulting.json
    python validate_gt.py ground_truth/consulting.json --contract contracts/consulting.docx
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


# GT Schema v4 field specifications
V4_FIELDS = {
    "detection_logic": {
        "type": str,
        "enum": ["standard", "new_clause_recommendation", "pattern_match", "any_mention"],
        "default": "standard",
    },
    "expected_output_patterns": {
        "type": list,
        "default": [],
    },
    "polarity": {
        "type": str,
        "enum": ["negative", "positive"],
        "default": "negative",
    },
    "required_concepts": {
        "type": list,
        "default": [],
    },
    "reasoning_must_contain": {
        "type": list,
        "default": [],
    },
    "reasoning_must_not_contain": {
        "type": list,
        "default": [],
    },
}


@dataclass
class ValidationResult:
    valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.valid = False

    def add_warning(self, msg: str):
        self.warnings.append(msg)


def validate_v4_fields(gt_item: dict, gt_id: str) -> list[str]:
    """Validate GT Schema v4 fields if present."""
    errors = []

    for field, spec in V4_FIELDS.items():
        if field not in gt_item:
            continue  # Optional field, skip

        value = gt_item[field]

        # Type check
        if not isinstance(value, spec["type"]):
            errors.append(
                f"{gt_id}: {field} must be {spec['type'].__name__}, "
                f"got {type(value).__name__}"
            )
            continue

        # Enum check
        if "enum" in spec and value not in spec["enum"]:
            errors.append(
                f"{gt_id}: {field} must be one of {spec['enum']}, got '{value}'"
            )

    return errors


def validate_gt(gt_path: str, contract_path: Optional[str] = None) -> ValidationResult:
    result = ValidationResult()
    
    # Load GT
    try:
        with open(gt_path) as f:
            gt = json.load(f)
    except json.JSONDecodeError as e:
        result.add_error(f"Invalid JSON: {e}")
        return result
    except FileNotFoundError:
        result.add_error(f"File not found: {gt_path}")
        return result

    # Required top-level keys
    for key in ['gt_metadata', 'ground_truth', 'tier_summary']:
        if key not in gt:
            result.add_error(f"Missing required key: {key}")

    if not result.valid:
        return result

    # Metadata validation
    meta = gt['gt_metadata']
    required_meta = ['contract_id', 'contract_type', 'parties', 'representing_party',
                     'gt_version', 'gt_author', 'gt_date']
    for key in required_meta:
        if key not in meta:
            result.add_error(f"Missing metadata field: {key}")

    # GT entry validation
    gt_ids = set()
    tier_counts = {'T1': 0, 'T2': 0, 'T3': 0}
    
    for i, entry in enumerate(gt['ground_truth']):
        prefix = f"GT entry {i+1}"
        
        # Required fields
        required = ['gt_id', 'clause', 'tier', 'issue', 'expected_classification', 'key_elements']
        for field in required:
            if field not in entry:
                result.add_error(f"{prefix}: Missing field '{field}'")
        
        if 'gt_id' in entry:
            # Duplicate check
            if entry['gt_id'] in gt_ids:
                result.add_error(f"{prefix}: Duplicate gt_id '{entry['gt_id']}'")
            gt_ids.add(entry['gt_id'])
            
            # Format check
            if not entry['gt_id'].startswith('GT-'):
                result.add_error(f"{prefix}: gt_id should be 'GT-XX' format")
        
        if 'tier' in entry:
            if entry['tier'] not in ['T1', 'T2', 'T3']:
                result.add_error(f"{prefix}: Invalid tier '{entry['tier']}'")
            else:
                tier_counts[entry['tier']] += 1
        
        if 'issue' in entry and len(entry['issue']) > 60:
            result.add_warning(f"{prefix}: Issue text exceeds 60 chars ({len(entry['issue'])})")
        
        if 'expected_classification' in entry:
            # Accept both symbol and text formats for backward compatibility
            valid_classes = [
                'UNFAVOURABLE', 'CLARIFY', 'FAVOURABLE',  # v3 text format
                'Unfavourable', 'Requires Clarification', 'Favourable',  # v3 verbose
                '❌', '⚠️', '✅',  # v4 symbol format
                'Unfavorable',  # US spelling variant
            ]
            if entry['expected_classification'] not in valid_classes:
                result.add_error(f"{prefix}: Invalid classification '{entry['expected_classification']}'")
        
        if 'key_elements' in entry:
            if not isinstance(entry['key_elements'], list):
                result.add_error(f"{prefix}: key_elements must be array")
            elif len(entry['key_elements']) < 2:
                result.add_warning(f"{prefix}: key_elements should have 2+ items")
        
        if 'contract_text' in entry and len(entry['contract_text']) < 10:
            result.add_warning(f"{prefix}: contract_text seems too short")

        # Validate v4 fields
        if 'gt_id' in entry:
            v4_errors = validate_v4_fields(entry, entry['gt_id'])
            for error in v4_errors:
                result.add_error(error)

    # Tier summary validation
    summary = gt['tier_summary']
    for tier in ['T1', 'T2', 'T3']:
        if tier not in summary:
            result.add_error(f"Missing tier_summary.{tier}")
            continue
        
        if summary[tier].get('count') != tier_counts[tier]:
            result.add_error(
                f"tier_summary.{tier}.count ({summary[tier].get('count')}) "
                f"doesn't match actual count ({tier_counts[tier]})"
            )
    
    # Weighted max calculation
    expected_weights = {'T1': 8, 'T2': 5, 'T3': 1}
    calculated_max = sum(tier_counts[t] * expected_weights[t] for t in tier_counts)
    
    if 'weighted_max' in summary:
        if summary['weighted_max'] != calculated_max:
            result.add_error(
                f"weighted_max ({summary['weighted_max']}) doesn't match "
                f"calculated value ({calculated_max})"
            )
    else:
        result.add_error("Missing tier_summary.weighted_max")

    # Contract text verification (if contract provided)
    if contract_path:
        result.add_warning("Contract text verification not implemented (requires python-docx)")

    return result


def main():
    parser = argparse.ArgumentParser(description='Validate Ground Truth JSON')
    parser.add_argument('gt_file', help='Path to GT JSON file')
    parser.add_argument('--contract', help='Path to contract .docx for text verification')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    result = validate_gt(args.gt_file, args.contract)

    if args.json:
        print(json.dumps({
            'valid': result.valid,
            'errors': result.errors,
            'warnings': result.warnings
        }, indent=2))
    else:
        if result.valid:
            print(f"✓ {args.gt_file} is valid")
        else:
            print(f"✗ {args.gt_file} has errors:")
            for err in result.errors:
                print(f"  ERROR: {err}")
        
        for warn in result.warnings:
            print(f"  WARNING: {warn}")

    sys.exit(0 if result.valid else 1)


if __name__ == '__main__':
    main()
