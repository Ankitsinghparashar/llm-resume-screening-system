import streamlit as st
import pdfplumber
from docx import Document
from io import BytesIO
from html import escape
from llm_utils import get_llm_response


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ResumeIQ | AI Recruitment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "analysis_result": None,
    "analysis_resume_name": "",
    "analysis_job_title": "",
    "analysis_count": 0,
    "history": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --primary: #3977e8;
        --primary-dark: #245bc4;
        --background: #f5f7fb;
        --text: #182230;
        --muted: #748094;
        --border: #e5eaf2;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--background);
    }

    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid var(--border);
    }

    .brand {
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #182230;
    }

    .brand span {
        color: var(--primary);
    }

    .muted {
        color: var(--muted);
        font-size: 12px;
    }

    .page-title {
        color: var(--text);
        font-size: 29px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .page-subtitle {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 24px;
    }

    .badge {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 20px;
        background: #e9f1ff;
        color: #2865c9;
        font-size: 11px;
        font-weight: 700;
    }

    .metric-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 19px;
        min-height: 116px;
        box-shadow: 0 2px 8px rgba(20, 35, 60, 0.025);
    }

    .metric-label {
        color: var(--muted);
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 14px;
    }

    .metric-value {
        color: var(--text);
        font-size: 28px;
        font-weight: 800;
        line-height: 1.2;
    }

    .metric-note {
        color: var(--muted);
        font-size: 11px;
        margin-top: 7px;
    }

    .section-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 21px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(20, 35, 60, 0.025);
    }

    .section-title {
        font-size: 16px;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 18px;
    }

    .score {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -2px;
        color: var(--primary);
    }

    .footer {
        text-align: center;
        padding: 28px 0 12px 0;
        color: #98a1b1;
        font-size: 11px;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 43px;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"] {
        background: var(--primary);
        border-color: var(--primary);
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

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        background: #fafbfe;
        border-radius: 9px;
        border-color: #e1e6ef;
        font-size: 13px;
    }

    hr {
        border-color: var(--border);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# RESUME EXTRACTION
# =========================================================

def extract_resume_text(uploaded_file):
    """Extract readable text from PDF, DOCX, or TXT."""

    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    try:
        if filename.endswith(".pdf"):
            uploaded_file.seek(0)
            pages = []

            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages.append(text)

            return "\n".join(pages).strip()

        elif filename.endswith(".docx"):
            document = Document(BytesIO(uploaded_file.getvalue()))

            paragraphs = [
                p.text.strip()
                for p in document.paragraphs
                if p.text.strip()
            ]

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
                errors="replace",
            ).strip()

        raise ValueError("Please upload a PDF, DOCX, or TXT file.")

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            "The file could not be read. Try another file or paste "
            "the resume text."
        ) from error


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">Resume<span>IQ</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="muted">AI-powered recruitment assistant</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Screening History",
            "How It Works",
            "About",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**AI Screening Assistant**")

    st.caption(
        "Compare resumes with job requirements and identify "
        "potential skill gaps."
    )

    st.markdown("---")
    st.caption("ResumeIQ · Version 2.0")


