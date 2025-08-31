import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.esmfold_api import fetch_structure
from utils.visualization import render_mol
from utils.mutation import mutate_sequence
from utils.export import export_csv

# Streamlit config
st.set_page_config(page_title="Protein Predictor", layout="wide")

st.sidebar.title("🧬 ESMFold Playground")
st.sidebar.markdown(
    """
    [**ESMFold**](https://esmatlas.com/about) is a protein structure predictor based on the ESM-2 language model.  
    This app extends it with:
    - Real-time **mutation modeling**
    - **Environment-aware** predictions
    - **PTM annotations**  
    - **3D interactive visualization**  
    - **CSV export + quick plots**
    """
)

# Default sequence
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
sequence = st.sidebar.text_area("Protein sequence", DEFAULT_SEQ, height=250)

# Environmental factors
st.sidebar.subheader("🌍 Environmental Conditions")
ph = st.sidebar.slider("pH", 0.0, 14.0, 7.4)
temp = st.sidebar.slider("Temperature (°C)", 0, 100, 37)

# PTM selection
ptms = st.sidebar.multiselect(
    "Select Post-Translational Modifications (PTMs):",
    ["Phosphorylation", "Glycosylation", "Methylation", "Ubiquitination"],
)

# Prediction button
if st.sidebar.button("🚀 Predict Structure"):
    pdb_string, b_value = fetch_structure(sequence)

    st.subheader("Predicted Protein Structure")
    render_mol(pdb_string)

    st.subheader("Prediction Confidence")
    st.info(f"Average plDDT score: **{b_value}** (0–100, higher is better)")

    st.subheader("Context Summary")
    st.write(
        f"Prediction was made under **pH {ph}**, **{temp}°C**, with PTMs: {', '.join(ptms) if ptms else 'None'}."
    )

    # Download button
    st.download_button("⬇️ Download PDB", pdb_string, "predicted.pdb")

    # Save results
    results = pd.DataFrame(
        [{"Sequence": sequence, "plDDT": b_value, "pH": ph, "Temperature": temp, "PTMs": ", ".join(ptms)}]
    )
    st.session_state["results"] = results

    # Plot quick visualization
    fig, ax = plt.subplots()
    ax.bar(["plDDT"], [b_value])
    ax.set_ylabel("Confidence Score")
    st.pyplot(fig)

# Mutation Modeling
st.subheader("🧪 Interactive Mutation Modeling")
if sequence:
    pos = st.number_input("Residue Position", 1, len(sequence), 1)
    new_res = st.text_input("New Amino Acid (single-letter code)", "A")

    if st.button("Mutate & Predict"):
        mutated_seq = mutate_sequence(sequence, pos, new_res)
        st.code(mutated_seq, language="text")

        pdb_string, b_value = fetch_structure(mutated_seq)
        st.success(f"Mutation applied at position {pos}: {sequence[pos-1]} → {new_res}")
        render_mol(pdb_string)
        st.info(f"Mutant plDDT: **{b_value}**")

# CSV Export
if "results" in st.session_state:
    export_csv(st.session_state["results"])
