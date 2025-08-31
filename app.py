import streamlit as st
from utils.esmfold_api import predict_structure
from utils.mutations import clean_sequence, mutate_sequence_simple, mutate_from_notation, AA_LIST
from utils.environment import ptm_targets, adjust_plddt
from utils.plotting import plot_per_residue
import pandas as pd
import os
import time
from typing import List

st.set_page_config(page_title="ESMFold+", layout="wide", page_icon="🧬")
st.title("ESMFold+ — Real predictions, mutations & context-aware annotations")

# Sidebar inputs
st.sidebar.header("Inputs")
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
seq_input = st.sidebar.text_area("Protein sequence (20 AAs only)", DEFAULT_SEQ, height=220)

mode = st.sidebar.radio("Mode", ["Normal Prediction", "Mutate Sequence", "Mutational Scan", "Context-Aware Prediction"])

# Context controls (visible always)
st.sidebar.markdown("### Context (for Context-Aware mode)")
ph = st.sidebar.slider("pH", 0, 14, 7)
temp_c = st.sidebar.slider("Temperature (°C)", 0, 100, 37)
ptm_choices = st.sidebar.multiselect("PTMs to annotate", ["Phosphorylation", "Glycosylation", "Methylation"])

# Mutate UI
if mode == "Mutate Sequence":
    st.sidebar.markdown("### Mutation")
    mut_pos = st.sidebar.number_input("Residue position (1-based)", min_value=1, max_value=1000, value=1, step=1)
    mut_aa = st.sidebar.selectbox("Mutate to", AA_LIST, index=0)

# Scan UI
if mode == "Mutational Scan":
    st.sidebar.markdown("### Mutational scan options")
    scan_pos = st.sidebar.number_input("Residue position to scan (1-based)", min_value=1, max_value=1000, value=1, step=1)
    run_scan_button = st.sidebar.button("Run mutational scan")

run_button = st.sidebar.button("Predict")

# ensure data dir
os.makedirs("data/results", exist_ok=True)

def save_csv(df: pd.DataFrame, prefix: str):
    ts = time.strftime("%Y%m%d_%H%M%S")
    fname = f"data/results/{prefix}_{ts}.csv"
    df.to_csv(fname, index=False)
    return fname

if not (run_button or (mode=="Mutational Scan" and run_scan_button)):
    st.info("Select inputs and click Predict (or Run mutational scan).")
    st.stop()

# validate sequence
try:
    seq = clean_sequence(seq_input)
except Exception as e:
    st.error(f"Sequence validation error: {e}")
    st.stop()

# === NORMAL PREDICTION ===
if mode == "Normal Prediction" and run_button:
    with st.spinner("Calling ESMFold API..."):
        pdb_str, mean_plddt, per_res_plddt = predict_structure(seq)
    st.subheader("Predicted structure")
    # render with py3Dmol + stmol if available
    try:
        from stmol import showmol
        import py3Dmol
        view = py3Dmol.view()
        view.addModel(pdb_str, "pdb")
        view.setStyle({"cartoon":{"color":"spectrum"}})
        view.setBackgroundColor("white")
        view.zoomTo()
        view.zoom(2, 300)
        view.spin(True)
        showmol(view, height=520, width=700)
    except Exception:
        st.text("3D viewer unavailable in this environment. PDB shown as text below.")
        st.code(pdb_str[:2000] + ("\n... (truncated)" if len(pdb_str)>2000 else ""))

    st.sidebar.success(f"Mean plDDT: {mean_plddt:.2f}")
    fig = plot_per_residue(per_res_plddt, title="Per-residue plDDT (Normal prediction)")
    st.pyplot(fig)

    # downloads
    st.download_button("Download PDB", data=pdb_str, file_name="prediction.pdb", mime="text/plain")
    df = pd.DataFrame({"residue": list(range(1, len(per_res_plddt)+1)), "plddt": per_res_plddt})
    st.download_button("Download per-residue CSV", data=df.to_csv(index=False), file_name="per_residue.csv", mime="text/csv")
    saved = save_csv(df, "normal_prediction")
    st.caption(f"Saved CSV to `{saved}` on server.")

