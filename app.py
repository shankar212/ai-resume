import os
import csv
import pdfplumber
import tempfile
import streamlit as st
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=os.getenv("AIzaSyAyPlDdB39Ass9fH9JB9qGfYYs9E418Lkk"))

# Initialize the model once
model = genai.GenerativeModel('models/gemini-1.5-pro')

# Function to extract text from PDF
def pdf_to_text(file):
    """Extracts text from a PDF file."""
    text = ''
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ''
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    return text

# Chat function using Gemini
def analyze_resume(resume_text, job_description, keywords):
    """Generates a response using the Gemini API based on the resume and job description."""
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

# Streamlit App UI
st.set_page_config(page_title="AI Resume Matcher", layout="centered")
st.title("📄 AI Resume Matcher using Gemini")
st.markdown("""
Upload candidate resumes and a job description. The app will evaluate suitability and provide a score.
This tool helps recruiters match resumes with job descriptions.
""")

# Form input
with st.form("resume_form"):
    resumes = st.file_uploader("Upload Resume PDFs", type="pdf", accept_multiple_files=True)
    job_desc = st.text_area("Job Description", height=200, placeholder="Enter job description here...")
    keywords = st.text_input("Mandatory Keywords (comma-separated)", placeholder="Enter mandatory keywords here...")
    submitted = st.form_submit_button("Analyze Resumes")

# Results placeholder
results = []

if submitted:
    # Ensure all inputs are provided
    if not resumes or not job_desc or not keywords:
        st.error("Please upload at least one resume, and fill in the job description and mandatory keywords.")
    else:
        with st.spinner("Analyzing resumes..."):
            for resume in resumes:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(resume.read())
                        resume_text = pdf_to_text(tmp_file.name)

                    # Analyze resume using Gemini model
                    analysis = analyze_resume(resume_text, job_desc, keywords)
                    lines = analysis.split('\n')

                    comments, score, suitability = "", "", "Unclear"
                    for line in lines:
                        if "Comments:" in line:
                            comments = line.replace("Comments:", "").strip()
                        elif "Score:" in line:
                            try:
                                score = int(''.join(filter(str.isdigit, line)))
                            except ValueError:
                                score = "N/A"
                        elif "Suitable" in line:
                            if "Not" in line:
                                suitability = "Not Suitable"
                            elif "Maybe" in line:
                                suitability = "Maybe Suitable"
                            elif "Suitable" in line:
                                suitability = "Suitable"

                    # Append results
                    results.append({
                        "Resume Name": resume.name,
                        "Comments": comments,
                        "Score": score,
                        "Suitability": suitability
                    })

                except Exception as e:
                    st.error(f"Error processing {resume.name}: {str(e)}")

        st.success("✅ Analysis complete!")

        # Display results
        st.subheader("📊 Results")
        for r in results:
            st.markdown(f"""
            **📄 {r['Resume Name']}**

            - **🗒️ Comments**: {r['Comments']}
            - **📈 Score**: {r['Score']}
            - **✅ Suitability**: {r['Suitability']}
            ---
            """)

        # Export to CSV
        csv_file = "results.csv"
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Resume Name", "Comments", "Score", "Suitability"])
                writer.writeheader()
                writer.writerows(results)

            with open(csv_file, 'rb') as f:
                st.download_button("📥 Download CSV Results", data=f, file_name="resume_results.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Error exporting results to CSV: {str(e)}")
