#!/bin/sh

podman run \
    --rm \
    -it \
    -v .:/workdir \
    -p 8000:8000 \
    --userns=keep-id:uid=1000,gid=1000 \
    localhost/snippets-fastapi:latest
