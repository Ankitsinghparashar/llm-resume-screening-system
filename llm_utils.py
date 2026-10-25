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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    result = json.loads(response.text)

    return {
        "match_score": int(result.get("match_score", 0)),
        "missing_skills": result.get("missing_skills", []),
        "explanation": result.get("explanation", "")
    }
