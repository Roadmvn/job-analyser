# Job Analyser (MVP)

Monorepo: Next.js (web) + FastAPI (api) + MySQL + Adminer.

## Lancement (dev)

1) Démarrer services:
```bash
docker compose up -d
```
2) Migrations:
```bash
make migrate
```
3) Données de test (Adzuna si clés présentes, sinon 3 offres factices):
```bash
make seed
```
4) Accès:
- API: http://localhost:8000 (santé /health)
- Web: http://localhost:3000
- Adminer: http://localhost:8080 (serveur: db, user: jobs, pass: jobs)

## Variables d’environnement clés
- API: `DATABASE_URL`, `JWT_SECRET`, `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_PRICE_ID`, `SCHEDULER_ENABLED`
- Web: `NEXT_PUBLIC_API_URL`
 - Worker (optionnel): `SCRAPE_HTML_ENABLED`, `GH_COMPANY`, `SCRAPE_DELAY`, `USER_AGENT`

### Lemmatisation spaCy (optionnelle)
- Activer via `LEMMATIZE_ENABLED=true` (service `api`).
- Installer un modèle FR localement si désiré: `python -m spacy download fr_core_news_sm` puis définir `SPACY_MODEL=fr_core_news_sm`.

## cURL utiles
Auth:
```bash
curl -X POST http://localhost:8000/auth/register -H 'content-type: application/json' -d '{"email":"u@ex.com","password":"x"}'
curl -i -X POST http://localhost:8000/auth/login -H 'content-type: application/json' -d '{"email":"u@ex.com","password":"x"}'
```

Offres/Keywords:
```bash
curl 'http://localhost:8000/jobs?page=1&page_size=10&q=devops'
curl 'http://localhost:8000/keywords?topk=20&q=devops'
```

Ingestion/Providers:
```bash
curl -X POST 'http://localhost:8000/ingest' -H 'content-type: application/json' -d '{"title":"DevOps","url":"https://ex","raw_description":"kubernetes terraform"}'
curl -X POST 'http://localhost:8000/providers/run?provider=greenhouse&company=openai'
curl -X POST 'http://localhost:8000/providers/run?provider=adzuna&what=devops&where=Paris'
curl -X POST 'http://localhost:8000/providers/run?provider=sitemap_jsonld&what=https://domain.com/sitemap.xml'
```

Worker (Playwright) — respect robots.txt:
```bash
# Activer dans docker-compose: SCRAPE_HTML_ENABLED=true
docker compose up -d --build worker
```

Analyse CV:
```bash
curl -X POST 'http://localhost:8000/jobs/score' --data-urlencode 'resume_text=Kubernetes Terraform AWS'
curl -X POST 'http://localhost:8000/resume/analyze' -H 'content-type: application/json' -d '{"resume_text":"kubernetes","terms":["kubernetes","terraform","aws"]}'
```

Stripe (mock si pas de clés):
```bash
curl -X POST http://localhost:8000/stripe/create-checkout-session
```

## Check‑list
- `docker compose up -d` → services OK
- `make migrate` → tables créées
- `make seed` → `/jobs` >= 3
- `/keywords?q=devops` → liste non vide
- `/resume/analyze` → `missing_terms`
- `/providers/run?provider=greenhouse&company=openai` → upsert > 0
- `/pricing` (web) → bouton Pro (mock si pas de clés Stripe)