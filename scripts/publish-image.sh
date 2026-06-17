#!/usr/bin/env bash
set -euo pipefail

SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
ROOT="$SCRIPTS/.."
IMAGES_DIR="$ROOT/ebrit_hands/images"

source "$SCRIPTS/.internal/menu.sh"

# shellcheck source=../.env
[ -f "$ROOT/.env" ] && set -a && source "$ROOT/.env" && set +a

REGISTRY="${IMAGE_REGISTRY:?IMAGE_REGISTRY is not set — add it to .env or export it before running this script}"

function build_and_push {
	local dockerfile="$1"
	local name="${dockerfile#Dockerfile.}"
	local tag="$REGISTRY:$name"

	echo ""
	echo "Building $tag from $dockerfile ..."
	docker build -t "$tag" -f "$IMAGES_DIR/$dockerfile" "$ROOT"

	echo "Pushing $tag ..."
	docker push "$tag"

	echo "Done: $tag"
}

mapfile -t DOCKERFILES < <(cd "$IMAGES_DIR" && ls Dockerfile.* 2>/dev/null)

if [ ${#DOCKERFILES[@]} -eq 0 ]; then
	echo "No Dockerfiles found in $IMAGES_DIR"
	exit 1
fi

echo "Select image to publish (↑↓ or j/k, Enter):"
echo "Registry: $REGISTRY"
echo ""
CHOICE=$(menu "All" "${DOCKERFILES[@]}" "Cancel")

if [ "$CHOICE" == "Cancel" ] || [ -z "$CHOICE" ]; then
	echo "Cancelled."
	exit 0
fi

if [ "$CHOICE" == "All" ]; then
	for df in "${DOCKERFILES[@]}"; do
		build_and_push "$df"
	done
else
	build_and_push "$CHOICE"
fi
