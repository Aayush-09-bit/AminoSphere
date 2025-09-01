def adjust_confidence(confidences, pH, temp, phospho, glyco):
    """
    Adjusts confidence values heuristically based on environment.
    """
    adjusted = confidences.copy()
    for i in range(len(adjusted)):
        if pH < 5 or pH > 9:
            adjusted[i] -= 5
        if temp > 60:
            adjusted[i] -= 10
        if phospho:
            adjusted[i] -= 3
        if glyco:
            adjusted[i] -= 2
        adjusted[i] = max(0, adjusted[i])  # keep non-negative
    return adjusted
