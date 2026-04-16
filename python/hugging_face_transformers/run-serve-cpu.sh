#!/bin/sh

podman run -d --rm --name hf-transformers-serve -v hf-cache:/home/user/.cache/huggingface -v .:/workdir --userns=keep-id:uid=1000,gid=1000 localhost/snippets-hf-transformers:latest transformers serve

echo "Run podman logs -f hf-transformers-serve to see the server logs." 