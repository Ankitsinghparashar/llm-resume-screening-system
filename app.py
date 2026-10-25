import streamlit as st
import pdfplumber
from docx import Document
from io import BytesIO
from llm_utils import get_llm_response


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ResumeIQ | Recruitment Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #3977e8;
        --primary-dark: #245bc4;
        --background: #f5f7fb;
        --text: #182230;
        --muted: #748094;
        --border: #e7ebf2;
        --success: #16845b;
        --danger: #d94b56;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--background);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.2rem;
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        color: #182230;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .brand span {
        color: var(--primary);
    }

    .brand-subtitle {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 30px;
    }

    .sidebar-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.4px;
        color: #a0a8b7;
        margin: 24px 0 10px 5px;
    }

    .page-title {
        font-size: 29px;
        font-weight: 800;
        letter-spacing: -1px;
        color: var(--text);
        margin-bottom: 4px;
    }

    .page-subtitle {
        font-size: 13px;
        color: var(--muted);
        margin-bottom: 25px;
    }

    .top-badge {
        display: inline-block;
        background: #e9f2ff;
        color: #2865c9;
        border-radius: 20px;
        padding: 7px 12px;
        font-size: 11px;
        font-weight: 700;
    }

    .metric-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 19px 20px;
        min-height: 120px;
        box-shadow: 0 2px 8px rgba(20, 35, 60, 0.025);
    }

    .metric-label {
        color: var(--muted);
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 14px;
    }

    .metric-value {
        font-size: 30px;
        line-height: 1.1;
        font-weight: 800;
        color: var(--text);
        letter-spacing: -1px;
    }

    .metric-note {
        font-size: 11px;
        color: var(--muted);
        margin-top: 8px;
    }

    .section-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 23px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(20, 35, 60, 0.025);
    }

    .section-title {
        font-size: 17px;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 5px;
    }

    .section-description {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 20px;
    }

    .result-score {
        font-size: 54px;
        font-weight: 800;
        letter-spacing: -2px;
        color: var(--primary);
        line-height: 1.2;
    }

    .skill-chip {
        display: inline-block;
        padding: 7px 11px;
        border-radius: 8px;
        background: #fff0f0;
        color: #bd4149;
        border: 1px solid #ffdddd;
        font-size: 12px;
        margin: 4px 4px 4px 0;
    }

    .success-chip {
        display: inline-block;
        padding: 7px 11px;
        border-radius: 8px;
        background: #e8f7ef;
        color: #16845b;
        border: 1px solid #d2efdf;
        font-size: 12px;
        margin: 4px 4px 4px 0;
    }

    .info-note {
        background: #edf4ff;
        border-left: 3px solid var(--primary);
        border-radius: 7px;
        padding: 12px 14px;
        font-size: 12px;
        color: #425778;
        margin-top: 15px;
    }

    .footer {
        text-align: center;
        color: #99a2b1;
        font-size: 11px;
        padding: 30px 0 12px 0;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 43px;
        font-weight: 600;
        border: 1px solid var(--border);
        transition: 0.2s;
    }

    div.stButton > button[kind="primary"] {
        background: var(--primary);
        border: 1px solid var(--primary);
        color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        background: var(--primary-dark);
        border-color: var(--primary-dark);
    }

    div[data-testid="stFileUploader"] {
        background: #fafbfe;
        border-radius: 10px;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 10px;
        border-color: #e1e6ef;
        background: #fafbfe;
        font-size: 13px;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 9px;
    }

    hr {
        border-color: var(--border);
    }

    @media (max-width: 768px) {
        .page-title {
            font-size: 24px;
        }

        .result-score {
            font-size: 42px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "analysis_resume_name" not in st.session_state:
    st.session_state.analysis_resume_name = ""

if "analysis_job_title" not in st.session_state:
    st.session_state.analysis_job_title = ""


# =========================================================
# RESUME TEXT EXTRACTION
# =========================================================

def extract_resume_text(uploaded_file):
    """Extract text from PDF, DOCX, or TXT files."""

    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()
    uploaded_file.seek(0)

    try:
        if filename.endswith(".pdf"):
            pages_text = []

            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()

                    if page_text:
                        pages_text.append(page_text)

            return "\n".join(pages_text).strip()

        elif filename.endswith(".docx"):
            document = Document(BytesIO(uploaded_file.getvalue()))

            paragraphs = [
                paragraph.text.strip()
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            # Also extract text from tables.
            for table in document.tables:
                for row in table.rows:
                    row_text = [
                        cell.text.strip()
                        for cell in row.cells
                        if cell.text.strip()
                    ]

                    if row_text:
                        paragraphs.append(" | ".join(row_text))

            return "\n".join(paragraphs).strip()

        elif filename.endswith(".txt"):
            return uploaded_file.getvalue().decode(
                "utf-8-sig",
                errors="replace"
            ).strip()

        else:
            raise ValueError(
                "Unsupported file format. Upload a PDF, DOCX, or TXT file."
            )

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            f"Could not read {uploaded_file.name}. "
            "Try another file or paste the resume text."
        ) from error


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">Resume<span>IQ</span></div>
        <div class="brand-subtitle">
            AI-powered recruitment assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">WORKSPACE</div>',
                unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Resume Screening",
            "How It Works",
            "About",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="font-size:12px;color:#748094;line-height:1.8;">
            <b style="color:#182230;">AI Screening Assistant</b><br>
            Compare resumes with job requirements and identify potential
            skill gaps.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("ResumeIQ · Version 1.0")


# =========================================================
# DASHBOARD PAGE
# =========================================================

if page == "Dashboard":

    header_left, header_right = st.columns([4, 1])

    with header_left:
        st.markdown(
            '<div class="page-title">Hiring Analytics Dashboard</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="page-subtitle">'
            'Understand candidate fit and make informed screening decisions.'
            '</div>',
            unsafe_allow_html=True,
        )

    with header_right:
        st.markdown(
            '<div style="text-align:right;padding-top:8px;">'
            '<span class="top-badge">● AI ASSISTED</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    # Dashboard metrics
    result = st.session_state.analysis_result

    if result:
        match_score = result["match_score"]
        missing_skills = result["missing_skills"]

        score_label = f"{match_score}%"
        skills_label = str(len(missing_skills))
        status_label = (
            "Strong match" if match_score >= 75
            else "Moderate match" if match_score >= 50
            else "Lower match"
        )
    else:
        score_label = "—"
        skills_label = "—"
        status_label = "Awaiting analysis"

    metric_columns = st.columns(4)

    metrics = [
        ("RESUMES ANALYZED", "1" if result else "0",
         "In this session"),
        ("LATEST MATCH SCORE", score_label,
         "AI-generated estimate"),
        ("SKILL GAPS IDENTIFIED", skills_label,
         "From the latest analysis"),
        ("SCREENING STATUS", status_label,
         "Based on available evidence"),
    ]

    for column, metric in zip(metric_columns, metrics):
        label, value, note = metric

        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value"
                         style="font-size:{'21px' if len(value) > 12 else '30px'}">
                        {value}
                    </div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.25, 1])

    with left:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Candidate Screening</div>
                <div class="section-description">
                    Start a new resume evaluation.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write(
            "Compare a candidate's resume with a job description "
            "to identify relevant experience and potential skill gaps."
        )

        if st.button(
            "＋ Start Resume Screening",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.navigate_to_screening = True
            st.rerun()

    with right:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Latest Analysis</div>
                <div class="section-description">
                    Most recent screening result.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if result:
            st.metric("Match score", f"{result['match_score']}%")

            st.progress(result["match_score"] / 100)

            st.caption(
                f"Resume: {st.session_state.analysis_resume_name}"
            )

            st.caption(
                f"Role: {st.session_state.analysis_job_title}"
            )

            if st.button(
                "View Detailed Results",
                use_container_width=True,
            ):
                st.session_state.show_latest_result = True
                st.rerun()

        else:
            st.info(
                "No screening results yet. Start a new analysis "
                "to see candidate insights here."
            )

    if st.session_state.get("show_latest_result") and result:
        st.markdown("---")
        st.markdown("### Latest Screening Results")

        st.write(result["explanation"])

        if result["missing_skills"]:
            st.markdown("**Potential skill gaps**")

            for skill in result["missing_skills"]:
                st.markdown(
                    f'<span class="skill-chip">{skill}</span>',
                    unsafe_allow_html=True,
                )

    st.markdown(
        """
        <div class="info-note">
            AI-generated screening results are estimates. Review the
            underlying resume and verify job-related qualifications
            before making hiring decisions.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# RESUME SCREENING PAGE
# =========================================================

elif page == "Resume Screening":

    st.markdown(
        '<div class="page-title">Resume Screening</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Upload a candidate resume, enter the job requirements, '
        'and generate an AI-assisted comparison.'
        '</div>',
        unsafe_allow_html=True,
    )

    resume_column, job_column = st.columns(2, gap="large")

    with resume_column:

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">01 · Candidate Resume</div>
                <div class="section-description">
                    Upload a PDF, DOCX, or TXT file.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=["pdf", "docx", "txt"],
            help="For best results, use a PDF with selectable text.",
            key="resume_uploader",
        )

        st.markdown("**Or paste resume text**")

        pasted_resume = st.text_area(
            "Resume content",
            placeholder=(
                "Paste the candidate's resume here...\n\n"
                "Include skills, education, experience, and projects."
            ),
            height=230,
            label_visibility="collapsed",
            key="resume_text_input",
        )

    with job_column:

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">02 · Job Requirements</div>
                <div class="section-description">
                    Describe the role and required qualifications.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        job_title = st.text_input(
            "Job title",
            placeholder="e.g. Software Developer",
            key="job_title_input",
        )

        job_description = st.text_area(
            "Job description",
            placeholder=(
                "Enter the job responsibilities, required skills, "
                "qualifications, and experience...\n\n"
                "Example: We need a software developer with Python, "
                "SQL, Git, data structures, and problem-solving skills."
            ),
            height=300,
            key="job_description_input",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    button_column, _ = st.columns([1, 1])

    with button_column:

        analyze_button = st.button(
            "✦ Analyze Resume",
            type="primary",
            use_container_width=True,
        )

    # -----------------------------------------------------
    # RUN ANALYSIS
    # -----------------------------------------------------

    if analyze_button:

        try:
            # Prefer pasted text when provided.
            if pasted_resume and pasted_resume.strip():
                resume_text = pasted_resume.strip()

            elif uploaded_file is not None:
                with st.spinner("Extracting resume text..."):
                    resume_text = extract_resume_text(uploaded_file)

            else:
                resume_text = ""

            if not resume_text:
                st.error(
                    "Please upload a readable resume or paste its text."
                )
                st.stop()

            if not job_description.strip():
                st.error("Please enter the job description.")
                st.stop()

            if len(resume_text) < 30:
                st.error(
                    "The resume contains too little readable text. "
                    "Try another file or paste the complete resume."
                )
                st.stop()

            with st.spinner(
                "Analyzing the resume with AI. This may take a moment..."
            ):
                result = get_llm_response(
                    resume_text,
                    job_description.strip(),
                )

            if not isinstance(result, dict):
                raise ValueError(
                    "The AI response has an unexpected format."
                )

            score = int(result.get("match_score", 0))
            score = max(0, min(100, score))

            missing_skills = result.get("missing_skills", [])

            if not isinstance(missing_skills, list):
                missing_skills = []

            explanation = str(result.get("explanation", ""))

            st.session_state.analysis_result = {
                "match_score": score,
                "missing_skills": missing_skills,
                "explanation": explanation,
            }

            st.session_state.analysis_resume_name = (
                uploaded_file.name
                if uploaded_file is not None
                else "Pasted resume"
            )

            st.session_state.analysis_job_title = (
                job_title.strip() or "Unspecified role"
            )

            st.session_state.show_latest_result = False

            st.success("Resume analysis completed successfully!")

        except Exception as error:
            # Avoid exposing API keys or internal credentials.
            error_text = str(error)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                st.error(
                    "The AI service rate limit has been reached. "
                    "Please wait before trying again."
                )

            elif "503" in error_text or "UNAVAILABLE" in error_text:
                st.error(
                    "The AI service is temporarily unavailable. "
                    "Please try again later."
                )

            elif "GROQ_API_KEY" in error_text:
                st.error(
                    "The Groq API key is missing. "
                    "Check your Streamlit Secrets configuration."
                )

            elif "401" in error_text or "invalid_api_key" in error_text.lower():
                st.error(
                    "The AI provider rejected the API key. "
                    "Check your Streamlit Secrets."
                )

            else:
                st.error(
                    "Resume analysis failed. Check the app logs "
                    "for the underlying error."
                )

            print(
                f"Resume analysis error: "
                f"{type(error).__name__}: {error}"
            )

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    result = st.session_state.analysis_result

    if result:

        st.markdown("---")

        st.markdown(
            '<div class="page-title">Screening Results</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="page-subtitle">'
            'Review the AI-generated comparison and skill-gap analysis.'
            '</div>',
            unsafe_allow_html=True,
        )

        score = result["match_score"]

        result_left, result_right = st.columns([1, 2], gap="large")

        with result_left:

            st.markdown(
                """
                <div class="section-card">
                    <div class="section-title">Resume Match</div>
                    <div class="section-description">
                        Estimated alignment with the job description.
                    </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="result-score">{score}%</div>',
                unsafe_allow_html=True,
            )

            st.progress(score / 100)

            if score >= 75:
                st.success("Strong alignment")
            elif score >= 50:
                st.warning("Partial alignment")
            else:
                st.info("Lower alignment")

            st.markdown("</div>", unsafe_allow_html=True)

        with result_right:

            st.markdown(
                """
                <div class="section-card">
                    <div class="section-title">AI Evaluation</div>
                    <div class="section-description">
                        Explanation of the candidate's job-related fit.
                    </div>
                """,
                unsafe_allow_html=True,
            )

            st.write(
                result["explanation"]
                or "No explanation was provided by the AI model."
            )

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Potential Skill Gaps</div>
                <div class="section-description">
                    Requirements that were not clearly demonstrated
                    in the supplied resume.
                </div>
            """,
            unsafe_allow_html=True,
        )

        missing_skills = result["missing_skills"]

        if missing_skills:
            for skill in missing_skills:
                st.markdown(
                    f'<span class="skill-chip">{skill}</span>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<span class="success-chip">'
                'No potential skill gaps reported'
                '</span>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="info-note">
                This score is an AI-generated estimate, not a validated
                probability of job success. Missing skills may simply
                be absent from the resume. Review the evidence and
                make hiring decisions using appropriate human judgment.
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# HOW IT WORKS PAGE
# =========================================================

elif page == "How It Works":

    st.markdown(
        '<div class="page-title">How ResumeIQ Works</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'A simple workflow for AI-assisted resume screening.'
        '</div>',
        unsafe_allow_html=True,
    )

    steps = [
        (
            "01",
            "Upload the resume",
            "Upload a PDF, DOCX, or TXT resume, or paste the resume text.",
        ),
        (
            "02",
            "Describe the role",
            "Enter the job title and the skills, responsibilities, "
            "and qualifications required.",
        ),
        (
            "03",
            "Extract and analyze",
            "Python extracts the resume text and sends the relevant "
            "content to the configured LLM through Groq.",
        ),
        (
            "04",
            "Review the results",
            "See the estimated match score, potential skill gaps, "
            "and an explanation of the comparison.",
        ),
    ]

    for number, title, description in steps:

        st.markdown(
            f"""
            <div class="section-card">
                <div style="display:flex;gap:18px;align-items:flex-start;">
                    <div style="
                        min-width:42px;
                        height:42px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        border-radius:12px;
                        background:#e9f2ff;
                        color:#3977e8;
                        font-weight:800;
                    ">
                        {number}
                    </div>
                    <div>
                        <div class="section-title">{title}</div>
                        <div class="section-description"
                             style="margin-bottom:0;">
                            {description}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "ResumeIQ is designed to support human review. "
        "Its AI-generated score should not be the sole basis for hiring."
    )


# =========================================================
# ABOUT PAGE
# =========================================================

elif page == "About":

    st.markdown(
        '<div class="page-title">About ResumeIQ</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'LLM-Based Resume Screening System'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Project Overview</div>
            <p style="color:#596579;font-size:13px;line-height:1.9;">
                ResumeIQ is an AI-assisted resume screening application
                that compares candidate resumes with job descriptions.
                It uses a Large Language Model through the Groq API to
                generate a match estimate, identify potential skill gaps,
                and explain the comparison.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Technology Stack")

    technologies = [
        ("Python", "Application logic"),
        ("Streamlit", "Web interface"),
        ("Groq API", "LLM inference"),
        ("PDFPlumber", "PDF text extraction"),
        ("Python-docx", "DOCX text extraction"),
        ("JSON", "Structured AI responses"),
        ("GitHub", "Source code management"),
        ("Streamlit Community Cloud", "Application hosting"),
    ]

    for technology, purpose in technologies:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"**{technology}**")

        with col2:
            st.write(purpose)

    st.markdown("---")

    st.caption(
        "ResumeIQ is an academic and decision-support project. "
        "Protect candidate data and verify AI-generated assessments."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        ResumeIQ · LLM-Based Resume Screening System<br>
        AI-assisted screening for human review
    </div>
    """,
    unsafe_allow_html=True,
)
