import biotite.structure.io as bsio

def compute_plddt(pdb_string: str) -> float:
    """Extract average plDDT (stored in B-factor field) from PDB string."""
    try:
        with open("temp_predicted.pdb", "w") as f:
            f.write(pdb_string)

        struct = bsio.load_structure("temp_predicted.pdb", extra_fields=["b_factor"])
        return round(struct.b_factor.mean(), 2)
    except Exception as e:
        print("Error in compute_plddt:", e)
        return -1.0
