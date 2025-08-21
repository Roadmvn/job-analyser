#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

company="${1:-openai}"
docker compose run --rm -e SCRAPE_HTML_ENABLED=true -e GH_COMPANY="$company" worker


