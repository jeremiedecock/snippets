#!/bin/sh

podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id -p 8000:8000 localhost/snippets-fastapi:latest