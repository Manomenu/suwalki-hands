#!/usr/bin/env bash
set -euo pipefail
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
ROOT="$SCRIPTS/.."

touch "$ROOT/ebrit_hands_ytrack_channel/.env"
touch "$ROOT/ebrit_hands_gitlab_channel/.env"

TUNNEL=rproxy
DISABLED=ngrok
ALL=0
for arg in "$@"; do
  [[ "$arg" == "--ngrok" ]] && { TUNNEL=ngrok; DISABLED=rproxy; }
  [[ "$arg" == "--all"  ]] && ALL=1
done

cd "$ROOT/infrastructure"
podman-compose stop "$DISABLED" 2>/dev/null || true
podman-compose rm -f "$DISABLED" 2>/dev/null || true

up() {
  podman-compose up -d --build "$@"
}

if [[ $ALL -eq 1 ]]; then
  up ytrack-channel ebrit-hands-web gitlab-channel "$TUNNEL"
else
  source "$SCRIPTS/.internal/menu.sh"
  CHOICE=$(menu \
    "all" \
    "ebrit-hands-web" \
    "ytrack-channel" \
    "gitlab-channel" \
    "tunnel ($TUNNEL)" \
    "cancel")

  case "$CHOICE" in
    "all")               up ytrack-channel ebrit-hands-web gitlab-channel "$TUNNEL" ;;
    "ebrit-hands-web")   up ebrit-hands-web ;;
    "ytrack-channel")    up ytrack-channel ;;
    "gitlab-channel")    up gitlab-channel ;;
    "tunnel ($TUNNEL)")  up "$TUNNEL" ;;
    "cancel")            echo "Cancelled."; exit 0 ;;
  esac
fi

"$SCRIPTS/print-links.sh"
