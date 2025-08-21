from typing import Iterable, Protocol
from pydantic import BaseModel, AnyUrl


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
    raw_description: str


class JobProvider(Protocol):
    def fetch(self, **kwargs) -> Iterable[JobIn]:
        ...


