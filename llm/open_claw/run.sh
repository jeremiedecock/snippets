#!/bin/sh

podman volume exists open-claw-home || { echo "Volume 'open-claw-home' not found. Run ./init.sh first."; exit 1; }

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v .:/workspace \
    -v open-claw-home:/home/user \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/open-claw:latest \
    openclaw
