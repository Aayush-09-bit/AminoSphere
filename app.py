import streamlit as st
import pandas as pd
import py3Dmol

from utils.esmfold_api import query_esmfold
from utils.mutations import mutate_sequence
from utils.environment import adjust_confidence
from utils.plotting import plot_confidence, save_results_csv


# Page config
st.set_page_config(page_title="Protein Prediction App", layout="wide")
st.title("🧬 Protein Structure Prediction (ESMFold + Context)")

# Sidebar: choose mode
mode = st.sidebar.radio(
    "Choose Mode:",
    ["Normal Prediction", "Mutate Sequence", "Context-Aware Prediction"],
)

# Sidebar: environment sliders
pH = st.sidebar.slider("pH", 0.0, 14.0, 7.4, 0.1)
temp = st.sidebar.slider("Temperature (°C)", 0.0, 100.0, 37.0, 1.0)
ptm_phospho = st.sidebar.checkbox("Phosphorylation")
ptm_glyco = st.sidebar.checkbox("Glycosylation")

# Sequence input (unlimited length allowed)
default_seq = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
sequence = st.text_area("Enter protein sequence:", default_seq, height=200)

if st.button("Predict Structure"):
    if sequence.strip():
        with st.spinner("Fetching prediction from ESMFold..."):
            pdb, confidences = query_esmfold(sequence)

        # Adjust confidence based on environment
        confidences = adjust_confidence(confidences, pH, temp, ptm_phospho, ptm_glyco)

        # 3D Viewer (always show)
        st.subheader("3D Predicted Structure")
        view = py3Dmol.view(width=800, height=600)
        view.addModel(pdb, "pdb")
        view.setStyle({"cartoon": {"color": "spectrum"}})
        view.zoomTo()
        view.spin(True)
        view.show()
        st.components.v1.html(view._make_html(), height=600)

        # Plot confidence
        st.subheader("Confidence Score Distribution")
        st.pyplot(plot_confidence(confidences))

        # Export CSV option
        if st.button("Export Results to CSV"):
            path = save_results_csv(sequence, confidences)
            st.success(f"Results saved to {path}")

    else:
        st.error("Please enter a protein sequence first.")

# Mutation mode
if mode == "Mutate Sequence" and sequence.strip():
    st.subheader("🔬 Mutation Mode")
    pos = st.number_input("Residue position (1-indexed):", min_value=1, step=1)
    new_residue = st.text_input("New residue (single-letter):", max_chars=1)
    if st.button("Apply Mutation"):
        mutated_seq = mutate_sequence(sequence, pos, new_residue)
        st.info(f"Mutated Sequence: {mutated_seq}")
        with st.spinner("Fetching mutated prediction..."):
            pdb, confidences = query_esmfold(mutated_seq)
        st.subheader("Mutated Structure (3D)")
        view = py3Dmol.view(width=800, height=600)
        view.addModel(pdb, "pdb")
        view.setStyle({"cartoon": {"color": "spectrum"}})
        view.zoomTo()
        view.show()
        st.components.v1.html(view._make_html(), height=600)
