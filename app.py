import streamlit as st
import pdfplumber
from docx import Document
from io import BytesIO
from llm_utils import get_llm_response


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ResumeIQ | AI Resume Screening",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(
            135deg,
            #faf8ff 0%,
            #f5f1ff 50%,
            #ffffff 100%
        );
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .hero {
        padding: 32px;
        border-radius: 24px;
        color: white;
        background: linear-gradient(
            120deg,
            #7c3aed,
            #5125bd
        );
        margin-bottom: 28px;
        box-shadow: 0 12px 30px rgba(91, 33, 182, 0.16);
    }

    .hero h1 {
        color: white;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero p {
        color: #f1eaff;
        font-size: 16px;
        margin-bottom: 0;
    }

    .section-card {
        background: white;
        padding: 24px;
        border: 1px solid #e8e0fa;
        border-radius: 20px;
        margin-bottom: 18px;
        box-shadow: 0 5px 18px rgba(45, 25, 80, 0.04);
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #28174c;
        margin-bottom: 8px;
    }

    .muted {
        color: #746b88;
        font-size: 14px;
    }

    div.stButton > button {
        width: 100%;
        border: none;
        border-radius: 12px;
        padding: 14px 20px;
        color: white;
        font-weight: 700;
        background: linear-gradient(
            100deg,
            #7c3aed,
            #5b21b6
        );
        min-height: 50px;
    }

    div.stButton > button:hover {
        color: white;
        border: none;
        background: linear-gradient(
            100deg,
            #6d28d9,
            #4c1d95
        );
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e8e0fa;
        border-radius: 16px;
        padding: 18px;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
    }

    .footer {
        color: #8b829b;
        text-align: center;
        font-size: 12px;
        padding: 25px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# RESUME TEXT EXTRACTION
# --------------------------------------------------

def extract_resume_text(uploaded_file):
    """Extract text from PDF, DOCX, or TXT files."""

    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    try:
        file_bytes = uploaded_file.getvalue()

        if filename.endswith(".pdf"):
            extracted_pages = []

            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()

                    if page_text:
                        extracted_pages.append(page_text)

            return "\n".join(extracted_pages).strip()

        elif filename.endswith(".docx"):
            document = Document(BytesIO(file_bytes))

            paragraphs = [
                paragraph.text
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
            return file_bytes.decode(
                "utf-8-sig",
                errors="replace"
            ).strip()

        else:
            return ""

    except Exception as error:
        st.error(
            "The uploaded file could not be read. "
            "Try another file or paste the resume text."
        )

        # Keep technical details in server logs.
        print(f"Resume extraction error: {error}")

        return ""


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 📄 ResumeIQ")
    st.caption("AI-Powered Resume Screening")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Home",
            "How It Works",
            "About"
        ],
        index=0
    )

    st.divider()

    st.markdown("### ✨ Features")
    st.markdown(
        """
        - Resume file upload
        - AI-powered job matching
        - Missing skills analysis
        - Match score and explanation
        """
    )

    st.divider()

    st.caption("Built with Streamlit and Gemini AI")


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <h1>ResumeIQ 📄</h1>
            <p>
                Screen resumes intelligently.
                Discover relevant skills, identify gaps,
                and compare candidate experience with job requirements.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    left_col, right_col = st.columns(
        [1, 1],
        gap="large"
    )

    with left_col:

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">
                    📤 Upload Your Resume
                </div>
                <div class="muted">
                    Supported formats: PDF, DOCX and TXT
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=False,
            help="Upload a text-based resume for analysis."
        )

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">
                    📝 Or Paste Resume Text
                </div>
                <div class="muted">
                    You can paste the complete resume instead of uploading a file.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        pasted_resume = st.text_area(
            "Resume text",
            placeholder="Paste the complete resume here...",
            height=220,
            label_visibility="collapsed"
        )

    with right_col:

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">
                    🎯 Job Description
                </div>
                <div class="muted">
                    Enter the responsibilities, required skills,
                    qualifications and experience for the role.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        job_description = st.text_area(
            "Job description",
            placeholder=(
                "Example: We are looking for a software developer "
                "with Python, SQL, data structures, Git and problem-solving skills..."
            ),
            height=300,
            label_visibility="collapsed"
        )

        st.info(
            "Tip: A detailed job description can help produce "
            "a more useful comparison."
        )

    st.write("")

    analyze = st.button(
        "✨ Analyze Resume",
        use_container_width=True
    )

    # ----------------------------------------------
    # ANALYSIS
    # ----------------------------------------------

    if analyze:

        # Pasted text takes priority if both inputs are provided.
        if pasted_resume.strip():
            resume_text = pasted_resume.strip()

        elif uploaded_file is not None:
            resume_text = extract_resume_text(uploaded_file)

        else:
            resume_text = ""

        if not resume_text:
            st.error(
                "Please upload a readable resume or paste its text."
            )

        elif not job_description.strip():
            st.error(
                "Please enter the job description before analyzing."
            )

        elif len(resume_text) < 30:
            st.error(
                "The extracted resume text is too short. "
                "Please upload another file or paste more resume content."
            )

        elif len(job_description.strip()) < 10:
            st.error(
                "Please provide a more detailed job description."
            )

        else:
            try:
                with st.spinner(
                    "Analyzing the resume with Gemini AI..."
                ):
                    result = get_llm_response(
                        resume_text,
                        job_description.strip()
                    )

                # Validate the response returned by llm_utils.py.
                if not isinstance(result, dict):
                    raise ValueError(
                        "The AI returned an unexpected response format."
                    )

                score = int(result.get("match_score", 0))
                score = max(0, min(100, score))

                missing_skills = result.get(
                    "missing_skills",
                    []
                )

                explanation = result.get(
                    "explanation",
                    "No explanation was provided."
                )

                if not isinstance(missing_skills, list):
                    missing_skills = []

                st.divider()

                st.markdown("## 📊 Screening Results")

                st.caption(
                    "AI-generated results for review. "
                    "These are not a hiring decision."
                )

                metric1, metric2, metric3 = st.columns(3)

                with metric1:
                    st.metric(
                        "Resume Match",
                        f"{score}%"
                    )

                with metric2:
                    st.metric(
                        "Missing Skills",
                        len(missing_skills)
                    )

                with metric3:
                    if score >= 80:
                        category = "Strong Match"
                    elif score >= 60:
                        category = "Moderate Match"
                    else:
                        category = "Low Match"

                    st.metric(
                        "Match Category",
                        category
                    )

                st.progress(score / 100)

                st.markdown("### 🧠 AI Explanation")

                st.write(str(explanation))

                st.markdown("### 🛠️ Missing or Unidentified Skills")

                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(f"- {skill}")
                else:
                    st.success(
                        "No missing skills were identified by the AI. "
                        "Review the resume and job requirements manually."
                    )

                st.markdown("### 📋 Screening Summary")

                if score >= 80:
                    st.success(
                        "The resume appears to align well with "
                        "the supplied job description."
                    )

                elif score >= 60:
                    st.warning(
                        "The resume shows some alignment. "
                        "Review the identified gaps and relevant experience."
                    )

                else:
                    st.info(
                        "The resume may have limited alignment with "
                        "the supplied job description. Verify the "
                        "requirements and candidate qualifications."
                    )

                # Save results in the current Streamlit session.
                st.session_state["resumeiq_results"] = {
                    "score": score,
                    "missing_skills": missing_skills,
                    "explanation": str(explanation)
                }

                st.caption(
                    "The match score is an AI estimate, not a "
                    "validated probability of job performance. "
                    "Verify all results before making decisions."
                )

            except Exception as error:
                print(f"Resume analysis error: {error}")

                st.error(
                    "The analysis could not be completed. "
                    "Check your Gemini API configuration and app logs."
                )

                st.caption(
                    "Check that GEMINI_API_KEY is configured in "
                    "Streamlit Secrets, the selected Gemini model is "
                    "available, and your API quota has not been exceeded."
                )