# === MUTATE SEQUENCE ===
elif mode == "Mutate Sequence" and run_button:
    # single mutation re-prediction
    try:
        mut_seq = mutate_sequence_simple(seq, int(mut_pos), mut_aa)
    except Exception as e:
        st.error(f"Mutation error: {e}")
        st.stop()

    with st.spinner("Folding original and mutated sequences..."):
        pdb_orig, plddt_orig_mean, plddt_orig_per = predict_structure(seq)
        pdb_mut, plddt_mut_mean, plddt_mut_per = predict_structure(mut_seq)

    st.subheader("Comparison: Original vs Mutant")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Original**")
        try:
            from stmol import showmol
            import py3Dmol
            v1 = py3Dmol.view()
            v1.addModel(pdb_orig, "pdb")
            v1.setStyle({"cartoon":{"color":"spectrum"}})
            v1.setBackgroundColor("white")
            v1.zoomTo(); v1.zoom(2,200); v1.spin(True)
            showmol(v1, height=420, width=520)
        except Exception:
            st.text("3D viewer unavailable.")
        st.write(f"Mean plDDT: {plddt_orig_mean:.2f}")
    with c2:
        st.markdown(f"**Mutant (pos {mut_pos} → {mut_aa})**")
        try:
            v2 = py3Dmol.view()
            v2.addModel(pdb_mut, "pdb")
            v2.setStyle({"cartoon":{"color":"spectrum"}})
            v2.setBackgroundColor("white")
            v2.zoomTo(); v2.zoom(2,200); v2.spin(True)
            showmol(v2, height=420, width=520)
        except Exception:
            st.text("3D viewer unavailable.")
        st.write(f"Mean plDDT: {plddt_mut_mean:.2f}")

    # delta table + CSV
    # align lengths: some predictions may differ by insertions/deletions; we truncate to min len
    minlen = min(len(plddt_orig_per), len(plddt_mut_per))
    df = pd.DataFrame({
        "residue": list(range(1, minlen+1)),
        "plddt_orig": plddt_orig_per[:minlen],
        "plddt_mut": plddt_mut_per[:minlen],
    })
    df["delta"] = df["plddt_mut"] - df["plddt_orig"]
    st.subheader("Per-residue delta (mut - orig)")
    st.dataframe(df.head(50))

    st.download_button("Download comparison CSV", data=df.to_csv(index=False), file_name=f"mutation_compare_{mut_pos}_{mut_aa}.csv", mime="text/csv")
    saved = save_csv(df, f"mut_compare_{mut_pos}_{mut_aa}")
    st.caption(f"Saved CSV to `{saved}`")

    # plot delta
    fig = plot_per_residue(df["delta"].tolist(), title="plDDT delta (mutant - original)")
    st.pyplot(fig)

# === MUTATIONAL SCAN ===
elif mode == "Mutational Scan" and run_scan_button:
    pos = int(scan_pos)
    if pos < 1 or pos > len(seq):
        st.error("Scan position out of range.")
        st.stop()

    st.info(f"Running single-point mutational scan at position {pos} (this will call the API ~19 times, cached results may speed it up).")
    results = []
    wt = seq[pos-1]
    for aa in AA_LIST:
        if aa == wt:
            continue
        mutated = mutate_sequence_simple(seq, pos, aa)
        with st.spinner(f"Folding {aa} at pos {pos} ..."):
            pdb_m, mean_m, per_m = predict_structure(mutated)
        # store global mean and also plDDT at mutation site if possible
        site_plddt = None
        if len(per_m) >= pos:
            site_plddt = per_m[pos-1]
        results.append({"mutant": f"{wt}{pos}{aa}", "mean_plddt": mean_m, "site_plddt": site_plddt})

    df = pd.DataFrame(results).sort_values(by="mean_plddt", ascending=False)
    st.subheader("Mutational scan results")
    st.dataframe(df)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download scan CSV", data=csv_bytes, file_name=f"mutational_scan_pos{pos}.csv", mime="text/csv")
    saved = save_csv(df, f"mut_scan_pos{pos}")
    st.caption(f"Saved CSV to `{saved}`")

    # quick plot: mean_plddt vs mutant
    fig = plot_per_residue(df["mean_plddt"].tolist(), title=f"Mutational scan (pos {pos}) — mean plDDT per mutant")
    st.pyplot(fig)

# === CONTEXT-AWARE PREDICTION ===
elif mode == "Context-Aware Prediction" and run_button:
    with st.spinner("Folding sequence..."):
        pdb_str, mean_plddt, per_res_plddt = predict_structure(seq)

    adj_mean, notes = adjust_plddt(mean_plddt, ph, temp_c, ptm_choices)
    targets = ptm_targets(seq, ptm_choices)
    all_highlight_positions = sorted({p for lst in targets.values() for p in lst})

    st.subheader("Predicted structure")
    try:
        from stmol import showmol
        import py3Dmol
        v = py3Dmol.view()
        v.addModel(pdb_str, "pdb")
        v.setStyle({"cartoon":{"color":"spectrum"}})
        v.setBackgroundColor("white")
        v.zoomTo(); v.zoom(2,200); v.spin(True)
        # highlight residues as sticks
        for p in all_highlight_positions:
            v.setStyle({"resi": int(p)}, {"stick":{}})
        showmol(v, height=520, width=700)
    except Exception:
        st.text("3D viewer unavailable.")

    st.markdown(f"**Mean plDDT:** {mean_plddt:.2f}")
    st.markdown(f"**Context-adjusted plDDT:** {adj_mean:.2f}")
    if notes:
        for n in notes:
            st.caption(f"• {n}")

    st.subheader("Annotated PTM candidate sites")
    if targets:
        for k, v in targets.items():
            st.write(f"**{k}**: {len(v)} sites — example positions: {v[:10] if v else '—'}")
    else:
        st.write("No PTMs selected.")

    # downloads
    df = pd.DataFrame({"residue": list(range(1, len(per_res_plddt)+1)), "plddt": per_res_plddt})
    st.download_button("Download per-residue CSV", data=df.to_csv(index=False), file_name="context_per_residue.csv", mime="text/csv")
    saved = save_csv(df, "context_prediction")
    st.caption(f"Saved CSV to `{saved}`")

else:
    st.warning("No action taken. Please press Predict or Run mutational scan.")
