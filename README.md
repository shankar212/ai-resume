# 🤖 AI Resume Matcher using Gemini

An AI-powered web application that evaluates candidate resumes against a given job description. Upload one or more resumes (PDF format), enter the job description and mandatory keywords, and get insightful feedback on the fit, score, and suitability — powered by Google Gemini (Generative AI) and Streamlit.

---

## 🧠 Features

- ✅ **Multiple Resume Uploads**: Upload multiple candidate PDFs at once.
- ✅ **PDF Text Extraction**: Smooth and accurate text parsing using `pdfplumber`.
- ✅ **Dynamic API & Model Config**: Enter your Gemini API key and select from the list of models (e.g., `gemini-1.5-flash`, `gemini-1.5-pro`) directly within the app.
- ✅ **Intelligent AI Evaluation**: Uses Google Gemini to assess alignment, match keywords, and identify gaps.
- ✅ **Score & Suitability Metric**: Automatically scores each candidate out of 100 and classifies them as *Suitable*, *Maybe Suitable*, or *Not Suitable*.
- ✅ **CSV Export**: Export all evaluation results in a structured CSV report for team sharing.
- ✅ **Premium UI Layout**: Beautiful, responsive, card-based glassmorphic dashboard design.

---

## ⚙️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Backend processing logic |
| **Streamlit** | Interactive web interface |
| **pdfplumber** | Resume text parsing |
| **Google Generative AI** | Resume evaluation & matching via Gemini models |
| **CSV** | Exportable report generation |

---

## 🚀 Getting Started

Follow these instructions to get the project running locally.

### Prerequisites

- Python 3.10 or higher installed.
- A Gemini API Key. You can get one for free at [Google AI Studio](https://aistudio.google.com/).

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/shankar212/ai-resume.git
   cd ai-resume
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   * **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   * **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 🔑 Set Up API Key

You can configure your API Key in two ways:

1. **Environment Variable (Recommended)**: Set the `GEMINI_API_KEY` or `GOOGLE_API_KEY` in your environment.
   * **Windows (PowerShell)**:
     ```powershell
     $env:GEMINI_API_KEY="your_api_key_here"
     ```
   * **macOS / Linux**:
     ```bash
     export GEMINI_API_KEY="your_api_key_here"
     ```
2. **Interactive Input**: Paste your API key directly in the app's sidebar when it loads.

### 🏃 Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser to interact with the application.

---

## 📝 License

This project is licensed under the MIT License. Feel free to use and modify it.

Developed by [@Rathod Shanker](https://github.com/shankar212).
