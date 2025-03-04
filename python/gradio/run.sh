#!/bin/sh

podman run --rm -it -p 7860:7860 -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id localhost/snippets-gradio:latest "$@"
