#!/bin/sh

podman run \
    --rm \
    -it \
    -v .:/workdir \
    -e CLEARML_CONFIG_FILE=/workdir/clearml.conf \
    --userns=keep-id:uid=1000,gid=1000 \
    localhost/snippets-pytorch:latest python3 "$@"

