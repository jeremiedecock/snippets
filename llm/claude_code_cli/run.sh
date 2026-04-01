#!/bin/sh

podman volume exists claude-code-home || { echo "Volume 'claude-code-home' not found. Run ./init.sh first."; exit 1; }

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v .:/workspace \
    -v claude-code-home:/home/user \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/claude-code-cli:latest \
    claude
