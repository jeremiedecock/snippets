#!/bin/sh

podman run \
    --rm \
    -it \
    -v hf-cache:/home/user/.cache/huggingface \
    -v .:/workdir \
    --userns=keep-id:uid=1000,gid=1000 \
    localhost/snippets-hf-diffusers:latest python3 "$@"

