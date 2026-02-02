"""Classification normalisation for detection matching."""

from typing import Optional

# Canonical detection signal: did Leah identify an issue?
DETECTED_SIGNALS = {
    # Emoji variants
    "\u274c",  # Red X
    "\u26a0\ufe0f",  # Warning sign
    # Text variants
    "Unfavorable", "Unfavourable",
    "Requires Clarification", "Clarification Required",
    "High Risk", "Medium Risk",
}

NOT_DETECTED_SIGNALS = {
    # Emoji variants
    "\u2705",  # Check mark
    # Text variants
    "Favorable", "Favourable",
    "Standard", "Acceptable",
    "Low Risk", "Compliant",
}


def is_issue_detected(classification: Optional[str]) -> Optional[bool]:
    """
    Determine if a classification indicates issue detection.

    Returns True if Leah flagged this as problematic.
    Returns False if Leah marked as acceptable/compliant.
    Returns None if classification is ambiguous or missing.
    """
    if not classification:
        return None

    # Normalise: strip whitespace, handle emoji extraction
    clean = classification.strip()

    # Check against known sets
    if clean in DETECTED_SIGNALS:
        return True
    if clean in NOT_DETECTED_SIGNALS:
        return False

    # Substring matching for variants
    lower = clean.lower()
    if any(sig.lower() in lower for sig in DETECTED_SIGNALS if len(sig) > 2):
        return True
    if any(sig.lower() in lower for sig in NOT_DETECTED_SIGNALS if len(sig) > 2):
        return False

    # Unknown classification - log and return None
    return None


def normalise_classification(classification: Optional[str]) -> str:
    """
    Normalise classification to canonical form for display.

    Returns: "Unfavorable", "Clarification", "Favorable", or "Unknown"
    """
    detected = is_issue_detected(classification)
    if detected is True:
        if classification and ("\u26a0\ufe0f" in classification or "clarif" in classification.lower()):
            return "Clarification"
        return "Unfavorable"
    elif detected is False:
        return "Favorable"
    else:
        return "Unknown"
