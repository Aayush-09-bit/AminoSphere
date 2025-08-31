import re
from typing import Tuple, List

AA_LIST = ["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y"]

def clean_sequence(seq: str) -> str:
    s = seq.strip().upper().replace("\n", "").replace(" ", "")
    if not re.fullmatch(r"[ACDEFGHIKLMNPQRSTVWY]+", s):
        raise ValueError("Sequence contains invalid characters. Only standard 20 amino acids allowed.")
    return s

def mutate_sequence_simple(seq: str, pos_1based: int, new_aa: str) -> str:
    seq = clean_sequence(seq)
    if new_aa not in AA_LIST:
        raise ValueError("Invalid amino acid.")
    if pos_1based < 1 or pos_1based > len(seq):
        raise ValueError("Position out of range.")
    if seq[pos_1based-1] == new_aa:
        return seq
    return seq[:pos_1based-1] + new_aa + seq[pos_1based:]

def mutate_from_notation(seq: str, notation: str) -> str:
    """
    notation example: A25K (wildtype A at pos 25 -> mutate to K)
    """
    seq = clean_sequence(seq)
    m = re.match(r"^([A-Z])(\d+)([A-Z])$", notation.strip().upper())
    if not m:
        raise ValueError("Mutation must be in format A25K.")
    wt, pos_str, mut = m.groups()
    pos = int(pos_str)
    if seq[pos-1] != wt:
        raise ValueError(f"Sequence mismatch: expected {wt} at position {pos}, found {seq[pos-1]}")
    return seq[:pos-1] + mut + seq[pos:]
