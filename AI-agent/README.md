# 🎯 B2B AI Lead Intelligence Tool

A lightweight but powerful AI-powered lead triage tool designed specifically for B2B Small-to-Medium Enterprises (SMEs). 

By pasting a raw client inquiry or an inbound email, the AI extracts structured intelligence, evaluates urgency and feasibility, and assigns a strict **Priority Score (1–10)** using Google's ultra-fast `gemini-1.5-flash` model.

---

## URL
https://cloud-computing-for-big-data-nybrvehysdbdyajurplstd.streamlit.app

## 💼 Business Value for SMEs

Many SME agencies and consulting firms suffer from **"Lead Fatigue"**. They receive dozens of unstructured inquiries via contact forms or inbound emails and spend hours manually identifying which leads have a real budget versus the "tire-kickers".

**This tool directly solves Lead Fatigue by providing immediate ROI:**
1. **Time Saved:** Saves the business owner **5–10 hours per week** of manual vetting.
2. **Prioritized Sales Effort:** Instead of reading every email deeply, sales teams instantly filter by the 🟢 High Priority (score 7-10) cohort. Lead cards highlight budgets and summarize projects at a glance.
3. **Risk Mitigation:** The tool automatically surfaces 🚩 **Red Flags** (e.g., unrealistic timelines, missing budgets, vague requirements) before you even schedule a discovery call.
4. **FinOps Visibility:** Real-time token tracking and a cost breakdown panel per lead ensure the operational cost of the AI triage is completely transparent (cents per lead).

---

## ⚙️ How to Install Dependencies

**1. Clone or navigate to the project directory:**
```bash
cd /path/to/AI-agent
```

**2. Create a virtual environment (highly recommended):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install requirements:**
```bash
pip install -r requirements.txt
```
*(Dependencies: `streamlit`, `google-generativeai`, `python-dotenv`, `pydantic`)*

---

## 🚀 How to Run the Application

**1. Setup your API Key:**
Copy the template to create your local environment file:
```bash
cp .env.example .env
```
Open `.env` and replace `AIzaSy...` with your actual **Google Gemini API Key**.
*(Alternatively, you can skip this step and paste your API key directly into the app's sidebar during runtime).*

**2. Launch the Streamlit Server:**
```bash
streamlit run app.py
```

**3. Open the App:**
Your browser should automatically open to **http://localhost:8501**. 
Paste a raw email inquiry into the main text box and click **⚡ Process Lead**.

---

## 🏗️ Architecture (IT4IT Alignment)
- **S2P:** Defined Business Value (Lead Triage > Lead Fatigue) & Strategy.
- **R2D (`processor.py`):** AI layer. Pure Python logic isolating Google Gemini API calls, schema validation, hallucination guards, and activity logging.
- **R2F (`app.py`):** Presentation UI. Premium dark Streamlit interface displaying parsed cards and cost metrics.
- **D2C:** FinOps panel displays prompt/completion tokens and estimated USD costs. Full session activity logged locally to `activity.log`.
