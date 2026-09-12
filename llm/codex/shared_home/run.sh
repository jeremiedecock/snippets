#!/bin/bash

CONTAINER_UID=1000
CONTAINER_GID=1000

# See https://learn.chatgpt.com/docs/auth/ci-cd-auth
# The first bind mount exposes the current project at the path expected by Codex.
# The named volume reuses init.sh credentials. The -c setting reads them from that
# mounted filesystem because no host keychain is exposed inside the container.
podman run --rm -it \
    --userns="keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID}" \
    -v .:/workspace \
    -v codex-home:/home/user/.codex \
    localhost/codex-cli:latest \
    codex -c 'cli_auth_credentials_store="file"' "$@"
