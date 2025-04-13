#!/bin/sh

# To use Nvidia GPUs with Podman, a CDI specification of the installed device(s) have to be made first:
# 1. Generate the CDI specification file: `sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`
# 2. (Optional) Check the names of the generated devices: `nvidia-ctk cdi list`
#
# More info: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html#procedure

podman run --rm -it -v .:/app -w /app -u $(id -u):$(id -g) --userns=keep-id  --device nvidia.com/gpu=all  localhost/snippets-hf-diffusers:latest python3 "$@"
