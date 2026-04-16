#!/bin/sh

podman run --rm -it -v hf-cache:/home/user/.cache/huggingface -v .:/workdir -e OPENAI_API_KEY="${OPENAI_API_KEY}"  --userns=keep-id:uid=1000,gid=1000 localhost/snippets-langchain:latest python3 "$@"
