#!/usr/bin/env bash
set -euo pipefail
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"

down() {
  cd "$SCRIPTS/../infrastructure"
  podman-compose stop "$@"
  podman-compose rm -f "$@"
}

if [[ "${1:-}" == "--all" ]]; then
  down
else
  source "$SCRIPTS/.internal/menu.sh"
  CHOICE=$(menu \
    "all" \
    "ebrit-hands-web" \
    "ytrack-channel" \
    "gitlab-channel" \
    "rproxy" \
    "ngrok" \
    "cancel")

  case "$CHOICE" in
    "all")             down ;;
    "ebrit-hands-web") down ebrit-hands-web ;;
    "ytrack-channel")  down ytrack-channel ;;
    "gitlab-channel")  down gitlab-channel ;;
    "rproxy")          down rproxy ;;
    "ngrok")           down ngrok ;;
    "cancel")          echo "Cancelled."; exit 0 ;;
  esac
fi
