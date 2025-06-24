import os
from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI(
    api_key = "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",
)

def generate_skill_suggestions(job_description: str, missing_skills: list) -> str:
    if not missing_skills:
        return "✅ Your resume already matches all key job skills."

    prompt = f"""
You're an AI career assistant. A user is applying to a job described below:

\"\"\"{job_description[:1000]}\"\"\"

They are missing the following skills: {', '.join(missing_skills)}.

Give them a list of:
1. Learning resources or advice for each skill
2. Example personal project ideas to help them practice

Format the output in bullet points grouped by skill.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You help job seekers improve their resumes and skills."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT error: {str(e)}"