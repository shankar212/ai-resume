import os
import csv
import pdfplumber
import tempfile
import streamlit as st
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize Gemini model
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Extract text from uploaded PDF
def pdf_to_text(file):
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

# Analyze resume vs job description using Gemini
def analyze_resume(resume_text, job_description, keywords):
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
st.title("📄 AI Resume Matcher")
st.markdown("### Match resumes to a job using AI (Gemini 1.5 Pro)")
st.info("Upload candidate resumes and paste the job description. The app evaluates and scores each candidate.", icon="📌")

# Input form
with st.form("resume_form"):
    st.subheader("🔍 Input Details")
    resumes = st.file_uploader("Upload Resume PDFs", type="pdf", accept_multiple_files=True)
    job_desc = st.text_area("📝 Job Description", height=200, placeholder="Paste the job description here...")
    keywords = st.text_input("🔑 Mandatory Keywords (comma-separated)", placeholder="e.g., Python, REST, Docker")
    submitted = st.form_submit_button("🚀 Analyze Resumes")

results = []

if submitted:
    if not resumes or not job_desc or not keywords:
        st.error("🚫 Please upload at least one resume, and provide both the job description and mandatory keywords.")
    else:
        with st.spinner("Analyzing resumes with Gemini AI..."):
            for resume in resumes:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(resume.read())
                    resume_text = pdf_to_text(tmp_file.name)

                # Analyze using Gemini
                analysis = analyze_resume(resume_text, job_desc, keywords)
                lines = analysis.split('\n')

                comments, score, suitability = "", "", "Unclear"
                for line in lines:
                    if "Comments:" in line:
                        comments = line.replace("Comments:", "").strip()
                    elif "Score:" in line:
                        try:
                            score = int(''.join(filter(str.isdigit, line)))
                        except:
                            score = "N/A"
                    elif "Suitable" in line:
                        if "Not" in line:
                            suitability = "❌ Not Suitable"
                        elif "Maybe" in line:
                            suitability = "🤔 Maybe Suitable"
                        elif "Suitable" in line:
                            suitability = "✅ Suitable"

                results.append({
                    "Resume Name": resume.name,
                    "Comments": comments,
                    "Score": score,
                    "Suitability": suitability
                })

        st.success("✅ Analysis complete!")

        # Display results
        st.subheader("📊 Results Summary")
        for r in results:
            with st.expander(f"📄 {r['Resume Name']}"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric(label="📈 Score", value=r['Score'])
                    st.markdown(f"**{r['Suitability']}**")
                with col2:
                    st.markdown(f"**🗒️ Comments:** {r['Comments']}")

        # Export results to CSV
        csv_file = "results.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Resume Name", "Comments", "Score", "Suitability"])
            writer.writeheader()
            writer.writerows(results)

        with open(csv_file, 'rb') as f:
            st.download_button("📥 Download CSV", data=f, file_name="resume_results.csv", mime="text/csv")

# Footer
st.write("")  # spacing
st.caption("Developed by @Rathod Shanker")
