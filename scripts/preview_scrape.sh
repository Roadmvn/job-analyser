#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

provider="${1:-greenhouse}"
shift || true
query="${*:-company=openai}"

curl -sS -X POST "http://localhost:8000/providers/preview?provider=${provider}&${query}" | jq .


