#!/usr/bin/env bash
set -euo pipefail
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
ROOT="$SCRIPTS/.."

touch "$ROOT/ebrit_hands_ytrack_channel/.env"
touch "$ROOT/ebrit_hands_gitlab_channel/.env"

# podman-compose 1.0.6 ignoruje `profiles:`, więc tunel wybieramy jawną listą serwisów.
# Domyślnie rproxy; z flagą --ngrok zamiast niego ngrok (wzajemnie wykluczone).
TUNNEL=rproxy
DISABLED=ngrok
for arg in "$@"; do
  [[ "$arg" == "--ngrok" ]] && { TUNNEL=ngrok; DISABLED=rproxy; }
done

cd "$ROOT/infrastructure"
podman-compose stop "$DISABLED" 2>/dev/null || true
podman-compose rm -f "$DISABLED" 2>/dev/null || true
podman-compose up -d ytrack-channel ebrit-hands-web gitlab-channel "$TUNNEL"

"$SCRIPTS/print-links.sh"
