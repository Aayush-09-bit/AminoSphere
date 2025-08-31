import matplotlib.pyplot as plt
import pandas as pd

def calculate_plddt(struct) -> float:
    """Calculate mean plDDT score from b-factors."""
    return round(struct.b_factor.mean(), 4)

def plot_plddt_distribution(struct):
    """Plot histogram of plDDT scores."""
    plt.figure(figsize=(6, 4))
    plt.hist(struct.b_factor, bins=30, color="skyblue", edgecolor="black")
    plt.title("plDDT Confidence Distribution")
    plt.xlabel("plDDT Score")
    plt.ylabel("Residue Count")
    return plt.gcf()

def save_results_csv(struct, filename="results.csv"):
    """Save per-residue plDDT scores to CSV."""
    df = pd.DataFrame({"Residue": range(len(struct.b_factor)), "plDDT": struct.b_factor})
    df.to_csv(filename, index=False)
