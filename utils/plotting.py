import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

def plot_confidence(confidences):
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(confidences, label="Confidence", color="blue")
    ax.set_xlabel("Residue index")
    ax.set_ylabel("plDDT (confidence)")
    ax.set_title("Residue Confidence Distribution")
    ax.legend()
    return fig

def save_results_csv(sequence, confidences):
    os.makedirs("data/results", exist_ok=True)
    df = pd.DataFrame({"Residue": list(sequence), "Confidence": confidences})
    filename = f"data/results/results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    return filename
