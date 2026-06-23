import os
import csv
import pdfplumber
import tempfile
import re
import streamlit as st
import google.generativeai as genai

# Extract text from uploaded PDF
def pdf_to_text(file):
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

# Analyze resume vs job description using Gemini
def analyze_resume(resume_text, job_description, keywords, model_name, api_key):
    if not api_key:
        raise ValueError("API Key is missing. Please provide a Gemini API Key.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
You are a recruiter AI. Evaluate how well the following resume matches the given job description.
Mandatory Keywords: {keywords}

Job Description:
{job_description}

Resume:
{resume_text}

Instructions:
1. Assess if the resume fits the job.
2. Comment on key matches or gaps.
3. Give a score out of 100 based on the fit.
4. At the end, write: Suitable / Maybe Suitable / Not Suitable

Response format:
Comments: <your comments here>
Score: <number>
Suitability: Suitable / Maybe Suitable / Not Suitable
"""
    response = model.generate_content(prompt)
    return response.text

# Page settings
st.set_page_config(page_title="🤖 AI Resume Matcher", layout="centered")

# Custom CSS for rich premium design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.75rem;
        margin-bottom: 0.25rem;
        text-align: center;
    }
    
    .main-subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .candidate-card {
        background: rgba(128, 128, 128, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .candidate-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .pill-suitable {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .pill-maybe {
        background-color: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .pill-not {
        background-color: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }

    .score-badge {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        color: white;
        padding: 8px 14px;
        border-radius: 10px;
        font-size: 1.4rem;
        font-weight: 700;
        text-align: center;
        min-width: 55px;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(99, 102, 241, 0.25);
    }
    
    div[data-testid="stForm"] {
        background: rgba(128, 128, 128, 0.03);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 16px;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Custom header
st.markdown('<div class="main-header">🤖 AI Resume Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Evaluate candidate resumes against any job description with Google Gemini</div>', unsafe_allow_html=True)

# Sidebar settings
st.sidebar.title("⚙️ API Configuration")

# Get default API key from environment variable
default_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""

# Use Streamlit sidebar input for API Key
api_key_input = st.sidebar.text_input(
    "Gemini API Key",
    value=default_key,
    type="password",
    help="Provide your Google Gemini API Key. Defaults to the environment key if found."
)

# Dynamically load models based on the API Key
available_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-flash-latest", "gemini-pro"]
if api_key_input:
    try:
        genai.configure(api_key=api_key_input)
        models_list = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                name = m.name.replace('models/', '')
                models_list.append(name)
        if models_list:
            # Sort to place standard models first
            pref_order = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-flash-latest", "gemini-pro", "gemini-2.0-flash"]
            def get_pref_index(x):
                try:
                    return pref_order.index(x)
                except ValueError:
                    return 999
            models_list.sort(key=get_pref_index)
            available_models = models_list
    except Exception as e:
        # If API key is invalid or has network issues, just keep the defaults
        pass

selected_model = st.sidebar.selectbox(
    "Gemini Model",
    options=available_models,
    index=0
)

st.sidebar.info("💡 **Tip:** Get your Gemini API Key from Google AI Studio.", icon="ℹ️")

# Info banner
st.info("Upload candidate resumes (PDF format) and paste the job description below to start matching.", icon="📌")

# Input form
with st.form("resume_form"):
    st.subheader("🔍 Input Details")
    resumes = st.file_uploader("Upload Resume PDFs", type="pdf", accept_multiple_files=True)
    job_desc = st.text_area("📝 Job Description", height=200, placeholder="Paste the job description here...")
    keywords = st.text_input("🔑 Mandatory Keywords (comma-separated)", placeholder="e.g., Python, REST, Docker")
    submitted = st.form_submit_button("🚀 Analyze Resumes")

results = []

if submitted:
    if not api_key_input:
        st.error("🚫 Please enter your Gemini API Key in the sidebar configuration.")
    elif not resumes or not job_desc or not keywords:
        st.error("🚫 Please upload at least one resume, and provide both the job description and mandatory keywords.")
    else:
        with st.spinner("Analyzing resumes with Gemini AI..."):
            for resume in resumes:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(resume.read())
                    resume_text = pdf_to_text(tmp_file.name)

                try:
                    # Analyze using Gemini
                    analysis = analyze_resume(resume_text, job_desc, keywords, selected_model, api_key_input)
                    
                    # Robust Parsing
                    comments = ""
                    score = "N/A"
                    suitability = "Unclear"
                    
                    # Suitability match
                    analysis_lower = analysis.lower()
                    if "not suitable" in analysis_lower:
                        suitability = "Not Suitable"
                    elif "maybe suitable" in analysis_lower:
                        suitability = "Maybe Suitable"
                    elif "suitable" in analysis_lower:
                        suitability = "Suitable"
                    
                    # Score match
                    score_match = re.search(r'(?:score|fit|rating)\s*:\s*(\d+)', analysis, re.IGNORECASE)
                    if score_match:
                        score = int(score_match.group(1))
                    else:
                        for line in analysis.split('\n'):
                            if "score" in line.lower():
                                try:
                                    score = int(''.join(filter(str.isdigit, line)))
                                    break
                                except:
                                    pass
                    
                    # Comments match
                    comments_match = re.search(r'(?:comments|feedback|gaps)\s*:\s*(.*)', analysis, re.IGNORECASE | re.DOTALL)
                    if comments_match:
                        comments = comments_match.group(1).strip()
                        # Clean up trailing Score or Suitability if captured in the match
                        comments = re.sub(r'\n*(?:score|suitability).*', '', comments, flags=re.IGNORECASE | re.DOTALL).strip()
                    else:
                        for line in analysis.split('\n'):
                            if "comments:" in line.lower() or "feedback:" in line.lower():
                                comments = re.sub(r'^(?:\*\*)*comments:(?:\*\*)*', '', line, flags=re.IGNORECASE).strip()
                                break
                        if not comments:
                            comments = analysis.strip()
                            
                except Exception as e:
                    comments = f"Error during analysis: {str(e)}"
                    score = "Error"
                    suitability = "Error"

                results.append({
                    "Resume Name": resume.name,
                    "Comments": comments,
                    "Score": score,
                    "Suitability": suitability
                })

        st.success("✅ Analysis complete!")

        # Display results
        st.subheader("📊 Evaluation Results Summary")
        for r in results:
            suit_pill = ""
            if r['Suitability'] == "Suitable":
                suit_pill = '<span class="pill-suitable">✅ Suitable</span>'
            elif r['Suitability'] == "Maybe Suitable":
                suit_pill = '<span class="pill-maybe">🤔 Maybe Suitable</span>'
            elif r['Suitability'] == "Not Suitable":
                suit_pill = '<span class="pill-not">❌ Not Suitable</span>'
            else:
                suit_pill = f'<span class="pill-maybe">{r["Suitability"]}</span>'
                
            st.markdown(f"""
            <div class="candidate-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.2rem;">📄 {r['Resume Name']}</h4>
                    <div>{suit_pill}</div>
                </div>
                <div style="display: flex; gap: 1.5rem; align-items: flex-start;">
                    <div style="text-align: center; flex-shrink: 0;">
                        <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #a0aec0; margin-bottom: 4px;">Score</div>
                        <div class="score-badge">{r['Score']}</div>
                    </div>
                    <div style="flex-grow: 1;">
                        <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #a0aec0; margin-bottom: 4px;">AI Comments & Gaps</div>
                        <div style="font-size: 0.95rem; line-height: 1.5; color: inherit;">{r['Comments']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Export results to CSV
        csv_file = "results.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Resume Name", "Comments", "Score", "Suitability"])
            writer.writeheader()
            writer.writerows(results)

        with open(csv_file, 'rb') as f:
            st.download_button("📥 Download CSV Report", data=f, file_name="resume_results.csv", mime="text/csv")

# Footer
st.write("")  # spacing
st.caption("Developed by @Rathod Shanker")
