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
    resume_text = st.text_area("📄 Paste Resume", height=400)

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