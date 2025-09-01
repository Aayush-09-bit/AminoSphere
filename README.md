# 🧬 AminoSphere (ESMFold + Streamlit)
An AI-powered web application for **protein structure prediction, mutation analysis, and interactive 3D visualization** using Meta’s ESMFold API.

## Official Site: https://aminosphere-gmckrpfubxhqu2htncewty.streamlit.app/

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.32+-red.svg)
![Py3Dmol](https://img.shields.io/badge/py3Dmol-latest-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🎯 Overview  
**AminoSphere** allows researchers, students, and enthusiasts to:  
- Predict **protein 3D structures** directly from amino acid sequences  
- Simulate **point mutations** and observe structural impact  
- Explore **confidence scores** and annotate environmental effects  
- Interactively view, rotate, and analyze proteins in **3D**  

It integrates **Meta’s ESMFold API** with a smooth **Streamlit web interface**.  

---

## ✨ Features  
- 🧪 **Protein Structure Prediction** – Predict 3D structures from any sequence  
- 🔄 **Mutation Mode** – Introduce single-point mutations and re-predict structures  
- 🌍 **Environment Simulation** – Annotate proteins with pH, temperature, and PTMs  
- 🎥 **Interactive 3D Viewer** – Auto-rotating model with user controls (Py3Dmol)  
- 💾 **Data Export** – Save mutation/scan results as CSV  
- 📊 **Quick Plots** – Visualize confidence scores and mutation effects  
- ⚡ **Caching** – Faster repeat queries with local cache  

---

## 🚀 Quick Start  

1. **Clone and setup**  
   ```bash
   git clone https://github.com/yourusername/AminoSphere.git
   cd AminoSphere
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
2. ```bash
   pip install -r requirements.txt
3. ```bash
   streamlit run app.py
4. Open browser → http://localhost:8501

---

## 📊 Example Workflow
1. Paste or use the default protein sequence (preloaded)
2. Predict its 3D structure
3. Apply a mutation (e.g., A → V at position 35)
4. View and rotate the updated structure in 3D
5. Export results as CSV or explore plots

---

## 📁 Project Structure
AminoSphere/
├── app.py              # Streamlit main app
├── esmfold_api.py      # Handles Meta ESMFold API calls
├── utils.py            # Helper functions (mutations, plotting, etc.)
├── requirements.txt    # Dependencies
└── .gitignore          # Ignore cache/venv files

---

## 🔧 Technical Details
- Backend: Streamlit + Python
- 3D Viewer: Py3Dmol (interactive + auto-rotation)
- Model: Meta’s ESMFold API for protein structure prediction
- Caching: Streamlit st.cache_data for performance
- Export: CSV download + plotting with Matplotlib

---

## 🤝 Contributing
- Fork the repository
- Create a feature branch (git checkout -b feature/improvement)
- Commit changes (git commit -m 'Add improvement')
- Push to branch (git push origin feature/improvement)
- Open Pull Request

---

## ⚠️ Scientific Disclaimer
For research and educational purposes only. Predictions are computational and not substitutes for experimental validation.

---

## 📜 License
MIT License.
