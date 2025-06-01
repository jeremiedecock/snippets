#!/bin/sh

# To use Nvidia GPUs with Podman, a CDI specification of the installed device(s) have to be made first:
# 1. Generate the CDI specification file: `sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`
# 2. (Optional) Check the names of the generated devices: `nvidia-ctk cdi list`
#
# More info: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html#procedure

podman run --rm -it \
           --name="clearml-agent-worker-cpu" \
           -e CLEARML_AGENT_PACKAGE_PYTORCH_RESOLVE=none \
           -e CLEARML_WORKER_ID="$(hostname):cpu" \
           -v clearml-agent-cache-worker-cpu:/root/.clearml \
           localhost/clearml-agent:latest clearml-agent daemon --queue "worker-cpu" --foreground
