# 🧬 Protein Prediction App (ESMFold + Streamlit)

This app predicts protein 3D structures using **Meta’s ESMFold API** and provides:
- Unlimited sequence input
- Mutation mode (position-based residue change)
- Environment-aware confidence adjustments (pH, temperature, PTMs)
- Interactive 3D visualization (via py3Dmol)
- CSV export of residue confidence scores

---

## 🚀 Run Locally

```bash
git clone https://github.com/your-username/protein-prediction-app.git
cd protein-prediction-app
pip install -r requirements.txt
streamlit run app.py
