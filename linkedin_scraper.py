from playwright.sync_api import sync_playwright
import re

def is_valid_linkedin_job_url(url):
    return re.match(r"^https:\/\/www\.linkedin\.com\/jobs\/view\/\d+", url)

def scrape_linkedin_job(url):
    if not is_valid_linkedin_job_url(url):
        return {"error": "Invalid LinkedIn job URL format."}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(url, timeout=15000)

            # Wait for content to load
            page.wait_for_selector('h1.topcard__title', timeout=10000)

            job_title = page.locator('h1.topcard__title').inner_text().strip()
            company = page.locator('a.topcard__org-name-link').inner_text().strip()
            location = page.locator('span.topcard__flavor--bullet').inner_text().strip()
            description = page.locator('div.description__text').inner_text().strip()

            return {
                "title": job_title,
                "company": company,
                "location": location,
                "description": description
            }

        except Exception as e:
            return {"error": f"Failed to scrape job: {str(e)}"}

        finally:
            browser.close()
