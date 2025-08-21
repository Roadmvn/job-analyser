from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.models import Job
from ..analysis.keywords import top_ngrams, tfidf_scores, merge_counts_tfidf

router = APIRouter()


@router.get("/keywords")
def keywords(
    q: str | None = Query(None, description="Recherche plein texte simple"),
    sector: str | None = Query(None),
    location: str | None = Query(None),
    n_max: int = Query(3, ge=1, le=3),
    topk: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Job)
    if q:
        like = f"%{q}%"
        query = query.filter((Job.title.ilike(like)) | (Job.raw_description.ilike(like)))
    if sector:
        query = query.filter(Job.sector == sector)
    if location:
        query = query.filter(Job.location == location)
    jobs = query.limit(1000).all()
    descriptions = [j.raw_description or "" for j in jobs]
    counts = top_ngrams(descriptions, n_max=n_max, topk=topk)
    tfidf = tfidf_scores(descriptions, n_max=n_max, topk=topk)
    return merge_counts_tfidf(counts, tfidf, topk=topk)


