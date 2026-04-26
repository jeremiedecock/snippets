#!/bin/sh

podman exec -it hf-transformers-serve transformers chat "$@"

