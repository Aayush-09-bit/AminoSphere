import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Streamlit page setup
# -------------------------
st.set_page_config(layout="wide", page_title="Protein Mutation Explorer")

st.sidebar.title("🎈 ESMFold Explorer")
mode = st.sidebar.radio(
    "Choose mode:",
    ["🔬 Predict Structure", "🧬 Mutation Scan", "🌱 Environment & PTMs"],
)

# -------------------------
# stmol renderer
# -------------------------
def render_mol(pdb, width=800, height=500):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb, "pdb")
    pdbview.setStyle({"cartoon": {"color": "spectrum"}})
    pdbview.setBackgroundColor("white")
    pdbview.zoomTo()
    pdbview.spin(True)
    showmol(pdbview, height=height, width=width)

# -------------------------
# ESMFold API call (cached)
# -------------------------
@st.cache_data(show_spinner=False)
def call_esmf(sequence: str) -> str:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://api.esmatlas.com/foldSequence/v1/pdb/",
        headers=headers,
        data=sequence,
    )
    return response.content.decode("utf-8")

def get_structure(sequence: str):
    pdb_string = call_esmf(sequence)
    with open("predicted.pdb", "w") as f:
        f.write(pdb_string)
    struct = bsio.load_structure("predicted.pdb", extra_fields=["b_factor"])
    return pdb_string, struct

# -------------------------
# Mode 1: Real structure prediction
# -------------------------
if mode == "🔬 Predict Structure":
    st.subheader("Predict 3D Protein Structure")
    DEFAULT_SEQ = (
        "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTA"
        "RQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGS"
    )
    seq = st.text_area("Input Sequence", DEFAULT_SEQ, height=200)
    if st.button("Predict Structure"):
        with st.spinner("Predicting with ESMFold..."):
            pdb_string, struct = get_structure(seq)

        st.success("Prediction complete ✅")
        st.subheader("3D Structure")
        render_mol(pdb_string)

        # Confidence (plDDT)
        b_value = round(struct.b_factor.mean(), 4)
        st.subheader("plDDT Confidence")
        st.info(f"Mean plDDT: {b_value}")

        # Plot distribution
        fig, ax = plt.subplots()
        ax.hist(struct.b_factor, bins=20, color="skyblue", edgecolor="black")
        ax.set_title("plDDT Score Distribution")
        ax.set_xlabel("plDDT")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        st.download_button(
            "Download PDB", pdb_string, file_name="predicted.pdb", mime="text/plain"
        )

# -------------------------
# Mode 2: Mutation scanning
# -------------------------
elif mode == "🧬 Mutation Scan":
    st.subheader("Mutation Mode")
    seq = st.text_area("Base Sequence", "", height=200)
    pos = st.number_input("Mutation Position (1-based)", min_value=1, step=1)
    new_res = st.text_input("New Residue (single letter)", "A")

    if st.button("Run Mutation"):
        if not seq:
            st.error("Please input a sequence first.")
        elif pos > len(seq):
            st.error("Position exceeds sequence length.")
        else:
            mutated_seq = seq[: pos - 1] + new_res + seq[pos:]
            st.info(f"Mutated Sequence: {mutated_seq}")

            with st.spinner("Predicting mutated structure..."):
                pdb_string, struct = get_structure(mutated_seq)

            render_mol(pdb_string)
            b_value = round(struct.b_factor.mean(), 4)
            st.write(f"Mean plDDT (mutant): {b_value}")

    # Batch scanning (example: all 20 residues at given position)
    st.subheader("Batch Mutation Scan (optional)")
    scan_pos = st.number_input("Scan Position", min_value=1, step=1)
    if st.button("Run Scan"):
        results = []
        for aa in "ACDEFGHIKLMNPQRSTVWY":
            mutated_seq = seq[: scan_pos - 1] + aa + seq[scan_pos:]
            pdb_string, struct = get_structure(mutated_seq)
            mean_conf = round(struct.b_factor.mean(), 4)
            results.append({"Residue": aa, "Mean_plDDT": mean_conf})

        df = pd.DataFrame(results)
        st.dataframe(df)

        # CSV Export
        st.download_button(
            "Download Scan Results (CSV)",
            df.to_csv(index=False).encode(),
            "mutation_scan.csv",
            "text/csv",
        )

        # Quick plot
        fig, ax = plt.subplots()
        ax.bar(df["Residue"], df["Mean_plDDT"], color="orchid")
        ax.set_title(f"Mutation Scan at position {scan_pos}")
        ax.set_ylabel("Mean plDDT")
        st.pyplot(fig)

# -------------------------
# Mode 3: Environment & PTMs
# -------------------------
elif mode == "🌱 Environment & PTMs":
    st.subheader("Environment & PTM Annotations")
    seq = st.text_area("Sequence", "", height=200)

    temp = st.slider("Temperature (°C)", 0, 100, 37)
    ph = st.slider("pH", 1, 14, 7)
    salt = st.slider("Salt concentration (mM)", 0, 500, 150)

    ptm_options = ["Phosphorylation", "Methylation", "Glycosylation", "Ubiquitination"]
    ptms = st.multiselect("Add PTMs", ptm_options)

    if st.button("Annotate Structure"):
        if not seq:
            st.error("Please enter a sequence.")
        else:
            pdb_string, struct = get_structure(seq)
            render_mol(pdb_string)

            b_value = round(struct.b_factor.mean(), 4)
            mod_conf = b_value
            # Example modifiers
            if temp > 50:
                mod_conf -= 5
            if ph < 5 or ph > 9:
                mod_conf -= 3
            if salt > 300:
                mod_conf -= 2
            mod_conf -= len(ptms) * 1.5

            st.write("Base Mean plDDT:", b_value)
            st.success(f"Modified Confidence Score: {mod_conf:.2f}")

            st.write("Annotations:")
            st.write(f"Temperature = {temp} °C, pH = {ph}, Salt = {salt} mM")
            st.write(f"PTMs applied: {', '.join(ptms) if ptms else 'None'}")
