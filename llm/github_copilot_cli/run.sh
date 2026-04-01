#!/bin/sh

podman volume exists github-copilot-cli-home || { echo "Volume 'github-copilot-cli-home' not found. Run ./init.sh first."; exit 1; }

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v .:/workspace \
    -v github-copilot-cli-home:/home/user \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/github-copilot-cli:latest \
    copilot
