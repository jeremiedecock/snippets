#!/bin/sh

podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id --network=host localhost/snippets-ray-core:latest python3 "$@"
