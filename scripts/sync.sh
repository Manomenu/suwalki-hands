#!/usr/bin/env bash
set -euo pipefail
ROOT="$(dirname "$0")/.."

for project in ebrit_hands_library ebrit_hands ebrit_hands_ytrack_channel ebrit_hands_gitlab_channel; do
    echo "==> syncing $project"
    (cd "$ROOT/$project" && unset VIRTUAL_ENV && uv sync)
done
