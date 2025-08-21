#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

provider="${1:-greenhouse}"
outfile="${2:-preview.json}"
shift 2 || true
query="${*:-company=openai}"

echo "Sauvegarde JSON -> $outfile"
curl -sS -X POST "http://localhost:8000/providers/preview?provider=${provider}&${query}" | jq . > "$outfile"
echo "OK: $outfile"


