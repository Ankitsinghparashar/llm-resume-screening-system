import ollama
import json
import os

# Ensure Ollama runs locally
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

PROMPT_TEMPLATE = """
You are an AI assistant that evaluates resume-job fit.

Be STRICT in evaluation.
If match_score is below 100, you MUST list at least one missing or partially demonstrated skill.
Do NOT assume indirect experience.

Resume:
{resume}

Job Description:
{job}

Return ONLY valid JSON in this format:

{{
  "match_score": <int between 0 and 100>,
  "missing_skills": ["explicitly required skill not clearly found in resume"],
  "explanation": "<concise explanation>"
}}
"""

def get_llm_response(resume_text: str, job_text: str) -> dict:

    prompt = PROMPT_TEMPLATE.format(
        resume=resume_text,
        job=job_text
    )

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2}
    )

    content = response["message"]["content"]

    try:
        return json.loads(content)
    except:
        return {
            "match_score": 0,
            "missing_skills": [],
            "explanation": "Failed to parse LLM response"
        }