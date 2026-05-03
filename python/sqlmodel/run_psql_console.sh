#!/bin/sh

podman exec \
    -it \
    postgres-sqlmodel-snippets \
    psql -U user -d snippetsdb
