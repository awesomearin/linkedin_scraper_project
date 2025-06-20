import pdfplumber
import os
import re
from typing import List

class ExperienceEntry:
    def __init__(self, title, company, start_date, end_date, description):
        self.title = title
        self.company = company
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

    def __repr__(self):
        return (
            f"{self.title} at {self.company} ({self.start_date} - {self.end_date})\n"
            f"{self.description.strip()}\n"
        )


def extract_text_from_pdf(pdf_path: str) -> dict:
    """
    Extract raw text from a PDF file.
    """
    if not os.path.exists(pdf_path) or not pdf_path.lower().endswith(".pdf"):
        return {"error": "Invalid file path or file type. Please upload a PDF."}

    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return {"text": text.strip()}
    except Exception as e:
        return {"error": f"Failed to read resume: {str(e)}"}


def parse_experience_entries_from_text(text: str) -> List[ExperienceEntry]:
    """
    Try to parse experience entries from plain resume text using simple regex patterns.
    Note: This is a naive implementation and can be improved with NLP later.
    """
    lines = text.split("\n")
    entries = []

    job_pattern = re.compile(r"(?P<title>.+?) at (?P<company>.+?) \((?P<start>[^)]+?) - (?P<end>[^)]+?)\)")
    buffer = []
    current_entry = None

    for line in lines:
        line = line.strip()

        # Match job header
        match = job_pattern.match(line)
        if match:
            if current_entry:
                current_entry.description = "\n".join(buffer)
                entries.append(current_entry)
                buffer = []

            current_entry = ExperienceEntry(
                title=match.group("title"),
                company=match.group("company"),
                start_date=match.group("start"),
                end_date=match.group("end"),
                description=""
            )
        elif current_entry:
            buffer.append(line)

    if current_entry:
        current_entry.description = "\n".join(buffer)
        entries.append(current_entry)
    return entries


def manual_experience_entry() -> ExperienceEntry:
    """
    Collect manual input from the user to build a single experience entry.
    """
    print("Enter experience information manually:\n")
    title = input("Job Title: ").strip()
    company = input("Company Name: ").strip()
    start = input("Start Date (e.g., Jan 2020): ").strip()
    end = input("End Date (e.g., Present): ").strip()
    description = input("Describe your work (one paragraph): ").strip()

    return ExperienceEntry(title, company, start, end, description)
