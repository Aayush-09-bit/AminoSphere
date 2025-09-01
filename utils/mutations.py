def mutate_sequence(sequence: str, position: int, new_residue: str) -> str:
    """
    Return sequence with a residue mutation at given 1-indexed position.
    """
    if position < 1 or position > len(sequence):
        raise ValueError("Position out of range.")
    return sequence[: position - 1] + new_residue + sequence[position:]
