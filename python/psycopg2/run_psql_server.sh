#!/bin/sh

podman run \
    -it \
    --rm \
    --name postgres \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=pass \
    -e POSTGRES_DB=snippetsdb \
    -e TZ=Europe/Paris \
    -p 5432:5432 \
    docker.io/library/postgres
