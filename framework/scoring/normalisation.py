"""Detection symbol normalisation to canonical set {Y, P, N, NMI}."""

from typing import Literal

CANONICAL_DETECTIONS = frozenset({"Y", "P", "N", "NMI"})

DETECTION_ALIASES = {
    # Identity mappings
    "Y": "Y", "P": "P", "N": "N", "NMI": "NMI",
    # Lowercase
    "y": "Y", "p": "P", "n": "N", "nmi": "NMI",
    # Verbose forms
    "YES": "Y", "PARTIAL": "P", "NO": "N", "NOT_MENTIONED": "NMI",
    # Legacy symbols (triangle variants sometimes used in older outputs)
    "triangle": "P", "TRIANGLE": "P",
}

def normalise_detection(value: str) -> str:
    """
    Normalise detection symbol to canonical form.

    Returns one of: Y, P, N, NMI
    Raises ValueError for unknown symbols.
    """
    if not isinstance(value, str):
        raise ValueError(f"Detection must be string, got {type(value).__name__}: {value!r}")

    normalised = DETECTION_ALIASES.get(value)
    if normalised is None:
        # Try uppercase lookup as fallback
        normalised = DETECTION_ALIASES.get(value.upper())

    if normalised is None:
        raise ValueError(
            f"Cannot normalise detection value: {value!r}. "
            f"Expected one of: {sorted(CANONICAL_DETECTIONS)}"
        )
    return normalised
