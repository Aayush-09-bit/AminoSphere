import py3Dmol
from stmol import showmol
import streamlit as st

def render_structure(pdb: str):
    """Render 3D protein structure in Streamlit."""
    try:
        pdbview = py3Dmol.view(width=800, height=500)
        pdbview.addModel(pdb, "pdb")
        pdbview.setStyle({"cartoon": {"color": "spectrum"}})
        pdbview.setBackgroundColor("white")
        pdbview.zoomTo()
        pdbview.zoom(2, 800)
        pdbview.spin(True)
        showmol(pdbview, height=500, width=800)
    except Exception as e:
        st.error(f"❌ Visualization error: {e}")
