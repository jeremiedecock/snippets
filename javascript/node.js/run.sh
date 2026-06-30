#!/bin/sh

# This script is used to run Node in a rootless Podman container.

# C.f. https://hub.docker.com/_/node

# Usage:
# - open node interpreter: `./run.sh` or `./run.sh node`
# - execute a Javascript (or Typescript) file: `./run.sh foo.js` or `./run.sh node foo.js`
# - open bash interpreter: `./run.sh bash`

CONTAINER_UID=1000
CONTAINER_GID=1000

podman run --rm -it \
    -v .:/workspace \
    -w /workspace \
    --userns=keep-id:uid=${CONTAINER_UID},gid=${CONTAINER_GID} \
    node:trixie-slim \
    $@
