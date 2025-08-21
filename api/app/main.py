from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Job API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

# Routers
from .routers import keywords, jobs, ingest, auth, providers, resume, stripe_routes, health
from .scheduler import start_scheduler
app.include_router(keywords.router)
app.include_router(jobs.router)
app.include_router(ingest.router)
app.include_router(auth.router)
app.include_router(providers.router)
app.include_router(resume.router)
app.include_router(stripe_routes.router)
app.include_router(health.router)

# Scheduler optionnel
_scheduler = start_scheduler()
