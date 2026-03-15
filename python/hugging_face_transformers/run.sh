#!/bin/sh

podman run --rm -it -v hf-cache:/home/snippets/.cache/huggingface -v .:/app -w /app --userns=keep-id:uid=1000,gid=1000 localhost/snippets-hf-transformers:latest python3 "$@"
