# test_resume_input.py
from resume_scraper import extract_text_from_pdf, ExperienceEntry

def manual_entry():
    title = input("Job Title: ")
    company = input("Company: ")
    start = input("Start Date (e.g., Jan 2020): ")
    end = input("End Date (e.g., Dec 2021 or 'Present'): ")
    desc = input("Describe your work (1-2 sentences): ")
    return ExperienceEntry(title, company, start, end, desc)

def main():
    mode = input("Choose input mode: (1) Upload PDF or (2) Manual Entry: ")

    if mode == "1":
        path = input("Enter the path to your resume PDF: ")
        result = extract_text_from_pdf(path)
        if "error" in result:
            print("❌", result["error"])
        else:
            print("✅ Extracted Text Preview:\n")
            print(result["text"][:1000])  # Just a preview
    elif mode == "2":
        exp = manual_entry()
        print("✅ You entered:\n")
        print(exp)
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
