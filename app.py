import streamlit as st
from utils import render_mol, fetch_structure, calculate_plddt, save_results_csv, plot_plddt_distribution

# Sidebar Title & Description
st.sidebar.title("🧬 ESMFold Protein Predictor")
st.sidebar.write(
    "[*ESMFold*](https://esmatlas.com/about) is an end-to-end single sequence "
    "protein structure predictor based on the ESM-2 language model."
)
st.sidebar.write(
    "🔗 [Research Article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) "
    "| [Nature News](https://www.nature.com/articles/d41586-022-03539-1)"
)

# Default protein sequence
DEFAULT_SEQ = (
    "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTA"
    "RQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGG"
    "SLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCAN"
    "SGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
)

# User input
txt = st.sidebar.text_area("✍️ Input Protein Sequence", DEFAULT_SEQ, height=250)

# Run prediction
if st.sidebar.button("🚀 Predict"):
    with st.spinner("⏳ Predicting structure... please wait"):
        pdb_string, struct = fetch_structure(txt)

    # Save results
    save_results_csv(struct)

    # Visualization
    st.subheader("🔬 3D Visualization of Predicted Protein Structure")
    render_mol(pdb_string)

    # Confidence score
    b_value = calculate_plddt(struct)
    st.subheader("📊 plDDT Confidence Score")
    st.info(f"plDDT (mean confidence): **{b_value}** / 100")

    # Confidence distribution plot
    st.pyplot(plot_plddt_distribution(struct))

    # Download button
    st.download_button(
        label="💾 Download Predicted PDB",
        data=pdb_string,
        file_name="predicted.pdb",
        mime="text/plain",
    )
else:
    st.warning("👈 Enter a protein sequence and click *Predict*")
