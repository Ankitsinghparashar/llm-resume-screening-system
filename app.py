# app.py

import streamlit as st
from llm_utils import get_llm_response

st.set_page_config(
    page_title="AI Resume–Job Fit Evaluator",
    layout="wide"
)

st.title("🤖 AI Resume–Job Fit Evaluator")
st.markdown("Evaluate resume compatibility using Local LLM (Mistral via Ollama)")

col1, col2 = st.columns(2)

with col1:
   uploaded_resume = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx", "txt"]
)

resume_text = ""

if uploaded_resume is not None:
    if uploaded_resume.name.endswith(".txt"):
        resume_text = uploaded_resume.getvalue().decode("utf-8")
    else:
        st.info("Resume uploaded. PDF/DOCX text extraction needs to be configured.")
        
resume_text = st.text_area(
    "Or Paste Resume",
    value=resume_text,
    height=300
)

with col2:
    job_text = st.text_area("💼 Paste Job Description", height=400)

if st.button("🔍 Evaluate Match"):

    if not resume_text or not job_text:
        st.warning("Please provide both resume and job description.")
    else:
        with st.spinner("Analyzing with LLM..."):
            result = get_llm_response(resume_text, job_text)

        st.subheader("📊 Results")

        st.metric("Match Score", f"{result['match_score']} / 100")

        st.write("### 🛠 Missing Skills")
        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.write(f"- {skill}")
        else:
            st.write("None")

        st.write("### 🧠 Explanation")
        st.write(result["explanation"])
