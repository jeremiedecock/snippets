#!/bin/bash

# Build the image. By default the Claude Code CLI install layer is reused from
# the build cache; pass --update to force it to re-run (i.e. to pick up a newer
# CLI release) without rebuilding the apt layer above it.

CACHEBUST=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --update)
            CACHEBUST="$(date +%Y-%m-%dT%H:%M:%S)"
            shift
            ;;
        *)
            echo "usage: $0 [--update]" >&2
            exit 1
            ;;
    esac
done

podman build -t claude-code-cli:latest -f claude.containerfile \
    --build-arg "CACHEBUST=${CACHEBUST}" .
