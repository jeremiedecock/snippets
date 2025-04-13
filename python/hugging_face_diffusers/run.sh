#!/bin/sh

podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-hf-diffusers:latest python3 "$@"
