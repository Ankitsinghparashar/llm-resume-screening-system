# ==========================================
# train.py
# Resume–Job Fit Evaluation Pipeline
# ==========================================

# Why: handle data
import pandas as pd
import os

# Why: progress bar (professional touch)
from tqdm import tqdm

# Why: local LLM (Mistral via Ollama)
import ollama


# ==========================================
# Load Data
# ==========================================

DATA_PATH = r"C:\Users\DELL\OneDrive\Desktop\llm\data\processed\resume_data_processed.csv"
data = pd.read_csv(DATA_PATH)
data = data.head(10)   # only first 10 resumes


# ==========================================
# Prompt Template
# ==========================================

PROMPT_TEMPLATE = """
You are an AI assistant that evaluates resume-job fit.

Resume:
{resume}

Job Description:
{job}

Return ONLY in this format:

Match Score: <0-100>
Skills Missing: <comma separated skills>
Explanation(2 points only): <short explanation>
"""


# ==========================================
# Function: Call LLM
# ==========================================

def get_llm_response(resume_text, job_text):
    prompt = PROMPT_TEMPLATE.format(resume=resume_text, job=job_text)
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        options={
            "num_predict": 40,
            "temperature": 0.2,
            "num_ctx": 2048
        },
        keep_alive="30m"   # VERY IMPORTANT
    )
    return response["message"]["content"]


# ==========================================
# Function: Parse LLM Output
# ==========================================

def parse_response(response_text):
    result = {"score": None, "missing_skills": None, "explanation": None}
    lines = response_text.strip().split("\n")
    for line in lines:
        if "Match Score" in line:
            result["score"] = line.split(":", 1)[1].strip()
        elif "Skills Missing" in line:
            result["missing_skills"] = line.split(":", 1)[1].strip()
        elif "Explanation" in line:
            result["explanation"] = line.split(":", 1)[1].strip()
    return result


# ==========================================
# Main Pipeline
# ==========================================

results = []

print("Starting Resume Evaluation...")

for _, row in tqdm(data.iterrows(), total=len(data)):
    resume = row["resume_text"]
    job = row["job_description_text"]

    try:
        response = get_llm_response(resume, job)
        parsed = parse_response(response)
        results.append({
            "resume_text": resume,
            "job_description_text": job,
            "true_label": row["label"],
            "predicted_score": parsed["score"],
            "missing_skills": parsed["missing_skills"],
            "explanation": parsed["explanation"]
        })
    except Exception as e:
        print("Error:", e)


# ==========================================
# Save Output
# ==========================================

output_df = pd.DataFrame(results)
OUTPUT_PATH = r"C:\Users\DELL\OneDrive\Desktop\llm\prompts\resume_results.csv"

# Ensure folder exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

output_df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved results to: {OUTPUT_PATH}")
