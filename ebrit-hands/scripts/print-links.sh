#!/usr/bin/env bash
set -euo pipefail

running() {
    podman ps --format "{{.Names}}" 2>/dev/null | grep -q "$1"
}

echo ""
echo "Services:"
echo "  [app]"
running "ebrit-hands-web"  && echo "    ebrit-hands-web       http://localhost:6011" \
                           || echo "    ebrit-hands-web       http://localhost:6011  (down)"
running "ytrack-channel"   && echo "    ytrack-channel docs   http://localhost:6010/docs" \
                           || echo "    ytrack-channel docs   http://localhost:6010/docs  (down)"
running "gitlab-channel"   && echo "    gitlab-channel docs   http://localhost:5085/docs" \
                           || echo "    gitlab-channel docs   http://localhost:5085/docs  (down)"
echo "    ebrit-hands api       http://localhost:6009/docs"

echo ""
echo "  [laminar]"
running "laminar-frontend"  && echo "    Laminar UI            http://localhost:5667" \
                            || echo "    Laminar UI            http://localhost:5667  (down)"

if running "infrastructure_ngrok"; then
    echo ""
    echo -n "  [ngrok]  "
    for i in $(seq 1 15); do
        URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null \
            | grep -o '"public_url":"https://[^"]*"' \
            | cut -d'"' -f4)
        if [ -n "$URL" ]; then
            echo "$URL"
            break
        fi
        sleep 1
    done
    [ -z "${URL:-}" ] && echo "(tunnel not ready — check NGROK_AUTHTOKEN)"
fi

echo ""
