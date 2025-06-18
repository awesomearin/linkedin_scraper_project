# test_scraper.py
from linkedin_scraper import scrape_linkedin_job

url = input("Enter a LinkedIn job URL: ").strip()
data = scrape_linkedin_job(url)

if "error" in data:
    print("❌ Error:", data["error"])
else:
    print("\n✅ Job Found:")
    print("Title:", data["title"])
    print("Company:", data["company"])
    print("Location:", data["location"])
    print("Description:\n", data["description"][:500] + "...")
