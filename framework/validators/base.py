"""Core validation types for pipeline gates."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Severity(Enum):
    """Validation issue severity level."""
    ERROR = "ERROR"      # Must abort processing
    WARNING = "WARNING"  # Can proceed with caution


@dataclass
class ValidationIssue:
    """A single validation issue (error or warning)."""
    severity: Severity
    message: str
    location: str  # e.g., "run1/consulting/pathfinder.json"
    context: dict = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Structured validation result with errors and warnings separated."""
    valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        """Return only ERROR-severity issues."""
        return [i for i in self.issues if i.severity == Severity.ERROR]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Return only WARNING-severity issues."""
        return [i for i in self.issues if i.severity == Severity.WARNING]

    def abort_if_errors(self, stage: str) -> None:
        """Raise ValidationError if any ERROR-severity issues exist.

        Args:
            stage: Name of pipeline stage being validated

        Raises:
            ValidationError: If any errors present, with formatted error list
        """
        if self.errors:
            error_list = "\n".join(f"  - {e.message} (at {e.location})" for e in self.errors)
            raise ValidationError(
                f"Validation failed at {stage} stage:\n{error_list}\n"
                f"Fix errors before proceeding."
            )


class ValidationError(Exception):
    """Raised when validation gate blocks processing."""
    pass
