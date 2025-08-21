from typing import Iterable, List
import requests
from bs4 import BeautifulSoup
import json
from .base import JobIn


def _find_jsonld_job_posting(html: str) -> List[JobIn]:
    out: List[JobIn] = []
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(tag.string or '{}')
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for it in items:
            if it.get('@type') in ('JobPosting', ['JobPosting']):
                title = it.get('title') or ''
                desc = it.get('description') or ''
                hiring_org = it.get('hiringOrganization') or {}
                company = hiring_org.get('name') if isinstance(hiring_org, dict) else None
                out.append(JobIn(title=title, company=company, url='about:blank', raw_description=desc))
    return out


def fetch(sitemap_url: str) -> Iterable[JobIn]:
    r = requests.get(sitemap_url, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')][:50]
    results: List[JobIn] = []
    for u in urls:
        try:
            page = requests.get(u, timeout=20)
            page.raise_for_status()
            found = _find_jsonld_job_posting(page.text)
            for j in found:
                results.append(JobIn(title=j.title, company=j.company, url=u, raw_description=j.raw_description))
        except Exception:
            continue
    return results


