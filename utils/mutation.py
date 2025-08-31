def mutate_sequence(sequence: str, position: int, new_res: str) -> str:
    if position < 1 or position > len(sequence):
        raise ValueError("Position out of range")
    return sequence[:position - 1] + new_res + sequence[position:]
