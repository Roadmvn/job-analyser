from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.models import Job
from ..core.utils import compute_job_hash
from ..providers import greenhouse, adzuna, sitemap_jsonld

router = APIRouter()


@router.post("/providers/run")
def run_provider(
    provider: str = Query(..., pattern="^(greenhouse|adzuna|sitemap_jsonld)$"),
    company: str | None = Query(None),
    what: str | None = Query(None),
    where: str | None = Query(None),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    if provider == "greenhouse":
        if not company:
            raise HTTPException(400, detail="paramètre company requis pour greenhouse")
        items = list(greenhouse.fetch(company=company))
    elif provider == "adzuna":
        if not what:
            raise HTTPException(400, detail="paramètre what requis pour adzuna")
        items = list(adzuna.fetch(what=what, where=where or "", page=page))
    elif provider == "sitemap_jsonld":
        if not company and not what:
            # réutiliser 'what' pour passer une URL de sitemap (choix MVP)
            raise HTTPException(400, detail="paramètre what=sitemap_url requis pour sitemap_jsonld")
        items = list(sitemap_jsonld.fetch(sitemap_url=what))
    else:
        raise HTTPException(400, detail="provider inconnu")

    inserted, updated = 0, 0
    for it in items:
        job_hash = compute_job_hash(it.title, it.company, it.location, None)
        existing = db.query(Job).filter(Job.hash == job_hash).first()
        if existing:
            existing.url = str(it.url)
            existing.raw_description = it.raw_description
            db.commit()
            updated += 1
        else:
            j = Job(
                source_id=it.source_id,
                external_id=it.external_id,
                company=it.company,
                title=it.title,
                location=it.location,
                url=str(it.url),
                raw_description=it.raw_description,
                hash=job_hash,
            )
            db.add(j)
            db.commit()
            inserted += 1
    return {"inserted": inserted, "updated": updated, "total": len(items)}


@router.post("/providers/preview")
def preview_provider(
    provider: str = Query(..., pattern="^(greenhouse|adzuna|sitemap_jsonld)$"),
    company: str | None = Query(None),
    what: str | None = Query(None),
    where: str | None = Query(None),
    page: int = Query(1, ge=1),
):
    if provider == "greenhouse":
        if not company:
            raise HTTPException(400, detail="paramètre company requis pour greenhouse")
        items = list(greenhouse.fetch(company=company))
    elif provider == "adzuna":
        if not what:
            raise HTTPException(400, detail="paramètre what requis pour adzuna")
        items = list(adzuna.fetch(what=what, where=where or "", page=page))
    elif provider == "sitemap_jsonld":
        if not what:
            raise HTTPException(400, detail="paramètre what=sitemap_url requis pour sitemap_jsonld")
        items = list(sitemap_jsonld.fetch(sitemap_url=what))
    else:
        raise HTTPException(400, detail="provider inconnu")

    out = []
    for it in items:
        try:
            out.append(it.model_dump())  # pydantic v2
        except Exception:
            try:
                out.append(it.dict())  # pydantic v1 compat
            except Exception:
                out.append({})
    return out


