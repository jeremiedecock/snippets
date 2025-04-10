#!/bin/sh

podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id  -e OPENAI_API_KEY="${OPENAI_API_KEY}"  localhost/snippets-langchain:latest python3 "$@"
