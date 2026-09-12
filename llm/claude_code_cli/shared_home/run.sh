#!/bin/bash

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    --userns="keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID}" \
    -v .:/workspace \
    -v claude-home:/home/user/.claude \
    localhost/claude-code-cli:latest \
    claude "$@"
