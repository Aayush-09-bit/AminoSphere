# 🧬 Protein Structure Explorer

A Streamlit web app to predict and visualize protein structures using [ESMFold](https://esmatlas.com).

## 🚀 Features
- Paste any protein sequence (20–1000+ amino acids)
- Predict 3D structure (via ESMFold API)
- Interactive **3D viewer** with rotation & zoom (py3Dmol)
- Graph of prediction confidence (pLDDT scores)
- Plain-English summary of results
- Optional **context-aware prediction**:
  - pH, temperature
  - Post-translational modifications (with simple explanations)
- Export results as CSV

## 📦 Installation
```bash
git clone https://github.com/yourusername/protein-structure-app.git
cd protein-structure-app
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/Mac
pip install -r requirements.txt
