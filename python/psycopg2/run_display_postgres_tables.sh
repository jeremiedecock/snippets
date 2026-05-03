#!/bin/sh

podman exec \
    -it \
    postgres psql -U user -d snippetsdb -c "\dt"
