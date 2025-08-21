from typing import Iterable, List
import requests
from .base import JobIn


def fetch(company: str) -> Iterable[JobIn]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json().get("jobs", [])
    results: List[JobIn] = []
    for j in data:
        title = j.get("title") or ""
        job_url = j.get("absolute_url") or j.get("url") or ""
        location = (j.get("location") or {}).get("name")
        content = j.get("content") or ""
        company_name = j.get("company") or None
        results.append(
            JobIn(
                source_id=1,
                external_id=str(j.get("id")),
                title=title,
                company=company_name,
                location=location,
                url=job_url,
                raw_description=content,
            )
        )
    return results


