"""F1 score calculation."""

def calculate_f1(recall: float, precision: float) -> float:
    """
    Calculate F1 score from recall and precision.

    F1 = 2 * (precision * recall) / (precision + recall)

    Returns 0.0 if both precision and recall are 0.
    """
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)
