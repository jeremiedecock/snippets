#!/bin/bash

CONTAINER_UID=1000
CONTAINER_GID=1000

CLAUDE_VOLUME_NAME="claude-home"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --claude-volume-name)
            CLAUDE_VOLUME_NAME="$2"
            shift 2
            ;;
        --claude-volume-name=*)
            CLAUDE_VOLUME_NAME="${1#*=}"
            shift
            ;;
        *)
            break
            ;;
    esac
done

podman run --rm -it \
    --userns="keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID}" \
    -v .:/workspace \
    -v "${CLAUDE_VOLUME_NAME}:/home/user/.claude" \
    localhost/claude-code-cli:latest \
    claude "$@"
