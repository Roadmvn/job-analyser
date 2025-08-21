import os
from pydantic import BaseModel

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "mysql+pymysql://jobs:jobs@db:3306/jobs")
    log_level: str = os.getenv("LOG_LEVEL", "info")
    jwt_secret: str = os.getenv("JWT_SECRET", "devsecret_change_me")
    jwt_algorithm: str = os.getenv("JWT_ALG", "HS256")
    jwt_exp_minutes: int = int(os.getenv("JWT_EXP_MIN", "60"))
    adzuna_app_id: str | None = os.getenv("ADZUNA_APP_ID")
    adzuna_app_key: str | None = os.getenv("ADZUNA_APP_KEY")
    stripe_secret_key: str | None = os.getenv("STRIPE_SECRET_KEY")
    stripe_price_id: str | None = os.getenv("STRIPE_PRICE_ID")

settings = Settings()
