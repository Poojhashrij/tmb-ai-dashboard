# tmb-ai-dashboard
# 🧬 Tumor Mutational Burden (TMB) AI Dashboard

This project is a smart bioinformatics web application that calculates **Tumor Mutational Burden (TMB)** from VCF files and integrates **clinical guidelines**, **AI predictions**, and **real-time immunotherapy drug** and **clinical trial** suggestions for cancer precision medicine.

---

## 🔍 Features

- 📂 Upload and parse VCF files
- 🧠 Machine Learning model to predict TMB level (Low / High)
- 💊 Suggest immunotherapy drugs based on TMB and clinical guidelines (OncoKB)
- 🧪 Match clinical trials (via ClinicalTrials.gov API)
- 📊 Visualization dashboard with results and clinical context
- 🌐 Easy-to-use web interface (Flask + HTML/CSS frontend)

---

## 📁 Project Structure
├── backend/ # Python APIs for ML, data parsing, and API integration
├── data/ # Sample VCF and test data files
├── frontend/ # HTML, CSS, JS files for UI (Flask templates/static)
├── model/ # Trained ML model (pickle or h5)
├── venv/ # Python virtual environment
├── .dist/ # Compiled or packaged app (if applicable)
├── requirements.txt # List of required Python libraries
├── train_model.py # Script to train ML model on TMB data
├── test_cbio.py # Test script for cBioPortal integration (optional)

yaml

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/tmb-ai-dashboard.git
cd tmb-ai-dashboard

# 2. Create and activate virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # For Windows
source venv/bin/activate  # For Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python backend/app.py
🧪 Input Format
Upload files in VCF format (.vcf) to compute TMB.

You can test with sample files inside the data/ folder.

🧠 ML Model
Trained on mutation counts and clinical labels.

Supports .pkl or .joblib format models inside model/ folder.

🌐 External APIs
✅ ClinicalTrials.gov for real-time clinical trials

✅ OncoKB (optional) for immunotherapy drug linking

✅ (Optional) cBioPortal testing via test_cbio.py

👩‍💻 Developed By
Poojhashri J
MSc Bioinformatics
Sri Ramachandra Faculty of Engineering and Technology



