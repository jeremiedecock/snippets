#!/bin/sh

# podman rmi localhost/codex-cli
podman build -t codex-cli:latest -f codex.containerfile .