# --------------------------------------------------
# HOW IT WORKS PAGE
# --------------------------------------------------

elif page == "How It Works":

    st.markdown(
        """
        <div class="hero">
            <h1>How ResumeIQ Works</h1>
            <p>
                A simple workflow for comparing resumes
                with job requirements.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    steps = [
        (
            "01",
            "Upload",
            "Upload a PDF, DOCX or TXT resume, "
            "or paste resume text."
        ),
        (
            "02",
            "Describe the Role",
            "Enter the job description, including "
            "relevant qualifications and skills."
        ),
        (
            "03",
            "Analyze",
            "Gemini AI compares the resume content "
            "with the supplied job requirements."
        ),
        (
            "04",
            "Review",
            "Examine the match score, missing skills "
            "and AI-generated explanation."
        ),
        (
            "05",
            "Make an Informed Decision",
            "Verify the findings and use human judgment "
            "rather than relying on the AI score alone."
        )
    ]

    for number, title, description in steps:
        st.markdown(
            f"""
            <div class="section-card">
                <h3>{number} · {title}</h3>
                <p class="muted">{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.warning(
        "ResumeIQ provides decision support only. "
        "It should not be used as the sole basis for hiring decisions."
    )


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

elif page == "About":

    st.markdown(
        """
        <div class="hero">
            <h1>About ResumeIQ</h1>
            <p>
                An LLM-based resume screening system
                built to support job-requirement comparisons.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>🎯 Project Objective</h3>
            <p>
                ResumeIQ explores how large language models can help
                compare resume content with job descriptions,
                identify relevant skills, and summarize potential gaps.
            </p>
        </div>

        <div class="section-card">
            <h3>⚙️ Technology Stack</h3>
            <ul>
                <li>Python</li>
                <li>Streamlit</li>
                <li>Google Gemini API</li>
                <li>pdfplumber for PDF text extraction</li>
                <li>python-docx for DOCX text extraction</li>
            </ul>
        </div>

        <div class="section-card">
            <h3>🔒 Privacy and Responsible Use</h3>
            <p>
                Resume documents can contain personal information.
                Use only authorized documents, protect API credentials,
                and review the API provider's data-use terms.
                AI results may be incomplete or inaccurate and
                must be verified by a human reviewer.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        ResumeIQ · LLM-Based Resume Screening System
        <br>
        AI-assisted screening for human review
    </div>
    """,
    unsafe_allow_html=True
)
