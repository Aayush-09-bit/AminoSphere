import requests

def fold_protein(sequence: str) -> str:
    """Send protein sequence to ESMFold API and return PDB string."""
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            "https://api.esmatlas.com/foldSequence/v1/pdb/",
            headers=headers,
            data=sequence,
            timeout=60
        )
        if response.status_code == 200:
            return response.content.decode("utf-8")
        return None
    except Exception as e:
        print("Error in fold_protein:", e)
        return None
