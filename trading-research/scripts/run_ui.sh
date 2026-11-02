#!/usr/bin/env bash
# Start the command center on this machine only (127.0.0.1). Do not change --host
# until real authentication exists.
set -euo pipefail
cd "$(dirname "$0")/.."
export TRADELAB_DB="${TRADELAB_DB:-data/research.db}"
export TRADELAB_CONFIG="${TRADELAB_CONFIG:-config/risk.toml}"
exec python3 -m uvicorn tradelab.web.app:app_from_env --factory --host 127.0.0.1 --port "${PORT:-8000}"
