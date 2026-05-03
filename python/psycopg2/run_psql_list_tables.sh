#!/bin/sh

podman exec \
    -it \
    postgres-psycopg2-snippets \
    psql -U user -d snippetsdb -c "\dt"
