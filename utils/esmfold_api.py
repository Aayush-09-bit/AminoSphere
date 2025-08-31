import requests
import numpy as np
from biotite.structure.io import load_structure
import tempfile
import os
import streamlit as st
from typing import Tuple

ESMFOLD_API = "https://api.esmatlas.com/foldSequence/v1/pdb/"

@st.cache_data(show_spinner=True, persist="disk")
def predict_structure(sequence: str, timeout: int = 180) -> Tuple[str, float, list]:
    """
    Send sequence to ESMFold API and return:
      - pdb_string
      - mean_plddt (float)
      - per-residue plDDT list (list of floats)
    The result is cached using streamlit's cache_data keyed on `sequence`.
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(ESMFOLD_API, headers=headers, data=sequence, timeout=timeout)
    resp.raise_for_status()
    pdb_str = resp.content.decode("utf-8")

    # Write to a temp file to parse b-factors (plDDT stored in B-factor)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdb") as f:
        tmp_path = f.name
        f.write(pdb_str.encode("utf-8"))

    try:
        struct = load_structure(tmp_path, extra_fields=["b_factor"])
        # If multiple models/chains, this extracts B-factors in order; we take mean per-residue
        bvals = struct.b_factor
        # In biotite structure arrays, b_factor may be per-atom. We'll compute per-residue mean by grouping by residue index.
        # If it's already per-residue, this still works.
        res_indices = struct.res_id  # may contain residue numbers
        # compute per-residue mean b-factor by unique residue ordering
        per_res_plddt = []
        # res_id may be multi-value, so fallback to simple atom grouping by (chain, res_id)
        uniq = []
        for atom in struct:
            key = (atom.chain_id, atom.res_id, atom.res_name)
            uniq.append(key)
        # Build mapping of residue -> list of b-factors
        res_map = {}
        for atom in struct:
            key = (atom.chain_id, atom.res_id)
            res_map.setdefault(key, []).append(float(atom.b_factor))
        # Flatten in order of appearance
        seen = set()
        for atom in struct:
            key = (atom.chain_id, atom.res_id)
            if key not in seen:
                seen.add(key)
                vals = res_map.get(key, [])
                per_res_plddt.append(float(np.mean(vals)) if vals else 0.0)
        mean_plddt = float(np.mean(per_res_plddt)) if per_res_plddt else 0.0
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    return pdb_str, mean_plddt, per_res_plddt
