import streamlit as st
import pandas as pd
from utils import (
    call_esmfold_api,
    show_3d_structure,
    summarize_structure,
    plot_plddt,
)

# ---- Streamlit Config ----
st.set_page_config(
    page_title="Protein Structure Explorer",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Protein Structure Explorer")
st.write("Predict, visualize, and understand protein structures with AI-powered tools.")

# ---- Sequence Input ----
sequence = st.text_area(
    "Enter protein sequence (A, C, D, E, ... single-letter amino acid codes)",
    height=150,
    placeholder="Paste or type your protein sequence here..."
)

if sequence:
    if len(sequence) < 20:
        st.warning("⚠️ Protein sequences shorter than 20 amino acids may not fold into stable structures.")

# ---- Prediction Mode ----
mode = st.radio(
    "Choose prediction mode",
    ["Normal Prediction", "Mutation Mode", "Context-Aware Prediction"]
)

# ---- Context Options ----
if mode == "Context-Aware Prediction":
    st.subheader("Environmental Context")
    ph = st.slider("pH Level", 1.0, 14.0, 7.4, step=0.1)
    temp = st.slider("Temperature (°C)", 0, 100, 37)

    st.subheader("Post-Translational Modifications (PTMs)")
    ptms = []
    if st.checkbox("Phosphorylation (switches activity on/off)"):
        ptms.append("Phosphorylation")
    if st.checkbox("Glycosylation (adds stability, helps recognition)"):
        ptms.append("Glycosylation")
    if st.checkbox("Acetylation (controls interactions & stability)"):
        ptms.append("Acetylation")
else:
    ph, temp, ptms = None, None, []

# ---- Run Prediction ----
if st.button("🔮 Predict Structure") and sequence:
    with st.spinner("Predicting structure..."):
        pdb_str, plddt_scores = call_esmfold_api(sequence)

    # ---- Show 3D Viewer ----
    st.subheader("Interactive 3D Structure")
    show_3d_structure(pdb_str)

    # ---- Plot Confidence ----
    st.subheader("Prediction Confidence Across Sequence")
    plot_plddt(plddt_scores)

    # ---- Plain-English Summary ----
    st.subheader("Summary")
    st.write(summarize_structure(plddt_scores))

    # ---- CSV Export ----
    df = pd.DataFrame({
        "Residue Position": list(range(1, len(plddt_scores) + 1)),
        "Confidence (pLDDT)": plddt_scores
    })

    st.download_button(
        label="📥 Download confidence scores (CSV)",
        data=df.to_csv(index=False),
        file_name="confidence_scores.csv",
        mime="text/csv"
    )
