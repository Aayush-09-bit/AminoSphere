import matplotlib.pyplot as plt
from typing import List
import io
import base64

def plot_per_residue(plddt: List[float], title: str = "Per-residue plDDT") -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(range(1, len(plddt)+1), plddt, marker="o", linewidth=1)
    ax.set_xlabel("Residue")
    ax.set_ylabel("plDDT")
    ax.set_title(title)
    ax.grid(True, linestyle='--', linewidth=0.4)
    plt.tight_layout()
    return fig

def create_csv_download_link(csv_bytes: bytes, filename: str) -> str:
    """
    Returns an href link to download the CSV (not used when using Streamlit's download_button).
    """
    b64 = base64.b64encode(csv_bytes).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'
