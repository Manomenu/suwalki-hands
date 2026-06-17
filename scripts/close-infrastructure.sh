#!/usr/bin/env bash
set -euo pipefail

SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPTS/.internal/menu.sh"

SERVICES=(
    "infrastructure_gitlab-channel_1"
    "infrastructure_ytrack-channel_1"
    "infrastructure_ebrit-hands-web_1"
)

RUNNING=()
for svc in "${SERVICES[@]}"; do
    if podman ps --format "{{.Names}}" 2>/dev/null | grep -q "^${svc}$"; then
        RUNNING+=("$svc")
    fi
done

if [ ${#RUNNING[@]} -eq 0 ]; then
    echo "No services running."
    exit 0
fi

echo "Select service to stop (↑↓ or j/k, Enter):"
echo ""
CHOICE=$(menu "${RUNNING[@]}" "Cancel")

if [ "$CHOICE" == "Cancel" ] || [ -z "$CHOICE" ]; then
    echo "Cancelled."
    exit 0
fi

echo "Stopping $CHOICE..."
podman stop "$CHOICE"
echo "Done."
