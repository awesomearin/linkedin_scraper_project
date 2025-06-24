import re
from collections import Counter
from typing import List, Tuple
from resume_scraper import ExperienceEntry

COMMON_SKILLS = [
    "python", "java", "R", "aws", "azure", "docker", "kubernetes", "sql",
    "c++", "git", "pytorch", "tensorflow", "graphql", "linux", "C",
    "javascript", "react", "agile", "jira", "ci/cd", "html", "css", "spark"
]

def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9 ]", " ", text.lower())


def extract_keywords(text, keywords=COMMON_SKILLS) -> List[str]:
    text = clean_text(text)
    return [word for word in keywords if word in text]


def match_resume_to_job(job_description: str, resume_text: str) -> dict:
    job_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume_text)

    matched = list(set(job_keywords) & set(resume_keywords))
    missing = list(set(job_keywords) - set(resume_keywords))

    match_score = int((len(matched) / len(job_keywords)) * 100) if job_keywords else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": match_score
    }


def rank_experience_entries(job_description: str, experiences: List[ExperienceEntry]) -> List[Tuple[ExperienceEntry, int]]:
    ranked = []
    for entry in experiences:
        score = len(extract_keywords(entry.description, COMMON_SKILLS + extract_keywords(job_description)))
        ranked.append((entry, score))
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
