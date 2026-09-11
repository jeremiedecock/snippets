#!/bin/bash

CONTAINER_UID=1000
CONTAINER_GID=1000

# See https://learn.chatgpt.com/docs/auth/ci-cd-auth
podman run --rm -it \
    --userns="keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID}" \
    -v codex-home:/home/user/.codex \
    localhost/codex-cli:latest \
    codex -c 'cli_auth_credentials_store="file"' login --device-auth
