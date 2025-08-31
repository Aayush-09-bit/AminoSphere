import streamlit as st
from utils.esm_api import fold_protein
from utils.visualization import render_structure
from utils.analysis import compute_plddt

# Sidebar
st.sidebar.title("🎈 ESMFold")
st.sidebar.write(
    "[*ESMFold*](https://esmatlas.com/about) is an end-to-end single-sequence "
    "protein structure predictor based on the ESM-2 language model. "
    "Read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) "
    "and [Nature news](https://www.nature.com/articles/d41586-022-03539-1)."
)

# Default sequence
DEFAULT_SEQ = (
    "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLA"
    "SHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNF"
    "SSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTR"
    "VSDFRTANCSLEDPAANKARKEAELAAATAEQ"
)

# UI Input
txt = st.sidebar.text_area("✍️ Input Protein Sequence", DEFAULT_SEQ, height=250)

# Prediction
if st.sidebar.button("🚀 Predict Structure"):
    with st.spinner("Folding protein... this may take a few seconds ⏳"):
        pdb_string = fold_protein(txt)

    if pdb_string:
        st.success("✅ Prediction complete!")

        # Show structure
        st.subheader("🧬 Predicted Protein Structure")
        render_structure(pdb_string)

        # Show confidence (plDDT)
        st.subheader("📊 plDDT Confidence Score")
        b_value = compute_plddt(pdb_string)
        st.info(f"Average plDDT: **{b_value}** (0–100 scale)")

        # Download option
        st.download_button(
            label="💾 Download Predicted Structure (PDB)",
            data=pdb_string,
            file_name="predicted.pdb",
            mime="text/plain",
        )
    else:
        st.error("❌ Failed to fetch prediction. Try again later.")
else:
    st.warning("👈 Enter a protein sequence and click **Predict Structure**.")
