#!/bin/sh

# C.f. https://github.com/pgvector/pgvector
#
# Some important notes:
# - "The defined VOLUME was changed in 18 and above to /var/lib/postgresql.
#    Mounts and volumes should be targeted at the updated location."
#    C.f. https://hub.docker.com/_/postgres/#pgdata
# - Locale Customization: https://github.com/docker-library/docs/blob/master/postgres/README.md#locale-customization

# TODO:
# - Where to Store Data: https://github.com/docker-library/docs/blob/master/postgres/README.md#where-to-store-data
# - Secrets (with Podman / Kubernetes): https://hub.docker.com/_/postgres/#docker-secrets
# - Locale Customization: https://github.com/docker-library/docs/blob/master/postgres/README.md#locale-customization
# - Set SHM size e.g. `podman run ... --shm-size=256MB ...`: https://github.com/docker-library/docs/blob/master/postgres/README.md#caveats
# - Deploy with Kubernetes

podman run \
    -it \
    --rm \
    --name pgvector-snippets \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=pass \
    -e POSTGRES_DB=snippetsdb \
    -e TZ=Europe/Paris \
    -p 5432:5432 \
    -v pgvector_snippets_data:/var/lib/postgresql \
    docker.io/pgvector/pgvector:pg18-trixie
