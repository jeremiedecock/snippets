#!/bin/sh

# To use Nvidia GPUs with Podman, a CDI specification of the installed device(s) have to be made first:
# 1. Generate the CDI specification file: `sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`
# 2. (Optional) Check the names of the generated devices: `nvidia-ctk cdi list`
#
# More info: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html#procedure

podman run \
    --rm \
    -it \
    -v hf-cache:/home/user/.cache/huggingface \
    -v .:/workdir \
    -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
    --userns=keep-id:uid=1000,gid=1000 \
    --device nvidia.com/gpu=all \
    localhost/snippets-langchain:latest python3 "$@"

