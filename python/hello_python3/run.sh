#!/bin/sh

podman run --rm -it -v .:/workdir --userns=keep-id localhost/snippets-hello-python3:latest python3 "$@"
