#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../infrastructure"
podman-compose -f docker-compose.laminar.yml up -d

echo ""
echo "Laminar:"
echo "  UI              http://localhost:5667"
