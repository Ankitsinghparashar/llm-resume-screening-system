# ResumeIQ — LLM-Based Resume Screening System

An AI-powered resume screening application that evaluates how well a candidate's resume matches a job description using a Large Language Model (LLM).

## 🚀 Live Demo

**Try ResumeIQ here:** [Open Live Website](https://llm-resume-screening-system-gdkywgykqrqc6q6oskitbs.streamlit.app/)

## 📂 GitHub Repository

[View Source Code on GitHub](https://github.com/Ankitsinghparashar/llm-resume-screening-system)

---

## 📌 Project Description

ResumeIQ is an LLM-based resume screening system designed to evaluate candidate suitability for a particular job role.

Users can upload a resume or paste resume text, provide a job description, and receive an AI-generated assessment of how closely the candidate's qualifications align with the role.

The system generates an estimated match score, identifies potential skill gaps, and provides an explanation of the results to support human review.

The application combines resume text extraction, prompt engineering, a cloud-based LLM API, and an interactive Streamlit interface.

## 🎯 Problem Statement

Traditional resume screening methods often rely on exact keyword matching. These methods can overlook relevant experience when candidates describe their skills using different terminology.

ResumeIQ addresses this limitation by using an LLM to interpret resume content in the context of a job description.

The system evaluates relevant skills, experience, and qualifications to provide a more context-aware assessment of candidate-job compatibility.

The generated results are intended to assist recruiters and reviewers, not replace human judgment.

## ✨ Features

- **Resume Upload:** Upload resumes in PDF, DOCX, and TXT formats.
- **Manual Resume Input:** Paste resume text directly into the application.
- **Job Description Analysis:** Enter the responsibilities, qualifications, and skills required for a position.
- **AI-Powered Screening:** Evaluate resume-job compatibility using a Large Language Model.
- **Match Score:** Generate an estimated compatibility score from 0 to 100.
- **Missing Skills Identification:** Highlight potentially missing or insufficiently demonstrated skills.
- **AI-Generated Explanation:** Provide a concise explanation of the assessment.
- **Interactive Dashboard:** View screening information through a Streamlit web interface.
- **Cloud Deployment:** Access the application through its live website.
- **Human Review:** Use the results as decision-support information rather than an automatic hiring decision.

## 🛠️ Technologies Used

- **Python** — Core programming language.
- **Streamlit** — Interactive web application and dashboard.
- **Groq API** — Cloud-based LLM inference.
- **Large Language Models (LLMs)** — Context-aware resume evaluation.
- **PDFPlumber** — Text extraction from PDF documents.
- **Python-docx** — Text extraction from DOCX documents.
- **JSON** — Structured representation of LLM responses.
- **Git and GitHub** — Version control and source code hosting.
- **Streamlit Community Cloud** — Application deployment.

Additional libraries may be used by the training, prediction, or evaluation scripts.

## 🏗️ Project Architecture

```text
                 Candidate Resume
                        |
                        v
             Resume Text Extraction
                        |
                        v
                  Job Description
                        |
                        v
                 Prompt Engineering
                        |
                        v
                 Groq API (LLM)
                        |
                        v
                Structured JSON Output
                        |
             +----------+----------+
             |          |          |
             v          v          v
         Match Score  Skill Gaps  Explanation
             |          |          |
             +----------+----------+
                        |
                        v
                Streamlit Dashboard
                        |
                        v
                 Human Review
```

## 📁 Folder Structure

The following represents the expected project structure. Adjust it if your repository differs.

```text
llm-resume-screening-system/
│
├── app.py
├── llm_utils.py
├── requirements.txt
├── README.md
│
├── train.py
├── predict.py
├── evaluate.py
│
├── data/
│   ├── raw/
│   │   └── resume_data.csv
│   └── processed/
│       ├── resume_data_processed.csv
│       ├── new_resume.csv
│       └── unseen_predictions.csv
│
├── prompts/
│   └── resume_results.csv
│
└── notebooks/
    └── load_data.ipynb
```

Only files and folders that actually exist should be listed in the final folder structure.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ankitsinghparashar/llm-resume-screening-system.git
```

### 2. Navigate to the project directory

```bash
cd llm-resume-screening-system
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create an API key through the official [Groq Console](https://console.groq.com/).

For local development, configure the key as an environment variable.

**Windows PowerShell:**

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

Replace the placeholder with your own key. Never commit API keys to GitHub.

For deployment on Streamlit Community Cloud, add the key to your application's Secrets settings:

```toml
GROQ_API_KEY = "your_api_key_here"
```

Do not put a real API key in this README or in source code.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to access the application.

## 🖥️ How to Use ResumeIQ

1. Open the [live ResumeIQ application](https://llm-resume-screening-system-gdkywgykqrqc6q6oskitbs.streamlit.app/).
2. Navigate to the resume screening section.
3. Upload a resume in PDF, DOCX, or TXT format, or paste the resume text.
4. Enter the job description for the target position.
5. Click **Analyze Resume**.
6. Review the estimated match score, identified skill gaps, and explanation.
7. Verify the findings against the original resume and job requirements before making decisions.

## 📊 Example Output

The following is an illustrative example, not a measured result from a specific candidate.

```text
Match Score: 82/100

Potential Missing Skills:
- Docker
- Kubernetes

Explanation:
The candidate demonstrates relevant programming and
machine learning experience. However, the resume does not
clearly demonstrate experience with Docker and Kubernetes,
which may be important for the target role.
```

Actual results depend on the resume, job description, model, and prompt.

## 🧪 Testing and Evaluation

The system can be evaluated using a labeled dataset and, where implemented, the project's training, prediction, and evaluation scripts.

Potential evaluation approaches include:

- Comparing predicted compatibility with human-labeled assessments.
- Measuring precision, recall, and F1-score for classification tasks.
- Evaluating the consistency of missing-skill identification.
- Reviewing the quality and factual accuracy of generated explanations.
- Testing the application with different resume formats and job descriptions.

A match score generated by an LLM should not be treated as a statistically validated probability of getting hired.

## 🔮 Future Improvements

- Implement Retrieval-Augmented Generation (RAG) for richer skill matching.
- Add batch processing for multiple resumes.
- Enable export of screening results to CSV or PDF.
- Add candidate comparison and filtering.
- Improve prompt engineering and structured output validation.
- Compare LLM-based screening with traditional machine learning approaches.
- Evaluate results against a human-reviewed dataset.
- Add screening history and analytics.
- Improve error handling and API rate-limit management.
- Explore additional LLM providers and models.

## 🔐 Privacy and Responsible Use

- Avoid uploading confidential resumes without appropriate authorization.
- Protect API keys using environment variables or deployment secrets.
- Review the data handling policies of the selected LLM provider.
- Verify extracted resume information before relying on generated results.
- Do not use AI-generated scores as the sole basis for hiring decisions.
- Assess candidates fairly and consistently using job-related criteria.

## 👨‍💻 Author

**Ankit Kumar**  
B.Tech Computer Science Engineering

## 📄 License

Add a license appropriate to your project if you intend to permit others to reuse, modify, or distribute the code.

---

**ResumeIQ — AI-assisted resume screening for human review.**
