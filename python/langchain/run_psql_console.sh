#!/bin/sh

podman exec \
    -it \
    pgvector-snippets \
    psql -U user -d snippetsdb
