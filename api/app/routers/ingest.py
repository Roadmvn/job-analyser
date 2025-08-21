from fastapi import APIRouter, Depends
from pydantic import BaseModel, AnyUrl
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.models import Job
from ..core.utils import compute_job_hash
from datetime import datetime

router = APIRouter()


class JobIn(BaseModel):
    source_id: int | None = None
    external_id: str | None = None
    title: str
    company: str | None = None
    location: str | None = None
    sector: str | None = None
    contract_type: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    currency: str | None = None
    url: AnyUrl
    posted_at: datetime | None = None
    raw_description: str


@router.post("/ingest")
def ingest(job: JobIn, db: Session = Depends(get_db)):
    job_hash = compute_job_hash(job.title, job.company, job.location, job.posted_at)
    existing = db.query(Job).filter(Job.hash == job_hash).first()
    if existing:
        # Update minimal fields
        existing.url = str(job.url)
        existing.raw_description = job.raw_description
        db.commit()
        return {"status": "updated", "id": existing.id}
    new = Job(
        source_id=job.source_id,
        external_id=job.external_id,
        company=job.company,
        title=job.title,
        location=job.location,
        sector=job.sector,
        contract_type=job.contract_type,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        currency=job.currency,
        url=str(job.url),
        posted_at=job.posted_at,
        raw_description=job.raw_description,
        hash=job_hash,
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return {"status": "inserted", "id": new.id}


