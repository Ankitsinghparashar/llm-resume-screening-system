import streamlit as st
import pdfplumber
from docx import Document
from io import BytesIO
from llm_utils import get_llm_response

st.set_page_config(
    page_title="ResumeIQ | AI Resume Analyzer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --purple: #8b5cf6;
    --purple-dark: #6d28d9;
    --ink: #201b35;
    --muted: #79748c;
    --border: #eae6f4;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, #eee5ff 0%, transparent 35%),
        radial-gradient(ellipse at 100% 100%, #f3e8ff 0%, transparent 32%),
        #f9f8fc;
    color: var(--ink);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] h2 {
    color: #7c3aed;
    font-weight: 800;
}

.brand {
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #29213f;
}

.brand span {
    color: #8b5cf6;
}

.topline {
    color: var(--muted);
    font-size: 13px;
    margin-top: 5px;
}

.hero {
    background: linear-gradient(120deg, #21153e, #5425a7 65%, #895cf6);
    border-radius: 24px;
    padding: 34px;
    color: white;
    margin: 24px 0;
    box-shadow: 0 18px 45px rgba(92, 54, 160, 0.18);
}

.hero h1 {
    color: white;
    font-size: 35px;
    line-height: 1.2;
    margin-bottom: 12px;
}

.hero p {
    color: #e6ddff;
    font-size: 15px;
}

.eyebrow {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 700;
    color: #c4b5fd;
    margin-bottom: 12px;
}

.panel {
    background: rgba(255,255,255,.96);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 28px rgba(42, 25, 80, .04);
}

.panel-title {
    font-size: 19px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 5px;
}

.panel-subtitle {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 20px;
}

div[data-testid="stFileUploader"] {
    background: #f8f5ff;
    border: 1.5px dashed #b9a0fa;
    border-radius: 15px;
    padding: 12px;
}

div[data-testid="stTextArea"] textarea {
    background: #fcfbff;
    border: 1px solid #e5def4;
    border-radius: 12px;
    color: #29213f;
    font-size: 14px;
}

.stButton > button {
    background: linear-gradient(100deg, #8b5cf6, #6d28d9);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 13px 22px;
    font-weight: 700;
    min-height: 48px;
    transition: .2s ease;
}

.stButton > button:hover {
    background: linear-gradient(100deg, #7c3aed, #5b21b6);
    color: white;
    box-shadow: 0 8px 22px rgba(109,40,217,.25);
}

.metric-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
}

.metric-label {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 10px;
}

.metric-value {
    color: #6d28d9;
    font-size: 38px;
    font-weight: 800;
}

.skill {
    display: inline-block;
    background: #eee7ff;
    color: #6d28d9;
    border: 1px solid #e2d6ff;
    border-radius: 30px;
    padding: 7px 12px;
    margin: 4px;
    font-size: 12px;
    font-weight: 600;
}

.missing {
    background: #fff0f0;
    color: #be3455;
    border-color: #ffd9df;
}

.footer {
    text-align: center;
    color: #9891a8;
    font-size: 12px;
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
}

#MainMenu, footer {
    visibility: hidden;
}

@media (max-width: 768px) {
    .hero { padding: 23px; }
    .hero h1 { font-size: 27px; }
    .panel { padding: 17px; }
}
</style>
""", unsafe_allow_html=True)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown(
        '<div class="brand">✦ Resume<span>IQ</span></div>',
        unsafe_allow_html=True
    )
    st.caption("AI-powered recruitment workspace")
    st.divider()

    st.markdown("### WORKSPACE")
    page = st.radio(
        "Navigation",
        ["Resume Analyzer", "How It Works", "About"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("### ANALYSIS ENGINE")
    st.markdown("🧠 **LLM-powered evaluation**")
    st.caption("Resume and job-description comparison")

    st.info(
        "Screening results are decision-support signals. "
        "Always review candidates fairly."
    )


# ---------- HEADER ----------
st.markdown(
    '<div class="brand">Resume<span>IQ</span> '
    '<span style="font-size:12px;letter-spacing:0;'
    'background:#eee7ff;padding:6px 10px;border-radius:20px;">'
    'AI ANALYZER</span></div>'
    '<div class="topline">Intelligent resume and job compatibility analysis</div>',
    unsafe_allow_html=True
)


if page == "Resume Analyzer":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">AI-powered talent intelligence</div>
        <h1>Find the right fit.<br>Understand every match.</h1>
        <p>Analyze resume compatibility, identify skill gaps, and generate
        actionable insights from your job requirements.</p>
    </div>
    """, unsafe_allow_html=True)

    resume_col, job_col = st.columns([1, 1], gap="large")

    with resume_col:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">📄 Upload your resume</div>
            <div class="panel-subtitle">
                PDF, Word document, or plain text
            </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose a resume",
            type=["pdf", "docx", "txt"],
            help="Upload a text-based PDF, DOCX, or TXT file.",
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="panel">
            <div class="panel-title">Or paste resume text</div>
            <div class="panel-subtitle">
                You can paste your resume instead of uploading a file.
            </div>
        """, unsafe_allow_html=True)

        pasted_resume = st.text_area(
            "Resume text",
            height=220,
            placeholder="Paste the complete resume here...",
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with job_col:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">💼 Job description</div>
            <div class="panel-subtitle">
                Include responsibilities, required skills, and experience.
            </div>
        """, unsafe_allow_html=True)

        job_text = st.text_area(
            "Job description",
            height=390,
            placeholder=(
                "Paste the job description here...\n\n"
                "Example:\n"
                "Role: Python Developer\n"
                "Required skills: Python, SQL, REST APIs, Git\n"
                "Experience: 0-2 years"
            ),
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    def extract_resume_text(upload):
        if upload is None:
            return ""

        file_bytes = upload.getvalue()
        filename = upload.name.lower()

        if filename.endswith(".txt"):
            return file_bytes.decode("utf-8", errors="replace")

        if filename.endswith(".pdf"):
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                return "\n".join(
                    page.extract_text() or "" for page in pdf.pages
                ).strip()

        if filename.endswith(".docx"):
            document = Document(BytesIO(file_bytes))
            paragraphs = [
                p.text for p in document.paragraphs if p.text.strip()
            ]
            return "\n".join(paragraphs).strip()

        return ""

    st.write("")

    left, center, right = st.columns([1, 2, 1])

    with center:
        analyze = st.button(
            "✦  Analyze Resume",
            use_container_width=True
        )

    if analyze:
        try:
            resume_text = pasted_resume.strip()

            if uploaded_file is not None:
                resume_text = extract_resume_text(uploaded_file)

            if not resume_text:
                st.error(
                    "Please upload a readable resume or paste its text."
                )
            elif not job_text.strip():
                st.error("Please enter a job description.")
            else:
                with st.spinner(
                    "Analyzing skills and evaluating job compatibility..."
                ):
                    result = get_llm_response(
                        resume_text,
                        job_text.strip()
                    )

                score = max(
                    0, min(100, int(result.get("match_score", 0)))
                )
                missing_skills = result.get("missing_skills", [])
                explanation = result.get(
                    "explanation", "No explanation was returned."
                )

                st.markdown("## Your analysis")
                st.caption(
                    "Review the score alongside the evidence and skill gaps."
                )

                score_col, gap_col = st.columns(2, gap="large")

                with score_col:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">RESUME MATCH SCORE</div>
                        <div class="metric-value">{score}%</div>
                        <div style="background:#eee7ff;border-radius:20px;
                                    height:9px;margin-top:15px;">
                            <div style="background:linear-gradient(90deg,
                                        #a78bfa,#6d28d9);
                                        width:{score}%;height:9px;
                                        border-radius:20px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with gap_col:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">SKILL GAPS IDENTIFIED</div>
                        <div class="metric-value">{len(missing_skills)}</div>
                        <div style="color:#79748c;font-size:13px;">
                            Skills to review against the job requirements
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(
                    '<div class="panel"><div class="panel-title">'
                    '🧠 AI evaluation</div></div>',
                    unsafe_allow_html=True
                )
                st.write(explanation)

                st.markdown("""
                <div class="panel">
                    <div class="panel-title">🎯 Missing or unverified skills</div>
                    <div class="panel-subtitle">
                        Confirm these gaps manually before making a decision.
                    </div>
                """, unsafe_allow_html=True)

                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(
                            f'<span class="skill missing">'
                            f'{skill}</span>',
                            unsafe_allow_html=True
                        )
                else:
                    st.success("No missing skills were reported.")

                st.markdown("</div>", unsafe_allow_html=True)

                st.download_button(
                    "⬇ Download analysis",
                    data=(
                        f"RESUME MATCH SCORE: {score}/100\n\n"
                        f"EXPLANATION:\n{explanation}\n\n"
                        f"MISSING SKILLS:\n"
                        + "\n".join(f"- {s}" for s in missing_skills)
                    ),
                    file_name="resume_analysis.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        except Exception as exc:
            st.error(
                "The analysis could not be completed. "
                "Check the app logs for the underlying error."
            )
            st.caption(f"Error type: {type(exc).__name__}")

    st.markdown("""
    <div class="footer">
        ResumeIQ · AI-assisted resume analysis<br>
        Use as a screening aid, not as the sole basis for hiring decisions.
    </div>
    """, unsafe_allow_html=True)


elif page == "How It Works":
    st.markdown("## How ResumeIQ works")
    st.markdown("""
    1. **Upload:** Provide a PDF, DOCX, or TXT resume.
    2. **Describe the role:** Paste the relevant job description.
    3. **Evaluate:** The configured LLM compares the resume with the role.
    4. **Review:** Examine the match score, missing skills, and explanation.
    5. **Decide fairly:** Verify the results and make decisions using human review.
    """)

elif page == "About":
    st.markdown("## About ResumeIQ")
    st.write(
        "ResumeIQ is an LLM-based resume screening project designed "
        "to assist with resume-to-job compatibility analysis."
    )
    st.info(
        "Results depend on resume quality, job requirements, and the "
        "configured language model. Scores are estimates, not guarantees."
    )
