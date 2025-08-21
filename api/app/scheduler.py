import os
from apscheduler.schedulers.background import BackgroundScheduler
from .providers import greenhouse
from .db import SessionLocal
from .models.models import Job
from .core.utils import compute_job_hash


def _run_greenhouse_job(company: str):
    items = greenhouse.fetch(company=company)
    db = SessionLocal()
    try:
        for it in items:
            h = compute_job_hash(it.title, it.company, it.location, None)
            existing = db.query(Job).filter(Job.hash == h).first()
            if existing:
                existing.url = str(it.url)
                existing.raw_description = it.raw_description
            else:
                db.add(Job(
                    source_id=it.source_id,
                    external_id=it.external_id,
                    company=it.company,
                    title=it.title,
                    location=it.location,
                    url=str(it.url),
                    raw_description=it.raw_description,
                    hash=h,
                ))
        db.commit()
    finally:
        db.close()


def start_scheduler():
    if os.getenv("SCHEDULER_ENABLED", "false").lower() != "true":
        return None
    scheduler = BackgroundScheduler()
    company = os.getenv("GH_COMPANY", "openai")
    scheduler.add_job(lambda: _run_greenhouse_job(company), "interval", minutes=int(os.getenv("GH_INTERVAL_MIN", "60")))
    scheduler.start()
    return scheduler


