import py3Dmol
from stmol import showmol
import streamlit as st

def render_mol(pdb: str):
    view = py3Dmol.view()
    view.addModel(pdb, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})
    view.setBackgroundColor("white")
    view.zoomTo()
    showmol(view, height=500, width=800)
