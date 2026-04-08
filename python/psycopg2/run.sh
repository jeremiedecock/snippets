#!/bin/sh

podman run --rm -it -v .:/workdir --userns=keep-id:uid=1000,gid=1000 localhost/snippets-psycopg:latest python3 "$@"
