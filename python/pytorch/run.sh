#!/bin/sh

podman run --rm -it -v .:/app -w /app -e CLEARML_CONFIG_FILE=/app/clearml.conf -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-pytorch:latest python3 "$@"
