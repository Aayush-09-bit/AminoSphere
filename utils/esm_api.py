import requests
import biotite.structure.io as bsio

def fetch_structure(sequence: str):
    """Fetch predicted protein structure from ESMFold API."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://api.esmatlas.com/foldSequence/v1/pdb/",
        headers=headers,
        data=sequence,
    )

    if response.status_code != 200:
        raise ValueError("Failed to fetch prediction from ESMFold API")

    pdb_string = response.content.decode("utf-8")

    with open("predicted.pdb", "w") as f:
        f.write(pdb_string)

    struct = bsio.load_structure("predicted.pdb", extra_fields=["b_factor"])
    return pdb_string, struct
