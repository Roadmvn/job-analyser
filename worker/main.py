import os
import time
import requests
from playwright.sync_api import sync_playwright
from robots import is_allowed

API = os.getenv("API_URL", "http://api:8000")
UA = os.getenv("USER_AGENT", "JobSiteBot/1.0")
DELAY = float(os.getenv("SCRAPE_DELAY", "2.0"))


def greenhouse_company(company: str):
    url = f"https://boards.greenhouse.io/{company}"
    if not is_allowed(url, UA):
        print("robots.txt interdit cette page")
        return
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent=UA)
        page.goto(url, wait_until="domcontentloaded")
        jobs = page.locator(".opening a[href*='/jobs/']").all()
        for j in jobs:
            job_url = j.get_attribute("href")
            title = j.inner_text().strip()
            page.goto(job_url, wait_until="domcontentloaded")
            desc = page.locator(".content").inner_text()
            payload = {
                "source_id": 1,
                "title": title,
                "url": job_url,
                "raw_description": desc,
            }
            try:
                requests.post(f"{API}/ingest", json=payload, headers={"User-Agent": UA}, timeout=20)
            except Exception:
                pass
            time.sleep(DELAY)
        browser.close()


if __name__ == "__main__":
    company = os.getenv("GH_COMPANY", "openai")
    if os.getenv("SCRAPE_HTML_ENABLED", "false").lower() == "true":
        greenhouse_company(company)
    else:
        print("SCRAPE_HTML_ENABLED=false; worker inactif")


