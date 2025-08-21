up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose exec -T api alembic -c alembic.ini upgrade head || true

seed:
	docker compose exec -T api python -m app.seed || true

web:
	docker compose exec -T web npm run dev || true

test:
	docker compose exec -T api pytest -q || true
