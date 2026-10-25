 
---

 LLM-Powered Resume–Job Fit Evaluator


---

Project Description

An end-to-end Generative AI system that evaluates how well a candidate’s resume matches a given job description using a Large Language Model (LLM). The system generates a match score, identifies missing skills, and provides a concise explanation to assist in automated resume screening.


---

Project Statement

Traditional resume screening methods rely on keyword matching, which fails to capture the semantic meaning of skills and experience. This project solves the problem by leveraging a Large Language Model to perform intelligent, context-aware evaluation of resume-job compatibility, improving accuracy and efficiency in candidate selection.


---

Features

Resume and job description compatibility evaluation

Match score generation (0–100)

Identification of missing skills

AI-generated explanation of results

Local LLM inference using Mistral (via Ollama)

Streamlit-based interactive web application

Prediction on unseen resumes

Evaluation using labeled dataset



---

Technologies Used

Python

Pandas

Streamlit

Ollama

Mistral LLM

Scikit-learn

TQDM

HuggingFace Datasets



---

### Project Architecture
```
[Resume + Job Description]
        ↓
[Prompt Engineering]
        ↓
[Mistral LLM (Ollama)]
        ↓
[Structured Output (JSON)]
        ↓
[Match Score + Missing Skills + Explanation]
        ↓
[Streamlit UI]

---
```
### Folder Structure
---
```
project-root/
│
├── app.py
├── train.py
├── predict.py
├── evaluate.py
├── llm_utils.py
├── requirements.txt
├── README.md
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
├── load_data.ipynb
└── prompts/
```

---

Installation

1. Clone the repository


2. Navigate to the project folder


3. Install dependencies using requirements.txt


4. Install Ollama and download the Mistral model




---

Run Application

Run the Streamlit app using: streamlit run app.py


---

Example Output

match_score: 82

missing_skills: Docker, Kubernetes

explanation: Candidate has strong programming and ML skills but lacks deployment and 

containerization experience.


---

Future Improvements

Add Retrieval-Augmented Generation (RAG) for better skill matching

Compare LLM performance with traditional ML models

Deploy using cloud-based LLM APIs

Improve evaluation metrics (precision, recall, F1-score)

Optimize prompts to reduce hallucinations



---

Author

Jahnavi
Aspiring Generative AI Engineer


 
