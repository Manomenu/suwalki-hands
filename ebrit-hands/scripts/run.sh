#!/usr/bin/env bash
set -euo pipefail
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"

if ! podman ps --format '{{.Names}}' 2>/dev/null | grep -q "ytrack-channel"; then
    echo "==> infrastructure is down, starting..."
    "$SCRIPTS/infrastructure-up.sh"
fi

cd "$SCRIPTS/../ebrit_hands"
uv run python -m ebrit_hands "$@"
