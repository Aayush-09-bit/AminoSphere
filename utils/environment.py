from typing import List, Dict

def ptm_targets(seq: str, ptms: List[str]) -> Dict[str, list]:
    """
    Return 1-based positions for PTM annotations:
      - Phosphorylation: S, T, Y
      - Glycosylation: N-X-S/T motif (X != P) -> highlight N
      - Methylation: K, R
    """
    s = seq.upper()
    out = {}
    if "Phosphorylation" in ptms:
        out["Phosphorylation"] = [i+1 for i,aa in enumerate(s) if aa in ("S","T","Y")]
    if "Glycosylation" in ptms:
        gly = []
        for i in range(len(s)-2):
            if s[i]=="N" and s[i+1]!="P" and s[i+2] in ("S","T"):
                gly.append(i+1)
        out["Glycosylation"] = gly
    if "Methylation" in ptms:
        out["Methylation"] = [i+1 for i,aa in enumerate(s) if aa in ("K","R")]
    return out

def adjust_plddt(mean_plddt: float, ph: int, temp_c: int, ptms: List[str]) -> (float, list):
    """
    Heuristic adjustments returning (adjusted_mean_plddt, notes list).
    Not a physical simulation — only a UI heuristic.
    """
    notes = []
    adj = mean_plddt
    # pH extremes
    if ph < 4 or ph > 10:
        notes.append("Extreme pH ( <4 or >10 ): −10%")
        adj *= 0.90
    # temperature
    if temp_c >= 60:
        notes.append("High temperature (≥60°C): −15%")
        adj *= 0.85
    elif temp_c <= 4:
        notes.append("Low temperature (≤4°C): −5%")
        adj *= 0.95
    # PTMs
    if ptms:
        notes.append("PTMs selected: −3% (uncertainty)")
        adj *= 0.97
    # clamp
    adj = max(0.0, min(100.0, adj))
    return adj, notes
