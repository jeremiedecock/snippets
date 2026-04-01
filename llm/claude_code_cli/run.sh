#!/bin/sh

CONTAINER_UID=1000
CONTAINER_GID=1000

    # # Décommenter si vous utilisez une clé API au lieu de l'auth OAuth (claude login)
    # -e ANTHROPIC_API_KEY \
    # # Décommenter les deux lignes ci-dessous pour faire du SSH agent forwarding
    # -v "$SSH_AUTH_SOCK:/tmp/ssh-agent" \
    # -e SSH_AUTH_SOCK=/tmp/ssh-agent \
    # -e HOME=/home/user \
 
podman run --rm -it \
    -v .:/workspace \
    -v claude-code-home:/home/user \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    localhost/claude-code-cli:latest \
    /home/user/.local/bin/claude