# =========================================================
# DASHBOARD
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
            'Screen candidates and understand job-related skill alignment.'
            '</div>',
            unsafe_allow_html=True,
        )

    with header_right:
        st.markdown(
            '<div style="text-align:right">'
            '<span class="badge">● AI ASSISTED</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    result = st.session_state.analysis_result

    if result:
        latest_score = result["match_score"]
        latest_gaps = len(result["missing_skills"])

        if latest_score >= 75:
            status = "Strong match"
        elif latest_score >= 50:
            status = "Partial match"
        else:
            status = "Lower match"
    else:
        latest_score = None
        latest_gaps = 0
        status = "Awaiting analysis"

    # Metrics
    metrics = [
        (
            "RESUMES ANALYZED",
            str(st.session_state.analysis_count),
            "In this session",
        ),
        (
            "LATEST MATCH SCORE",
            f"{latest_score}%" if latest_score is not None else "—",
            "AI-generated estimate",
        ),
        (
            "SKILL GAPS IDENTIFIED",
            str(latest_gaps) if result else "—",
            "From the latest analysis",
        ),
        (
            "SCREENING STATUS",
            status,
            "Based on available evidence",
        ),
    ]

    columns = st.columns(4)

    for column, (label, value, note) in zip(columns, metrics):
        with column:
            font_size = "19px" if len(value) > 13 else "28px"

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:{font_size}">
                        {escape(value)}
                    </div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # RESUME UPLOAD + JOB DESCRIPTION ON THE DASHBOARD
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">New Candidate Screening</div>
            <div class="section-subtitle">
                Step 1: Upload a resume. Step 2: Enter the job requirements.
                Step 3: Analyze the candidate.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    resume_column, job_column = st.columns(2, gap="large")

    with resume_column:
        st.markdown("### 📄 Candidate Resume")

        uploaded_file = st.file_uploader(
            "Upload resume",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, and TXT.",
            key="dashboard_resume_upload",
        )

        pasted_resume = st.text_area(
            "Or paste resume text",
            placeholder=(
                "Paste the complete resume here...\n\n"
                "Include skills, education, projects, and experience."
            ),
            height=190,
            key="dashboard_resume_text",
        )

    with job_column:
        st.markdown("### 🎯 Job Requirements")

        job_title = st.text_input(
            "Job title",
            placeholder="e.g. Software Developer",
            key="dashboard_job_title",
        )

        job_description = st.text_area(
            "Job description",
            placeholder=(
                "Describe the role, responsibilities, required skills, "
                "qualifications, and experience..."
            ),
            height=190,
            key="dashboard_job_description",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    _, button_column, _ = st.columns([1, 2, 1])

    with button_column:
        analyze_button = st.button(
            "✦ Analyze Resume",
            type="primary",
            use_container_width=True,
        )

    # -----------------------------------------------------
    # ANALYZE RESUME
    # -----------------------------------------------------

    if analyze_button:

        try:
            if pasted_resume.strip():
                resume_text = pasted_resume.strip()
                resume_name = "Pasted resume"

            elif uploaded_file is not None:
                with st.spinner("Extracting resume text..."):
                    resume_text = extract_resume_text(uploaded_file)

                resume_name = uploaded_file.name

            else:
                st.error(
                    "Please upload a resume or paste the resume text."
                )
                st.stop()

            if not resume_text or len(resume_text) < 30:
                st.error(
                    "No readable resume text was found. If this is a "
                    "scanned PDF, use OCR to extract the text or paste "
                    "the resume text manually."
                )
                st.stop()

            if not job_description.strip():
                st.error("Please enter a job description.")
                st.stop()

            with st.spinner(
                "Analyzing the candidate with Groq AI..."
            ):
                ai_result = get_llm_response(
                    resume_text,
                    job_description.strip(),
                )

            if not isinstance(ai_result, dict):
                raise ValueError(
                    "The AI returned an unexpected result format."
                )

            score = int(ai_result.get("match_score", 0))
            score = max(0, min(100, score))

            missing_skills = ai_result.get("missing_skills", [])

            if not isinstance(missing_skills, list):
                missing_skills = []

            explanation = str(ai_result.get("explanation", ""))

            cleaned_result = {
                "match_score": score,
                "missing_skills": missing_skills,
                "explanation": explanation,
            }

            st.session_state.analysis_result = cleaned_result
            st.session_state.analysis_resume_name = resume_name
            st.session_state.analysis_job_title = (
                job_title.strip() or "Unspecified role"
            )
            st.session_state.analysis_count += 1

            st.session_state.history.insert(
                0,
                {
                    "resume_name": resume_name,
                    "job_title": job_title.strip() or "Unspecified role",
                    "match_score": score,
                    "missing_skills": missing_skills,
                    "explanation": explanation,
                },
            )

            st.success("Resume analysis completed!")

        except Exception as error:
            error_text = str(error).lower()

            if (
                "429" in error_text
                or "resource_exhausted" in error_text
                or "rate limit" in error_text
            ):
                st.error(
                    "The Groq API rate limit has been reached. "
                    "Wait briefly before trying again."
                )

            elif "groq_api_key" in error_text:
                st.error(
                    "The Groq API key is missing. Check your "
                    "Streamlit Secrets settings."
                )

            elif (
                "401" in error_text
                or "invalid_api_key" in error_text
                or "authentication" in error_text
            ):
                st.error(
                    "Groq rejected the API key. Verify the key in "
                    "Streamlit Secrets."
                )

            else:
                st.error(
                    "Resume analysis failed. Check the Streamlit "
                    "app logs for the underlying error."
                )

            print(f"Resume analysis error: {type(error).__name__}: {error}")

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    result = st.session_state.analysis_result

    if result:
        st.markdown("---")

        st.markdown(
            '<div class="page-title">Candidate Analysis</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="page-subtitle">'
            'Review the estimated match, potential skill gaps, '
            'and AI-generated explanation.'
            '</div>',
            unsafe_allow_html=True,
        )

        result_left, result_right = st.columns([1, 2], gap="large")

        with result_left:
            st.markdown(
                '<div class="section-card">'
                '<div class="section-title">Resume Match Score</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="score">{result["match_score"]}%</div>',
                unsafe_allow_html=True,
            )

            st.progress(result["match_score"] / 100)

            if result["match_score"] >= 75:
                st.success("Strong alignment")
            elif result["match_score"] >= 50:
                st.warning("Partial alignment")
            else:
                st.info("Lower alignment")

            st.markdown("</div>", unsafe_allow_html=True)

        with result_right:
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-title">AI Evaluation</div>
                """,
                unsafe_allow_html=True,
            )

            st.write(
                result["explanation"]
                or "No explanation was returned by the model."
            )

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Potential Skill Gaps</div>
            """,
            unsafe_allow_html=True,
        )

        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.markdown(f"- {skill}")
        else:
            st.success("No potential skill gaps were reported.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.caption(
            f"Resume: {st.session_state.analysis_resume_name} · "
            f"Role: {st.session_state.analysis_job_title}"
        )

        st.info(
            "The match score is an AI-generated estimate, not a "
            "validated probability of job success. Review the resume "
            "and verify job-related qualifications before making "
            "hiring decisions."
        )


# =========================================================
# SCREENING HISTORY
# =========================================================

elif page == "Screening History":

    st.markdown(
        '<div class="page-title">Screening History</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Review analyses performed during this session.'
        '</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.history:
        st.info(
            "No screening history is available yet. Run an analysis "
            "from the Dashboard first."
        )

    else:
        for index, item in enumerate(st.session_state.history, start=1):
            with st.expander(
                f"{index}. {item['resume_name']} — "
                f"{item['match_score']}% match"
            ):
                st.write(f"**Job title:** {item['job_title']}")
                st.write(f"**Match score:** {item['match_score']}%")
                st.write(f"**AI explanation:** {item['explanation']}")

                st.write("**Potential skill gaps:**")

                if item["missing_skills"]:
                    for skill in item["missing_skills"]:
                        st.write(f"- {skill}")
                else:
                    st.write("No potential skill gaps reported.")


# =========================================================
# HOW IT WORKS
# =========================================================

elif page == "How It Works":

    st.markdown(
        '<div class="page-title">How ResumeIQ Works</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Four steps from resume upload to AI-assisted evaluation.'
        '</div>',
        unsafe_allow_html=True,
    )

    steps = [
        (
            "01",
            "Upload the resume",
            "Upload a PDF, DOCX, or TXT file, or paste the resume text.",
        ),
        (
            "02",
            "Enter job requirements",
            "Provide the job title and the role's required skills, "
            "qualifications, and responsibilities.",
        ),
        (
            "03",
            "AI-assisted comparison",
            "The application extracts resume text and passes it to "
            "your configured LLM through the Groq API.",
        ),
        (
            "04",
            "Review the results",
            "Examine the match estimate, possible skill gaps, "
            "and explanation.",
        ),
    ]

    for number, title, description in steps:
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">{number} · {title}</div>
                <div class="section-subtitle"
                     style="margin-bottom:0;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "Use the results as decision support, not as the sole basis "
        "for hiring."
    )


# =========================================================
# ABOUT
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
            <p>
                ResumeIQ is an AI-assisted resume screening application
                that compares resume content with job descriptions.
                It generates a match estimate, identifies possible
                skill gaps, and provides an explanation using a
                Large Language Model.
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
        ("GitHub", "Version control"),
        ("Streamlit Community Cloud", "Deployment"),
    ]

    for technology, description in technologies:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.write(f"**{technology}**")

        with col2:
            st.write(description)

    st.info(
        "Protect candidate information and verify AI-generated "
        "assessments before using them."
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
