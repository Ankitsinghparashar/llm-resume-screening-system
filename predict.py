# ==========================================
# predict.py
# Run LLM inference on new resumes (Ollama)
# ==========================================

import pandas as pd
from tqdm import tqdm
import ollama
import os

# ------------------------------------------
# FIX: Explicitly tell Python where Ollama runs
# ------------------------------------------
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

print("Starting Prediction on New Resumes...")

# ------------------------------------------
# Load dataset
# ------------------------------------------
data = pd.read_csv(
    r"C:\Users\DELL\OneDrive\Desktop\llm\data\processed\new_resumes.csv",
    encoding="utf-8"
)

# ------------------------------------------
# Prompt Template
# ------------------------------------------
PROMPT_TEMPLATE = """
You are an AI assistant that evaluates resume-job fit.

Resume:
{resume}

Job Description:
{job}

Return ONLY in this format:

Match Score: <0-100>
Skills Missing: <comma separated skills>
Explanation: <short explanation>
"""

# ------------------------------------------
# LLM Call
# ------------------------------------------
def get_llm_response(resume_text, job_text):

    prompt = PROMPT_TEMPLATE.format(
        resume=resume_text,
        job=job_text
    )

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0   # more consistent scoring
        }
    )

    return response["message"]["content"]


# ------------------------------------------
# Parse Response
# ------------------------------------------
def parse_response(response_text):

    result = {
        "score": None,
        "missing_skills": None,
        "explanation": None
    }

    lines = response_text.strip().split("\n")

    for line in lines:
        if "Match Score" in line:
            result["score"] = line.split(":", 1)[1].strip()

        elif "Skills Missing" in line:
            result["missing_skills"] = line.split(":", 1)[1].strip()

        elif "Explanation" in line:
            result["explanation"] = line.split(":", 1)[1].strip()

    return result


# ------------------------------------------
# Prediction Loop
# ------------------------------------------
results = []

for _, row in tqdm(data.iterrows(), total=len(data)):

    resume = str(row["resume_text"])
    job = str(row["job_description_text"])

    try:
        response = get_llm_response(resume, job)
        parsed = parse_response(response)

    except Exception as e:
        print("Error:", e)
        parsed = {
            "score": None,
            "missing_skills": None,
            "explanation": "LLM error"
        }

    results.append({
        "resume_text": resume,
        "job_description_text": job,
        "predicted_score": parsed["score"],
        "missing_skills": parsed["missing_skills"],
        "explanation": parsed["explanation"]
    })


# ------------------------------------------
# Save Results
# ------------------------------------------
pd.DataFrame(results).to_csv(
    "data/processed/unseen_predictions.csv",
    index=False,
    encoding="utf-8"
)

print("✅ Prediction complete!")