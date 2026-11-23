# AI-IDPS: AI-Driven Cyber Threat Detection & Intelligent Intrusion Prevention

An MCA Mini Project implementing machine-learning-based network intrusion detection and confidence-driven automated intrusion prevention using the NSL-KDD dataset, Scikit-learn, XGBoost, Flask, SQLite, and Chart.js.

## Features
- **5-Class Threat Classification:** Normal, DoS, Probe, R2L, U2R
- **Model Comparison:** Decision Tree, Random Forest (`class_weight="balanced"`), and XGBoost
- **Intelligent Prevention Engine:**
  - Confidence `>= 0.90` -> **Blocked** (`HIGH`)
  - Confidence `0.60 – 0.90` -> **Rate-limited** (`MEDIUM`)
  - Confidence `< 0.60` / Normal -> **Logged** (`LOW`)
- **Web Console:** Authentication, Start/Stop Replay, Live Monitor, Alerts Filter, Blocked IP Management, Model Performance Charts, and CSV Reports.

## Setup & Run
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ml/train.py
python seed_demo.py
python app.py