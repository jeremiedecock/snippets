#!/bin/sh

#podman run --rm -it -v hf-cache:/home/snippets/.cache/huggingface -v .:/app -w /app --userns=keep-id:uid=1000,gid=1000 localhost/claude-code-cli:latest python3 "$@"
podman run --rm -it -v .:/workspace -w /workspace --userns=keep-id localhost/claude-code-cli:latest /bin/bash "$@"
