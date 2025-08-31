import py3Dmol
from stmol import showmol

def render_mol(pdb_string: str, width: int = 800, height: int = 500):
    """Render 3D protein structure using py3Dmol + stmol."""
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb_string, "pdb")
    pdbview.setStyle({"cartoon": {"color": "spectrum"}})
    pdbview.setBackgroundColor("white")
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height=height, width=width)
