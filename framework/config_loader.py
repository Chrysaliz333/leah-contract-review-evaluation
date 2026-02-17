"""
Configuration loading and validation for evaluation modes.

This module provides utilities to load and validate evaluation mode configuration
files against the JSON schema, with clear error messages for debugging.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any
import warnings


class ConfigValidationError(Exception):
    """Raised when a configuration file fails validation."""

    def __init__(self, config_path: Path, errors: list):
        self.config_path = config_path
        self.errors = errors
        message = self._format_errors()
        super().__init__(message)

    def _format_errors(self) -> str:
        """Format validation errors with clear field paths."""
        lines = [f"Configuration validation failed for: {self.config_path}"]
        lines.append("")
        for i, error in enumerate(self.errors, 1):
            lines.append(f"Error {i}:")
            if hasattr(error, 'json_path'):
                lines.append(f"  Location: {error.json_path}")
            elif hasattr(error, 'path'):
                path = " → ".join(str(p) for p in error.path)
                if path:
                    lines.append(f"  Field: {path}")
            lines.append(f"  Message: {error.message}")
            if hasattr(error, 'validator') and error.validator == 'enum':
                if hasattr(error, 'validator_value'):
                    allowed = ", ".join(str(v) for v in error.validator_value)
                    lines.append(f"  Allowed values: {allowed}")
            lines.append("")
        return "\n".join(lines)


def load_mode_config(
    config_path: Path,
    schema_path: Optional[Path] = None,
    validate: bool = True
) -> Dict[str, Any]:
    """
    Load and validate an evaluation mode configuration file.

    Args:
        config_path: Path to the configuration JSON file
        schema_path: Optional path to the JSON schema file. If None, uses default.
        validate: Whether to validate against schema (default True)

    Returns:
        Dictionary containing the configuration

    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file contains invalid JSON
        ConfigValidationError: If config fails schema validation
    """
    config_path = Path(config_path)

    # Load the configuration file
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in {config_path} at line {e.lineno}, column {e.colno}: {e.msg}",
            e.doc,
            e.pos
        )

    # Validate against schema if requested
    if validate:
        if schema_path is None:
            # Default schema location
            schema_path = Path(__file__).parent / "schemas" / "mode_config_schema.json"

        if not schema_path.exists():
            warnings.warn(
                f"Schema file not found at {schema_path}. "
                "Skipping validation (config loaded successfully).",
                UserWarning
            )
            return config

        # Import jsonschema only if validation is requested
        try:
            import jsonschema
            from jsonschema import Draft7Validator
        except ImportError:
            warnings.warn(
                "jsonschema package not installed. "
                "Run 'pip install jsonschema>=4.17.0' to enable validation. "
                "Config loaded without validation.",
                UserWarning
            )
            return config

        # Load and compile schema
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        # Validate
        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(config))

        if errors:
            raise ConfigValidationError(config_path, errors)

    return config


def validate_all_configs(
    config_dir: Path,
    schema_path: Optional[Path] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Load and validate all configuration files in a directory.

    Args:
        config_dir: Directory containing configuration JSON files
        schema_path: Optional path to the JSON schema file

    Returns:
        Dictionary mapping config names to their loaded configurations

    Raises:
        ConfigValidationError: If any config fails validation (with details of all failures)
    """
    config_dir = Path(config_dir)

    if not config_dir.exists():
        raise FileNotFoundError(f"Configuration directory not found: {config_dir}")

    configs = {}
    errors = []

    # Load all JSON files
    for config_file in sorted(config_dir.glob("*.json")):
        try:
            config = load_mode_config(config_file, schema_path=schema_path, validate=True)
            configs[config_file.stem] = config
        except (json.JSONDecodeError, ConfigValidationError) as e:
            errors.append((config_file, e))

    if errors:
        # Collect all error messages
        error_lines = ["Multiple configuration validation failures:"]
        error_lines.append("")
        for config_file, error in errors:
            error_lines.append(f"{'='*60}")
            error_lines.append(str(error))
            error_lines.append("")

        # Raise a general exception since we have multiple config errors
        raise Exception("\n".join(error_lines))

    return configs
