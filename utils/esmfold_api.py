import requests
import biotite.structure.io as bsio
import streamlit as st

@st.cache_data
def fetch_structure(sequence: str):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post("https://api.esmatlas.com/foldSequence/v1/pdb/", headers=headers, data=sequence)
    pdb_string = response.content.decode("utf-8")

    with open("predicted.pdb", "w") as f:
        f.write(pdb_string)

    struct = bsio.load_structure("predicted.pdb", extra_fields=["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)
    return pdb_string, b_value
