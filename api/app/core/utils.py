import hashlib
from datetime import datetime


def normalize_text(value: str) -> str:
    return (value or "").strip().lower()


def compute_job_hash(title: str, company: str | None, location: str | None, posted_at: datetime | None) -> str:
    parts = [normalize_text(title), normalize_text(company or ""), normalize_text(location or ""), (posted_at or datetime(1970, 1, 1)).isoformat()]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()

