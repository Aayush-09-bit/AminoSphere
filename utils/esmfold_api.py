import requests
import streamlit as st

@st.cache_data(show_spinner=False)
def query_esmfold(sequence: str):
    """
    Query ESMFold API with sequence and return (pdb, confidence_scores).
    Caches results for identical sequences.
    """
    url = "https://api.esmatlas.com/foldSequence/v1/pdb/"
    response = requests.post(url, data=sequence, headers={"Content-Type": "text/plain"})

    if response.status_code == 200:
        pdb = response.text
        # Dummy confidence: 0-100, one per residue
        confidences = [80 for _ in sequence]
        return pdb, confidences
    else:
        raise RuntimeError(f"ESMFold API Error: {response.status_code}")
