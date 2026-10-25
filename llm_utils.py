import os
import json
from google import genai

def get_llm_response(resume_text, job_text):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it in Streamlit Secrets."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert resume screening assistant.

    Compare the resume with the job description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_text}

    Return ONLY valid JSON in this exact format:
    {{
        "match_score": 75,
        "missing_skills": ["Python", "SQL"],
        "explanation": "Explain the match and gaps briefly."
    }}

    Rules:
    - match_score must be an integer from 0 to 100.
    - missing_skills must be a list of skills missing from the resume.
    - explanation must be a short, clear explanation.
    - Evaluate only job-related qualifications.
    - Do not infer qualifications from personal characteristics.
    """
import time

response = None

for attempt in range(3):
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )
        break

    except Exception as e:
        if attempt == 2:
            raise

        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            time.sleep(2 * (attempt + 1))
        else:
            raise

    result = json.loads(response.text)

    return {
        "match_score": int(result.get("match_score", 0)),
        "missing_skills": result.get("missing_skills", []),
        "explanation": result.get("explanation", "")
    }
