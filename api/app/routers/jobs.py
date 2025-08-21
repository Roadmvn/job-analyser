from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.models import Job
from ..analysis.scoring import compute_tfidf_cosine_scores

router = APIRouter()


@router.get("/jobs")
def list_jobs(
    q: str | None = Query(None),
    sector: str | None = Query(None),
    location: str | None = Query(None),
    contract: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    base = db.query(Job)
    if q:
        like = f"%{q}%"
        base = base.filter((Job.title.ilike(like)) | (Job.raw_description.ilike(like)))
    if sector:
        base = base.filter(Job.sector == sector)
    if location:
        base = base.filter(Job.location == location)
    if contract:
        base = base.filter(Job.contract_type == contract)
    total = base.count()
    items = (
        base.order_by(Job.posted_at.desc().nullslast(), Job.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {"items": [
        {
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "sector": j.sector,
            "contract_type": j.contract_type,
            "posted_at": j.posted_at.isoformat() if j.posted_at else None,
            "url": j.url,
        } for j in items
    ], "total": total}


@router.post("/jobs/score")
def jobs_score(
    resume_text: str,
    job_ids: list[int] | None = None,
    db: Session = Depends(get_db),
):
    if job_ids:
        jobs = db.query(Job).filter(Job.id.in_(job_ids)).all()
    else:
        jobs = db.query(Job).limit(50).all()
    texts = [j.title + ". " + (j.raw_description or "") for j in jobs]
    scores = compute_tfidf_cosine_scores(resume_text, texts)
    return [
        {"job_id": j.id, "match_score": float(s)}
        for j, s in zip(jobs, scores)
    ]


