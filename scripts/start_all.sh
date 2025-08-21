#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Detect docker compose command
dcmd=""
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  dcmd="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  dcmd="docker-compose"
fi

if [[ -z "$dcmd" ]]; then
  echo "[ERREUR] Docker/Compose introuvable. Installez Docker puis réessayez." >&2
  echo "Astuce (Debian/Kali): suivez l'installation via le repo officiel Docker (docker-ce + docker-compose-plugin)." >&2
  exit 1
fi

$dcmd build api web worker
$dcmd up -d

# Migrations + seed (sans échec bloquant)
$dcmd exec -T api alembic -c alembic.ini upgrade head || true
$dcmd exec -T api python -m app.seed || true

cat <<EOF

Services démarrés:
- API: http://localhost:8000
- Web: http://localhost:3000
- Adminer: http://localhost:8080

Endpoints utiles:
- Santé:       curl -sS http://localhost:8000/health | jq .
- Santé (DB):  curl -sS http://localhost:8000/health/db | jq .
EOF


