#!/bin/sh

podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-hf-transformers:latest "$@"
