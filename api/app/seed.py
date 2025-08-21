from sqlalchemy.orm import Session
from .db import SessionLocal
from .models.models import Job
from .config import settings
from .providers import adzuna


def run_seed():
    db: Session = SessionLocal()
    try:
        inserted = 0
        if settings.adzuna_app_id and settings.adzuna_app_key:
            items = adzuna.fetch(what="devops", where="Paris")
            for it in items:
                j = Job(
                    title=it.title, company=it.company, location=it.location,
                    sector="it", contract_type="CDI", url=str(it.url), raw_description=it.raw_description,
                    hash=f"seed_adzuna_{inserted}"
                )
                db.add(j)
                inserted += 1
        else:
            samples = [
                ("Ingénieur DevOps", "Acme", "Paris", "kubernetes terraform cloud security"),
                ("Data Engineer", "Beta", "Lyon", "spark airflow aws glue kafka"),
                ("SRE", "Gamma", "Remote", "observability prometheus grafana k8s"),
            ]
            for idx, (title, company, location, desc) in enumerate(samples):
                j = Job(title=title, company=company, location=location, sector="it", contract_type="CDI", url="https://example.com", raw_description=desc, hash=f"seed_fake_{idx}")
                db.add(j)
                inserted += 1
        db.commit()
        return inserted
    finally:
        db.close()


if __name__ == "__main__":
    print(run_seed())


