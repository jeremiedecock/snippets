#!/bin/sh

# Install Open Claw into the persistent home volume.
# Run this script once before using run.sh.
# C.f. https://openclaws.io/fr/install

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v open-claw-home:/home/user \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/open-claw:latest \
    sh -c 'curl -sSL https://openclaw.ai/install.sh | bash'
