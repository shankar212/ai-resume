# 🤖 AI Resume Matcher using Gemini

An AI-powered web application that evaluates candidate resumes against a given job description. Upload one or more resumes (PDF format), enter the job description and mandatory keywords, and get insightful feedback on the fit, score, and suitability — powered by Google Gemini (Generative AI).

### 🔗 Live App
[🚀 Try it on Streamlit](https://ai-resume-matching.streamlit.app/)

---

## 📸 Demo

![Demo GIF](https://user-images.githubusercontent.com/your-username/demo.gif) <!-- Replace with actual demo GIF or screenshot -->

---

## 🧠 Features

- ✅ Upload multiple resume PDFs
- ✅ Extracts text using `pdfplumber`
- ✅ Uses Google Gemini (LLM) to analyze resume–job description fit
- ✅ Generates AI-based comments, score (out of 100), and suitability
- ✅ CSV export of results
- ✅ Fully responsive UI with Streamlit

---

## ⚙️ Tech Stack

| Tool             | Purpose                                      |
|------------------|----------------------------------------------|
| `Python`         | Backend logic                                |
| `Streamlit`      | Web interface                                |
| `pdfplumber`     | Resume PDF text extraction                   |
| `Google Generative AI (Gemini Pro)` | Resume evaluation using LLM |
| `CSV`            | Downloadable report                          |

---

## 🚀 Getting Started

### 1. Clone this repository
```bash
git clone https://github.com/your-username/ai-resume-matcher.git
cd ai-resume-matcher
