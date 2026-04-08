#!/bin/sh

podman run --rm -it -v .:/workdir --userns=keep-id localhost/snippets-psycopg:latest python3 "$@"
