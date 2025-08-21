from pydantic import BaseModel, AnyUrl
from typing import Optional
from datetime import datetime


class JobIn(BaseModel):
    source_id: Optional[int] = None
    external_id: Optional[str] = None
    title: str
    location: Optional[str] = None
    sector: Optional[str] = None
    contract_type: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: Optional[str] = None
    url: AnyUrl
    posted_at: Optional[datetime] = None
    raw_description: str


class KeywordStat(BaseModel):
    term: str
    ngram: int
    freq: int
    tfidf: float


