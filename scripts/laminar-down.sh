#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../infrastructure"
podman-compose -f docker-compose.laminar.yml down
