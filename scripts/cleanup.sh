#!/usr/bin/env bash
set -euo pipefail
ROOT="$(dirname "$0")/.."

echo "==> Removing artifacts/project-* and artifacts/metadata-* ..."
rm -rf "$ROOT"/artifacts/project-* "$ROOT"/artifacts/metadata-*

echo "==> Removing agent-server containers ..."
containers=$(podman ps -a --filter "name=agent-server" --format "{{.Names}}" 2>/dev/null || true)
if [ -n "$containers" ]; then
    echo "$containers" | xargs podman rm -f
else
    echo "    none found"
fi
