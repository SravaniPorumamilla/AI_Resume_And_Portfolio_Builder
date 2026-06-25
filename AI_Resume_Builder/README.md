# 📄 AI Resume & Portfolio Builder

Powered by **Google Gemini 2.0 Flash** + **Streamlit**

## ✨ Features
1. 📝 **Resume Builder** — Professional, ATS-optimised resumes
2. 💼 **Portfolio Builder** — Full portfolio website content
3. 🔍 **ATS Checker** — Score your resume against a job description
4. 💌 **Cover Letter Generator** — Personalised cover letters
5. 🔗 **LinkedIn Summary Generator** — Magnetic LinkedIn profiles
6. 📊 **Skills Gap Analyser** — Roadmap to your dream job

---

## 🚀 How to Run

### Step 1 — Get your free Gemini API Key
Go to: https://aistudio.google.com/
Click "Get API Key" → Copy the key (starts with AIza...)

### Step 2 — Install dependencies
Open terminal in this folder and run:
```bash
pip install -r requirements.txt --break-system-packages
```

### Step 3 — Run the app
```bash
python3 -m streamlit run app.py
```

OR simply double-click / run:
```bash
bash run.sh
```

### Step 4 — Use the app
- Open browser at: http://localhost:8501
- Paste your Gemini API key in the sidebar
- Fill in your details and click Generate!

---

## ❓ Troubleshooting

**"streamlit: command not found"**
```bash
python3 -m streamlit run app.py
```

**"ModuleNotFoundError"**
```bash
pip3 install -r requirements.txt --break-system-packages
```

**"Invalid API Key"**
- Make sure you copied the full key from https://aistudio.google.com/
- The key should start with "AIza"

---

## 📦 Requirements
- Python 3.9 or higher
- Internet connection (for Gemini API calls)
- Free Google Gemini API key
