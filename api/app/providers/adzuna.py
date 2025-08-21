from typing import Iterable, List
import requests
from ..config import settings
from .base import JobIn


def fetch(what: str, where: str = "", page: int = 1) -> Iterable[JobIn]:
    if not settings.adzuna_app_id or not settings.adzuna_app_key:
        return []
    url = f"https://api.adzuna.com/v1/api/jobs/fr/search/{page}"
    params = {
        "app_id": settings.adzuna_app_id,
        "app_key": settings.adzuna_app_key,
        "what": what,
        "where": where,
        "content-type": "application/json",
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json().get("results", [])
    items: List[JobIn] = []
    for j in data:
        title = j.get("title") or ""
        company = (j.get("company") or {}).get("display_name")
        location = (j.get("location") or {}).get("display_name")
        url = j.get("redirect_url") or ""
        desc = j.get("description") or ""
        items.append(
            JobIn(
                source_id=2,
                external_id=str(j.get("id")),
                title=title,
                company=company,
                location=location,
                url=url,
                raw_description=desc,
            )
        )
    return items


