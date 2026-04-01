#!/bin/sh

# Install Mistral Vibe CLI into the persistent home volume.
# Run this script once before using run.sh.
# C.f. https://docs.mistral.ai/mistral-vibe/introduction/install

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v mistral-vibe-home:/home/user \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/mistral-vibe-cli:latest \
    sh -c 'curl -LsSf https://mistral.ai/vibe/install.sh | bash'
