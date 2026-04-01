#!/bin/sh

podman volume exists mistral-vibe-home || { echo "Volume 'mistral-vibe-home' not found. Run ./init.sh first."; exit 1; }

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v .:/workspace \
    -v mistral-vibe-home:/home/user \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/mistral-vibe-cli:latest \
    vibe
