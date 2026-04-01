#!/bin/sh

# Install Claude Code CLI into the persistent home volume.
# Run this script once before using run.sh.
# C.f. https://code.claude.com/docs/en/overview

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v claude-code-home:/home/user \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/claude-code-cli:latest \
    sh -c 'curl -fsSL https://claude.ai/install.sh | bash'
