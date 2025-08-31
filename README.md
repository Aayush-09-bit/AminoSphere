# ESMFold+ — Streamlit app

Enhanced ESMFold-based single-sequence structure predictor with:
- Real predictions from ESMFold API (https://esmatlas.com)
- Single-residue mutation mode (re-predicts mutated sequence)
- Mutational scan (single-position scan across 19 mutants) with CSV export + quick plots
- Context-aware metadata (pH, temperature, PTMs) with heuristic plDDT adjustments
- Caching of API responses using `st.cache_data` to speed repeated requests

## Install & run locally

```bash
git clone <your-repo-url>
cd esmfold-plus
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
