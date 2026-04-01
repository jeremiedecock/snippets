#!/bin/sh

# Install GitHub Copilot CLI into the persistent home volume.
# Run this script once before using run.sh.
# C.f. https://github.com/features/copilot/cli/

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v github-copilot-cli-home:/home/user \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/github-copilot-cli:latest \
    sh -c 'curl -fsSL https://gh.io/copilot-install | bash'
