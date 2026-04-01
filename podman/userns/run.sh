#!/bin/sh

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v .:/workspace \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/snippets-podman-userns:latest \
    /bin/bash
